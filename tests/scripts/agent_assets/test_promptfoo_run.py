from pathlib import Path

from scripts.agent_assets import promptfoo_run as runner

ROOT = Path(__file__).resolve().parents[3]


def test_runner_defaults_are_local_and_non_sharing() -> None:
    env = runner.build_env({"PROMPTFOO_DISABLE_TELEMETRY": "0"})
    state_dir = ROOT / ".tmp" / "promptfoo"

    assert env["PROMPTFOO_DISABLE_TELEMETRY"] == "0"
    assert env["PROMPTFOO_DISABLE_UPDATE"] == "1"
    assert env["PROMPTFOO_DISABLE_REMOTE_GENERATION"] == "true"
    assert env["PROMPTFOO_DISABLE_SHARING"] == "1"
    assert env["PROMPTFOO_CONFIG_DIR"] == str(state_dir)
    assert env["PROMPTFOO_LOG_DIR"] == str(state_dir / "logs")
    assert env["PROMPTFOO_CACHE_PATH"] == str(state_dir / "cache")
    assert env["PROMPTFOO_PYTHON"]
    assert runner.parse_node_version("v22.22.0") == (22, 22, 0)


def test_runner_installs_explicit_sdk_for_native_only(
    tmp_path: Path, monkeypatch
) -> None:
    class Result:
        returncode = 0

    commands: list[list[str]] = []

    def fake_subprocess(command: list[str], **kwargs) -> Result:
        commands.append(command)
        return Result()

    monkeypatch.setattr(runner, "resolve_npx", lambda env: "npx")
    monkeypatch.setattr(runner, "ROOT", tmp_path)
    monkeypatch.setattr(runner.subprocess, "run", fake_subprocess)
    assert runner.main(["eval"], extra_packages=("@openai/codex-sdk@0.156.1",)) == 0
    assert commands[-1] == [
        "npx",
        "--yes",
        f"--package=promptfoo@{runner.PROMPTFOO_VERSION}",
        "--package=@openai/codex-sdk@0.156.1",
        "promptfoo",
        "eval",
    ]
    assert runner.main(["eval"]) == 0
    assert commands[-1] == [
        "npx", "--yes", f"promptfoo@{runner.PROMPTFOO_VERSION}", "eval"
    ]
