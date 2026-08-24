from __future__ import annotations

import csv

from scripts.generate_docs_indexes import generate_docs_indexes


def _write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _read_tsv(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def test_generate_docs_indexes_projects_global_and_first_level_subtrees(tmp_path):
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
        docs / "references" / "reference.md",
        "---\ndescription: Reference.\n---\n# Reference\n",
    )
    _write(
        docs / "references" / "nested" / "deep.md",
        "---\ndescription: Deep reference.\n---\n# Deep\n",
    )

    assert generate_docs_indexes(docs) == []

    assert _read_tsv(docs / "INDEX.tsv") == [
        {"path": "ARCHITECTURE.md", "description": ""},
        {"path": "guide.md", "description": "Guide description."},
        {"path": "references/nested/deep.md", "description": "Deep reference."},
        {"path": "references/reference.md", "description": "Reference."},
    ]
    assert _read_tsv(docs / "references" / "INDEX.tsv") == [
        {"path": "nested/deep.md", "description": "Deep reference."},
        {"path": "reference.md", "description": "Reference."},
    ]
    assert not (docs / "references" / "nested" / "INDEX.tsv").exists()


def test_generate_docs_indexes_removes_deeper_indexes(tmp_path):
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
