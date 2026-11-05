"""Generate the catalog's root index from reusable content and metadata."""

from __future__ import annotations

from pathlib import Path

from scripts.docs_indexes_generate import HEADER, ROOT, generate_index

CATALOG_ROOT = ROOT / "catalog"
INDEX_NAME = "INDEX.tsv"


def expected_catalog_indexes(catalog_root: Path = CATALOG_ROOT) -> dict[Path, str]:
    """Calculate the catalog projection without writing it."""
    if not catalog_root.is_dir():
        raise NotADirectoryError(catalog_root)

    content = generate_index(
        catalog_root,
        format="tsv",
        fields=["path", "description"],
        globs=["*.md", "**/*.md", "*.json", "**/*.json"],
        file_extensions=[".md", ".json"],
        max_depth=None,
        exclude=["AGENTS.md", "README.md"],
        exclude_globs=[".*.md", "__*__.md"],
        include_without_frontmatter=True,
        include_directories=True,
        directory_entry_files=["README.md"],
    )
    return {} if content == HEADER else {catalog_root / INDEX_NAME: content}


def generate_catalog_indexes(catalog_root: Path = CATALOG_ROOT) -> None:
    """Synchronize the generated root index; validation remains read-only."""
    expected = expected_catalog_indexes(catalog_root)
    path = catalog_root / INDEX_NAME
    if path in expected:
        path.write_text(expected[path], encoding="utf-8")
    elif path.exists():
        path.unlink()

