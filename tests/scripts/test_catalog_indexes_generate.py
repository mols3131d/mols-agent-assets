from __future__ import annotations

import csv

from scripts.catalog_indexes_generate import (
    expected_catalog_indexes,
    generate_catalog_indexes,
)


def _write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _rows(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def test_catalog_index_includes_markdown_directories_and_json(tmp_path):
    catalog = tmp_path / "catalog"
    _write(
        catalog / "patterns" / "README.md",
        "---\ndescription: Pattern library.\n---\n# Patterns\n",
    )
    _write(
        catalog / "patterns" / "nested" / "README.md",
        "---\ndescription: Nested patterns.\n---\n# Nested\n",
    )
    _write(
        catalog / "patterns" / "nested" / "pattern.md",
        "---\ndescription: Useful pattern.\n---\n# Pattern\n",
    )
    _write(catalog / "templates" / "review.md", "# {{ title }}\n")
    _write(catalog / "skills.json", "[]\n")
    _write(catalog / "README.md", "# Catalog\n")
    _write(catalog / "AGENTS.md", "# Local instruction\n")

    expected = expected_catalog_indexes(catalog)
    assert list(expected) == [catalog / "INDEX.tsv"]
    assert not (catalog / "INDEX.tsv").exists()

    generate_catalog_indexes(catalog)
    assert _rows(catalog / "INDEX.tsv") == [
        {"path": "patterns/", "description": "Pattern library."},
        {"path": "patterns/nested/", "description": "Nested patterns."},
        {"path": "patterns/nested/pattern.md", "description": "Useful pattern."},
        {"path": "skills.json", "description": ""},
        {"path": "templates/", "description": ""},
        {"path": "templates/review.md", "description": ""},
    ]
    assert expected[catalog / "INDEX.tsv"] == (catalog / "INDEX.tsv").read_text(
        encoding="utf-8"
    )


def test_catalog_index_regenerates_and_removes_empty_projection(tmp_path):
    catalog = tmp_path / "catalog"
    source = catalog / "pattern.md"
    _write(source, "---\ndescription: First.\n---\n# Pattern\n")
    generate_catalog_indexes(catalog)
    assert _rows(catalog / "INDEX.tsv") == [
        {"path": "pattern.md", "description": "First."}
    ]

    _write(source, "---\ndescription: Updated.\n---\n# Pattern\n")
    generate_catalog_indexes(catalog)
    assert _rows(catalog / "INDEX.tsv")[0]["description"] == "Updated."

    source.unlink()
    generate_catalog_indexes(catalog)
    assert not (catalog / "INDEX.tsv").exists()
