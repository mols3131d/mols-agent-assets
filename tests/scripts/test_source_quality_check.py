from __future__ import annotations

import subprocess
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

import pytest

from scripts import source_quality_check as quality


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)


def test_selects_staged_and_committed_paths_without_untracked_or_deleted(
    tmp_path: Path,
) -> None:
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.name", "Test")
    git(tmp_path, "config", "user.email", "test@example.com")
    for path in ("한글 파일.md", "deleted.json", "modified.py"):
        (tmp_path / path).write_text("initial\n", encoding="utf-8")
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-qm", "initial")

    (tmp_path / "한글 파일.md").write_text("staged\n", encoding="utf-8")
    (tmp_path / "deleted.json").unlink()
    (tmp_path / "modified.py").write_text("changed\n", encoding="utf-8")
    (tmp_path / "new.jsonc").write_text("{}\n", encoding="utf-8")
    (tmp_path / "untracked.ts").write_text("x\n", encoding="utf-8")
    git(tmp_path, "add", "한글 파일.md", "deleted.json", "new.jsonc")

    assert quality.staged_paths(tmp_path) == ("new.jsonc", "한글 파일.md")

    git(tmp_path, "add", "modified.py")
    git(tmp_path, "commit", "-qm", "change")
    assert quality.changed_paths("HEAD^", tmp_path) == (
        "modified.py",
        "new.jsonc",
        "한글 파일.md",
    )


def test_chosen_tools_do_not_mutate_files_or_confuse_format_and_lint() -> None:
    checks = quality.checks_for_paths(
        ("src/main.py", "docs/guide.md", "settings.jsonc", "ignored.txt")
    )
    assert checks == [
        ("Ruff lint", ["ruff", "check", "./src/main.py"]),
        ("Ruff format", ["ruff", "format", "--diff", "./src/main.py"]),
        ("rumdl lint", ["rumdl", "check", "./docs/guide.md"]),
        ("rumdl format", ["rumdl", "fmt", "--check", "./docs/guide.md"]),
        (
            "Biome lint",
            ["biome", "lint", "--no-errors-on-unmatched", "./settings.jsonc"],
        ),
        (
            "Biome format",
            ["biome", "format", "--no-errors-on-unmatched", "./settings.jsonc"],
        ),
    ]


def test_quality_check_reports_failure_without_skipping_following_checks(
    tmp_path: Path, capsys
) -> None:
    commands: list[list[str]] = []

    def fake_runner(command: list[str], root: Path) -> int:
        commands.append(command)
        return 1 if command[:2] == ["ruff", "check"] else 0

    assert quality.verify(("sample.py",), tmp_path, fake_runner) == 1
    assert len(commands) == 2
    assert "FAIL Ruff lint" in capsys.readouterr().err


def test_quality_selection_failure_is_not_silently_ignored(
    tmp_path: Path, capsys
) -> None:
    assert quality.main(["--changed-from", "missing-revision"], tmp_path) == 2
    assert "ERROR source selection" in capsys.readouterr().err


def test_no_supported_sources_runs_no_tools(capsys) -> None:
    assert quality.verify(("sample.txt",)) == 0
    assert "No supported source files affected" in capsys.readouterr().out


def test_staged_source_with_unstaged_changes_fails_before_lint(tmp_path: Path) -> None:
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.name", "Test")
    git(tmp_path, "config", "user.email", "test@example.com")
    source = tmp_path / "example.py"
    source.write_text("print('original')\n", encoding="utf-8")
    git(tmp_path, "add", "example.py")
    git(tmp_path, "commit", "-qm", "initial")

    source.write_text("bad =\n", encoding="utf-8")
    git(tmp_path, "add", "example.py")
    source.write_text("good = 1\n", encoding="utf-8")

    assert quality.main(["--staged"], tmp_path) == 2
    git(tmp_path, "add", "example.py")
    assert quality.staged_paths(tmp_path) == ("example.py",)


