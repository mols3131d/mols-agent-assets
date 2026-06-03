#!/usr/bin/env python3
"""Agent Skills 표준 스킬 디렉터리를 초기화한다."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, Sequence


MAX_SKILL_NAME_LENGTH: Final[int] = 64
ALLOWED_RESOURCES: Final[set[str]] = {"scripts", "references", "assets"}
DEFAULT_DESCRIPTION: Final[str] = (
    "TODO: Describe what this skill does and when to use it. Use when the user "
    "asks for tasks, workflows, files, or domain work covered by this skill."
)

SKILL_TEMPLATE: Final[str] = """---
name: {skill_name}
description: {description}
{optional_frontmatter}---

# {skill_title}

목표: 이 스킬이 에이전트에게 제공하는 재사용 가능한 능력을 1-2문장으로 설명한다.

## 사용 절차

1. 요청을 분류한다.
   - 어떤 입력, 파일, 도메인, 작업이 이 스킬의 범위인지 확인한다.
   - 범위 밖이면 이 스킬을 사용하지 않는다.

2. 필요한 리소스를 선택한다.
   - 상세 지식이 필요하면 `references/`의 특정 파일을 읽는다.
   - 반복 실행이나 결정적 처리가 필요하면 `scripts/`의 특정 스크립트를 실행한다.
   - 산출물에 복사할 템플릿이나 정적 파일이 필요하면 `assets/`를 사용한다.

3. 작업을 수행하고 검증한다.
   - 결과가 사용자의 요청과 이 스킬의 완료 기준을 만족하는지 확인한다.
   - 실패하면 원인을 반영해 수정한 뒤 다시 검증한다.

## 리소스

필요한 리소스만 유지한다. 사용하지 않는 섹션과 예시 파일은 삭제한다.

{resource_notes}

## 완료 기준

- 요청된 산출물이 생성되거나 수정되었다.
- 필요한 검증을 실행했고 실패 항목을 해결했다.
- 사용하지 않는 placeholder, TODO, 불필요한 리소스가 남아 있지 않다.
"""

EXAMPLE_SCRIPT: Final[str] = '''#!/usr/bin/env python3
"""예시 스크립트. 실제 로직으로 교체하거나 삭제한다."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Sequence


def build_parser() -> argparse.ArgumentParser:
    """명령행 인자를 정의한다."""
    parser = argparse.ArgumentParser(description="예시 입력을 JSON으로 요약한다.")
    parser.add_argument("value", help="요약할 값")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """명령행 진입점."""
    args = build_parser().parse_args(argv)
    payload: dict[str, Any] = {"value": args.value, "length": len(args.value)}
    sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''

EXAMPLE_REFERENCE: Final[str] = """# 상세 참조

이 파일은 `SKILL.md`에 항상 넣기에는 긴 도메인 지식, API 세부사항, 예시, 정책을 담는다.

## 읽는 조건

- `SKILL.md`에서 이 파일을 읽어야 하는 조건을 명확히 지정한다.
- 조건 없이 항상 읽어야 하는 내용이면 `SKILL.md` 본문으로 옮긴다.
"""

EXAMPLE_ASSET: Final[str] = """이 파일은 실제 템플릿, 이미지, 설정 예시 같은 정적 자산으로 교체한다.
사용하지 않으면 `assets/`와 함께 삭제한다.
"""


@dataclass(frozen=True)
class InitRequest:
    """스킬 초기화 요청을 표현한다."""

    raw_name: str
    output_dir: Path
    description: str
    resources: list[str]
    include_examples: bool
    license_value: str | None
    compatibility: str | None
    metadata: dict[str, str]
    allowed_tools: str | None
    dry_run: bool


def normalize_skill_name(skill_name: str) -> str:
    """스킬 이름을 Agent Skills 호환 kebab-case로 정규화한다."""
    normalized: str = skill_name.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = normalized.strip("-")
    normalized = re.sub(r"-{2,}", "-", normalized)
    return normalized


def title_case_skill_name(skill_name: str) -> str:
    """kebab-case 스킬 이름을 제목으로 바꾼다."""
    return " ".join(part.capitalize() for part in skill_name.split("-") if part)


def yaml_quote(value: str) -> str:
    """YAML double-quoted scalar를 생성한다."""
    escaped: str = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return f'"{escaped}"'


