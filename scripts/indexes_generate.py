"""Generate scoped INDEX.tsv files for repository and custom content roots."""

from __future__ import annotations

import argparse
import csv
import glob
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
    "catalog": IndexConfig(ROOT / "catalog", extensions=(".md", ".json"), prune=True),
}


def _normalize_extensions(extensions: tuple[str, ...]) -> tuple[str, ...]:
    normalized = []
    for ext in extensions:
        cleaned = ext.strip()
        if cleaned.startswith("."):
            cleaned = cleaned[1:]
        if not cleaned:
            raise ValueError("extensions must not contain empty values")
        normalized.append(f".{cleaned}")
    if not normalized:
        raise ValueError("at least one extension is required")
    return tuple(normalized)


def _validated_config(config: IndexConfig) -> IndexConfig:
    if not config.root.is_dir():
        raise NotADirectoryError(config.root)
    if config.index_depth < -1 or config.depth < -1 or config.min_entries < 1:
        raise ValueError(
            "index_depth and depth must be >= -1; min_entries must be >= 1"
        )
    extensions = _normalize_extensions(config.extensions)
    if not config.directory_entry_files:
        raise ValueError("at least one directory entry file is required")
    return replace(config, extensions=extensions)


def _is_content_file(path: Path, extensions: tuple[str, ...]) -> bool:
    name = path.name
    return (
        path.is_file()
        and name.endswith(extensions)
        and name != "AGENTS.md"
        and not name.startswith(("INDEX", "__index__"))
        and not (name.startswith(".") and name.endswith(".md"))
        and not (name.startswith("__") and name.endswith("__.md"))
    )


def _has_content(directory: Path, extensions: tuple[str, ...]) -> bool:
    return any(_is_content_file(path, extensions) for path in directory.rglob("*"))


def _targets(config: IndexConfig) -> list[Path]:
    targets = []
    queue = deque([(config.root, 0)])
    while queue:
        directory, level = queue.popleft()
        targets.append(directory)
        if config.index_depth != -1 and level >= config.index_depth:
            continue
        for child in sorted(directory.iterdir(), key=lambda child: child.name):
            if not child.is_dir() or child.is_symlink():
                continue
            if level == 0 and config.traverse_roots is not None:
                if child.name not in config.traverse_roots:
                    continue
            if _has_content(child, config.extensions):
                queue.append((child, level + 1))
    return targets


def _empty_directory_globs(directory: Path, extensions: tuple[str, ...]) -> list[str]:
    content_ancestors: set[Path] = set()
    subdirs: list[Path] = []
    symlink_dirs: list[Path] = []
    for path in directory.rglob("*"):
        if path.is_dir():
            if path.is_symlink():
                symlink_dirs.append(path)
            else:
                subdirs.append(path)
        elif _is_content_file(path, extensions):
            parent = path.parent
            while (
                parent != directory
                and parent != parent.parent
                and parent not in content_ancestors
            ):
                content_ancestors.add(parent)
                parent = parent.parent
    globs = [
        f"/{glob.escape(path.relative_to(directory).as_posix())}"
        for path in subdirs
        if path not in content_ancestors
    ]
    for path in symlink_dirs:
        escaped = glob.escape(path.relative_to(directory).as_posix())
        globs.extend((f"/{escaped}", f"/{escaped}/**"))
    return globs


def _desired_index(directory: Path, config: IndexConfig) -> str | None:
    empty_directories = _empty_directory_globs(directory, config.extensions)
    blocked_root_subtrees = []
    if directory == config.root and config.traverse_roots is not None:
        blocked_root_subtrees = [
            f"{glob.escape(child.name)}/**"
            for child in config.root.iterdir()
            if child.is_dir()
            and not child.is_symlink()
            and child.name not in config.traverse_roots
        ]
    content = generate_index(
        directory,
        format="tsv",
        fields=["path", "description"],
        max_depth=None if config.depth == -1 else config.depth,
        file_extensions=list(config.extensions),
        exclude=["AGENTS.md", *config.directory_entry_files],
        exclude_globs=[".*.md", "__*__.md", *blocked_root_subtrees, *empty_directories],
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


def _display_index_path(root: Path, path: Path) -> str:
    root_label = root.resolve().name if root.name in {"", ".", ".."} else root.name
    relative = path.relative_to(root).as_posix()
    return f"{root_label}/{relative}" if root_label else relative


def expected_indexes(config: IndexConfig) -> dict[Path, str]:
    """Calculate index projections without modifying any files."""
    validated = _validated_config(config)
    return {
        directory / INDEX_NAME: content
        for directory in _targets(validated)
        if (content := _desired_index(directory, validated)) is not None
    }


def sync_indexes(config: IndexConfig, *, check: bool = False) -> list[str]:
    """Write projections, or report missing/outdated/stale indexes read-only."""
    validated = _validated_config(config)
    expected = expected_indexes(validated)
    existing = set(validated.root.rglob(INDEX_NAME)) if validated.prune else set()
    existing.update(path for path in expected if path.exists())
    drift = []
    # Windows Path 대소문자 무시로 순서가 달라지지 않도록 상대 경로 tuple로 정렬
    for path in sorted(
        existing | expected.keys(),
        key=lambda path: path.relative_to(validated.root).parts,
    ):
        relative = _display_index_path(validated.root, path)
        desired = expected.get(path)
        if desired is None:
            if check:
                drift.append(f"stale: {relative}")
            else:
                path.unlink()
            continue
        if not path.exists():
            if check:
                drift.append(f"missing: {relative}")
            else:
                path.write_text(desired, encoding="utf-8", newline="\n")
            continue
        try:
            actual = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            actual = None
        if actual != desired:
            if check:
                drift.append(f"outdated: {relative}")
            else:
                path.write_text(desired, encoding="utf-8", newline="\n")
    return drift


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--target", choices=tuple(PRESETS))
    target.add_argument("--root", type=Path, help="Custom content root")
    parser.add_argument("--extensions", nargs="+", help="Indexed file extensions")
    parser.add_argument(
        "--directory-entry-files",
        nargs="+",
        help="Ordered filenames supplying directory frontmatter",
    )
    parser.add_argument(
        "--index-depth", type=int, help="Maximum INDEX.tsv materialization depth"
    )
    parser.add_argument(
        "--depth", type=int, help="Subtree depth included by each index"
    )
    parser.add_argument(
        "--min-entries", type=int, help="Minimum entries for non-root indexes"
    )
    parser.add_argument(
        "--traverse-roots",
        nargs="+",
        help="Root child directories eligible for nested indexes",
    )
    parser.add_argument(
        "--prune",
        action="store_true",
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
