#!/usr/bin/env python3
"""Agent Skills 구조와 기본 품질 기준을 검증한다."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

FORBIDDEN_FILES: Final[set[str]] = {
    "CHANGELOG.md",
    "INSTALLATION_GUIDE.md",
    "QUICK_REFERENCE.md",
}
ALLOWED_FRONTMATTER_KEYS: Final[set[str]] = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
NAME_PATTERN: Final[re.Pattern[str]] = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TRIGGER_WORDS: Final[tuple[str, ...]] = (
    "trigger",
    "use when",
    "사용",
    "트리거",
    "invoke",
    "when",
    "/",
)
REFERENCE_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"\((references/[^)]+)\)|`(references/[^`]+)`"
)


@dataclass(frozen=True)
class ValidationResult:
    """검증 결과 한 건을 표현한다."""

    level: str
    code: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {"level": self.level, "code": self.code, "message": self.message}


def parse_frontmatter(content: str) -> tuple[dict[str, str], str]:
    """간단한 YAML frontmatter에서 문자열 필드를 추출한다."""
    if not content.startswith("---\n"):
        return {}, content

    end_index: int = content.find("\n---\n", 4)
    if end_index == -1:
        return {}, content

    raw_frontmatter: str = content[4:end_index]
    body: str = content[end_index + 5 :]
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


def find_reference_links(skill_md: str) -> set[str]:
    """SKILL.md 본문에서 references 링크를 찾는다."""
    references: set[str] = set()
    for match in REFERENCE_PATTERN.finditer(skill_md):
        reference_path: str | None = match.group(1) or match.group(2)
        if reference_path:
            references.add(reference_path)
    return references


def validate_skill(skill_dir: Path) -> list[ValidationResult]:
    """스킬 디렉터리 전체를 검증한다."""
    results: list[ValidationResult] = []
    skill_md_path: Path = skill_dir / "SKILL.md"

    if not skill_md_path.exists():
        return [
            ValidationResult(
                level="error",
                code="missing_skill_md",
                message=f"{skill_md_path} 파일이 없습니다.",
            )
        ]

    content: str = skill_md_path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(content)

    expected_name: str = skill_dir.name
    actual_name: str | None = frontmatter.get("name")
    description: str = frontmatter.get("description", "")
    compatibility: str = frontmatter.get("compatibility", "")

    unexpected_keys: set[str] = set(frontmatter) - ALLOWED_FRONTMATTER_KEYS
    if unexpected_keys:
        results.append(
            ValidationResult(
                level="error",
                code="unexpected_frontmatter",
                message=f"허용되지 않은 frontmatter 필드: {', '.join(sorted(unexpected_keys))}",
            )
        )

    if actual_name != expected_name:
        results.append(
            ValidationResult(
                level="error",
                code="name_mismatch",
                message=f"frontmatter name={actual_name!r}, folder={expected_name!r}",
            )
        )
    elif actual_name is not None:
        if len(actual_name) > 64:
            results.append(
                ValidationResult(
                    level="error",
                    code="name_too_long",
                    message=f"name은 64자 이하여야 합니다. 현재 {len(actual_name)}자입니다.",
                )
            )
        if not NAME_PATTERN.fullmatch(actual_name):
            results.append(
                ValidationResult(
                    level="error",
                    code="invalid_name",
                    message="name은 소문자 영문, 숫자, 단일 하이픈만 사용할 수 있습니다.",
                )
            )

    if not description:
        results.append(
            ValidationResult(
                level="error",
                code="missing_description",
                message="frontmatter description이 없습니다.",
            )
        )
    else:
        if len(description) > 1024:
            results.append(
                ValidationResult(
                    level="error",
                    code="description_too_long",
                    message=f"description은 1024자 이하여야 합니다. 현재 {len(description)}자입니다.",
                )
            )
        if not any(word.lower() in description.lower() for word in TRIGGER_WORDS):
            results.append(
                ValidationResult(
                    level="warning",
                    code="weak_trigger",
                    message="description에 사용 시점 또는 트리거 표현이 부족합니다.",
                )
            )

    if compatibility and len(compatibility) > 500:
        results.append(
            ValidationResult(
                level="error",
                code="compatibility_too_long",
                message=f"compatibility는 500자 이하여야 합니다. 현재 {len(compatibility)}자입니다.",
            )
        )

    body_line_count: int = len(body.splitlines())
    if body_line_count > 500:
        results.append(
            ValidationResult(
                level="warning",
                code="long_skill_body",
                message=f"SKILL.md 본문이 {body_line_count}줄입니다. references/ 분리를 검토하세요.",
            )
        )

    existing_file_names: set[str] = {
        path.name for path in skill_dir.iterdir() if path.is_file()
    }
    for forbidden_file in sorted(existing_file_names & FORBIDDEN_FILES):
        results.append(
            ValidationResult(
                level="warning",
                code="forbidden_aux_doc",
                message=f"{forbidden_file} 파일은 스킬 산출물에서 보통 불필요합니다.",
            )
        )

    reference_dir: Path = skill_dir / "references"
    if reference_dir.exists():
        linked_references: set[str] = find_reference_links(content)
        for reference_path in sorted(reference_dir.glob("*.md")):
            relative_path: str = reference_path.relative_to(skill_dir).as_posix()
            if relative_path not in linked_references:
                results.append(
                    ValidationResult(
                        level="warning",
                        code="unlinked_reference",
                        message=f"{relative_path} 파일이 SKILL.md에서 연결되지 않았습니다.",
                    )
                )

    return results


def main(argv: list[str]) -> int:
    """명령행 진입점."""
    if len(argv) != 2:
        payload: dict[str, Any] = {
            "status": "error",
            "results": [
                ValidationResult(
                    level="error",
                    code="usage",
                    message="사용법: validate_skill.py <skill-dir>",
                ).to_dict()
            ],
        }
        sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        return 2

    skill_dir: Path = Path(argv[1]).resolve()
    results: list[ValidationResult] = validate_skill(skill_dir)
    has_error: bool = any(result.level == "error" for result in results)
    payload = {
        "status": "fail" if has_error else "pass",
        "results": [result.to_dict() for result in results],
    }
    sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    return 1 if has_error else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