def test_staged_merge_checks_content_changed_from_both_parents(tmp_path: Path) -> None:
    git(tmp_path, "init", "-q", "--initial-branch=topic")
    git(tmp_path, "config", "user.name", "Test")
    git(tmp_path, "config", "user.email", "test@example.com")
    git(tmp_path, "commit", "-qm", "initial", "--allow-empty")
    git(tmp_path, "switch", "-qc", "upstream")
    upstream_source = tmp_path / "inherited.py"
    upstream_source.write_text("bad =\n", encoding="utf-8")
    git(tmp_path, "add", "inherited.py")
    git(tmp_path, "commit", "-qm", "upstream")
    git(tmp_path, "switch", "-q", "topic")
    git(tmp_path, "merge", "-q", "--no-ff", "--no-commit", "upstream")

    assert quality.staged_paths(tmp_path) == ()

    upstream_source.write_text("fixed = 1\n", encoding="utf-8")
    git(tmp_path, "add", "inherited.py")
    assert quality.staged_paths(tmp_path) == ("inherited.py",)


def test_missing_staged_source_is_an_error_not_a_silent_skip(tmp_path: Path) -> None:
    git(tmp_path, "init", "-q")
    source = tmp_path / "new.py"
    source.write_text("print(1)\n", encoding="utf-8")
    git(tmp_path, "add", "new.py")
    source.unlink()
    assert quality.main(["--staged"], tmp_path) == 2


def test_selected_symlink_source_is_not_silently_skipped(tmp_path: Path) -> None:
    (tmp_path / "actual.py").write_text("print(1)\n", encoding="utf-8")
    try:
        (tmp_path / "link.py").symlink_to("actual.py")
    except OSError as exc:
        pytest.skip(f"Filesystem symlinks unavailable: {exc}")
    with pytest.raises(ValueError, match="link.py"):
        quality._check_source_paths((("link.py", "100644"),), tmp_path)


def test_type_change_rejects_git_symlink_checked_out_as_regular_file(tmp_path: Path):
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.name", "Test")
    git(tmp_path, "config", "user.email", "test@example.com")
    git(tmp_path, "config", "core.symlinks", "false")
    path = tmp_path / "source.py"
    path.write_text("target.py\n", encoding="utf-8")
    git(tmp_path, "add", "source.py")
    git(tmp_path, "commit", "-qm", "initial")

    oid = subprocess.check_output(
        ["git", "rev-parse", "HEAD:source.py"], cwd=tmp_path, text=True
    ).strip()
    git(tmp_path, "update-index", "--cacheinfo", f"120000,{oid},source.py")

    assert path.is_file() and not path.is_symlink()
    with pytest.raises(ValueError, match="source.py"):
        quality.staged_paths(tmp_path)
    with pytest.raises(ValueError, match="source.py"):
        quality.all_paths(tmp_path)
    git(tmp_path, "commit", "-qm", "make symlink")
    with pytest.raises(ValueError, match="source.py"):
        quality.changed_paths("HEAD^", tmp_path)

    git(tmp_path, "update-index", "--cacheinfo", f"100644,{oid},source.py")
    assert quality.staged_paths(tmp_path) == ("source.py",)


def test_run_uses_biome_package_without_windows_wrapper(tmp_path: Path) -> None:
    modules = tmp_path / "managed tools" / "node_modules"
    wrapper = modules / ".bin" / "biome.cmd"
    entry = modules / "@biomejs" / "biome" / "bin" / "biome"
    entry.parent.mkdir(parents=True)
    entry.touch()
    node = str(tmp_path / "node.exe")
    command = ["biome", "lint", "./source %NAME% file.ts"]
    tools = {"biome": str(wrapper), "node.exe": node}
    with (
        patch("shutil.which", side_effect=tools.get),
        patch.object(
            quality.subprocess,
            "run",
            return_value=subprocess.CompletedProcess([], 1),
        ) as run,
    ):
        assert quality._run(command, tmp_path) == 1

    run.assert_called_once_with(
        [node, str(entry), *command[1:]], cwd=tmp_path, check=False
    )


class SourceQualityRegressionTests(TestCase):
    def test_missing_tool_reports_execution_error_without_running(self) -> None:
        errors = StringIO()
        with (
            patch("shutil.which", return_value=None),
            patch.object(
                quality.subprocess,
                "run",
                return_value=subprocess.CompletedProcess([], 0),
            ) as run,
            redirect_stderr(errors),
        ):
            self.assertEqual(quality.verify(("sample.ts",)), 2)

        run.assert_not_called()
        self.assertIn("ERROR Biome lint", errors.getvalue())
        self.assertIn("biome", errors.getvalue())
