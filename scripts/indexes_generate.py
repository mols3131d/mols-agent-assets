"""Generate scoped INDEX.tsv files for repository and custom content roots."""

from __future__ import annotations

import argparse
import csv
import io
import sys
from collections import deque
from dataclasses import dataclass, replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX_TOOL_DIR = (
    ROOT / "src/rulesync/.rulesync/skills/mols-markdown-maintenance/scripts"
)
sys.path.insert(0, str(INDEX_TOOL_DIR))

from generate_index import generate_index  # noqa: E402

INDEX_NAME = "INDEX.tsv"
HEADER = "path\tdescription\n"


@dataclass(frozen=True)
class IndexConfig:
    root: Path
    extensions: tuple[str, ...] = (".md",)
    index_depth: int = -1
    depth: int = 0
    min_entries: int = 1
    traverse_roots: tuple[str, ...] | None = None
    directory_entry_files: tuple[str, ...] = ("README.md",)
    prune: bool = False


PRESETS = {
    "docs": IndexConfig(
        ROOT / "docs",
        traverse_roots=("development", "documentation", "references", "tools"),
        prune=True,
    ),
    "catalog": IndexConfig(
        ROOT / "catalog", extensions=(".md", ".json"), prune=True
    ),
}


def _is_content_file(path: Path, config: IndexConfig) -> bool:
    name = path.name
    return (
        path.is_file()
        and any(
            path.name.endswith(ext if ext.startswith(".") else f".{ext}")
            for ext in config.extensions
        )
        and name != "AGENTS.md"
        and not name.startswith("INDEX")
        and not (name.startswith(".") and name.endswith(".md"))
        and not (name.startswith("__") and name.endswith("__.md"))
    )


def _has_content(directory: Path, config: IndexConfig) -> bool:
    return any(_is_content_file(path, config) for path in directory.rglob("*"))


def _targets(config: IndexConfig) -> list[Path]:
    if not config.root.is_dir():
        raise NotADirectoryError(config.root)
    if config.index_depth < -1 or config.depth < -1 or config.min_entries < 1:
        raise ValueError(
            "index_depth and depth must be >= -1; min_entries must be >= 1"
        )
    if not config.extensions:
        raise ValueError("at least one extension is required")
    if not config.directory_entry_files:
        raise ValueError("at least one directory entry file is required")

    targets = []
    queue = deque([(config.root, 0)])
    while queue:
        directory, level = queue.popleft()
        targets.append(directory)
        if config.index_depth != -1 and level >= config.index_depth:
            continue
        for child in sorted(directory.iterdir()):
            if not child.is_dir():
                continue
            if level == 0 and config.traverse_roots is not None:
                if child.name not in config.traverse_roots:
                    continue
            if _has_content(child, config):
                queue.append((child, level + 1))
    return targets


def _desired_index(directory: Path, config: IndexConfig) -> str | None:
    empty_directories = [
        path.relative_to(directory).as_posix()
        for path in directory.rglob("*")
        if path.is_dir() and not _has_content(path, config)
    ]
    blocked_root_subtrees = []
    if directory == config.root and config.traverse_roots is not None:
        blocked_root_subtrees = [
            f"{child.name}/**"
            for child in config.root.iterdir()
            if child.is_dir() and child.name not in config.traverse_roots
        ]
    content = generate_index(
        directory,
        format="tsv",
        fields=["path", "description"],
        max_depth=None if config.depth == -1 else config.depth,
        file_extensions=list(config.extensions),
        exclude=["AGENTS.md", *config.directory_entry_files],
        exclude_globs=[
            ".*.md", "__*__.md", *blocked_root_subtrees, *empty_directories
        ],
        include_without_frontmatter=True,
        include_directories=True,
        directory_entry_files=list(config.directory_entry_files),
    )
    if content == HEADER:
        return None
    entries = sum(1 for _ in csv.reader(io.StringIO(content), delimiter="\t")) - 1
    if directory != config.root and entries < config.min_entries:
        return None
    return content


def expected_indexes(config: IndexConfig) -> dict[Path, str]:
    """Calculate index projections without modifying any files."""
    return {
        directory / INDEX_NAME: content
        for directory in _targets(config)
        if (content := _desired_index(directory, config)) is not None
    }


def sync_indexes(config: IndexConfig, *, check: bool = False) -> list[str]:
    """Write projections, or report missing/outdated/stale indexes read-only."""
    expected = expected_indexes(config)
    existing = set(config.root.rglob(INDEX_NAME)) if config.prune else set()
    existing.update(path for path in expected if path.exists())
    drift = []
    for path in sorted(existing | expected.keys()):
        relative = path.relative_to(config.root.parent).as_posix()
        desired = expected.get(path)
        actual = path.read_text(encoding="utf-8") if path.exists() else None
        if desired is None:
            if check:
                drift.append(f"stale: {relative}")
            else:
                path.unlink()
        elif actual != desired:
            if check:
                status = "missing" if actual is None else "outdated"
                drift.append(f"{status}: {relative}")
            else:
                path.write_text(desired, encoding="utf-8")
    return drift


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--target", choices=tuple(PRESETS))
    target.add_argument("--root", type=Path, help="Custom content root")
    parser.add_argument("--extensions", nargs="+", help="Indexed file extensions")
    parser.add_argument(
        "--directory-entry-files", nargs="+",
        help="Ordered filenames supplying directory frontmatter",
    )
    parser.add_argument(
        "--index-depth", type=int, help="Maximum INDEX.tsv materialization depth"
    )
    parser.add_argument("--depth", type=int, help="Subtree depth included by each index")
    parser.add_argument(
        "--min-entries", type=int, help="Minimum entries for non-root indexes"
    )
    parser.add_argument(
        "--traverse-roots",
        nargs="+",
        help="Root child directories eligible for nested indexes",
    )
    parser.add_argument(
        "--prune", action="store_true",
        help="Also remove INDEX.tsv files not in the expected output (custom roots)",
    )
    parser.add_argument(
        "--check", action="store_true", help="Report drift without writing files"
    )
    args = parser.parse_args(argv)
    config = PRESETS[args.target] if args.target else IndexConfig(args.root)
    overrides = {
        "extensions": tuple(args.extensions) if args.extensions is not None else None,
        "directory_entry_files": tuple(args.directory_entry_files)
        if args.directory_entry_files is not None
        else None,
        "index_depth": args.index_depth,
        "depth": args.depth,
        "min_entries": args.min_entries,
        "prune": args.prune if args.prune else None,
        "traverse_roots": tuple(args.traverse_roots)
        if args.traverse_roots is not None
        else None,
    }
    config = replace(
        config,
        **{key: value for key, value in overrides.items() if value is not None},
    )
    try:
        drift = sync_indexes(config, check=args.check)
    except (ValueError, NotADirectoryError) as exc:
        parser.error(str(exc))
    for item in drift:
        print(item, file=sys.stderr)
    return 1 if drift else 0


if __name__ == "__main__":
    raise SystemExit(main())
