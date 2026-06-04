#!/usr/bin/env python3
"""문서 디렉터리를 초기화하거나 새 문서를 생성한다."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

# Add current scripts directory to sys.path to allow importing templates and update_index
scripts_dir = Path(__file__).resolve().parent
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

from core import (
    DocStatus,
    DocType,
    format_yaml_list,
    normalize_kebab_case,
    title_case_name,
    write_if_not_exists,
)
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


def format_id(raw_id: str) -> str:
    """숫자 형식의 ID를 3자리 패딩 형식(예: 001)으로 정규화한다."""
    if raw_id.isdigit():
        return f"{int(raw_id):03d}"
    return raw_id


class DocumentScaffolder:
    """문서 디렉터리 구조를 초기화하는 클래스."""

    def __init__(self, base_path: Path) -> None:
        self.base_path = base_path

    def needs_init(self, doc_type: DocType) -> list[str]:
        """초기화가 필요한 파일들의 목록을 반환한다."""
        target_dir = self.base_path / doc_type.value
        init_files = ["INDEX.md", "README.md", "archive/INDEX.md"]
        needed = []
        for f_name in init_files:
            if not (target_dir / f_name).exists():
                needed.append(f"{doc_type.value}/{f_name}")
        return needed

    def initialize(self, doc_type: DocType) -> list[str]:
        """디렉터리 구조 및 인덱스 파일을 생성한다."""
        target_dir = self.base_path / doc_type.value
        target_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / "archive").mkdir(parents=True, exist_ok=True)

        created_files = []
        templates = TEMPLATE_MAP[doc_type.value]

        if write_if_not_exists(target_dir / "INDEX.md", templates["index"]):
            created_files.append(f"{doc_type.value}/INDEX.md")
        if write_if_not_exists(target_dir / "README.md", templates["readme"]):
            created_files.append(f"{doc_type.value}/README.md")
        if write_if_not_exists(
            target_dir / "archive/INDEX.md", templates["archive_index"]
        ):
            created_files.append(f"{doc_type.value}/archive/INDEX.md")

        return created_files


class DocumentCreator:
    """새로운 개별 문서를 생성하는 클래스."""

    def __init__(self, base_path: Path, doc_type: DocType) -> None:
        self.base_path = base_path
        self.doc_type = doc_type
        self.target_dir = base_path / doc_type.value
        self.scaffolder = DocumentScaffolder(base_path)

    def get_next_id(self) -> str:
        """디렉터리 내 기존 파일들을 스캔하여 다음 문서 ID를 결정한다."""
        if not self.target_dir.exists():
            return "001"

        max_id = 0
        pattern = f"{self.doc_type.value}-*.md"
        for file_path in self.target_dir.glob(pattern):
            name = file_path.name
            prefix = f"{self.doc_type.value}-"
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

    def create(
        self,
        name: str,
        title: str | None = None,
        doc_id: str | None = None,
        status: DocStatus | None = None,
        description: str = "",
        categories: list[str] | None = None,
        tags: list[str] | None = None,
        related_files: list[str] | None = None,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        """새로운 문서를 생성하거나 드라이런 계획을 수행한다."""
        # 1. ID 및 파일명 계산
        final_id = format_id(doc_id) if doc_id else self.get_next_id()
        kebab_name = normalize_kebab_case(name)
        filename = f"{self.doc_type.value}-{final_id}-{kebab_name}.md"
        doc_path = self.target_dir / filename

        # 2. 파일 생성 계획 수집
        needed_init = self.scaffolder.needs_init(self.doc_type)
        planned = list(needed_init)
        planned.append(f"{self.doc_type.value}/{filename}")

        if dry_run:
            return {
                "status": "dry_run",
                "type": self.doc_type.value,
                "target_dir": str(self.target_dir),
                "planned": planned,
                "name": kebab_name,
                "filename": filename,
                "id": final_id,
            }

        # 3. 실제 파일 생성 수행
        if doc_path.exists():
            raise FileExistsError(f"문서 파일이 이미 존재합니다: {doc_path}")

        # 디렉터리 생성 및 구조 초기화
        created_files = self.scaffolder.initialize(self.doc_type)

        # 문서 내용 작성
        templates = TEMPLATE_MAP[self.doc_type.value]
        final_status = status or DocStatus(templates["default_status"])
        final_title = title or title_case_name(kebab_name)

        doc_content = templates["document"].format(
            doc_id=final_id,
            title=final_title,
            status=final_status.value,
            description=description,
            categories=format_yaml_list(categories or []),
            tags=format_yaml_list(tags or []),
            related_files=format_yaml_list(related_files or [])
            if self.doc_type == DocType.ADR
            else "[]",
        )

        doc_path.write_text(doc_content, encoding="utf-8")
        created_files.append(f"{self.doc_type.value}/{filename}")

        # INDEX.csv 업데이트 (출력 리다이렉트 처리)
        import contextlib
        import io

        from update_index import main as update_index_main

        f_io = io.StringIO()
        with contextlib.redirect_stdout(f_io):
            try:
                update_index_main([str(self.target_dir)])
            except Exception:
                pass

        return {
            "status": "created",
            "type": self.doc_type.value,
            "target_dir": str(self.target_dir),
            "created": created_files,
            "name": kebab_name,
            "filename": filename,
            "id": final_id,
        }


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
        doc_type = DocType(args.type)
        base_path = Path(args.path)

        scaffolder = DocumentScaffolder(base_path)
        creator = DocumentCreator(base_path, doc_type)

        if args.init_dir:
            planned = scaffolder.needs_init(doc_type)
            if args.dry_run:
                payload = {
                    "status": "dry_run",
                    "type": doc_type.value,
                    "target_dir": str(base_path / doc_type.value),
                    "planned": planned,
                }
            else:
                created = scaffolder.initialize(doc_type)
                payload = {
                    "status": "created",
                    "type": doc_type.value,
                    "target_dir": str(base_path / doc_type.value),
                    "created": created,
                }
        else:

            def parse_list(val: str) -> list[str]:
                if not val:
                    return []
                return [item.strip() for item in val.split(",") if item.strip()]

            categories = parse_list(args.categories)
            tags = parse_list(args.tags)
            related_files = (
                parse_list(args.related_files) if doc_type == DocType.ADR else []
            )

            status_enum = DocStatus(args.status) if args.status else None

            payload = creator.create(
                name=args.name,
                title=args.title,
                doc_id=args.id,
                status=status_enum,
                description=args.description,
                categories=categories,
                tags=tags,
                related_files=related_files,
                dry_run=args.dry_run,
            )

    except (OSError, ValueError) as exc:
        payload = {"status": "error", "message": str(exc)}
        sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        return 1

    sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
