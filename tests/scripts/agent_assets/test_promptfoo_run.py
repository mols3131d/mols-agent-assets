import json
import subprocess
from pathlib import Path

import pytest

from scripts.agent_assets import promptfoo_run as runner

BOOTSTRAP = ["-c", str(runner.CONFIG_DIR / "mols-dev-env-bootstrap-design.yaml")]
SMOKE = ["-c", str(runner.CONFIG_DIR / "mols-dev-env-bootstrap-design-smoke.yaml")]
REFERENCE = ["-c", str(runner.CONFIG_DIR / "mols-test-design.yaml")]
ROUTING = ["-c", str(runner.CONFIG_DIR / "mols-implementation-guidance.yaml")]
CALIBRATION = [
    "-c",
    str(runner.CONFIG_DIR / "mols-dev-env-bootstrap-design-grader.yaml"),
]
OLLAMA = ["--provider", "ollama", "--model", "qwen:test"]
CODEX = ["--provider", "codex", "--model", "codex-test"]
NO_GRADER = ["--grader", "none"]


@pytest.mark.parametrize("args", [[], ["eval"], ["--help"], ["eval", "-h"]])
def test_help_does_not_start_promptfoo(args, monkeypatch, capsys):
    monkeypatch.setattr(runner, "resolve_npx", lambda env: pytest.fail("CLI started"))
    monkeypatch.setenv("REQUEST_TIMEOUT_MS", "invalid")
    assert runner.main(args) == 0
    assert "usage: mise run eval" in capsys.readouterr().out


@pytest.mark.parametrize(
    "args, error",
    [
        (["--filter-first-n", "1"], "select one repository evaluation"),
        (["--config= "], "one non-blank value"),
        (BOOTSTRAP * 2 + OLLAMA + NO_GRADER, "one non-blank value"),
        (BOOTSTRAP + ["--model", "ambient"] + NO_GRADER, "--provider and --model"),
        (BOOTSTRAP + ["--provider", "ollama"] + NO_GRADER, "--model"),
        (BOOTSTRAP + ["--provider", "ollama", "--model= "] + NO_GRADER, "non-blank"),
        (
            BOOTSTRAP + ["--provider", "ollama", "--model=invalid model"] + NO_GRADER,
            "valid ollama",
        ),
        (BOOTSTRAP + OLLAMA, "select --grader"),
        (BOOTSTRAP + OLLAMA + ["--grader", "ollama"], "--grader-model"),
        (
            BOOTSTRAP + OLLAMA + NO_GRADER + ["--grader-model", "unused"],
            "--grader none",
        ),
        (BOOTSTRAP + CODEX + NO_GRADER, "--codex-auth"),
        (REFERENCE + CODEX + NO_GRADER, "requires --provider ollama"),
        (
            ROUTING + OLLAMA + ["--grader", "ollama", "--grader-model", "x"],
            "no semantic grading",
        ),
        (CALIBRATION + NO_GRADER, "calibration requires a grader model"),
        (CALIBRATION + OLLAMA + NO_GRADER, "fixture/echo runtime"),
        (SMOKE, "--fixture is required"),
        (SMOKE + ["--fixture", *OLLAMA], "fixture/echo runtime"),
        (SMOKE + ["--fixture", *NO_GRADER], "does not take grader options"),
    ],
)
def test_rejects_invalid_selections_before_install(args, error, monkeypatch, capsys):
    monkeypatch.setattr(runner, "resolve_npx", lambda env: pytest.fail("CLI started"))
    monkeypatch.setenv("PROMPTFOO_RUNTIME_PROVIDER", "ollama:chat:fallback")
    monkeypatch.setenv("PROMPTFOO_GRADER_PROVIDER", "ollama:chat:fallback")
    assert runner.main(args) == 2
    assert error in capsys.readouterr().err


