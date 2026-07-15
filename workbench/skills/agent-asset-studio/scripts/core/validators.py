from __future__ import annotations

import csv
from pathlib import Path

from configs import common, skill
from core.base import Asset, ValidationResult, Validator


def clean_scalar(value: str) -> str:
    """단순 YAML scalar의 block marker와 외부 quote를 제거한다."""
    cleaned = value.strip()
    if cleaned in {">", "|"}:
        return ""
    if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] and cleaned[0] in "\"'":
        return cleaned[1:-1]
    return cleaned


def parse_frontmatter(content: str) -> tuple[dict[str, str], str]:
    """YAML frontmatter에서 메타데이터 필드와 본문을 분리한다."""
    if not content.startswith("---\n"):
        return {}, content

    end_index = content.find("\n---\n", 4)
    if end_index == -1:
        return {}, content

    raw_frontmatter = content[4:end_index]
    body = content[end_index + 5 :]
    fields: dict[str, str] = {}
    current_key: str | None = None
    current_value: list[str] = []

    for line in raw_frontmatter.splitlines():
        if line.startswith((" ", "\t")) and current_key is not None:
            current_value.append(line.strip())
            continue

        if current_key is not None:
            fields[current_key] = clean_scalar(" ".join(current_value))
            current_key = None
            current_value = []

        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        current_key = key.strip()
        current_value = [value]

    if current_key is not None:
        fields[current_key] = clean_scalar(" ".join(current_value))

    return fields, body


def get_frontmatter(asset: Asset, filename: str) -> tuple[dict[str, str], str] | None:
    """자산 파일의 frontmatter 파싱 결과를 캐시해 재사용한다."""
    cached = asset.get_cached_frontmatter(filename)
    if cached is not None:
        return cached

    content = asset.read_text_file(filename)
    if content is None:
        return None

    parsed = parse_frontmatter(content)
    asset.cache_frontmatter(filename, parsed)
    return parsed


class FrontmatterValidator(Validator):
    """Frontmatter의 구조, 정규 명칭 규칙, 스키마 적합성을 검증한다."""

    def validate(self, asset: Asset) -> list[ValidationResult]:
        parsed = get_frontmatter(asset, asset.get_filename())
        if parsed is None:
            return []

        frontmatter, _ = parsed
        return asset.config.FRONTMATTER_SCHEMA.validate(frontmatter, asset.name)


class SkillTriggerValidator(Validator):
    """스킬 설명란(description)의 트리거 키워드 포함 여부를 검증한다."""

    def validate(self, asset: Asset) -> list[ValidationResult]:
        results: list[ValidationResult] = []
        parsed = get_frontmatter(asset, asset.get_filename())
        if parsed is None:
            return results

        frontmatter, _ = parsed
        description = frontmatter.get("description", "")

        if description:
            normalized_description = description.lower()
            trigger_check = any(
                word.lower() in normalized_description for word in skill.TRIGGER_WORDS
            )
            if not trigger_check:
                results.append(
                    ValidationResult(
                        level="warning",
                        code="weak_trigger",
                        message=(
                            "description에 사용 시점 또는 트리거 표현이 부족합니다."
                        ),
                    )
                )
        return results


class AssetBodyLengthValidator(Validator):
    """본문(Body) 라인 수의 길이를 분석하여 references 분할이 권장되는지 경고한다."""

    def validate(self, asset: Asset) -> list[ValidationResult]:
        results: list[ValidationResult] = []
        filename = asset.get_filename()
        parsed = get_frontmatter(asset, filename)
        if parsed is None:
            return results

        _, body = parsed
        body_line_count = len(body.splitlines())

        if body_line_count > 500:
            results.append(
                ValidationResult(
                    level="warning",
                    code="long_asset_body",
                    message=(
                        f"{filename} 본문이 {body_line_count}줄입니다. "
                        "references/ 분리를 검토하세요."
                    ),
                )
            )
        return results


