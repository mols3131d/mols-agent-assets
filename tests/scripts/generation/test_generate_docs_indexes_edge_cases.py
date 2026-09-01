from __future__ import annotations

import csv

from scripts.generation.generate_docs_indexes import generate_docs_indexes


def _write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _read_tsv(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def test_generate_docs_indexes_does_not_route_index_only_directories(tmp_path):
    docs = tmp_path / "docs"
    _write(docs / "index-only" / "INDEX.md", "# Generated index\n")
    _write(docs / "system-only" / "__index__.md", "# System index\n")
    _write(
        docs / "references" / "guide.md",
        "---\ndescription: Guide.\n---\n# Guide\n",
    )

    assert generate_docs_indexes(docs) == []

    assert _read_tsv(docs / "INDEX.tsv") == [
        {"path": "references/", "description": ""},
        {"path": "references/guide.md", "description": "Guide."},
    ]
    assert not (docs / "index-only" / "INDEX.tsv").exists()
    assert not (docs / "system-only" / "INDEX.tsv").exists()
