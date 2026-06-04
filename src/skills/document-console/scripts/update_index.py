#!/usr/bin/env python3
"""Create/update folder-local INDEX.csv from markdown frontmatter."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from index_common import (
    read_csv_header,
    resolve_output_path,
    sort_rows,
    split_csv_arg,
    write_csv,
)

DEFAULT_FIELD_ORDER = (
    "file",
    "id",
    "title",
    "name",
    "status",
    "description",
    "owner",
    "team",
    "updated",
    "created",
    "tags",
    "categories",
)


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_frontmatter(path: Path) -> dict[str, str]:
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        return {}

    end = content.find("\n---\n", 4)
    if end == -1:
        return {}

    data: dict[str, str] = {}
    current_key: str | None = None
    list_items: list[str] = []

    for raw_line in content[4:end].splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped:
            continue

        if current_key and stripped.startswith("- "):
            list_items.append(unquote(stripped[2:]))
            continue

        if current_key:
            data[current_key] = "; ".join(list_items)
            current_key = None
            list_items = []

        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue

        if value == "":
            current_key = key
            list_items = []
        elif value == "[]":
            data[key] = ""
        elif value.startswith("[") and value.endswith("]"):
            items = [unquote(item) for item in value[1:-1].split(",")]
            data[key] = "; ".join(item for item in items if item)
        else:
            data[key] = unquote(value)

    if current_key:
        data[current_key] = "; ".join(list_items)

    return data


def should_skip(path: Path, include_readme: bool) -> bool:
    name = path.name.lower()
    if path.name.endswith(".original.md"):
        return True
    if name in {"index.md", "index.csv"}:
        return True
    return name == "readme.md" and not include_readme


def find_markdown_files(folder: Path, include_readme: bool) -> list[Path]:
    return sorted(
        path
        for path in folder.glob("*.md")
        if path.is_file() and not should_skip(path, include_readme)
    )


def derive_fields(rows: list[dict[str, str]]) -> list[str]:
    available = {field for row in rows for field in row}
    fields = [field for field in DEFAULT_FIELD_ORDER if field in available]
    fields.extend(sorted(available - set(fields)))
    if "file" not in fields:
        fields.insert(0, "file")
    return fields


def build_rows(folder: Path, files: Sequence[Path]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in files:
        row = parse_frontmatter(path)
        row["file"] = path.relative_to(folder).as_posix()
        rows.append(row)
    return rows


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Create/update folder-local INDEX.csv from markdown frontmatter."
    )
    parser.add_argument("folder", help="Folder containing markdown documents.")
    parser.add_argument("--output", default="INDEX.csv", help="Output CSV filename/path.")
    parser.add_argument("--fields", help="Comma-separated output fields.")
    parser.add_argument("--sort", help="Comma-separated sort priority fields.")
    parser.add_argument("--include-readme", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    folder = Path(args.folder).resolve()
    if not folder.is_dir():
        raise SystemExit(f"not a directory: {folder}")

    index_path = resolve_output_path(folder, args.output, "INDEX.csv")

    files = find_markdown_files(folder, args.include_readme)
    rows = build_rows(folder, files)

    fields = (
        split_csv_arg(args.fields)
        or read_csv_header(index_path)
        or derive_fields(rows)
    )
    sort_fields = split_csv_arg(args.sort) or [
        field for field in ("id", "name", "file") if field in fields
    ]
    rows = sort_rows(rows, sort_fields)

    missing = {}
    for row in rows:
        missing_fields = [
            field for field in fields if field != "file" and not row.get(field)
        ]
        if missing_fields:
            missing[row.get("file", "")] = missing_fields
    missing = {key: value for key, value in missing.items() if value}

    payload = {
        "folder": str(folder),
        "index": str(index_path),
        "files": len(files),
        "fields": fields,
        "sort": sort_fields,
        "missing": missing,
        "dry_run": args.dry_run,
    }

    if not args.dry_run:
        write_csv(index_path, fields, rows)

    sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