@pytest.mark.parametrize(
    "override",
    [
        ["--providers", "echo"],
        ["-r", "echo"],
        ["--assertions", "replacement.yaml"],
        ["--env-file", "replacement.env"],
        ["--model-outputs", "results.json"],
        ["--suggest-prompts", "1"],
        ["--watch"],
        ["--remote"],
        ["--resume"],
        ["--share"],
        ["--extension", "extra.js"],
        ["--grad", "ollama"],
    ],
)
def test_promptfoo_options_cannot_bypass_selections(override, monkeypatch):
    monkeypatch.setattr(runner, "resolve_npx", lambda env: pytest.fail("CLI started"))
    with pytest.raises(SystemExit) as error:
        runner.main(SMOKE + ["--fixture", *override])
    assert error.value.code == 2


def test_config_cannot_be_replaced_by_other_files(tmp_path):
    copy = tmp_path / "mols-dev-env-bootstrap-design.yaml"
    copy.write_text("providers: [echo]", encoding="utf-8")
    with pytest.raises(ValueError, match="suite in evals/promptfoo"):
        runner.select_config(runner.parser().parse_args(["-c", str(copy)]))


def test_native_ollama_config_and_no_grader(tmp_path):
    config, env, codex = runner.configure(
        runner.parser().parse_args(BOOTSTRAP + OLLAMA + NO_GRADER),
        tmp_path,
        {
            "PROMPTFOO_RUNTIME_PROVIDER": "unused",
            "PROMPTFOO_GRADER_PROVIDER": "unused",
            "OLLAMA_BASE_URL": "http://localhost:12345/",
            "PROMPTFOO_RUNTIME_TIMEOUT_SECONDS": "75",
            "PROMPTFOO_DISABLE_TELEMETRY": "0",
        },
    )
    assert not codex
    assert config["prompts"] == ["file://skill-chat.json"]
    assert {provider["id"] for provider in config["providers"]} == {
        "ollama:chat:qwen:test"
    }
    assert config["providers"][0]["config"] == {"temperature": 0, "showThinking": False}
    assert all(spec["config"]["semantic"] is False for spec in config["tests"])
    assert all("grader" not in spec["config"] for spec in config["tests"])
    assert env["REQUEST_TIMEOUT_MS"] == "75000"
    assert env["OLLAMA_BASE_URL"] == "http://localhost:12345"
    assert env["PROMPTFOO_DISABLE_TELEMETRY"] == "1"
    assert env["PROMPTFOO_DISABLE_SHARING"] == "1"
    assert "PROMPTFOO_RUNTIME_PROVIDER" not in env
    assert "PROMPTFOO_GRADER_PROVIDER" not in env


def test_selected_custom_ollama_model_cannot_be_overridden(tmp_path):
    cfg, env, codex = runner.configure(
        runner.parser().parse_args(REFERENCE + OLLAMA + NO_GRADER),
        tmp_path,
        {"PROMPTFOO_RUNTIME_MODEL": "legacy", "PROMPTFOO_RUNTIME_THINK": "false"},
    )
    assert not codex
    assert cfg["providers"][0]["id"].endswith("skills_promptfoo.py:call_api")
    assert env["PROMPTFOO_RUNTIME_MODEL"] == "qwen:test"
    assert env["PROMPTFOO_RUNTIME_THINK"] == "false"


