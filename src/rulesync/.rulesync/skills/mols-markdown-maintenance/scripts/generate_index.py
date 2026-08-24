#!/usr/bin/env python3
"""Generate indexes from Markdown YAML frontmatter."""

from __future__ import annotations

import argparse
import csv
import fnmatch
import io
from pathlib import Path
from typing import Any

from frontmatter import parse_frontmatter_document

CORE_FIELDS = ("title", "description", "tags", "status")
CSV_FIELDS = ("file", *CORE_FIELDS)
SUPPORTED_FORMATS = ("csv", "tsv", "table", "list")
GROUP_SORTS = ("alpha", "input")
DEFAULT_FILE_GLOBS = ("*.md", "**/*.md")


def _is_excluded(
    path: Path,
    relative_path: str,
    exclude: list[str] | None,
    exclude_globs: list[str] | None,
) -> bool:
    if path.name in set(exclude or []):
        return True
    return any(
        fnmatch.fnmatch(path.name, pattern) or fnmatch.fnmatch(relative_path, pattern)
        for pattern in exclude_globs or []
    )


def _normalize_extensions(extensions: list[str] | None) -> tuple[str, ...]:
    normalized = []
    for extension in extensions or []:
        value = extension.strip()
        if not value:
            raise ValueError("file extensions must not be empty")
        normalized.append(value if value.startswith(".") else f".{value}")
    return tuple(dict.fromkeys(normalized))


def _matches_extension(path: Path, extensions: tuple[str, ...]) -> bool:
    return not extensions or path.name.endswith(extensions)


def _file_patterns(
    globs: list[str] | None,
    extensions: tuple[str, ...],
) -> tuple[str, ...] | list[str]:
    if globs:
        return globs
    if extensions:
        return ("*", "**/*")
    return DEFAULT_FILE_GLOBS


def _path_depth(path: Path, directory: Path, *, is_directory: bool) -> int:
    parts = path.relative_to(directory).parts
    return len(parts) - (1 if is_directory else 1)


def _collect_entries(
    directory: Path,
    globs: list[str] | None = None,
    max_depth: int | None = None,
    required_fields: list[str] | None = None,
    unique_fields: list[str] | None = None,
    exclude: list[str] | None = None,
    exclude_globs: list[str] | None = None,
    include_without_frontmatter: bool = False,
    include_files: bool = True,
    file_extensions: list[str] | None = None,
    include_directories: bool = False,
) -> list[dict[str, Any]]:
    extensions = _normalize_extensions(file_extensions)
    found_paths: set[Path] = set()

    if include_files:
        for pattern in _file_patterns(globs, extensions):
            for path in directory.glob(pattern):
                if not path.is_file() or not _matches_extension(path, extensions):
                    continue
                if path.name.upper().startswith("INDEX") or path.name.startswith(
                    "__index__"
                ):
                    continue

                relative_path = path.relative_to(directory).as_posix()
                if _is_excluded(path, relative_path, exclude, exclude_globs):
                    continue

                depth = _path_depth(path, directory, is_directory=False)
                if max_depth is not None and depth > max_depth:
                    continue

                found_paths.add(path)

    if include_directories:
        for path in directory.glob("**/*"):
            if not path.is_dir():
                continue
            relative_path = path.relative_to(directory).as_posix()
            if _is_excluded(path, relative_path, exclude, exclude_globs):
                continue

            depth = _path_depth(path, directory, is_directory=True)
            if max_depth is not None and depth > max_depth:
                continue

            found_paths.add(path)

    entries = []
    for path in sorted(found_paths):
        relative_path = path.relative_to(directory).as_posix()
        if path.is_dir():
            entries.append({"path": f"{relative_path}/", "file": f"{relative_path}/"})
            continue

        parsed = parse_frontmatter_document(path.read_text(encoding="utf-8"))
        if parsed is None:
            if required_fields:
                raise ValueError(
                    f"{relative_path}: YAML frontmatter is required for fields: "
                    + ", ".join(required_fields)
                )
            if include_without_frontmatter:
                entries.append({"path": relative_path, "file": relative_path})
            continue
        frontmatter, _ = parsed
        missing = [
            field
            for field in required_fields or []
            if not _stringify(frontmatter.get(field)).strip()
        ]
        if missing:
            raise ValueError(
                f"{relative_path}: required frontmatter fields missing: "
                + ", ".join(missing)
            )
        entries.append(
            {**frontmatter, "path": relative_path, "file": relative_path}
        )

    for field in unique_fields or []:
        seen: dict[str, str] = {}
        for entry in entries:
            value = _stringify(entry.get(field)).strip()
            if not value:
                continue
            if value in seen:
                raise ValueError(
                    f"duplicate frontmatter {field}={value!r}: "
                    f"{seen[value]}, {entry['path']}"
                )
            seen[value] = entry["path"]
    return entries


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return ", ".join(_stringify(item) for item in value)
    if isinstance(value, dict):
        return ", ".join(f"{key}: {_stringify(item)}" for key, item in value.items())
    return str(value)


def _delimited_output(
    entries: list[dict[str, Any]],
    fields: tuple[str, ...] | list[str],
    delimiter: str,
    quoting: int,
) -> str:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(
        output,
        fieldnames=fields,
        extrasaction="ignore",
        delimiter=delimiter,
        quoting=quoting,
        lineterminator="\n",
    )
    writer.writeheader()
    for entry in entries:
        writer.writerow({field: _stringify(entry.get(field)) for field in fields})
    return output.getvalue()


