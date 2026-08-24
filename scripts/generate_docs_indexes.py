#!/usr/bin/env python3
"""Generate breadth-first repository-local ``docs/**/INDEX.tsv`` files."""

from __future__ import annotations

import argparse
import csv
import io
import sys
from collections import deque
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INDEX_TOOL_DIR = (
    ROOT / "src/rulesync/.rulesync/skills/mols-markdown-maintenance/scripts"
)
sys.path.insert(0, str(INDEX_TOOL_DIR))

from frontmatter import parse_frontmatter_document  # noqa: E402
from generate_index import generate_index  # noqa: E402

DOCS_ROOT = ROOT / "docs"
INDEX_NAME = "INDEX.tsv"
HEADER = "path\tdescription\n"
DEFAULT_DEPTH = 1
DEFAULT_DIRECTORY_ENTRY_FILES = ("README.md", "index.md")
BASE_EXCLUDE = ("AGENTS.md",)
EXCLUDE_GLOBS = [".*.md", "__*__.md"]


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return ", ".join(_stringify(item) for item in value)
    if isinstance(value, dict):
        return ", ".join(f"{key}: {_stringify(item)}" for key, item in value.items())
    return str(value)


def _has_markdown_content(directory: Path) -> bool:
    return any(path.is_file() for path in directory.rglob("*.md"))


def _index_targets(docs_root: Path, depth: int | None) -> list[Path]:
    if depth is not None and depth < 0:
        raise ValueError("depth must be >= 0 or None")

    targets: list[Path] = []
    queue = deque([(docs_root, 0)])
    while queue:
        directory, current_depth = queue.popleft()
        targets.append(directory)

        if depth is not None and current_depth >= depth:
            continue

        for child in sorted(directory.iterdir()):
            if child.is_dir() and _has_markdown_content(child):
                queue.append((child, current_depth + 1))

    return targets


def _directory_frontmatter(
    directory: Path,
    entry_files: tuple[str, ...],
) -> dict[str, object]:
    for filename in entry_files:
        entry = directory / filename
        if not entry.is_file():
            continue
        parsed = parse_frontmatter_document(entry.read_text(encoding="utf-8"))
        if parsed is not None:
            frontmatter, _ = parsed
            return frontmatter
    return {}


def _enrich_directory_frontmatter(
    content: str,
    directory: Path,
    entry_files: tuple[str, ...],
) -> str:
    reader = csv.DictReader(io.StringIO(content), delimiter="\t")
    rows = list(reader)
    fieldnames = reader.fieldnames or ["path", "description"]

    for row in rows:
        path = row.get("path", "")
        if not path.endswith("/"):
            continue
        frontmatter = _directory_frontmatter(directory / path.rstrip("/"), entry_files)
        for field in fieldnames:
            if field in {"path", "file"} or field not in frontmatter:
                continue
            row[field] = _stringify(frontmatter[field])

    output = io.StringIO(newline="")
    writer = csv.DictWriter(
        output,
        fieldnames=fieldnames,
        delimiter="\t",
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def _desired_index(directory: Path, entry_files: tuple[str, ...]) -> str | None:
    content = generate_index(
        directory,
        format="tsv",
        fields=["path", "description"],
        max_depth=0,
        exclude=[*BASE_EXCLUDE, *entry_files],
        exclude_globs=EXCLUDE_GLOBS,
        include_without_frontmatter=True,
        include_directories=True,
    )
    content = _enrich_directory_frontmatter(content, directory, entry_files)
    return None if content == HEADER else content


def generate_docs_indexes(
    docs_root: Path = DOCS_ROOT,
    check: bool = False,
    depth: int | None = DEFAULT_DEPTH,
    directory_entry_files: tuple[str, ...] | list[str] = DEFAULT_DIRECTORY_ENTRY_FILES,
) -> list[str]:
    """Generate breadth-first docs indexes or report drift when ``check`` is true."""
    if not docs_root.is_dir():
        raise NotADirectoryError(docs_root)

    entry_files = tuple(directory_entry_files)
    drift: list[str] = []
    target_indexes: set[Path] = set()

    for directory in _index_targets(docs_root, depth):
        index_path = directory / INDEX_NAME
        target_indexes.add(index_path)
        desired = _desired_index(directory, entry_files)
        relative = index_path.relative_to(docs_root.parent).as_posix()

        if desired is None:
            if index_path.exists():
                if check:
                    drift.append(f"stale: {relative}")
                else:
                    index_path.unlink()
            continue

        current = index_path.read_text(encoding="utf-8") if index_path.exists() else None
        if current == desired:
            continue
        if check:
            drift.append(
                f"outdated: {relative}" if current is not None else f"missing: {relative}"
            )
        else:
            index_path.write_text(desired, encoding="utf-8")

    for index_path in sorted(docs_root.rglob(INDEX_NAME)):
        if index_path in target_indexes:
            continue
        relative = index_path.relative_to(docs_root.parent).as_posix()
        if check:
            drift.append(f"stale: {relative}")
        else:
            index_path.unlink()

    return drift


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report generated-index drift without modifying files",
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=DEFAULT_DEPTH,
        help="Maximum INDEX directory depth (0=root only, -1=unlimited)",
    )
    parser.add_argument(
        "--directory-entry-files",
        nargs="+",
        default=list(DEFAULT_DIRECTORY_ENTRY_FILES),
        help="Ordered directory entrypoint filenames whose frontmatter supplies directory metadata",
    )
    args = parser.parse_args(argv)

    if args.depth < -1:
        parser.error("--depth must be -1 or greater")
    depth = None if args.depth == -1 else args.depth

    drift = generate_docs_indexes(
        check=args.check,
        depth=depth,
        directory_entry_files=args.directory_entry_files,
    )
    if drift:
        for item in drift:
            print(item, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
