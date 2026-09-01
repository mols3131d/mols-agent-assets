from __future__ import annotations

import subprocess
from pathlib import Path

from scripts.changed_files_format import changed_paths, select_paths


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)


def test_changed_paths_include_local_changes_and_skip_deleted(tmp_path: Path) -> None:
    git(tmp_path, "init")
    git(tmp_path, "config", "user.email", "test@example.com")
    git(tmp_path, "config", "user.name", "Test")

    for name in ("staged.md", "unstaged.py", "deleted.json"):
        (tmp_path / name).write_text("base\n", encoding="utf-8")
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-m", "test: seed")

    (tmp_path / "staged.md").write_text("staged\n", encoding="utf-8")
    git(tmp_path, "add", "staged.md")
    (tmp_path / "unstaged.py").write_text("unstaged\n", encoding="utf-8")
    (tmp_path / "new.jsonc").write_text("{}\n", encoding="utf-8")
    (tmp_path / "deleted.json").unlink()

    assert changed_paths(tmp_path) == ("new.jsonc", "staged.md", "unstaged.py")


def test_select_paths_filters_supported_suffixes() -> None:
    paths = ("a.py", "b.PY", "docs/a.md", "data.json", "notes.txt")

    assert select_paths(paths, {".py"}) == ["./a.py", "./b.PY"]
    assert select_paths(paths, {".md"}) == ["./docs/a.md"]
