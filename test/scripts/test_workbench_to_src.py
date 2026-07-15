from pathlib import Path

import pytest

from scripts.workbench_to_src import promote, resolve_paths


def make_repo(tmp_path: Path) -> Path:
    (tmp_path / "workbench").mkdir()
    (tmp_path / "src").mkdir()
    return tmp_path


def test_resolve_paths_maps_relative_path_to_src_and_archive(tmp_path: Path):
    root = make_repo(tmp_path)
    source = root / "workbench" / "skills" / "demo"
    source.mkdir(parents=True)

    actual_source, destination, archive = resolve_paths("skills/demo", root)

    assert actual_source == source
    assert destination == root / "src" / "skills" / "demo"
    assert archive == root / ".tmp" / "src" / "skills" / "demo"


def test_promote_copies_new_directory_and_preserves_source(tmp_path: Path):
    root = make_repo(tmp_path)
    source_file = root / "workbench" / "skills" / "demo" / "SKILL.md"
    source_file.parent.mkdir(parents=True)
    source_file.write_text("demo", encoding="utf-8")

    result = promote("skills/demo", root)

    assert result["archive"] is None
    assert source_file.read_text(encoding="utf-8") == "demo"
    assert (root / "src" / "skills" / "demo" / "SKILL.md").read_text(
        encoding="utf-8"
    ) == "demo"


def test_promote_moves_existing_src_to_archive_and_replaces_cleanly(tmp_path: Path):
    root = make_repo(tmp_path)
    source = root / "workbench" / "skills" / "demo"
    destination = root / "src" / "skills" / "demo"
    source.mkdir(parents=True)
    destination.mkdir(parents=True)
    (source / "SKILL.md").write_text("new", encoding="utf-8")
    (destination / "SKILL.md").write_text("old", encoding="utf-8")
    (destination / "deleted.md").write_text("archive me", encoding="utf-8")

    result = promote("skills/demo", root)

    archive = root / ".tmp" / "src" / "skills" / "demo"
    assert result["archive"] == str(archive)
    assert (destination / "SKILL.md").read_text(encoding="utf-8") == "new"
    assert not (destination / "deleted.md").exists()
    assert (archive / "SKILL.md").read_text(encoding="utf-8") == "old"
    assert (archive / "deleted.md").read_text(encoding="utf-8") == "archive me"
    assert (source / "SKILL.md").read_text(encoding="utf-8") == "new"


def test_promote_replaces_existing_archive(tmp_path: Path):
    root = make_repo(tmp_path)
    source = root / "workbench" / "rules" / "demo.md"
    destination = root / "src" / "rules" / "demo.md"
    archive = root / ".tmp" / "src" / "rules" / "demo.md"
    source.parent.mkdir(parents=True)
    destination.parent.mkdir(parents=True)
    archive.parent.mkdir(parents=True)
    source.write_text("new", encoding="utf-8")
    destination.write_text("current", encoding="utf-8")
    archive.write_text("stale archive", encoding="utf-8")

    promote("rules/demo.md", root)

    assert destination.read_text(encoding="utf-8") == "new"
    assert archive.read_text(encoding="utf-8") == "current"


def test_resolve_paths_rejects_path_outside_workbench(tmp_path: Path):
    root = make_repo(tmp_path)
    outside = root / "outside.md"
    outside.write_text("outside", encoding="utf-8")

    with pytest.raises(ValueError):
        resolve_paths(str(outside), root)