def test_codex_api_isolation_and_independent_ollama_grader(tmp_path):
    config, env, codex = runner.configure(
        runner.parser().parse_args(
            BOOTSTRAP
            + CODEX
            + [
                "--codex-auth",
                "api",
                "--grader",
                "ollama",
                "--grader-model",
                "different",
            ]
        ),
        tmp_path,
        {
            "PROMPTFOO_CODEX_API_KEY": "test-only-selected",
            "CODEX_API_KEY": "test-only-ambient",
            "OPENAI_API_KEY": "test-only-openai",
            "OPENAI_BASE_URL": "test-only-wrong-endpoint",
            "PROMPTFOO_CODEX_TIMEOUT_MS": "5000",
            "REQUEST_TIMEOUT_MS": "9000",
        },
    )
    assert codex
    assert config["prompts"] == ["file://skill-agent.txt"]
    assert {provider["id"] for provider in config["providers"]} == {
        "openai:codex-sdk:codex-test"
    }
    trigger, behavior = [provider["config"] for provider in config["providers"]]
    assert trigger["output_schema"]["required"] == ["selected_skills", "primary_skill"]
    assert "output_schema" not in behavior
    assert "temperature" not in behavior
    assert set(Path(behavior["working_dir"]).iterdir()) == set()
    assert behavior["approval_policy"] == "never"
    assert behavior["web_search_mode"] == "disabled"
    assert behavior["persist_threads"] is False
    assert behavior["inherit_process_env"] is False
    cli_config = behavior["cli_config"]
    assert cli_config["default_permissions"] == "evaluation"
    assert cli_config["permissions"]["evaluation"]["network"] == {"enabled": False}
    assert cli_config["shell_environment_policy"] == {"inherit": "none"}
    assert cli_config["features"]["shell_tool"] is False
    assert cli_config["forced_login_method"] == "api"
    assert cli_config["cli_auth_credentials_store"] == "ephemeral"
    assert Path(behavior["cli_env"]["CODEX_HOME"]).parent == tmp_path
    assert env["CODEX_API_KEY"] == "test-only-selected"
    assert "OPENAI_API_KEY" not in env
    assert "OPENAI_BASE_URL" not in env
    assert "test-only-" not in json.dumps(config)
    assert env["PROMPTFOO_EVAL_TIMEOUT_MS"] == "5000"
    assert env["REQUEST_TIMEOUT_MS"] == "9000"
    grader = config["tests"][1]["config"]["grader"]
    assert grader["id"] == "ollama:chat:different"


@pytest.mark.parametrize(
    "base, message",
    [
        ({}, "requires PROMPTFOO_CODEX_API_KEY"),
        (
            {"PROMPTFOO_CODEX_API_KEY": " ", "CODEX_API_KEY": "ambient"},
            "requires PROMPTFOO_CODEX_API_KEY",
        ),
        (
            {
                "PROMPTFOO_CODEX_API_KEY": "test-only-key",
                "PROMPTFOO_CODEX_TIMEOUT_MS": "0",
            },
            "PROMPTFOO_CODEX_TIMEOUT_MS",
        ),
    ],
)
def test_codex_fails_closed_without_selected_key_or_valid_timeout(
    tmp_path, base, message
):
    with pytest.raises(ValueError, match=message):
        runner.configure(
            runner.parser().parse_args(
                BOOTSTRAP + CODEX + NO_GRADER + ["--codex-auth", "api"]
            ),
            tmp_path,
            base,
        )


def test_codex_chatgpt_grader_has_isolated_home_and_no_ambient_keys(tmp_path):
    auth_profile = tmp_path / "auth"
    auth_profile.mkdir()
    config, env, codex = runner.configure(
        runner.parser().parse_args(
            CALIBRATION
            + [
                "--grader",
                "codex",
                "--grader-model",
                "grader-test",
                "--codex-auth",
                "chatgpt",
            ]
        ),
        tmp_path,
        {
            "PROMPTFOO_CODEX_CHATGPT_HOME": str(auth_profile),
            "PROMPTFOO_CODEX_API_KEY": "unused",
            "CODEX_API_KEY": "ambient",
            "OPENAI_API_KEY": "also-ambient",
        },
    )
    assert codex
    assert config["providers"][0]["id"] == "echo"
    grader = config["tests"][0]["config"]["grader"]
    assert grader["id"] == "openai:codex-sdk:grader-test"
    options = grader["config"]
    assert options["cli_config"]["forced_login_method"] == "chatgpt"
    assert options["cli_env"]["CODEX_HOME"] == str(auth_profile)
    assert options["cli_env"]["HOME"] != str(auth_profile)
    assert options["output_schema"]["required"] == ["pass", "score", "reason"]
    assert (
        not {"CODEX_API_KEY", "OPENAI_API_KEY", "PROMPTFOO_CODEX_API_KEY"} & env.keys()
    )


