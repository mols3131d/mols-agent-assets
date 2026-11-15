from __future__ import annotations

import subprocess
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

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
        ("Ruff format", ["ruff", "format", "--check", "./src/main.py"]),
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


def test_format_failure_prints_read_only_diff(tmp_path: Path) -> None:
    commands: list[list[str]] = []

    def fake_runner(command: list[str], root: Path) -> int:
        commands.append(command)
        return 1 if command[:3] == ["ruff", "format", "--check"] else 0

    assert quality.verify(("sample.py",), tmp_path, fake_runner) == 1
    assert commands[-1] == ["ruff", "format", "--diff", "./sample.py"]


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


def test_missing_staged_source_is_an_error_not_a_silent_skip(tmp_path: Path) -> None:
    git(tmp_path, "init", "-q")
    source = tmp_path / "new.py"
    source.write_text("print(1)\n", encoding="utf-8")
    git(tmp_path, "add", "new.py")
    source.unlink()
    assert quality.main(["--staged"], tmp_path) == 2


def test_selected_symlink_source_is_not_silently_skipped(tmp_path: Path) -> None:
    (tmp_path / "actual.py").write_text("print(1)\n", encoding="utf-8")
    (tmp_path / "link.py").symlink_to("actual.py")
    try:
        quality._check_source_paths(("link.py",), tmp_path)
    except ValueError as exc:
        assert "link.py" in str(exc)
    else:
        raise AssertionError("expected a symlink selection failure")


class SourceQualityRegressionTests(TestCase):
    def test_run_uses_resolved_windows_wrapper_and_preserves_arguments(self) -> None:
        root = Path("repository")
        executable = str(Path.cwd() / "managed tools" / "biome.cmd")
        command = ["biome", "lint", "./source file.ts"]
        with (
            patch("shutil.which", return_value=executable) as which,
            patch.object(
                quality.subprocess,
                "run",
                return_value=subprocess.CompletedProcess(command, 1),
            ) as run,
        ):
            self.assertEqual(quality._run(command, root), 1)

        which.assert_called_once_with("biome")
        run.assert_called_once_with(
            [executable, "lint", "./source file.ts"], cwd=root, check=False
        )

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

    def test_type_changes_reach_source_selection_and_symlink_guard(self) -> None:
        def git_type_change(command: list[str], **kwargs):
            # Model Git's T status without creating a symlink or fixture repository.
            committed_or_staged = "HEAD" in command or "--cached" in command
            filters = [arg for arg in command if arg.startswith("--diff-filter=")]
            includes_type_change = not filters or "T" in filters[0].split("=")[1]
            selected = committed_or_staged and includes_type_change
            stdout = b"source.py\0" if selected else b""
            return subprocess.CompletedProcess(command, 0, stdout=stdout)

        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "source.py").write_text("bad =\n", encoding="utf-8")
            for staged in (False, True):
                for symlink in (False, True):
                    with (
                        self.subTest(staged=staged, symlink=symlink),
                        patch.object(
                            quality.subprocess, "run", side_effect=git_type_change
                        ),
                        patch.object(Path, "is_symlink", return_value=symlink),
                    ):
                        if symlink:
                            with self.assertRaisesRegex(ValueError, "source.py"):
                                if staged:
                                    quality.staged_paths(root)
                                else:
                                    quality.changed_paths("base", root)
                        else:
                            selected = (
                                quality.staged_paths(root)
                                if staged
                                else quality.changed_paths("base", root)
                            )
                            self.assertEqual(selected, ("source.py",))
