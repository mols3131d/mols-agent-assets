from __future__ import annotations

import csv

import pytest

from scripts.generate_docs_indexes import generate_docs_indexes


def _write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _read_tsv(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def test_generate_docs_indexes_projects_one_hop_breadth_first(tmp_path):
    docs = tmp_path / "docs"
    _write(
        docs / "guide.md",
        "---\ndescription: Guide description.\n---\n# Guide\n",
    )
    _write(docs / "ARCHITECTURE.md", "# Architecture\n")
    _write(docs / "README.md", "# Readme\n")
    _write(docs / "AGENTS.md", "# Agents\n")
    _write(docs / ".private.md", "# Hidden\n")
    _write(docs / "__system__.md", "# System\n")
    _write(
        docs / "references" / "README.md",
        "---\ndescription: Reference docs.\n---\n# References\n",
    )
    _write(
        docs / "references" / "reference.md",
        "---\ndescription: Reference.\n---\n# Reference\n",
    )
    _write(
        docs / "references" / "nested" / "README.md",
        "---\ndescription: Nested references.\n---\n# Nested\n",
    )
    _write(
        docs / "references" / "nested" / "deep.md",
        "---\ndescription: Deep reference.\n---\n# Deep\n",
    )

    assert generate_docs_indexes(docs) == []

    assert _read_tsv(docs / "INDEX.tsv") == [
        {"path": "ARCHITECTURE.md", "description": ""},
        {"path": "guide.md", "description": "Guide description."},
        {"path": "references/", "description": "Reference docs."},
    ]
    assert _read_tsv(docs / "references" / "INDEX.tsv") == [
        {"path": "nested/", "description": "Nested references."},
        {"path": "reference.md", "description": "Reference."},
    ]
    assert not (docs / "references" / "nested" / "INDEX.tsv").exists()


def test_generate_docs_indexes_depth_controls_recursive_materialization(tmp_path):
    docs = tmp_path / "docs"
    _write(
        docs / "references" / "nested" / "deep" / "guide.md",
        "---\ndescription: Guide.\n---\n# Guide\n",
    )

    assert generate_docs_indexes(docs, depth=2) == []

    assert (docs / "INDEX.tsv").exists()
    assert (docs / "references" / "INDEX.tsv").exists()
    assert (docs / "references" / "nested" / "INDEX.tsv").exists()
    assert not (docs / "references" / "nested" / "deep" / "INDEX.tsv").exists()
    assert _read_tsv(docs / "references" / "nested" / "INDEX.tsv") == [
        {"path": "deep/", "description": ""},
    ]


def test_generate_docs_indexes_depth_minus_one_is_unlimited(tmp_path):
    docs = tmp_path / "docs"
    _write(
        docs / "one" / "two" / "three" / "guide.md",
        "---\ndescription: Guide.\n---\n# Guide\n",
    )

    assert generate_docs_indexes(docs, depth=-1) == []

    assert (docs / "INDEX.tsv").exists()
    assert (docs / "one" / "INDEX.tsv").exists()
    assert (docs / "one" / "two" / "INDEX.tsv").exists()
    assert (docs / "one" / "two" / "three" / "INDEX.tsv").exists()


def test_generate_docs_indexes_rejects_invalid_depth(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()

    with pytest.raises(ValueError, match="-1 or greater"):
        generate_docs_indexes(docs, depth=-2)


def test_generate_docs_indexes_directory_entry_falls_back_to_index(tmp_path):
    docs = tmp_path / "docs"
    _write(docs / "references" / "README.md", "# No frontmatter\n")
    _write(
        docs / "references" / "index.md",
        "---\ndescription: Index fallback.\n---\n# Index\n",
    )
    _write(
        docs / "references" / "guide.md",
        "---\ndescription: Guide.\n---\n# Guide\n",
    )

    assert generate_docs_indexes(docs) == []

    assert _read_tsv(docs / "INDEX.tsv") == [
        {"path": "references/", "description": "Index fallback."},
    ]
    assert _read_tsv(docs / "references" / "INDEX.tsv") == [
        {"path": "guide.md", "description": "Guide."},
    ]


def test_generate_docs_indexes_directory_entry_precedence_does_not_merge(tmp_path):
    docs = tmp_path / "docs"
    _write(
        docs / "references" / "README.md",
        "---\ntitle: References\n---\n# Readme\n",
    )
    _write(
        docs / "references" / "index.md",
        "---\ndescription: Must not merge.\n---\n# Index\n",
    )
    _write(
        docs / "references" / "guide.md",
        "---\ndescription: Guide.\n---\n# Guide\n",
    )

    assert generate_docs_indexes(docs) == []

    assert _read_tsv(docs / "INDEX.tsv") == [
        {"path": "references/", "description": ""},
    ]


def test_generate_docs_indexes_keeps_directory_without_entry_description_blank(tmp_path):
    docs = tmp_path / "docs"
    _write(
        docs / "skills" / "nested" / "guide.md",
        "---\ndescription: Guide.\n---\n# Guide\n",
    )

    assert generate_docs_indexes(docs) == []

    assert _read_tsv(docs / "skills" / "INDEX.tsv") == [
        {"path": "nested/", "description": ""},
    ]


def test_generate_docs_indexes_excludes_non_markdown_child_routes(tmp_path):
    docs = tmp_path / "docs"
    _write(docs / "assets" / "logo.png", "not really an image")
    _write(docs / "hidden" / ".private.md", "# Hidden\n")
    _write(
        docs / "references" / "guide.md",
        "---\ndescription: Guide.\n---\n# Guide\n",
    )

    assert generate_docs_indexes(docs) == []

    assert _read_tsv(docs / "INDEX.tsv") == [
        {"path": "references/", "description": ""},
    ]
    assert not (docs / "assets" / "INDEX.tsv").exists()
    assert not (docs / "hidden" / "INDEX.tsv").exists()


def test_generate_docs_indexes_removes_indexes_beyond_depth(tmp_path):
    docs = tmp_path / "docs"
    _write(
        docs / "references" / "nested" / "guide.md",
        "---\ndescription: Guide.\n---\n# Guide\n",
    )
    stale = docs / "references" / "nested" / "INDEX.tsv"
    _write(stale, "path\tdescription\nold.md\tOld.\n")

    assert generate_docs_indexes(docs) == []
    assert not stale.exists()
    assert (docs / "INDEX.tsv").exists()
    assert (docs / "references" / "INDEX.tsv").exists()


def test_generate_docs_indexes_check_reports_scoped_drift_and_deeper_stale(tmp_path):
    docs = tmp_path / "docs"
    _write(
        docs / "guide.md",
        "---\ndescription: Guide description.\n---\n# Guide\n",
    )
    _write(
        docs / "references" / "nested" / "reference.md",
        "---\ndescription: Nested reference.\n---\n# Reference\n",
    )
    generate_docs_indexes(docs)

    _write(
        docs / "guide.md",
        "---\ndescription: Updated description.\n---\n# Guide\n",
    )
    (docs / "references" / "INDEX.tsv").unlink()
    _write(
        docs / "references" / "nested" / "INDEX.tsv",
        "path\tdescription\nold.md\tOld.\n",
    )

    assert generate_docs_indexes(docs, check=True) == [
        "outdated: docs/INDEX.tsv",
        "missing: docs/references/INDEX.tsv",
        "stale: docs/references/nested/INDEX.tsv",
    ]
