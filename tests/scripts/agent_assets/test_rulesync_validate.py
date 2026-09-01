from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "scripts" / "agent_assets" / "validate_rulesync.py"
SPEC = importlib.util.spec_from_file_location("validate_rulesync_assets", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
validate_rulesync = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validate_rulesync
SPEC.loader.exec_module(validate_rulesync)


def result(*, returncode: int = 0, stdout: str = '{"success":true}', stderr: str = ""):
    return subprocess.CompletedProcess([], returncode, stdout, stderr)


def test_validate_runs_all_read_only_checks() -> None:
    calls: list[tuple[str, ...]] = []

    def runner(args: tuple[str, ...]):
        calls.append(args)
        return result()

    assert validate_rulesync.validate(runner) == 0
    assert calls == [check.args for check in validate_rulesync.CHECKS]
    assert all("--dry-run" in args for args in calls[1:])


def test_validate_fails_on_rulesync_warning(capsys) -> None:
    def runner(_args: tuple[str, ...]):
        return result(stdout='{"success":true,"warnings":["bad asset"]}')

    assert validate_rulesync.validate(runner) == 1
    assert "bad asset" in capsys.readouterr().err


def test_validate_fails_on_rulesync_error(capsys) -> None:
    def runner(_args: tuple[str, ...]):
        return result(
            returncode=1,
            stdout='{"success":false,"error":{"message":"invalid frontmatter"}}',
        )

    assert validate_rulesync.validate(runner) == 1
    assert "invalid frontmatter" in capsys.readouterr().err


def test_validate_fails_when_success_is_false_with_zero_exit(capsys) -> None:
    def runner(_args: tuple[str, ...]):
        return result(stdout='{"success":false}')

    assert validate_rulesync.validate(runner) == 1
    assert "FAIL" in capsys.readouterr().err


def test_validate_fails_on_malformed_warnings_contract(capsys) -> None:
    def runner(_args: tuple[str, ...]):
        return result(stdout='{"success":true,"warnings":"bad asset"}')

    assert validate_rulesync.validate(runner) == 1
    assert "warnings" in capsys.readouterr().err


def test_validate_fails_on_non_json_output(capsys) -> None:
    def runner(_args: tuple[str, ...]):
        return result(stdout="not-json")

    assert validate_rulesync.validate(runner) == 1
    assert "JSON" in capsys.readouterr().err


def test_run_rulesync_uses_json_and_library_workspace(monkeypatch) -> None:
    seen: dict[str, object] = {}

    def fake_run(command, **kwargs):
        seen["command"] = command
        seen.update(kwargs)
        return result()

    monkeypatch.setattr(validate_rulesync, "rulesync_command", lambda: "/tools/rulesync")
    monkeypatch.setattr(validate_rulesync.subprocess, "run", fake_run)

    validate_rulesync.run_rulesync(("doctor", "--strict"))

    assert seen["command"] == ["/tools/rulesync", "--json", "doctor", "--strict"]
    assert seen["cwd"] == validate_rulesync.WORKSPACE
    assert seen["check"] is False
    assert seen["capture_output"] is True
    assert seen["text"] is True