def parse_resources(raw_resources: str) -> list[str]:
    """쉼표로 구분된 리소스 목록을 검증하고 중복을 제거한다."""
    if not raw_resources:
        return []

    resources: list[str] = [item.strip() for item in raw_resources.split(",") if item.strip()]
    invalid: list[str] = sorted({item for item in resources if item not in ALLOWED_RESOURCES})
    if invalid:
        allowed: str = ", ".join(sorted(ALLOWED_RESOURCES))
        raise ValueError(f"알 수 없는 리소스 유형: {', '.join(invalid)}. 허용값: {allowed}")

    deduped: list[str] = []
    seen: set[str] = set()
    for resource in resources:
        if resource not in seen:
            deduped.append(resource)
            seen.add(resource)
    return deduped


def parse_metadata(raw_items: Sequence[str]) -> dict[str, str]:
    """key=value 형식 metadata 인자를 파싱한다."""
    metadata: dict[str, str] = {}
    for item in raw_items:
        if "=" not in item:
            raise ValueError(f"metadata는 key=value 형식이어야 합니다: {item}")
        key, value = item.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise ValueError(f"metadata key가 비어 있습니다: {item}")
        metadata[key] = value
    return metadata


def build_optional_frontmatter(request: InitRequest) -> str:
    """선택 frontmatter 필드를 만든다."""
    lines: list[str] = []
    if request.license_value:
        lines.append(f"license: {yaml_quote(request.license_value)}")
    if request.compatibility:
        lines.append(f"compatibility: {yaml_quote(request.compatibility)}")
    if request.metadata:
        lines.append("metadata:")
        for key in sorted(request.metadata):
            lines.append(f"  {key}: {yaml_quote(request.metadata[key])}")
    if request.allowed_tools:
        lines.append(f"allowed-tools: {yaml_quote(request.allowed_tools)}")
    if not lines:
        return ""
    return "\n".join(lines) + "\n"


def build_skill_content(skill_name: str, request: InitRequest) -> str:
    """SKILL.md 템플릿 내용을 만든다."""
    return SKILL_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=title_case_skill_name(skill_name),
        description=yaml_quote(request.description),
        optional_frontmatter=build_optional_frontmatter(request),
        resource_notes=build_resource_notes(request),
    )


def build_resource_notes(request: InitRequest) -> str:
    """선택한 리소스에 맞는 SKILL.md 안내 문구를 만든다."""
    if not request.resources:
        return "현재 선택된 리소스 디렉터리는 없다. 필요한 경우에만 `scripts/`, `references/`, `assets/`를 추가한다."

    lines: list[str] = []
    if "scripts" in request.resources:
        lines.append("- `scripts/`: 반복 실행 또는 결정적 처리가 필요한 명령을 둔다.")
        if request.include_examples:
            lines.append("- `scripts/example.py`: 예시 스크립트다. 실제 로직으로 교체하거나 삭제한다.")
    if "references" in request.resources:
        lines.append("- `references/`: 조건부로 읽을 상세 문서를 둔다.")
        if request.include_examples:
            lines.append("- 상세 참조가 필요하면 `references/reference.md`를 읽는다.")
    if "assets" in request.resources:
        lines.append("- `assets/`: 산출물에 복사하거나 삽입할 정적 자산을 둔다.")
        if request.include_examples:
            lines.append("- `assets/example.txt`: 예시 자산이다. 실제 자산으로 교체하거나 삭제한다.")
    return "\n".join(lines)


def write_text(path: Path, content: str, executable: bool = False) -> None:
    """텍스트 파일을 쓰고 필요하면 실행 권한을 부여한다."""
    path.write_text(content, encoding="utf-8")
    if executable:
        path.chmod(0o755)


def create_resource_dirs(skill_dir: Path, request: InitRequest) -> list[str]:
    """요청된 리소스 디렉터리와 예시 파일을 생성한다."""
    created: list[str] = []
    for resource in request.resources:
        resource_dir: Path = skill_dir / resource
        resource_dir.mkdir(exist_ok=True)
        created.append(resource_dir.relative_to(skill_dir).as_posix() + "/")

        if not request.include_examples:
            continue

        if resource == "scripts":
            example_path: Path = resource_dir / "example.py"
            write_text(example_path, EXAMPLE_SCRIPT, executable=True)
            created.append(example_path.relative_to(skill_dir).as_posix())
        elif resource == "references":
            example_path = resource_dir / "reference.md"
            write_text(example_path, EXAMPLE_REFERENCE)
            created.append(example_path.relative_to(skill_dir).as_posix())
        elif resource == "assets":
            example_path = resource_dir / "example.txt"
            write_text(example_path, EXAMPLE_ASSET)
            created.append(example_path.relative_to(skill_dir).as_posix())
    return created


