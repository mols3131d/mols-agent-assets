from __future__ import annotations

import csv

import pytest

from scripts.indexes_generate import IndexConfig, expected_indexes, main, sync_indexes


def _write(path, contents):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents, encoding="utf-8")


def _rows(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def test_scoped_indexes_route_from_root_to_relevant_directory(tmp_path):
    root = tmp_path / "docs"
    _write(root / "guide.md", "---\ndescription: Guide.\n---\n# Guide\n")
    _write(
        root / "development" / "README.md",
        "---\ndescription: Development.\n---\n",
    )
    for filename in ("one.md", "two.md", "three.md"):
        _write(
            root / "development" / filename,
            f"---\ndescription: {filename}\n---\n",
        )
    _write(root / "skills" / "skill" / "maintenance.md", "# Maintenance\n")
    config = IndexConfig(root, traverse_roots=("development",))

    expected = expected_indexes(config)
    assert set(expected) == {
        root / "INDEX.tsv",
        root / "development" / "INDEX.tsv",
    }
    assert not (root / "INDEX.tsv").exists()
    assert sync_indexes(config) == []
    assert _rows(root / "INDEX.tsv") == [
        {"path": "development/", "description": "Development."},
        {"path": "guide.md", "description": "Guide."},
        {"path": "skills/", "description": ""},
    ]
    assert [
        item["path"] for item in _rows(root / "development" / "INDEX.tsv")
    ] == ["one.md", "three.md", "two.md"]
    assert not (root / "skills" / "INDEX.tsv").exists()
    assert sync_indexes(config, check=True) == []


def test_small_directory_uses_no_index_but_is_discoverable(tmp_path):
    root = tmp_path / "catalog"
    _write(
        root / "patterns" / "README.md",
        "---\ndescription: Patterns.\n---\n",
    )
    _write(
        root / "patterns" / "example.md",
        "---\ndescription: Example.\n---\n",
    )
    sync_indexes(IndexConfig(root))
    assert _rows(root / "INDEX.tsv") == [
        {"path": "patterns/", "description": "Patterns."}
    ]
    assert not (root / "patterns" / "INDEX.tsv").exists()


def test_generic_options_handle_json_and_limited_materialization(tmp_path):
    root = tmp_path / "other"
    _write(root / "reference.json", "[]\n")
    for name in ("first.md", "second.md", "third.md"):
        _write(
            root / "nested" / name,
            "---\ndescription: Document.\n---\n",
        )
    config = IndexConfig(
        root,
        extensions=(".md", ".json"),
        index_depth=0,
    )
    assert set(expected_indexes(config)) == {root / "INDEX.tsv"}
    sync_indexes(config)
    assert [row["path"] for row in _rows(root / "INDEX.tsv")] == [
        "nested/",
        "reference.json",
    ]
    assert not (root / "nested" / "INDEX.tsv").exists()


def test_check_reports_missing_outdated_and_stale_without_mutation(tmp_path):
    root = tmp_path / "docs"
    for name in ("one.md", "two.md", "three.md"):
        _write(
            root / "branch" / name,
            f"---\ndescription: {name}\n---\n",
        )
    config = IndexConfig(root)
    sync_indexes(config)
    nested = root / "branch" / "INDEX.tsv"
    root_index = root / "INDEX.tsv"
    root_index.write_text("wrong\n", encoding="utf-8")
    nested.unlink()
    stale = root / "branch" / "stale" / "INDEX.tsv"
    _write(stale, "old\n")

    assert sync_indexes(config, check=True) == [
        "outdated: docs/INDEX.tsv",
        "missing: docs/branch/INDEX.tsv",
        "stale: docs/branch/stale/INDEX.tsv",
    ]
    assert root_index.read_text(encoding="utf-8") == "wrong\n"
    assert not nested.exists()
    assert stale.exists()
    assert sync_indexes(config) == []
    assert sync_indexes(config, check=True) == []
    assert not stale.exists()


def test_excludes_hidden_system_index_and_non_content_paths(tmp_path):
    root = tmp_path / "docs"
    _write(root / ".hidden.md", "# Hidden\n")
    _write(root / "AGENTS.md", "# Agent\n")
    _write(root / "INDEX.md", "# Index\n")
    _write(root / "__system__.md", "# System\n")
    _write(root / "images" / "image.png", "binary\n")
    _write(root / "nested" / "visible.md", "# Visible\n")
    sync_indexes(IndexConfig(root))
    assert [row["path"] for row in _rows(root / "INDEX.tsv")] == [
        "nested/"
    ]


@pytest.mark.parametrize(
    "kwargs",
    [
        {"depth": -2},
        {"index_depth": -2},
        {"min_entries": 0},
        {"extensions": ()},
    ],
)
def test_rejects_invalid_controls(tmp_path, kwargs):
    root = tmp_path / "docs"
    root.mkdir()
    with pytest.raises(ValueError):
        expected_indexes(IndexConfig(root, **kwargs))


def test_cli_supports_reuse_for_another_directory(tmp_path):
    root = tmp_path / "other"
    _write(root / "metadata.json", "[]\n")
    args = ["--root", str(root), "--extensions", ".json"]
    assert main([*args, "--check"]) == 1
    assert not (root / "INDEX.tsv").exists()
    assert main(args) == 0
    assert main([*args, "--check"]) == 0
