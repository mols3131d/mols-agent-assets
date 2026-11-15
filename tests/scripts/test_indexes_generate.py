from __future__ import annotations

import csv
from pathlib import Path

import pytest

from scripts.indexes_generate import (
    PRESETS,
    IndexConfig,
    expected_indexes,
    main,
    sync_indexes,
)


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
    assert [item["path"] for item in _rows(root / "development" / "INDEX.tsv")] == [
        "one.md",
        "three.md",
        "two.md",
    ]
    assert not (root / "skills" / "INDEX.tsv").exists()
    assert sync_indexes(config, check=True) == []


def test_small_directory_gets_local_index(tmp_path):
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
    assert _rows(root / "patterns" / "INDEX.tsv") == [
        {"path": "example.md", "description": "Example."}
    ]


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

    assert sync_indexes(IndexConfig(root, prune=True), check=True) == [
        "outdated: docs/INDEX.tsv",
        "missing: docs/branch/INDEX.tsv",
        "stale: docs/branch/stale/INDEX.tsv",
    ]
    assert root_index.read_text(encoding="utf-8") == "wrong\n"
    assert not nested.exists()
    assert stale.exists()
    assert sync_indexes(IndexConfig(root, prune=True)) == []
    assert sync_indexes(IndexConfig(root, prune=True), check=True) == []
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
    assert [row["path"] for row in _rows(root / "INDEX.tsv")] == ["nested/"]


