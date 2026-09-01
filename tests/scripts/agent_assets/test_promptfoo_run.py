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