def _csv_output(
    entries: list[dict[str, Any]], fields: tuple[str, ...] | list[str] = CSV_FIELDS
) -> str:
    return _delimited_output(entries, fields, ",", csv.QUOTE_ALL)


def _tsv_output(
    entries: list[dict[str, Any]], fields: tuple[str, ...] | list[str] = CSV_FIELDS
) -> str:
    return _delimited_output(entries, fields, "\t", csv.QUOTE_MINIMAL)


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
            f"[{_escape_table(entry['path'])}]({entry['path']})",
            _link_title(_stringify(entry.get("title")), entry["path"]),
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
        title = _stringify(entry.get("title")) or entry["path"]
        lines.append(f"{'#' * level} [{title}]({entry['path']})")
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
    fields: list[str] | None = None,
    globs: list[str] | None = None,
    max_depth: int | None = None,
    group_by: list[str] | None = None,
    group_label: bool = True,
    group_missing: str = "[unset]",
    group_sort: str = "alpha",
    required_fields: list[str] | None = None,
    unique_fields: list[str] | None = None,
    exclude: list[str] | None = None,
    exclude_globs: list[str] | None = None,
    include_without_frontmatter: bool = False,
    include_files: bool = True,
    file_extensions: list[str] | None = None,
    include_directories: bool = False,
) -> str:
    """Generate an index string from selected filesystem entries below ``directory``."""
    if not directory.is_dir():
        raise NotADirectoryError(directory)
    if format not in SUPPORTED_FORMATS:
        raise ValueError(f"unsupported format: {format}")
    if group_by and format != "list":
        raise ValueError("group_by is only supported with format='list'")
    if group_sort not in GROUP_SORTS:
        raise ValueError(f"unsupported group sort: {group_sort}")
    if not include_files and file_extensions:
        raise ValueError("file_extensions requires include_files=True")

    entries = _collect_entries(
        directory,
        globs=globs,
        max_depth=max_depth,
        required_fields=required_fields,
        unique_fields=unique_fields,
        exclude=exclude,
        exclude_globs=exclude_globs,
        include_without_frontmatter=include_without_frontmatter,
        include_files=include_files,
        file_extensions=file_extensions,
        include_directories=include_directories,
    )
    selected_fields = fields if fields else list(CSV_FIELDS)
    if format == "csv":
        return _csv_output(entries, fields=selected_fields)
    if format == "tsv":
        return _tsv_output(entries, fields=selected_fields)
    if format == "table":
        return _table_output(entries)
    return _list_output(entries, group_by, group_label, group_missing, group_sort)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--format", choices=SUPPORTED_FORMATS, default="csv")
    parser.add_argument(
        "--fields",
        nargs="+",
        help="Custom fields/headers for delimited output (e.g. --fields path description)",
    )
    parser.add_argument(
        "--globs",
        nargs="+",
        help="Glob patterns to search (e.g. --globs '*.md' 'workflows/**/*.md')",
    )
    parser.add_argument(
        "--files",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Include files (default: enabled; use --no-files for directory-only indexes)",
    )
    parser.add_argument(
        "--file-extensions",
        nargs="+",
        default=[],
        help="Filter files by one or more suffixes (e.g. .md .mdx .skill.md)",
    )
    parser.add_argument(
        "--directories",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Include directories as path entries ending with '/'",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=0,
        help="Maximum directory depth to scan (0 = directory root entries only)",
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--group-by", nargs="+", default=[])
    parser.add_argument(
        "--group-label", action=argparse.BooleanOptionalAction, default=True
    )
    parser.add_argument("--group-missing", default="[unset]")
    parser.add_argument("--group-sort", choices=GROUP_SORTS, default="alpha")
    parser.add_argument(
        "--require-fields",
        nargs="+",
        default=[],
        help="Fail when an indexed file lacks any listed frontmatter field",
    )
    parser.add_argument(
        "--unique-fields",
        nargs="+",
        default=[],
        help="Fail when any listed frontmatter field contains duplicate values",
    )
    parser.add_argument(
        "--exclude",
        nargs="+",
        default=[],
        help="Exclude entries by exact basename",
    )
    parser.add_argument(
        "--exclude-glob",
        nargs="+",
        default=[],
        help="Exclude entries when basename or relative path matches a glob",
    )
    parser.add_argument(
        "--include-without-frontmatter",
        action="store_true",
        help="Include matching files without YAML frontmatter",
    )
    args = parser.parse_args(argv)
    result = generate_index(
        directory=args.directory,
        format=args.format,
        fields=args.fields,
        globs=args.globs,
        max_depth=args.max_depth,
        group_by=args.group_by,
        group_label=args.group_label,
        group_missing=args.group_missing,
        group_sort=args.group_sort,
        required_fields=args.require_fields,
        unique_fields=args.unique_fields,
        exclude=args.exclude,
        exclude_globs=args.exclude_glob,
        include_without_frontmatter=args.include_without_frontmatter,
        include_files=args.files,
        file_extensions=args.file_extensions,
        include_directories=args.directories,
    )
    if args.output:
        args.output.write_text(result, encoding="utf-8")
    else:
        print(result, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
