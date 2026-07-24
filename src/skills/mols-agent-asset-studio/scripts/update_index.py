#!/usr/bin/env python3
"""Routing Skill 및 Asset Directory 인덱스를 스크립트로 생성한다."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from types import ModuleType

# mols-markdown-scripts 의존성 모듈 임포트 시도
gen_idx: ModuleType | None = None
try:
    markdown_scripts_dir = (
        Path(__file__).resolve().parents[2] / "mols-markdown-scripts" / "scripts"
    )
    if markdown_scripts_dir.exists() and str(markdown_scripts_dir) not in sys.path:
        sys.path.insert(0, str(markdown_scripts_dir))
    import generate_index as imported_gen_idx

    gen_idx = imported_gen_idx
except ImportError:
    pass


def generate_index_content(
    directory: Path,
    index_format: str = "csv",
    index_name: str = "__index__.csv",
    fields: list[str] | None = None,
    globs: list[str] | None = None,
    max_depth: int | None = 0,
) -> str:
    """mols-markdown-scripts 또는 내장 엔진을 활용해 인덱스 생성."""
    if gen_idx is not None:
        # format 매핑: csv -> csv, md-list -> list, md-table -> table
        fmt_map = {"csv": "csv", "md-list": "list", "md-table": "table"}
        fmt = fmt_map.get(index_format, "csv")
        return gen_idx.generate_index(
            directory, format=fmt, fields=fields, globs=globs, max_depth=max_depth
        )

    # mols-markdown-scripts를 직접 찾지 못할 경우 기본 구현체 제공
    entries = []
    for path in sorted(directory.rglob("*.md")):
        if path.name == index_name or path.name.upper().startswith("INDEX"):
            continue
        entries.append({"path": path.relative_to(directory).as_posix()})

    field_names = fields if fields else ["path", "description"]
    if index_format == "csv":
        import io

        output = io.StringIO(newline="")
        writer = csv.DictWriter(output, fieldnames=field_names, extrasaction="ignore")
        writer.writeheader()
        for entry in entries:
            writer.writerow({f: entry.get(f, "") for f in field_names})
        return output.getvalue()
    elif index_format == "md-table":
        lines = ["| Path | Description |", "| --- | --- |"]
        for entry in entries:
            lines.append(f"| [{entry['path']}]({entry['path']}) |  |")
        return "\n".join(lines) + "\n"
    else:  # md-list
        lines = ["# Index", ""]
        for entry in entries:
            lines.append(f"- [{entry['path']}]({entry['path']})")
        return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="에이전트 라우터 및 디렉토리 인덱스를 스크립트로 파싱/생성한다."
    )
    parser.add_argument("directory", type=Path, help="인덱스를 생성할 대상 디렉토리")
    parser.add_argument(
        "--format",
        choices=["csv", "md-list", "md-table"],
        default="csv",
        help="인덱스 포맷 (csv, md-list: 헤더와 리스트, md-table: 헤더와 테이블)",
    )
    parser.add_argument(
        "--fields",
        nargs="+",
        help="인덱스 출력 커스텀 필드 목록 (예: --fields file description)",
    )
    parser.add_argument(
        "--globs",
        nargs="+",
        help="탐색할 Glob 패턴 목록 (예: --globs '*.md' 'workflows/**/*.md')",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=0,
        help="최대 탐색 디렉토리 깊이 (0: 루트 디렉토리 직하위만 탐색)",
    )
    parser.add_argument(
        "--name",
        default="__index__.csv",
        help="인덱스 파일 이름 (기본값: __index__.csv)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="인덱스를 저장할 파일 경로 (미지정시 directory/name 경로 사용)",
    )

    args = parser.parse_args()
    output_path = args.output or (args.directory / args.name)

    content = generate_index_content(
        directory=args.directory,
        index_format=args.format,
        index_name=args.name,
        fields=args.fields,
        globs=args.globs,
        max_depth=args.max_depth,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    print(f"인덱스 파일이 생성되었습니다: {output_path}")


if __name__ == "__main__":
    main()
