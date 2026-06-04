#!/usr/bin/env python3
"""문서 디렉터리를 초기화하거나 새 문서를 생성한다."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

# Add current scripts directory to sys.path to allow importing templates and update_index
scripts_dir = Path(__file__).resolve().parent
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

from templates import (
    ADR_ARCHIVE_INDEX_TEMPLATE,
    ADR_DOCUMENT_TEMPLATE,
    ADR_INDEX_TEMPLATE,
    ADR_README_TEMPLATE,
    PRD_ARCHIVE_INDEX_TEMPLATE,
    PRD_DOCUMENT_TEMPLATE,
    PRD_INDEX_TEMPLATE,
    PRD_README_TEMPLATE,
    SPEC_ARCHIVE_INDEX_TEMPLATE,
    SPEC_DOCUMENT_TEMPLATE,
    SPEC_INDEX_TEMPLATE,
    SPEC_README_TEMPLATE,
)

TEMPLATE_MAP = {
    "adr": {
        "index": ADR_INDEX_TEMPLATE,
        "readme": ADR_README_TEMPLATE,
        "archive_index": ADR_ARCHIVE_INDEX_TEMPLATE,
        "document": ADR_DOCUMENT_TEMPLATE,
        "default_status": "proposed",
    },
    "prd": {
        "index": PRD_INDEX_TEMPLATE,
        "readme": PRD_README_TEMPLATE,
        "archive_index": PRD_ARCHIVE_INDEX_TEMPLATE,
        "document": PRD_DOCUMENT_TEMPLATE,
        "default_status": "draft",
    },
    "spec": {
        "index": SPEC_INDEX_TEMPLATE,
        "readme": SPEC_README_TEMPLATE,
        "archive_index": SPEC_ARCHIVE_INDEX_TEMPLATE,
        "document": SPEC_DOCUMENT_TEMPLATE,
        "default_status": "draft",
    },
}


def normalize_kebab_case(s: str) -> str:
    """문자열을 kebab-case 형태로 정규화한다."""
    import re

    s = s.strip().lower()
    s = re.sub(r"[\s_.]+", "-", s)
    s = re.sub(r"[^a-z0-9-]", "", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def title_case_name(name: str) -> str:
    """kebab-case 명칭을 가독성 높은 제목으로 변환한다."""
    return " ".join(part.capitalize() for part in name.split("-") if part)


def format_id(raw_id: str) -> str:
    """숫자 형식의 ID를 3자리 패딩 형식(예: 001)으로 정규화한다."""
    if raw_id.isdigit():
        return f"{int(raw_id):03d}"
    return raw_id


def format_yaml_list(items: list[str]) -> str:
    """리스트를 YAML/JSON 배열 문자열로 포맷한다."""
    return json.dumps(items, ensure_ascii=False)


def get_next_id(target_dir: Path, doc_type: str) -> str:
    """디렉터리 내 기존 파일들을 스캔하여 다음 문서 ID를 결정한다."""
    if not target_dir.exists():
        return "001"

    max_id = 0
    pattern = f"{doc_type}-*.md"
    for file_path in target_dir.glob(pattern):
        name = file_path.name
        prefix = f"{doc_type}-"
        if not name.startswith(prefix):
            continue
        rest = name[len(prefix) :]
        parts = rest.split(".", 1)[0].split("-", 1)
        num_str = parts[0]
        if num_str.isdigit():
            val = int(num_str)
            if val > max_id:
                max_id = val
    return f"{max_id + 1:03d}"


def write_if_not_exists(file_path: Path, content: str) -> bool:
    """파일이 존재하지 않을 경우에만 생성한다."""
    if not file_path.exists():
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        return True
    return False


def main(argv: Sequence[str] | None = None) -> int:
    """명령행 진입점."""
    parser = argparse.ArgumentParser(
        description="Product/Architecture/Specification 문서를 생성하거나 디렉터리를 초기화한다.",
    )
    parser.add_argument(
        "name",
        nargs="?",
        help="생성할 문서 이름 (kebab-case). 디렉터리 초기화만 수행하는 경우 생략 가능.",
    )
    parser.add_argument(
        "--type",
        choices=["adr", "prd", "spec"],
        required=True,
        help="문서 유형",
    )
    parser.add_argument(
        "--path",
        required=True,
        help="문서 폴더(adr, prd, spec)가 위치하거나 생성될 상위 디렉터리",
    )
    parser.add_argument(
        "--title",
        help="문서 제목. 생략 시 name으로부터 자동 생성됩니다.",
    )
    parser.add_argument(
        "--id",
        help="문서 ID (예: 001). 생략 시 폴더 내 문서들을 스캔하여 다음 번호를 자동 부여합니다.",
    )
    parser.add_argument(
        "--status",
        help="frontmatter status 값. 생략 시 기본값(adr: proposed, prd/spec: draft)을 사용합니다.",
    )
    parser.add_argument(
        "--description",
        default="",
        help="frontmatter description 값.",
    )
    parser.add_argument(
        "--categories",
        default="",
        help="frontmatter categories 값 (쉼표로 구분).",
    )
    parser.add_argument(
        "--tags",
        default="",
        help="frontmatter tags 값 (쉼표로 구분).",
    )
    parser.add_argument(
        "--related-files",
        default="",
        help="frontmatter related-files 값 (쉼표로 구분, adr 한정).",
    )
    parser.add_argument(
        "--init-dir",
        action="store_true",
        help="개별 문서 생성 없이 해당 타입의 디렉터리 구조(INDEX.md, README.md, archive/)만 초기화합니다.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="파일을 쓰지 않고 생성 계획만 JSON으로 출력합니다.",
    )

    args = parser.parse_args(argv)

    if not args.name and not args.init_dir:
        payload = {
            "status": "error",
            "message": "자산 이름(name)을 지정하거나 --init-dir 옵션을 지정해야 합니다.",
        }
        sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        return 1

    try:
        target_dir = Path(args.path) / args.type

        # 생성 예정인 파일들을 추적한다.
        init_files = ["INDEX.md", "README.md", "archive/INDEX.md"]
        needed_init_files = []
        for f_name in init_files:
            if not (target_dir / f_name).exists():
                needed_init_files.append(f"{args.type}/{f_name}")

        planned = []
        if args.init_dir or needed_init_files:
            planned.extend(needed_init_files)

        doc_id = None
        doc_name = None
        filename = None
        doc_path = None

        if not args.init_dir:
            if args.id:
                doc_id = format_id(args.id)
            else:
                doc_id = get_next_id(target_dir, args.type)

            doc_name = normalize_kebab_case(args.name)
            filename = f"{args.type}-{doc_id}-{doc_name}.md"
            doc_path = target_dir / filename
            planned.append(f"{args.type}/{filename}")

        if args.dry_run:
            payload = {
                "status": "dry_run",
                "type": args.type,
                "target_dir": str(target_dir),
                "planned": planned,
            }
            if not args.init_dir:
                payload["name"] = doc_name
                payload["filename"] = filename
                payload["id"] = doc_id
            sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
            return 0

        # 실제 파일 생성 수행
        target_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / "archive").mkdir(parents=True, exist_ok=True)

        created_files = []
        templates = TEMPLATE_MAP[args.type]

        if write_if_not_exists(target_dir / "INDEX.md", templates["index"]):
            created_files.append(f"{args.type}/INDEX.md")
        if write_if_not_exists(target_dir / "README.md", templates["readme"]):
            created_files.append(f"{args.type}/README.md")
        if write_if_not_exists(
            target_dir / "archive/INDEX.md", templates["archive_index"]
        ):
            created_files.append(f"{args.type}/archive/INDEX.md")

        if not args.init_dir:
            assert doc_path is not None
            if doc_path.exists():
                raise FileExistsError(f"문서 파일이 이미 존재합니다: {doc_path}")

            def parse_list(val: str) -> list[str]:
                if not val:
                    return []
                return [item.strip() for item in val.split(",") if item.strip()]

            categories = parse_list(args.categories)
            tags = parse_list(args.tags)
            related_files = parse_list(args.related_files) if args.type == "adr" else []

            status = args.status or templates["default_status"]
            title = args.title or title_case_name(doc_name)

            doc_content = templates["document"].format(
                doc_id=doc_id,
                title=title,
                status=status,
                description=args.description,
                categories=format_yaml_list(categories),
                tags=format_yaml_list(tags),
                related_files=format_yaml_list(related_files),
            )

            doc_path.write_text(doc_content, encoding="utf-8")
            created_files.append(f"{args.type}/{filename}")

            # INDEX.csv를 업데이트한다. (stdout 혼선 방지를 위해 출력 리다이렉트)
            import contextlib
            import io

            f_io = io.StringIO()
            with contextlib.redirect_stdout(f_io):
                try:
                    from update_index import main as update_index_main

                    update_index_main([str(target_dir)])
                except Exception:
                    pass

        payload = {
            "status": "created",
            "type": args.type,
            "target_dir": str(target_dir),
            "created": created_files,
        }
        if not args.init_dir:
            payload["name"] = doc_name
            payload["filename"] = filename
            payload["id"] = doc_id

    except (OSError, ValueError) as exc:
        payload = {"status": "error", "message": str(exc)}
        sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        return 1

    sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