def init_skill(request: InitRequest) -> dict[str, Any]:
    """스킬 디렉터리를 생성하고 결과 payload를 반환한다."""
    skill_name: str = normalize_skill_name(request.raw_name)
    if not skill_name:
        raise ValueError("스킬 이름에는 영문자 또는 숫자가 1개 이상 필요합니다.")
    if len(skill_name) > MAX_SKILL_NAME_LENGTH:
        raise ValueError(
            f"스킬 이름은 {MAX_SKILL_NAME_LENGTH}자 이하여야 합니다. 현재 {len(skill_name)}자입니다."
        )

    skill_dir: Path = request.output_dir.resolve() / skill_name
    planned_files: list[str] = ["SKILL.md"]
    for resource in request.resources:
        planned_files.append(f"{resource}/")
        if request.include_examples:
            example_name: str = {
                "scripts": "scripts/example.py",
                "references": "references/reference.md",
                "assets": "assets/example.txt",
            }[resource]
            planned_files.append(example_name)

    if request.dry_run:
        return {
            "status": "dry_run",
            "skill_name": skill_name,
            "skill_dir": str(skill_dir),
            "normalized": skill_name != request.raw_name,
            "planned": planned_files,
        }

    if skill_dir.exists():
        raise FileExistsError(f"스킬 디렉터리가 이미 있습니다: {skill_dir}")

    skill_dir.mkdir(parents=True, exist_ok=False)
    write_text(skill_dir / "SKILL.md", build_skill_content(skill_name, request))
    created: list[str] = ["SKILL.md"]
    created.extend(create_resource_dirs(skill_dir, request))

    return {
        "status": "created",
        "skill_name": skill_name,
        "skill_dir": str(skill_dir),
        "normalized": skill_name != request.raw_name,
        "created": created,
        "next_steps": [
            "SKILL.md의 TODO와 범위 설명을 실제 내용으로 교체한다.",
            "사용하지 않는 예시 파일과 리소스 디렉터리를 삭제한다.",
            "skills-ref validate <skill-dir> 또는 scripts/validate_skill.py로 검증한다.",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    """명령행 파서를 만든다."""
    parser = argparse.ArgumentParser(
        description="Agent Skills 표준 SKILL.md 기반 스킬 디렉터리를 초기화한다.",
    )
    parser.add_argument("skill_name", help="생성할 스킬 이름. kebab-case로 정규화된다.")
    parser.add_argument("--path", required=True, help="스킬 폴더를 만들 상위 디렉터리")
    parser.add_argument(
        "--description",
        default=DEFAULT_DESCRIPTION,
        help="frontmatter description 값. 생략하면 TODO placeholder를 사용한다.",
    )
    parser.add_argument(
        "--resources",
        default="",
        help="생성할 리소스 디렉터리. 예: scripts,references,assets",
    )
    parser.add_argument(
        "--examples",
        action="store_true",
        help="선택한 리소스 디렉터리에 예시 파일을 함께 생성한다.",
    )
    parser.add_argument("--license", dest="license_value", help="frontmatter license 값")
    parser.add_argument("--compatibility", help="frontmatter compatibility 값")
    parser.add_argument(
        "--metadata",
        action="append",
        default=[],
        help="frontmatter metadata 항목. key=value 형식으로 반복 지정 가능",
    )
    parser.add_argument("--allowed-tools", help="frontmatter allowed-tools 값")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="파일을 만들지 않고 생성 계획만 JSON으로 출력한다.",
    )
    return parser


def request_from_args(args: argparse.Namespace) -> InitRequest:
    """argparse 결과를 초기화 요청으로 변환한다."""
    resources: list[str] = parse_resources(args.resources)
    if args.examples and not resources:
        raise ValueError("--examples는 --resources와 함께 사용해야 합니다.")
    return InitRequest(
        raw_name=args.skill_name,
        output_dir=Path(args.path),
        description=args.description,
        resources=resources,
        include_examples=args.examples,
        license_value=args.license_value,
        compatibility=args.compatibility,
        metadata=parse_metadata(args.metadata),
        allowed_tools=args.allowed_tools,
        dry_run=args.dry_run,
    )


def main(argv: Sequence[str] | None = None) -> int:
    """명령행 진입점."""
    parser: argparse.ArgumentParser = build_parser()
    try:
        request: InitRequest = request_from_args(parser.parse_args(argv))
        payload: dict[str, Any] = init_skill(request)
    except (OSError, ValueError) as exc:
        payload = {"status": "error", "message": str(exc)}
        sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        return 1

    sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
