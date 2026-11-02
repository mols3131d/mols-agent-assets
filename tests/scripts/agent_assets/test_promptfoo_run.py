from pathlib import Path

import pytest

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


def test_runner_preserves_explicit_model_and_grader_settings() -> None:
    defaults = runner.build_env({})
    assert defaults["PROMPTFOO_RUNTIME_MODEL"] == "qwen2.5"
    assert defaults["PROMPTFOO_RUNTIME_PROVIDER"] == "ollama:chat:qwen2.5"
    assert defaults["PROMPTFOO_GRADER_PROVIDER"] == "ollama:chat:qwen2.5"
    assert defaults["REQUEST_TIMEOUT_MS"] == "120000"

    overrides = runner.build_env(
        {
            "PROMPTFOO_RUNTIME_MODEL": "custom-local-model",
            "PROMPTFOO_GRADER_PROVIDER": "ollama:chat:custom-grader",
            "OLLAMA_BASE_URL": "http://127.0.0.1:11434",
            "PROMPTFOO_RUNTIME_TIMEOUT_SECONDS": "75",
        }
    )
    assert overrides["PROMPTFOO_RUNTIME_MODEL"] == "custom-local-model"
    assert overrides["PROMPTFOO_RUNTIME_PROVIDER"] == "ollama:chat:custom-local-model"
    assert overrides["PROMPTFOO_GRADER_PROVIDER"] == "ollama:chat:custom-grader"
    assert overrides["OLLAMA_BASE_URL"] == "http://127.0.0.1:11434"
    assert overrides["PROMPTFOO_RUNTIME_TIMEOUT_SECONDS"] == "75"
    assert overrides["REQUEST_TIMEOUT_MS"] == "75000"
    assert overrides["PROMPTFOO_DISABLE_REMOTE_GENERATION"] == "true"


@pytest.mark.parametrize(
    "provider",
    [
        "ollama:chat:another-model",
        "openai:chat:example-model",
        "anthropic:messages:example-model",
        "google:gemini-2.5-flash",
    ],
)
def test_explicit_native_provider_takes_precedence_over_legacy_model(provider) -> None:
    base = {
        "PROMPTFOO_RUNTIME_PROVIDER": provider,
        "PROMPTFOO_RUNTIME_MODEL": "legacy-ollama-model",
    }
    env = runner.build_env(base)

    assert env["PROMPTFOO_RUNTIME_PROVIDER"] == provider
    assert env["PROMPTFOO_RUNTIME_MODEL"] == "legacy-ollama-model"
    assert env["PROMPTFOO_GRADER_PROVIDER"] == "ollama:chat:qwen2.5"
    assert base == {
        "PROMPTFOO_RUNTIME_PROVIDER": provider,
        "PROMPTFOO_RUNTIME_MODEL": "legacy-ollama-model",
    }


def test_native_provider_and_grader_keep_independent_credentials_and_options() -> None:
    base = {
        "PROMPTFOO_RUNTIME_PROVIDER": "anthropic:messages:example-model",
        "PROMPTFOO_GRADER_PROVIDER": "openai:chat:example-grader",
        "ANTHROPIC_API_KEY": "test-only-anthropic-key",
        "OPENAI_API_KEY": "test-only-openai-key",
        "OPENAI_API_BASE_URL": "http://127.0.0.1:12345/v1",
        "REQUEST_TIMEOUT_MS": "9000",
        "PROMPTFOO_RUNTIME_TIMEOUT_SECONDS": "75",
    }
    env = runner.build_env(base)

    assert all(env[key] == value for key, value in base.items())


def test_runner_passes_native_provider_environment_to_promptfoo(
    tmp_path, monkeypatch
) -> None:
    monkeypatch.setenv("PROMPTFOO_CONFIG_DIR", str(tmp_path))
    monkeypatch.setenv("PROMPTFOO_RUNTIME_PROVIDER", "openai:chat:example-model")
    monkeypatch.setenv("PROMPTFOO_GRADER_PROVIDER", "anthropic:messages:example-grader")
    monkeypatch.setattr(runner, "resolve_npx", lambda env: "npx")
    observed = []

    def run(command, *, check, env):
        observed.append((command, check, env))
        return runner.subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(runner.subprocess, "run", run)
    args = ["eval", "-c", "evals/promptfoo/mols-loops.yaml"]

    assert runner.main(args) == 0
    command, check, env = observed[0]
    assert command == ["npx", "--yes", f"promptfoo@{runner.PROMPTFOO_VERSION}", *args]
    assert check is False
    assert env["PROMPTFOO_RUNTIME_PROVIDER"] == "openai:chat:example-model"
    assert env["PROMPTFOO_GRADER_PROVIDER"] == "anthropic:messages:example-grader"
    assert env["PROMPTFOO_PYTHON"]


def test_native_timeout_does_not_evaluate_shadowed_legacy_value() -> None:
    env = runner.build_env(
        {
            "REQUEST_TIMEOUT_MS": "9000",
            "PROMPTFOO_RUNTIME_TIMEOUT_SECONDS": "invalid",
        }
    )
    assert env["REQUEST_TIMEOUT_MS"] == "9000"


def test_empty_owned_settings_use_local_defaults() -> None:
    env = runner.build_env(
        {
            "PROMPTFOO_RUNTIME_PROVIDER": " ",
            "PROMPTFOO_RUNTIME_MODEL": "",
            "PROMPTFOO_GRADER_PROVIDER": "",
            "REQUEST_TIMEOUT_MS": "",
        }
    )
    assert env["PROMPTFOO_RUNTIME_PROVIDER"] == "ollama:chat:qwen2.5"
    assert env["PROMPTFOO_RUNTIME_MODEL"] == "qwen2.5"
    assert env["PROMPTFOO_GRADER_PROVIDER"] == "ollama:chat:qwen2.5"
    assert env["REQUEST_TIMEOUT_MS"] == "120000"


def test_invalid_environment_reports_error_before_filesystem_or_cli(
    tmp_path, monkeypatch, capsys
) -> None:
    state = tmp_path / "not-created"
    monkeypatch.setenv("PROMPTFOO_CONFIG_DIR", str(state))
    monkeypatch.setenv("REQUEST_TIMEOUT_MS", "invalid-secret-like-value")
    monkeypatch.setattr(runner, "resolve_npx", lambda env: pytest.fail("CLI started"))

    assert runner.main(["--help"]) == 2
    error = capsys.readouterr().err
    assert "REQUEST_TIMEOUT_MS must be a positive integer" in error
    assert "invalid-secret-like-value" not in error
    assert "Traceback" not in error
    assert not state.exists()
