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


def test_generate_docs_indexes_projects_directories_and_all_descendant_files(tmp_path):
    docs = tmp_path / "docs"
    _write(
        docs / "guide.md",
        "---\ndescription: Guide description.\n---\n# Guide\n",
    )
    _write(
        docs / "index.md",
        "---\ndescription: Lowercase index is an ordinary document.\n---\n# Index\n",
    )
    _write(docs / "ARCHITECTURE.md", "# Architecture\n")
    _write(docs / "README.md", "# Readme\n")
    _write(docs / "INDEX.md", "# Curated index\n")
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
        {
            "path": "index.md",
            "description": "Lowercase index is an ordinary document.",
        },
        {"path": "references/", "description": "Reference docs."},
        {"path": "references/nested/", "description": "Nested references."},
        {"path": "references/nested/deep.md", "description": "Deep reference."},
        {"path": "references/reference.md", "description": "Reference."},
    ]
    assert not (docs / "references" / "INDEX.tsv").exists()
    assert not (docs / "references" / "nested" / "INDEX.tsv").exists()


def test_generate_docs_indexes_depth_limits_each_index_subtree(tmp_path):
    docs = tmp_path / "docs"
    _write(
        docs / "references" / "nested" / "deep.md",
        "---\ndescription: Deep.\n---\n# Deep\n",
    )
    _write(
        docs / "references" / "reference.md",
        "---\ndescription: Reference.\n---\n# Reference\n",
    )

    assert generate_docs_indexes(docs, index_depth=0, depth=1) == []

    assert _read_tsv(docs / "INDEX.tsv") == [
        {"path": "references/", "description": ""},
        {"path": "references/nested/", "description": ""},
        {"path": "references/reference.md", "description": "Reference."},
    ]
    assert not (docs / "references" / "INDEX.tsv").exists()


def test_generate_docs_indexes_index_depth_controls_materialization_only(tmp_path):
    docs = tmp_path / "docs"
    _write(
        docs / "references" / "nested" / "deep" / "guide.md",
        "---\ndescription: Guide.\n---\n# Guide\n",
    )

    assert generate_docs_indexes(docs, index_depth=2) == []

    assert (docs / "INDEX.tsv").exists()
    assert (docs / "references" / "INDEX.tsv").exists()
    assert (docs / "references" / "nested" / "INDEX.tsv").exists()
    assert not (docs / "references" / "nested" / "deep" / "INDEX.tsv").exists()
    assert _read_tsv(docs / "references" / "INDEX.tsv") == [
        {"path": "nested/", "description": ""},
        {"path": "nested/deep/", "description": ""},
        {"path": "nested/deep/guide.md", "description": "Guide."},
    ]


def test_generate_docs_indexes_index_depth_minus_one_is_unlimited(tmp_path):
    docs = tmp_path / "docs"
    _write(
        docs / "one" / "two" / "three" / "guide.md",
        "---\ndescription: Guide.\n---\n# Guide\n",
    )

    assert generate_docs_indexes(docs, index_depth=-1) == []

    assert (docs / "INDEX.tsv").exists()
    assert (docs / "one" / "INDEX.tsv").exists()
    assert (docs / "one" / "two" / "INDEX.tsv").exists()
    assert (docs / "one" / "two" / "three" / "INDEX.tsv").exists()


def test_generate_docs_indexes_rejects_invalid_depths(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()

    with pytest.raises(ValueError, match="index_depth"):
        generate_docs_indexes(docs, index_depth=-2)
    with pytest.raises(ValueError, match="depth"):
        generate_docs_indexes(docs, depth=-2)


def test_generate_docs_indexes_uses_readme_only_for_directory_metadata(tmp_path):
    docs = tmp_path / "docs"
    _write(docs / "references" / "README.md", "# No frontmatter\n")
    _write(
        docs / "references" / "index.md",
        "---\ndescription: Ordinary document.\n---\n# Index\n",
    )
    _write(
        docs / "references" / "guide.md",
        "---\ndescription: Guide.\n---\n# Guide\n",
    )

    assert generate_docs_indexes(docs) == []

    assert _read_tsv(docs / "INDEX.tsv") == [
        {"path": "references/", "description": ""},
        {"path": "references/guide.md", "description": "Guide."},
        {"path": "references/index.md", "description": "Ordinary document."},
    ]
    assert not (docs / "references" / "INDEX.tsv").exists()


def test_generate_docs_indexes_keeps_directory_without_entry_description_blank(tmp_path):
    docs = tmp_path / "docs"
    _write(
        docs / "skills" / "nested" / "guide.md",
        "---\ndescription: Guide.\n---\n# Guide\n",
    )

    assert generate_docs_indexes(docs) == []

    assert _read_tsv(docs / "INDEX.tsv") == [
        {"path": "skills/", "description": ""},
        {"path": "skills/nested/", "description": ""},
        {"path": "skills/nested/guide.md", "description": "Guide."},
    ]
    assert not (docs / "skills" / "INDEX.tsv").exists()


def test_generate_docs_indexes_excludes_non_markdown_directories_recursively(tmp_path):
    docs = tmp_path / "docs"
    _write(docs / "assets" / "logo.png", "not really an image")
    _write(docs / "hidden" / ".private.md", "# Hidden\n")
    _write(
        docs / "references" / "nested" / "guide.md",
        "---\ndescription: Guide.\n---\n# Guide\n",
    )

    assert generate_docs_indexes(docs) == []

    assert _read_tsv(docs / "INDEX.tsv") == [
        {"path": "references/", "description": ""},
        {"path": "references/nested/", "description": ""},
        {"path": "references/nested/guide.md", "description": "Guide."},
    ]
    assert not (docs / "assets" / "INDEX.tsv").exists()
    assert not (docs / "hidden" / "INDEX.tsv").exists()


def test_generate_docs_indexes_removes_indexes_beyond_index_depth(tmp_path):
    docs = tmp_path / "docs"
    _write(
        docs / "references" / "nested" / "guide.md",
        "---\ndescription: Guide.\n---\n# Guide\n",
    )
    child = docs / "references" / "INDEX.tsv"
    nested = docs / "references" / "nested" / "INDEX.tsv"
    _write(child, "path\tdescription\nold.md\tOld.\n")
    _write(nested, "path\tdescription\nold.md\tOld.\n")

    assert generate_docs_indexes(docs) == []
    assert (docs / "INDEX.tsv").exists()
    assert not child.exists()
    assert not nested.exists()


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
    generate_docs_indexes(docs, index_depth=1)

    _write(
        docs / "guide.md",
        "---\ndescription: Updated description.\n---\n# Guide\n",
    )
    (docs / "references" / "INDEX.tsv").unlink()
    _write(
        docs / "references" / "nested" / "INDEX.tsv",
        "path\tdescription\nold.md\tOld.\n",
    )

    assert generate_docs_indexes(docs, check=True, index_depth=1) == [
        "outdated: docs/INDEX.tsv",
        "missing: docs/references/INDEX.tsv",
        "stale: docs/references/nested/INDEX.tsv",
    ]
