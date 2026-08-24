#!/usr/bin/env python3
"""Generate breadth-first repository-local ``docs/**/INDEX.tsv`` files."""

from __future__ import annotations

import argparse
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX_TOOL_DIR = (
    ROOT / "src/rulesync/.rulesync/skills/mols-markdown-maintenance/scripts"
)
sys.path.insert(0, str(INDEX_TOOL_DIR))

from generate_index import generate_index  # noqa: E402

DOCS_ROOT = ROOT / "docs"
INDEX_NAME = "INDEX.tsv"
HEADER = "path\tdescription\n"
DEFAULT_DEPTH = 1
DEFAULT_DIRECTORY_ENTRY_FILES = ("README.md", "index.md")
BASE_EXCLUDE = ("AGENTS.md",)
EXCLUDE_GLOBS = [".*.md", "__*__.md"]


def _is_route_markdown(path: Path) -> bool:
    name = path.name
    if not path.is_file() or path.suffix != ".md":
        return False
    if name in BASE_EXCLUDE or name.startswith("."):
        return False
    if name.upper().startswith("INDEX") or name.startswith("__index__"):
        return False
    if name.startswith("__") and name.endswith("__.md"):
        return False
    return True


def _has_markdown_content(directory: Path) -> bool:
    return any(_is_route_markdown(path) for path in directory.rglob("*.md"))


def _route_children(directory: Path) -> list[Path]:
    return [
        child
        for child in sorted(directory.iterdir())
        if child.is_dir() and _has_markdown_content(child)
    ]


def _index_targets(docs_root: Path, depth: int) -> list[Path]:
    if depth < -1:
        raise ValueError("depth must be -1 or greater")

    targets: list[Path] = []
    queue = deque([(docs_root, 0)])
    while queue:
        directory, current_depth = queue.popleft()
        targets.append(directory)

        if depth != -1 and current_depth >= depth:
            continue

        queue.extend((child, current_depth + 1) for child in _route_children(directory))

    return targets


def _desired_index(directory: Path, entry_files: tuple[str, ...]) -> str | None:
    route_children = set(_route_children(directory))
    excluded_directories = [
        child.name
        for child in directory.iterdir()
        if child.is_dir() and child not in route_children
    ]
    content = generate_index(
        directory,
        format="tsv",
        fields=["path", "description"],
        max_depth=0,
        exclude=[*BASE_EXCLUDE, *entry_files, *excluded_directories],
        exclude_globs=EXCLUDE_GLOBS,
        include_without_frontmatter=True,
        include_directories=True,
        directory_entry_files=list(entry_files),
    )
    return None if content == HEADER else content


def generate_docs_indexes(
    docs_root: Path = DOCS_ROOT,
    check: bool = False,
    depth: int = DEFAULT_DEPTH,
    directory_entry_files: tuple[str, ...] | list[str] = DEFAULT_DIRECTORY_ENTRY_FILES,
) -> list[str]:
    """Generate breadth-first docs indexes or report drift when ``check`` is true."""
    if not docs_root.is_dir():
        raise NotADirectoryError(docs_root)
    if depth < -1:
        raise ValueError("depth must be -1 or greater")

    entry_files = tuple(directory_entry_files)
    if not entry_files:
        raise ValueError("directory_entry_files must not be empty")

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

    drift = generate_docs_indexes(
        check=args.check,
        depth=args.depth,
        directory_entry_files=args.directory_entry_files,
    )
    if drift:
        for item in drift:
            print(item, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