def test_invalid_environment_does_not_start_cli(monkeypatch, capsys):
    monkeypatch.setenv("REQUEST_TIMEOUT_MS", "invalid-secret-like-value")
    monkeypatch.setattr(runner, "resolve_npx", lambda env: pytest.fail("CLI started"))
    assert runner.main(BOOTSTRAP + OLLAMA + NO_GRADER) == 2
    error = capsys.readouterr().err
    assert "REQUEST_TIMEOUT_MS must be a positive integer" in error
    assert "invalid-secret-like-value" not in error
    assert "Traceback" not in error


def test_runner_uses_pinned_cli_in_temp_directory_and_keeps_filter_and_output_paths(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setenv("REQUEST_TIMEOUT_MS", "bad-unused-value")
    monkeypatch.setattr(runner, "resolve_npx", lambda env: "npx")
    monkeypatch.chdir(tmp_path)
    recorded = []

    def run(command, *, check, cwd, env):
        recorded.append(cwd)
        assert command == [
            "npx",
            "--yes",
            "--ignore-scripts",
            "--package=promptfoo@0.126.0",
            "--",
            "promptfoo",
            "eval",
            "--config",
            str(cwd / "eval.json"),
            "--filter-first-n=2",
            "--filter-metadata=suite=trigger",
            "--output",
            str(tmp_path / "results.json"),
        ]
        config = json.loads((cwd / "eval.json").read_text(encoding="utf-8"))
        assert config["basePath"] == str(runner.CONFIG_DIR)
        assert config["providers"][0]["config"]["mode"] == "fixture"
        assert "REQUEST_TIMEOUT_MS" not in env
        assert check is False
        return subprocess.CompletedProcess(command, 7)

    monkeypatch.setattr(runner.subprocess, "run", run)
    assert (
        runner.main(
            SMOKE
            + [
                "--fixture",
                "-n",
                "2",
                "--filter-metadata",
                "suite=trigger",
                "-o",
                "results.json",
            ]
        )
        == 7
    )
    assert not recorded[0].exists()


def test_minimum_node_matches_pinned_promptfoo_runtime(monkeypatch):
    monkeypatch.setattr(runner.shutil, "which", lambda name, **kwargs: name)
    monkeypatch.setattr(
        runner.subprocess,
        "run",
        lambda cmd, **kwargs: subprocess.CompletedProcess(cmd, 0, stdout="v22.21.0\n"),
    )
    with pytest.raises(RuntimeError, match=r"0\.126\.0 requires Node.js >= 22\.22\.0"):
        runner.resolve_npx({})
    assert runner.parse_node_version("v22.22.0") == (22, 22, 0)


@pytest.mark.parametrize(
    ("returncode", "status", "accepted"),
    [
        (0, "Logged in using ChatGPT", True),
        (0, "API key configured - test-only-private-suffix", False),
        (1, "Not logged in", False),
    ],
)
def test_chatgpt_status_does_not_switch_auth_or_report_cli_output(
    tmp_path,
    monkeypatch,
    capsys,
    returncode,
    status,
    accepted,
):
    def run(command, **kwargs):
        assert command[-5:] == [
            "codex",
            "-c",
            'cli_auth_credentials_store="file"',
            "login",
            "status",
        ]
        assert kwargs["env"]["CODEX_HOME"] == str(tmp_path / "profile")
        assert kwargs["stdin"] == subprocess.DEVNULL
        assert kwargs["capture_output"] is True
        assert kwargs["timeout"] == 120
        return subprocess.CompletedProcess(
            command, returncode, stdout="", stderr=status
        )

    monkeypatch.setattr(runner.subprocess, "run", run)
    if accepted:
        runner.verify_chatgpt_login(["npx"], tmp_path, {}, str(tmp_path / "profile"))
    else:
        with pytest.raises(ValueError, match="needs an active ChatGPT login") as error:
            runner.verify_chatgpt_login(
                ["npx"], tmp_path, {}, str(tmp_path / "profile")
            )
        assert status not in str(error.value)
    assert not capsys.readouterr().err


def test_runner_covers_the_active_config_directory():
    assert {path.name for path in runner.CONFIG_DIR.glob("*.yaml")} == set(
        runner.CONFIG_MODES
    )
