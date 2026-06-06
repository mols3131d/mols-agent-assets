from __future__ import annotations

from configs import skill
from core.base import Asset, ValidationResult, Validator


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
            fields[current_key] = " ".join(current_value).strip()
            current_key = None
            current_value = []

        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        current_key = key.strip()
        current_value = [value.strip().strip(">")]

    if current_key is not None:
        fields[current_key] = " ".join(current_value).strip()

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