class RoutingSkillValidator(Validator):
    """Routing Skill의 index, entrypoint, discovery 경계를 검증한다."""

    def validate(self, asset: Asset) -> list[ValidationResult]:
        index_path = asset.path / "INDEX.csv"
        workflows_path = asset.path / "workflows"
        if not index_path.exists() and not workflows_path.exists():
            return []

        results: list[ValidationResult] = []
        if not index_path.is_file():
            results.append(
                ValidationResult(
                    "error", "missing_route_index", "INDEX.csv가 없습니다."
                )
            )
        if not workflows_path.is_dir():
            results.append(
                ValidationResult("error", "missing_workflows", "workflows/가 없습니다.")
            )
        if results:
            return results

        try:
            with index_path.open("r", encoding="utf-8", newline="") as file:
                reader = csv.DictReader(file)
                if reader.fieldnames != list(skill.ROUTE_INDEX_FIELDS):
                    return [
                        ValidationResult(
                            "error",
                            "invalid_route_schema",
                            "INDEX.csv schema는 "
                            + ",".join(skill.ROUTE_INDEX_FIELDS)
                            + " 이어야 합니다.",
                        )
                    ]
                routes = list(reader)
        except (csv.Error, OSError) as exc:
            return [
                ValidationResult(
                    "error",
                    "invalid_route_index",
                    f"INDEX.csv를 읽을 수 없습니다: {exc}",
                )
            ]

        if not routes:
            results.append(
                ValidationResult(
                    "warning", "empty_route_index", "INDEX.csv에 route가 없습니다."
                )
            )

        seen_ids: set[str] = set()
        skill_root = asset.path.resolve()
        for line_number, route in enumerate(routes, start=2):
            route_id = (route.get("id") or "").strip()
            if not common.NAME_PATTERN.fullmatch(route_id):
                results.append(
                    ValidationResult(
                        "error",
                        "invalid_route_id",
                        f"INDEX.csv:{line_number} id가 kebab-case가 아닙니다: "
                        f"{route_id!r}",
                    )
                )
            elif route_id in seen_ids:
                results.append(
                    ValidationResult(
                        "error",
                        "duplicate_route_id",
                        f"INDEX.csv:{line_number} id가 중복됩니다: {route_id}",
                    )
                )
            seen_ids.add(route_id)

            for field in ("use_when", "avoid_when"):
                if not (route.get(field) or "").strip():
                    results.append(
                        ValidationResult(
                            "error",
                            f"missing_{field}",
                            f"INDEX.csv:{line_number} {field}이 비어 있습니다.",
                        )
                    )

            raw_entrypoint = (route.get("entrypoint") or "").strip()
            entrypoint = Path(raw_entrypoint)
            if (
                not raw_entrypoint
                or entrypoint.is_absolute()
                or ".." in entrypoint.parts
                or not entrypoint.parts
                or entrypoint.parts[0] != "workflows"
            ):
                results.append(
                    ValidationResult(
                        "error",
                        "unsafe_entrypoint",
                        f"INDEX.csv:{line_number} entrypoint가 workflows/ 내부 "
                        f"상대 경로가 아닙니다: {raw_entrypoint!r}",
                    )
                )
                continue

            resolved_entrypoint = (asset.path / entrypoint).resolve()
            try:
                resolved_entrypoint.relative_to(skill_root)
            except ValueError:
                results.append(
                    ValidationResult(
                        "error",
                        "unsafe_entrypoint",
                        f"INDEX.csv:{line_number} entrypoint가 Skill 밖을 "
                        f"가리킵니다: {raw_entrypoint!r}",
                    )
                )
                continue
            if not resolved_entrypoint.is_file():
                results.append(
                    ValidationResult(
                        "error",
                        "missing_entrypoint",
                        f"INDEX.csv:{line_number} entrypoint가 없습니다: "
                        f"{raw_entrypoint}",
                    )
                )

        nested_skills = sorted(
            path.relative_to(asset.path).as_posix()
            for path in workflows_path.rglob("SKILL.md")
        )
        if nested_skills:
            results.append(
                ValidationResult(
                    "error",
                    "nested_skill_entrypoint",
                    "workflows/ 아래 discoverable SKILL.md가 있습니다: "
                    + ", ".join(nested_skills),
                )
            )
        return results