@pytest.mark.parametrize(
    "kwargs",
    [
        {"depth": -2},
        {"index_depth": -2},
        {"min_entries": 0},
        {"extensions": ()},
        {"directory_entry_files": ()},
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


def test_old_doc_boundary_applies_even_with_recursive_depth(tmp_path):
    root = tmp_path / "docs"
    _write(root / "skills" / "example" / "guide.md", "# Guide\n")
    _write(root / "development" / "nested" / "guide.md", "# Policy\n")
    config = IndexConfig(
        root,
        index_depth=0,
        depth=-1,
        traverse_roots=("development", "documentation", "references", "tools"),
    )
    sync_indexes(config)
    paths = [row["path"] for row in _rows(root / "INDEX.tsv")]
    assert "skills/" in paths
    assert "skills/example/" not in paths
    assert "skills/example/guide.md" not in paths
    assert "development/nested/guide.md" in paths
    assert not (root / "skills" / "INDEX.tsv").exists()


def test_directory_entry_files_override_and_priority(tmp_path):
    root = tmp_path / "docs"
    _write(
        root / "manual" / "README.md",
        "---\ndescription: Readme.\n---\n",
    )
    _write(
        root / "manual" / "index.md",
        "---\ndescription: Preferred index.\n---\n",
    )
    _write(root / "manual" / "guide.md", "# Guide\n")
    config = IndexConfig(root, directory_entry_files=("index.md", "README.md"))
    sync_indexes(config)
    assert _rows(root / "INDEX.tsv") == [
        {"path": "manual/", "description": "Preferred index."}
    ]
    assert _rows(root / "manual" / "INDEX.tsv") == [
        {"path": "guide.md", "description": ""}
    ]


def test_single_and_two_file_directories_keep_descriptions(tmp_path):
    root = tmp_path / "catalog"
    _write(root / "patterns" / "one.md", "---\ndescription: One.\n---\n")
    _write(root / "patterns" / "nested" / "a.md", "---\ndescription: A.\n---\n")
    _write(root / "patterns" / "nested" / "b.md", "---\ndescription: B.\n---\n")
    config = IndexConfig(root)
    sync_indexes(config)
    assert _rows(root / "patterns" / "INDEX.tsv") == [
        {"path": "nested/", "description": ""},
        {"path": "one.md", "description": "One."},
    ]
    assert _rows(root / "patterns" / "nested" / "INDEX.tsv") == [
        {"path": "a.md", "description": "A."},
        {"path": "b.md", "description": "B."},
    ]


def test_custom_root_preserves_unowned_index_unless_prune_enabled(tmp_path):
    root = tmp_path / "notes"
    _write(root / "guide.md", "# Guide\n")
    manual = root / "external" / "INDEX.tsv"
    _write(manual, "owned by something else\n")
    config = IndexConfig(root)
    sync_indexes(config)
    assert manual.read_text(encoding="utf-8") == "owned by something else\n"
    assert sync_indexes(config, check=True) == []
    assert sync_indexes(IndexConfig(root, prune=True), check=True) == [
        "stale: notes/external/INDEX.tsv"
    ]
    sync_indexes(IndexConfig(root, prune=True))
    assert not manual.exists()


def test_preset_prunes_stale_but_does_not_expose_generated_only_directory(
    tmp_path,
):
    root = tmp_path / "docs"
    _write(root / "visible" / "guide.md", "# Guide\n")
    stale = root / "old" / "INDEX.tsv"
    _write(stale, "path\tdescription\nobsolete.md\tobsolete\n")
    config = IndexConfig(root, prune=True)
    sync_indexes(config)
    assert not stale.exists()
    assert _rows(root / "INDEX.tsv") == [{"path": "visible/", "description": ""}]


def test_depth_limit_and_materialization_depth_are_independent(tmp_path):
    root = tmp_path / "docs"
    _write(root / "parent" / "child" / "guide.md", "# Guide\n")
    config = IndexConfig(root, index_depth=1, depth=1)
    sync_indexes(config)
    assert [r["path"] for r in _rows(root / "INDEX.tsv")] == [
        "parent/",
        "parent/child/",
    ]
    assert [r["path"] for r in _rows(root / "parent" / "INDEX.tsv")] == [
        "child/",
        "child/guide.md",
    ]
    assert not (root / "parent" / "child" / "INDEX.tsv").exists()


def test_invalid_directory_entry_files_rejected(tmp_path):
    root = tmp_path / "docs"
    root.mkdir()
    with pytest.raises(ValueError, match="directory entry file"):
        expected_indexes(IndexConfig(root, directory_entry_files=()))


def test_extension_option_matches_library_suffix_semantics(tmp_path):
    root = tmp_path / "custom"
    _write(root / "thing.skill.md", "# Skill\n")
    _write(root / "other.md", "# Other\n")
    config = IndexConfig(root, extensions=("skill.md",))
    sync_indexes(config)
    assert _rows(root / "INDEX.tsv") == [{"path": "thing.skill.md", "description": ""}]


def test_non_system_double_underscore_and_hidden_json_are_preserved(tmp_path):
    root = tmp_path / "catalog"
    _write(root / "__history.md", "---\ndescription: Historical.\n---\n")
    _write(root / "__system__.md", "# System\n")
    _write(root / ".hidden.json", "[]\n")
    config = IndexConfig(root, extensions=(".md", ".json"))
    sync_indexes(config)
    assert _rows(root / "INDEX.tsv") == [
        {"path": ".hidden.json", "description": ""},
        {"path": "__history.md", "description": "Historical."},
    ]


def test_index_only_directories_are_not_routed(tmp_path):
    root = tmp_path / "docs"
    _write(root / "index-only" / "INDEX.md", "# Index\n")
    _write(root / "system-only" / "__index__.md", "# System\n")
    _write(root / "reference" / "guide.md", "# Guide\n")
    sync_indexes(IndexConfig(root))
    assert _rows(root / "INDEX.tsv") == [{"path": "reference/", "description": ""}]


def test_nested_hidden_json_remains_discoverable(tmp_path):
    root = tmp_path / "catalog"
    _write(root / "patterns" / ".special.json", "[]\n")
    config = IndexConfig(root, extensions=(".md", ".json"))
    sync_indexes(config)
    assert _rows(root / "INDEX.tsv") == [{"path": "patterns/", "description": ""}]
    assert _rows(root / "patterns" / "INDEX.tsv") == [
        {"path": ".special.json", "description": ""}
    ]


def test_empty_preset_index_is_removed_after_last_source_deletion(tmp_path):
    root = tmp_path / "catalog"
    source = root / "pattern.md"
    _write(source, "---\ndescription: First.\n---\n")
    config = IndexConfig(root, prune=True)
    sync_indexes(config)
    source.unlink()
    assert sync_indexes(config, check=True) == ["stale: catalog/INDEX.tsv"]
    sync_indexes(config)
    assert not (root / "INDEX.tsv").exists()


def test_min_entries_counts_tsv_records_not_multiline_description_lines(tmp_path):
    root = tmp_path / "docs"
    _write(
        root / "policy" / "guide.md",
        "---\ndescription: |-\n  First line\n  Second line\n---\n",
    )
    config = IndexConfig(root, min_entries=2)
    sync_indexes(config)
    assert [row["path"] for row in _rows(root / "INDEX.tsv")] == ["policy/"]
    assert not (root / "policy" / "INDEX.tsv").exists()


def test_cli_rejects_unknown_target_preset():
    with pytest.raises(SystemExit) as exc_info:
        main(["--target", "unknown"])
    assert exc_info.value.code == 2


def test_cli_root_prune_removes_stale_indexes_only_when_enabled(tmp_path, capsys):
    root = tmp_path / "notes"
    _write(root / "guide.md", "---\ndescription: Guide.\n---\n")
    stale = root / "external" / "INDEX.tsv"
    _write(stale, "stale\n")

    assert main(["--root", str(root)]) == 0
    assert stale.exists()

    assert main(["--root", str(root), "--prune", "--check"]) == 1
    assert "stale: notes/external/INDEX.tsv" in capsys.readouterr().err
    assert stale.exists()

    assert main(["--root", str(root), "--prune"]) == 0
    assert not stale.exists()


def test_cli_supports_presets_overrides_check_and_validation_errors(
    monkeypatch,
    tmp_path,
    capsys,
):
    docs_dir = tmp_path / "docs"
    _write(docs_dir / "allowed" / "guide.md", "---\ndescription: Allowed.\n---\n")
    _write(docs_dir / "blocked" / "note.md", "---\ndescription: Blocked.\n---\n")
    _write(docs_dir / "allowed" / "alt.txt", "---\ndescription: Text.\n---\n")
    _write(docs_dir / "allowed" / "entry.md", "---\ndescription: Entry.\n---\n")
    stale = docs_dir / "stale" / "INDEX.tsv"
    _write(stale, "stale\n")

    preset_config = IndexConfig(docs_dir, prune=True)
    monkeypatch.setitem(PRESETS, "docs", preset_config)

    assert main(["--target", "docs", "--check"]) == 1
    err = capsys.readouterr().err
    assert "missing: docs/INDEX.tsv" in err
    assert "stale: docs/stale/INDEX.tsv" in err

    override_args = [
        "--target",
        "docs",
        "--extensions",
        ".md",
        ".txt",
        "--directory-entry-files",
        "entry.md",
        "--index-depth",
        "1",
        "--depth",
        "0",
        "--min-entries",
        "1",
        "--traverse-roots",
        "allowed",
        "--prune",
    ]
    assert main(override_args) == 0
    assert main([*override_args, "--check"]) == 0
    assert _rows(docs_dir / "INDEX.tsv") == [
        {"path": "allowed/", "description": "Entry."},
        {"path": "blocked/", "description": ""},
    ]
    assert _rows(docs_dir / "allowed" / "INDEX.tsv") == [
        {"path": "alt.txt", "description": "Text."},
        {"path": "guide.md", "description": "Allowed."},
    ]
    assert not stale.exists()

    for bad_args in (
        ["--root", str(tmp_path / "missing")],
        ["--root", str(docs_dir), "--depth", "-2"],
        ["--root", str(docs_dir), "--min-entries", "0"],
        ["--root", str(docs_dir), "--extensions", ""],
    ):
        with pytest.raises(SystemExit) as exc_info:
            main(bad_args)
        assert exc_info.value.code == 2


def test_metacharacter_empty_and_blocked_dirs_do_not_hide_matching_siblings(
    tmp_path,
):
    root = tmp_path / "docs"
    _write(root / "[a-z]" / ".hidden.md", "# Empty\n")
    _write(root / "[b-c]" / "secret.md", "# Blocked\n")
    _write(root / "a" / "guide.md", "---\ndescription: Letter A.\n---\n")
    _write(root / "b" / "guide.md", "---\ndescription: Letter B.\n---\n")

    config = IndexConfig(root, depth=-1, traverse_roots=("a", "b"))
    sync_indexes(config)

    paths = [row["path"] for row in _rows(root / "INDEX.tsv")]
    assert paths == ["[b-c]/", "a/", "a/guide.md", "b/", "b/guide.md"]
    assert not (root / "[a-z]" / "INDEX.tsv").exists()


def test_empty_root_directory_does_not_suppress_same_named_nested_directory(tmp_path):
    root = tmp_path / "docs"
    _write(root / "assets" / ".hidden.md", "# Ignored\n")
    _write(
        root / "guide" / "assets" / "spec.md",
        "---\ndescription: Spec.\n---\n",
    )

    sync_indexes(IndexConfig(root, depth=-1))

    assert [row["path"] for row in _rows(root / "INDEX.tsv")] == [
        "guide/",
        "guide/assets/",
        "guide/assets/spec.md",
    ]


def test_double_underscore_index_prefixes_are_treated_as_non_content(tmp_path):
    root = tmp_path / "catalog"
    _write(root / "only-md" / "__index__v2.md", "# Internal\n")
    _write(root / "only-json" / "__index__.json", "{}\n")
    _write(root / "visible" / "item.json", "{}\n")

    sync_indexes(IndexConfig(root, extensions=(".md", ".json")))

    assert _rows(root / "INDEX.tsv") == [{"path": "visible/", "description": ""}]
    assert not (root / "only-md" / "INDEX.tsv").exists()
    assert not (root / "only-json" / "INDEX.tsv").exists()


def test_index_md_is_indexed_when_not_configured_as_directory_entry_file(tmp_path):
    root = tmp_path / "docs"
    _write(root / "section" / "index.md", "---\ndescription: Index doc.\n---\n")

    sync_indexes(IndexConfig(root))

    assert _rows(root / "INDEX.tsv") == [{"path": "section/", "description": ""}]
    assert _rows(root / "section" / "INDEX.tsv") == [
        {"path": "index.md", "description": "Index doc."}
    ]


def test_hidden_markdown_files_are_excluded_recursively(tmp_path):
    root = tmp_path / "docs"
    _write(root / "hidden-only" / ".private.md", "# Hidden\n")
    _write(root / "mixed" / ".private.md", "# Hidden\n")
    _write(root / "mixed" / "public.md", "---\ndescription: Public.\n---\n")

    sync_indexes(IndexConfig(root, depth=-1))

    assert _rows(root / "INDEX.tsv") == [
        {"path": "mixed/", "description": ""},
        {"path": "mixed/public.md", "description": "Public."},
    ]


def test_prune_removes_stale_indexes_beyond_index_depth(tmp_path):
    root = tmp_path / "docs"
    _write(root / "nested" / "deep" / "guide.md", "---\ndescription: Deep.\n---\n")
    stale = root / "nested" / "deep" / "INDEX.tsv"
    _write(stale, "stale\n")

    config = IndexConfig(root, index_depth=0, prune=True)
    assert sync_indexes(config, check=True) == [
        "missing: docs/INDEX.tsv",
        "stale: docs/nested/deep/INDEX.tsv",
    ]
    sync_indexes(config)
    assert (root / "INDEX.tsv").exists()
    assert not stale.exists()


def test_extensions_normalization_and_validation(tmp_path):
    root = tmp_path / "custom"
    _write(root / "note.txt", "# Note\n")
    _write(root / "spec.md", "---\ndescription: Spec.\n---\n")

    sync_indexes(IndexConfig(root, extensions=(" .md ", " txt")))
    assert [row["path"] for row in _rows(root / "INDEX.tsv")] == [
        "note.txt",
        "spec.md",
    ]

    for invalid in ((), ("",), ("   ",), (".",)):
        with pytest.raises(ValueError, match="extension"):
            expected_indexes(IndexConfig(root, extensions=invalid))


def test_non_utf8_expected_index_is_reported_outdated_and_repaired(tmp_path):
    root = tmp_path / "docs"
    _write(root / "guide.md", "---\ndescription: Guide.\n---\n")
    target = root / "INDEX.tsv"
    target.write_bytes(b"\xff\xfe\x00")

    config = IndexConfig(root)
    assert sync_indexes(config, check=True) == ["outdated: docs/INDEX.tsv"]
    assert sync_indexes(config) == []
    assert _rows(target) == [{"path": "guide.md", "description": "Guide."}]


def test_non_utf8_stale_index_is_unlinked_without_decoding(tmp_path):
    root = tmp_path / "docs"
    _write(root / "guide.md", "---\ndescription: Guide.\n---\n")
    stale = root / "obsolete" / "INDEX.tsv"
    stale.parent.mkdir(parents=True)
    stale.write_bytes(b"\xff\xfe\x00")

    config = IndexConfig(root, prune=True)
    assert sync_indexes(config, check=True) == [
        "missing: docs/INDEX.tsv",
        "stale: docs/obsolete/INDEX.tsv",
    ]
    sync_indexes(config)
    assert not stale.exists()


def test_symlink_directory_is_ignored_during_index_traversal(monkeypatch, tmp_path):
    root = tmp_path / "docs"
    _write(root / "real" / "guide.md", "---\ndescription: Real.\n---\n")
    linked = root / "linked"
    _write(linked / "loop.md", "---\ndescription: Linked.\n---\n")
    _write(linked / "nested" / "deep.md", "---\ndescription: Deep.\n---\n")

    original_is_symlink = Path.is_symlink
    monkeypatch.setattr(
        Path,
        "is_symlink",
        lambda self: True if self == linked else original_is_symlink(self),
    )

    shallow = expected_indexes(IndexConfig(root, depth=0))
    assert set(shallow) == {root / "INDEX.tsv", root / "real" / "INDEX.tsv"}
    assert "linked/" not in shallow[root / "INDEX.tsv"]

    deep = expected_indexes(IndexConfig(root, depth=-1))
    assert set(deep) == {root / "INDEX.tsv", root / "real" / "INDEX.tsv"}
    assert deep[root / "INDEX.tsv"] == (
        "path\tdescription\nreal/\t\nreal/guide.md\tReal.\n"
    )


def test_directory_entry_file_is_excluded_from_own_index(tmp_path):
    root = tmp_path / "docs"
    _write(root / "README.md", "---\ndescription: Root readme.\n---\n")
    _write(root / "sub" / "README.md", "---\ndescription: Sub readme.\n---\n")
    _write(root / "sub" / "guide.md", "---\ndescription: Guide.\n---\n")

    sync_indexes(IndexConfig(root))

    assert _rows(root / "INDEX.tsv") == [{"path": "sub/", "description": "Sub readme."}]
    assert _rows(root / "sub" / "INDEX.tsv") == [
        {"path": "guide.md", "description": "Guide."}
    ]


def test_dot_prefixed_directories_stay_consistent_across_depths(tmp_path):
    root = tmp_path / "docs"
    _write(
        root / ".internal" / "README.md",
        "---\ndescription: Internal.\n---\n",
    )
    _write(root / ".internal" / "guide.md", "---\ndescription: Guide.\n---\n")
    _write(root / ".internal" / ".private.md", "# Private\n")

    shallow = expected_indexes(IndexConfig(root, depth=0))
    assert set(shallow) == {root / "INDEX.tsv", root / ".internal" / "INDEX.tsv"}
    assert shallow[root / "INDEX.tsv"] == "path\tdescription\n.internal/\tInternal.\n"
    assert shallow[root / ".internal" / "INDEX.tsv"] == (
        "path\tdescription\nguide.md\tGuide.\n"
    )

    deep = expected_indexes(IndexConfig(root, depth=-1))
    assert set(deep) == {root / "INDEX.tsv", root / ".internal" / "INDEX.tsv"}
    assert deep[root / "INDEX.tsv"] == (
        "path\tdescription\n.internal/\tInternal.\n.internal/guide.md\tGuide.\n"
    )


def test_dotdot_root_path_formats_drift_labels_safely(tmp_path):
    root = tmp_path / "notes"
    _write(root / "sub" / "guide.md", "---\ndescription: Sub.\n---\n")
    stale = root / "external" / "INDEX.tsv"
    _write(stale, "stale\n")

    dotdot_root = root / "sub" / ".."
    config = IndexConfig(dotdot_root, prune=True)
    assert sync_indexes(config, check=True) == [
        "missing: notes/INDEX.tsv",
        "stale: notes/external/INDEX.tsv",
        "missing: notes/sub/INDEX.tsv",
    ]
