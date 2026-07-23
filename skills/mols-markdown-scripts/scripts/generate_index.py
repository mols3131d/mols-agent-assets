#!/usr/bin/env python3
"""Generate indexes from Markdown YAML frontmatter."""

from __future__ import annotations

import argparse
import csv
import io
from pathlib import Path
from typing import Any

import yaml

CORE_FIELDS = ("title", "description", "tags", "status")
CSV_FIELDS = ("file", *CORE_FIELDS)
SUPPORTED_FORMATS = ("csv", "table", "list")
GROUP_SORTS = ("alpha", "input")


def _parse_frontmatter(content: str) -> dict[str, Any] | None:
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return None

    end = next(
        (index for index, line in enumerate(lines[1:], 1) if line.strip() == "---"),
        None,
    )
    if end is None:
        return None

    data = yaml.safe_load("\n".join(lines[1:end]))
    return data if isinstance(data, dict) else None


def _collect_entries(directory: Path) -> list[dict[str, Any]]:
    entries = []
    for path in sorted(directory.rglob("*.md")):
        if path.name.upper().startswith("INDEX"):
            continue
        frontmatter = _parse_frontmatter(path.read_text(encoding="utf-8"))
        if frontmatter is None:
            continue
        entries.append({"file": path.relative_to(directory).as_posix(), **frontmatter})
    return entries


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return ", ".join(_stringify(item) for item in value)
    if isinstance(value, dict):
        return ", ".join(f"{key}: {_stringify(item)}" for key, item in value.items())
    return str(value)


def _csv_output(entries: list[dict[str, Any]]) -> str:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(
        output,
        fieldnames=CSV_FIELDS,
        extrasaction="ignore",
        quoting=csv.QUOTE_ALL,
    )
    writer.writeheader()
    for entry in entries:
        writer.writerow({field: _stringify(entry.get(field)) for field in CSV_FIELDS})
    return output.getvalue()


def _escape_table(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", "<br>")


def _link_title(value: str, path: str) -> str:
    return f"[{_escape_table(value)}]({path})"


def _table_output(entries: list[dict[str, Any]]) -> str:
    headers = ("File", "Title", "Description", "Tags", "Status")
    lines: list[str] = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for entry in entries:
        values = [
            f"[{_escape_table(entry['file'])}]({entry['file']})",
            _link_title(_stringify(entry.get("title")), entry["file"]),
            _escape_table(_stringify(entry.get("description"))),
            _escape_table(_stringify(entry.get("tags"))),
            _escape_table(_stringify(entry.get("status"))),
        ]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines) + "\n"


def _group_value(entry: dict[str, Any], field: str, missing: str) -> str:
    value = _stringify(entry.get(field))
    return value or missing


def _group_entries(
    entries: list[dict[str, Any]],
    fields: list[str],
    missing: str,
    sort: str,
) -> dict[str, Any]:
    if not fields:
        return {"entries": entries}

    groups: dict[str, list[dict[str, Any]]] = {}
    for entry in entries:
        groups.setdefault(_group_value(entry, fields[0], missing), []).append(entry)
    if sort == "alpha":
        groups = dict(sorted(groups.items()))
    return {
        "groups": {
            value: _group_entries(group, fields[1:], missing, sort)
            for value, group in groups.items()
        }
    }


def _append_list_entries(
    lines: list[str], entries: list[dict[str, Any]], level: int
) -> None:
    for entry in entries:
        title = _stringify(entry.get("title")) or entry["file"]
        lines.append(f"{'#' * level} [{title}]({entry['file']})")
        for field in CORE_FIELDS:
            value = _stringify(entry.get(field))
            if value:
                lines.append(f"- **{field.capitalize()}**: {value}")
        lines.append("")


def _append_grouped_list(
    lines: list[str],
    tree: dict[str, Any],
    fields: list[str],
    level: int,
    label: bool,
) -> None:
    if "entries" in tree:
        _append_list_entries(lines, tree["entries"], level)
        return
    field = fields[0]
    for value, child in tree["groups"].items():
        heading = f"{field.capitalize()}: {value}" if label else value
        lines.extend([f"{'#' * level} {heading}", ""])
        _append_grouped_list(lines, child, fields[1:], level + 1, label)


def _list_output(
    entries: list[dict[str, Any]],
    group_by: list[str] | None = None,
    group_label: bool = True,
    group_missing: str = "[unset]",
    group_sort: str = "alpha",
) -> str:
    lines = ["# Index", ""]
    if group_by:
        tree = _group_entries(entries, group_by, group_missing, group_sort)
        _append_grouped_list(lines, tree, group_by, 2, group_label)
    else:
        _append_list_entries(lines, entries, 2)
    return "\n".join(lines).rstrip() + "\n"


def generate_index(
    directory: Path,
    format: str = "csv",
    group_by: list[str] | None = None,
    group_label: bool = True,
    group_missing: str = "[unset]",
    group_sort: str = "alpha",
) -> str:
    """Generate an index string from Markdown files below ``directory``."""
    if not directory.is_dir():
        raise NotADirectoryError(directory)
    if format not in SUPPORTED_FORMATS:
        raise ValueError(f"unsupported format: {format}")
    if group_by and format != "list":
        raise ValueError("group_by is only supported with format='list'")
    if group_sort not in GROUP_SORTS:
        raise ValueError(f"unsupported group sort: {group_sort}")

    entries = _collect_entries(directory)
    if format == "csv":
        return _csv_output(entries)
    if format == "table":
        return _table_output(entries)
    return _list_output(entries, group_by, group_label, group_missing, group_sort)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--format", choices=SUPPORTED_FORMATS, default="csv")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--group-by", nargs="+", default=[])
    parser.add_argument(
        "--group-label", action=argparse.BooleanOptionalAction, default=True
    )
    parser.add_argument("--group-missing", default="[unset]")
    parser.add_argument("--group-sort", choices=GROUP_SORTS, default="alpha")
    args = parser.parse_args()
    result = generate_index(
        args.directory,
        args.format,
        args.group_by,
        args.group_label,
        args.group_missing,
        args.group_sort,
    )
    if args.output:
        args.output.write_text(result, encoding="utf-8")
    else:
        print(result, end="")


if __name__ == "__main__":
    main()
