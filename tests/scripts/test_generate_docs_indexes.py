from __future__ import annotations

import csv

from scripts.generate_docs_indexes import generate_docs_indexes


def _write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _read_tsv(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def test_generate_docs_indexes_uses_direct_children_and_role_exclusions(tmp_path):
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
        docs / "nested" / "reference.md",
        "---\ndescription: Nested reference.\n---\n# Reference\n",
    )

    assert generate_docs_indexes(docs) == []

    assert _read_tsv(docs / "INDEX.tsv") == [
        {"path": "ARCHITECTURE.md", "description": ""},
        {"path": "guide.md", "description": "Guide description."},
    ]
    assert _read_tsv(docs / "nested" / "INDEX.tsv") == [
        {"path": "reference.md", "description": "Nested reference."}
    ]


def test_generate_docs_indexes_removes_stale_index(tmp_path):
    docs = tmp_path / "docs"
    stale = docs / "empty" / "INDEX.tsv"
    _write(stale, "path\tdescription\nold.md\tOld.\n")

    assert generate_docs_indexes(docs) == []
    assert not stale.exists()


def test_generate_docs_indexes_check_reports_missing_outdated_and_stale(tmp_path):
    docs = tmp_path / "docs"
    _write(
        docs / "guide.md",
        "---\ndescription: Guide description.\n---\n# Guide\n",
    )
    _write(
        docs / "nested" / "reference.md",
        "---\ndescription: Nested reference.\n---\n# Reference\n",
    )
    generate_docs_indexes(docs)

    _write(
        docs / "guide.md",
        "---\ndescription: Updated description.\n---\n# Guide\n",
    )
    (docs / "nested" / "INDEX.tsv").unlink()
    _write(docs / "stale" / "INDEX.tsv", "path\tdescription\nold.md\tOld.\n")

    assert generate_docs_indexes(docs, check=True) == [
        "outdated: docs/INDEX.tsv",
        "missing: docs/nested/INDEX.tsv",
        "stale: docs/stale/INDEX.tsv",
    ]
