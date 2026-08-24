#!/usr/bin/env python3
"""Generate repository-local ``docs/INDEX.tsv`` and ``docs/*/INDEX.tsv`` files."""

from __future__ import annotations

import argparse
import sys
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
EXCLUDE = ["README.md", "AGENTS.md"]
EXCLUDE_GLOBS = [".*.md", "__*__.md"]


def _index_targets(docs_root: Path) -> list[Path]:
    targets = [docs_root]
    targets.extend(
        path
        for path in sorted(docs_root.iterdir())
        if path.is_dir() and any(path.rglob("*.md"))
    )
    return targets


def _desired_index(directory: Path) -> str | None:
    content = generate_index(
        directory,
        format="tsv",
        fields=["path", "description"],
        max_depth=None,
        exclude=EXCLUDE,
        exclude_globs=EXCLUDE_GLOBS,
        include_without_frontmatter=True,
    )
    return None if content == HEADER else content


def generate_docs_indexes(docs_root: Path = DOCS_ROOT, check: bool = False) -> list[str]:
    """Generate scoped docs indexes or return drift messages when ``check`` is true."""
    if not docs_root.is_dir():
        raise NotADirectoryError(docs_root)

    drift: list[str] = []
    target_indexes: set[Path] = set()

    for directory in _index_targets(docs_root):
        index_path = directory / INDEX_NAME
        target_indexes.add(index_path)
        desired = _desired_index(directory)
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
    args = parser.parse_args(argv)

    drift = generate_docs_indexes(check=args.check)
    if drift:
        for item in drift:
            print(item, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
