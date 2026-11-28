from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml

if __package__:
    from . import promptfoo_env, skills_promptfoo
else:
    import promptfoo_env
    import skills_promptfoo

ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT / "evals" / "promptfoo"
PROMPTFOO_VERSION = "0.126.0"
CODEX_SDK_VERSION = "0.169.1"
MIN_NODE_VERSION = (22, 22, 0)
CONFIG_MODES = {
    "mols-loops.yaml": "native",
    "mols-dev-env-bootstrap-design.yaml": "native",
    "mols-stdd.yaml": "native",
    "mols-test-design.yaml": "ollama",
    "mols-stdd-references.yaml": "ollama",
    "mols-dev-env-bootstrap-design-grader.yaml": "calibration",
    "mols-loops-smoke.yaml": "fixture",
}
# Forward only presentation, subset and result options. Promptfoo also has CLI
# options that replace inputs or choose additional providers and callbacks.
VALUE_OPTIONS = {
    "filter_first_n": ("-n", "--filter-first-n"),
    "filter_pattern": ("--filter-pattern",),
    "filter_range": ("--filter-range",),
    "filter_prompts": ("--filter-prompts",),
    "filter_providers": ("--filter-providers", "--filter-targets"),
    "filter_sample": ("--filter-sample",),
    "filter_sample_seed": ("--filter-sample-seed",),
    "filter_failing": ("--filter-failing",),
    "filter_failing_only": ("--filter-failing-only",),
    "filter_errors_only": ("--filter-errors-only",),
    "filter_metadata": ("--filter-metadata",),
    "description": ("--description",),
    "repeat": ("--repeat",),
    "delay": ("--delay",),
}
SWITCH_OPTIONS = ("no-cache", "no-write", "no-share", "no-table", "no-progress-bar")
MODEL_SEGMENT = r"[A-Za-z0-9][A-Za-z0-9._-]*"
CODEX_MODEL = re.compile(MODEL_SEGMENT)
OLLAMA_MODEL = re.compile(
    rf"(?:{MODEL_SEGMENT}(?::[0-9]+)?/)?(?:{MODEL_SEGMENT}/)?"
    rf"{MODEL_SEGMENT}(?::{MODEL_SEGMENT})?"
)
RUBRIC_SCHEMA = {
    "type": "object",
    "properties": {
        "pass": {"type": "boolean"},
        "score": {"type": "number"},
        "reason": {"type": "string"},
    },
    "required": ["pass", "score", "reason"],
    "additionalProperties": False,
}


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(
        prog="mise run eval",
        allow_abbrev=False,
        add_help=False,
        description="Run one repository evaluation with explicit model selections.",
    )
    cli.add_argument("-h", "--help", action="store_true")
    cli.add_argument("-c", "--config", action="append")
    cli.add_argument(
        "--fixture", action="store_true", help="run model-free fixture smoke"
    )
    cli.add_argument("--provider", choices=("ollama", "codex"), action="append")
    cli.add_argument("--model", action="append")
    cli.add_argument("--grader", choices=("none", "ollama", "codex"), action="append")
    cli.add_argument("--grader-model", action="append")
    cli.add_argument("--codex-auth", choices=("chatgpt", "api"), action="append")
    for dest, flags in VALUE_OPTIONS.items():
        cli.add_argument(*flags, dest=dest, action="append", metavar="VALUE")
    for flag in SWITCH_OPTIONS:
        cli.add_argument(f"--{flag}", action="store_true")
    cli.add_argument("-o", "--output", action="extend", nargs="+", metavar="PATH")
    return cli


def one_value(args: argparse.Namespace, name: str) -> str | None:
    values = getattr(args, name)
    if values is None:
        return None
    if len(values) != 1 or not values[0].strip():
        flag = name.replace("_", "-")
        raise ValueError(f"--{flag} requires exactly one non-blank value")
    return values[0].strip()


def validate_model(provider: str, model: str | None, flag: str) -> str:
    pattern = CODEX_MODEL if provider == "codex" else OLLAMA_MODEL
    if model is None or not pattern.fullmatch(model):
        raise ValueError(f"{flag} requires an explicit, valid {provider} model ID")
    return model


def select_config(args: argparse.Namespace) -> tuple[Path, str]:
    value = one_value(args, "config")
    if value is None:
        raise ValueError("select one repository evaluation with -c/--config")
    path = Path(value).absolute()
    mode = CONFIG_MODES.get(path.name)
    if mode is None or path.resolve() != CONFIG_DIR / path.name:
        raise ValueError("-c/--config must select a suite in evals/promptfoo/")
    return path.resolve(), mode


def forwarded_args(args: argparse.Namespace) -> list[str]:
    forwarded = []
    for dest, flags in VALUE_OPTIONS.items():
        for value in getattr(args, dest) or ():
            if dest in {"filter_failing", "filter_failing_only", "filter_errors_only"}:
                if Path(value).is_file():
                    value = str(Path(value).resolve())
            forwarded.append(f"{flags[-1]}={value}")
    for flag in SWITCH_OPTIONS:
        if getattr(args, flag.replace("-", "_")):
            forwarded.append(f"--{flag}")
    if args.output:
        forwarded.extend(
            ["--output", *(str(Path(path).absolute()) for path in args.output)]
        )
    return forwarded


def build_env(base: dict[str, str]) -> dict[str, str]:
    # Own Promptfoo's execution switches and avoid passing ambient provider keys.
    env = {
        name: value
        for name, value in base.items()
        if name.upper() != "REQUEST_TIMEOUT_MS"
        and not name.upper().startswith(("PROMPTFOO_", "OPENAI_", "CODEX_", "OLLAMA_"))
    }
    state_dir = ROOT / ".tmp" / "promptfoo"
    env.update(
        PROMPTFOO_DISABLE_TELEMETRY="1",
        PROMPTFOO_DISABLE_UPDATE="1",
        PROMPTFOO_DISABLE_REMOTE_GENERATION="true",
        PROMPTFOO_DISABLE_SHARING="1",
        PROMPTFOO_DISABLE_DEBUG_LOG="1",
        PROMPTFOO_DISABLE_ERROR_LOG="1",
        PROMPTFOO_CONFIG_DIR=str(state_dir),
        PROMPTFOO_LOG_DIR=str(state_dir / "logs"),
        PROMPTFOO_CACHE_PATH=str(state_dir / "cache"),
        PROMPTFOO_PYTHON=sys.executable,
    )
    return env


def codex_options(
    auth: str, base: dict[str, str], env: dict[str, str], directory: Path
) -> dict:
    working_dir = directory / "agent"
    working_dir.mkdir()
    isolated_home = directory / "home"
    isolated_home.mkdir()
    if auth == "api":
        key = base.get("PROMPTFOO_CODEX_API_KEY", "").strip()
        if not key:
            raise ValueError("--codex-auth api requires PROMPTFOO_CODEX_API_KEY")
        codex_home = directory / "codex"
        codex_home.mkdir()
        env["CODEX_API_KEY"] = key
    else:
        value = base.get("PROMPTFOO_CODEX_CHATGPT_HOME", "").strip()
        if not value or not Path(value).is_absolute():
            raise ValueError(
                "--codex-auth chatgpt requires an absolute PROMPTFOO_CODEX_CHATGPT_HOME"
            )
        codex_home = Path(value).resolve()
        if not codex_home.is_dir() or codex_home.is_relative_to(ROOT):
            raise ValueError(
                "PROMPTFOO_CODEX_CHATGPT_HOME must be a dedicated directory "
                "outside the repository"
            )
        profile_inputs = (
            "config.toml",
            "AGENTS.md",
            "AGENTS.override.md",
            "skills",
            "plugins",
            "hooks.json",
            "rules",
        )
        if codex_home == Path.home() / ".codex" or any(
            (codex_home / name).exists() or (codex_home / name).is_symlink()
            for name in profile_inputs
        ):
            raise ValueError(
                "PROMPTFOO_CODEX_CHATGPT_HOME must be a dedicated login-only Codex home"
            )

    env["PROMPTFOO_EVAL_TIMEOUT_MS"] = str(promptfoo_env.codex_timeout_ms(base))
    return {
        "working_dir": str(working_dir),
        "skip_git_repo_check": True,
        "persist_threads": False,
        "inherit_process_env": False,
        "approval_policy": "never",
        "web_search_mode": "disabled",
        "model_provider": "openai",
        "cli_env": {
            "HOME": str(isolated_home),
            "USERPROFILE": str(isolated_home),
            "CODEX_HOME": str(codex_home),
        },
        "cli_config": {
            "forced_login_method": auth,
            "cli_auth_credentials_store": "ephemeral" if auth == "api" else "file",
            "default_permissions": "evaluation",
            "check_for_update_on_startup": False,
            "project_doc_max_bytes": 0,
            "history": {"persistence": "none"},
            "log_dir": str(directory / "codex-logs"),
            "sqlite_home": str(directory / "codex-db"),
            "permissions": {
                "evaluation": {
                    "filesystem": {":minimal": "read", ":workspace_roots": "read"},
                    "network": {"enabled": False},
                },
            },
            "shell_environment_policy": {"inherit": "none"},
            "features": {
                "apps": False,
                "memories": False,
                "plugins": False,
                "remote_models": False,
                "request_permissions": False,
                "shell_tool": False,
                "unified_exec": False,
            },
        },
    }


def provider_options(
    provider: str, model: str, codex: dict, output_schema: dict | None = None
) -> dict:
    if provider == "ollama":
        return {
            "id": f"ollama:chat:{model}",
            "config": {"temperature": 0, "showThinking": False},
        }
    return {
        "id": f"openai:codex-sdk:{model}",
        "config": {
            **codex,
            **({"output_schema": output_schema} if output_schema else {}),
        },
    }


def configure(
    args: argparse.Namespace, directory: Path, base: dict[str, str]
) -> tuple[dict, dict[str, str], dict]:
    path, mode = select_config(args)
    provider = one_value(args, "provider")
    model = one_value(args, "model")
    grader = one_value(args, "grader")
    grader_model = one_value(args, "grader_model")
    auth = one_value(args, "codex_auth")

    if args.fixture != (mode == "fixture"):
        raise ValueError(
            "--fixture is required for mols-loops-smoke.yaml and is only for that suite"
        )
    if mode in {"fixture", "calibration"}:
        if provider is not None or model is not None:
            raise ValueError("this suite supplies its own fixture/echo runtime")
    elif provider is None:
        raise ValueError("select --provider and --model")
    else:
        model = validate_model(provider, model, "--model")
        if mode == "ollama" and provider != "ollama":
            raise ValueError("this reference suite requires --provider ollama")

    config = yaml.safe_load(path.read_text(encoding="utf-8"))
    supports_grader = mode == "calibration" or any(
        test["config"].get("semantic") is True for test in config["tests"]
    )
    if mode == "fixture":
        if grader is not None or grader_model is not None:
            raise ValueError("fixture smoke does not take grader options")
    elif grader is None:
        raise ValueError("select --grader none, ollama, or codex")
    elif grader == "none":
        if grader_model is not None or mode == "calibration":
            raise ValueError(
                "calibration requires a grader model; "
                "--grader none cannot take --grader-model"
            )
    else:
        if not supports_grader:
            raise ValueError("this suite has no semantic grading")
        grader_model = validate_model(grader, grader_model, "--grader-model")

    uses_codex = "codex" in {provider, grader}
    if uses_codex != (auth is not None):
        raise ValueError(
            "--codex-auth is required exactly when a Codex provider is selected"
        )

    env = build_env(base)
    # Promptfoo probes default grader credentials even when the rubric names a
    # provider. Prevent Google ADC from discovering a host login or metadata server.
    env["GOOGLE_APPLICATION_CREDENTIALS"] = str(directory / "unused-google-auth.json")
    env["CODEX_HOME"] = str(directory / "unused-codex-home")
    if "ollama" in {provider, grader}:
        env["REQUEST_TIMEOUT_MS"] = str(promptfoo_env.request_timeout_ms(base))
        env["OLLAMA_BASE_URL"] = promptfoo_env.ollama_base_url(base)
        if base.get("OLLAMA_API_KEY"):
            env["OLLAMA_API_KEY"] = base["OLLAMA_API_KEY"]
    codex = codex_options(auth, base, env, directory) if uses_codex else {}
    if mode == "native":
        if provider == "codex":
            config["prompts"] = ["file://skill-agent.txt"]
        for entry in config["providers"]:
            output_schema = (
                skills_promptfoo.TRIGGER_RESPONSE_SCHEMA
                if entry["label"].endswith("-trigger")
                else None
            )
            entry.update(provider_options(provider, model, codex, output_schema))
    if mode == "ollama":
        env["PROMPTFOO_RUNTIME_MODEL"] = model
        if "PROMPTFOO_RUNTIME_THINK" in base:
            think = base["PROMPTFOO_RUNTIME_THINK"]
            if think not in {"true", "false"}:
                raise ValueError("PROMPTFOO_RUNTIME_THINK must be true or false")
            env["PROMPTFOO_RUNTIME_THINK"] = think
    for entry in config["tests"]:
        test = entry["config"]
        if supports_grader and (mode == "calibration" or test.get("semantic") is True):
            if grader == "none":
                test["semantic"] = False
            else:
                test["grader"] = provider_options(
                    grader, grader_model, codex, RUBRIC_SCHEMA
                )

    config["basePath"] = str(path.parent)
    return config, env, codex


def parse_node_version(value: str) -> tuple[int, int, int]:
    match = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)(?:[-+].*)?", value.strip())
    if match is None:
        raise ValueError(f"unsupported Node.js version string: {value!r}")
    return tuple(int(part) for part in match.groups())


def resolve_npx(env: dict[str, str]) -> str:
    path = env.get("PATH")
    node = shutil.which("node", path=path)
    npx = shutil.which("npx", path=path)
    if node is None or npx is None:
        raise RuntimeError("Promptfoo eval requires Node.js and npx on PATH")

    result = subprocess.run(
        [node, "--version"],
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )
    version = parse_node_version(result.stdout)
    if version < MIN_NODE_VERSION:
        required = ".".join(str(part) for part in MIN_NODE_VERSION)
        actual = ".".join(str(part) for part in version)
        raise RuntimeError(
            f"Promptfoo {PROMPTFOO_VERSION} requires Node.js >= {required}; "
            f"found {actual}"
        )
    return npx


def verify_chatgpt_login(
    command: list[str], directory: Path, env: dict[str, str], codex_home: str
) -> None:
    result = subprocess.run(
        [
            *command,
            "--",
            "codex",
            "-c",
            'cli_auth_credentials_store="file"',
            "login",
            "status",
        ],
        cwd=directory,
        env={**env, "CODEX_HOME": codex_home},
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    status = (*result.stdout.splitlines(), *result.stderr.splitlines())
    if result.returncode != 0 or "Logged in using ChatGPT" not in status:
        raise ValueError("the dedicated Codex home needs an active ChatGPT login")


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args[:1] == ["eval"]:
        args.pop(0)
    cli = parser()
    if not args or args in (["-h"], ["--help"]):
        cli.print_help()
        return 0

    selected = cli.parse_args(args)
    if selected.help:
        cli.print_help()
        return 0
    try:
        with TemporaryDirectory(prefix="mols-promptfoo-") as temporary:
            directory = Path(temporary).resolve()
            if directory.is_relative_to(ROOT):
                raise ValueError(
                    "the temporary directory must be outside the repository"
                )
            config, env, codex = configure(selected, directory, dict(os.environ))
            npx = resolve_npx(env)
            command = [
                npx,
                "--yes",
                "--ignore-scripts",
                f"--package=promptfoo@{PROMPTFOO_VERSION}",
            ]
            if codex:
                command.extend(
                    [
                        f"--package=@openai/codex-sdk@{CODEX_SDK_VERSION}",
                        f"--package=@openai/codex@{CODEX_SDK_VERSION}",
                    ]
                )
                if codex["cli_config"]["forced_login_method"] == "chatgpt":
                    verify_chatgpt_login(
                        command, directory, env, codex["cli_env"]["CODEX_HOME"]
                    )
            Path(env["PROMPTFOO_CONFIG_DIR"]).mkdir(parents=True, exist_ok=True)
            config_path = directory / "eval.json"
            config_path.write_text(json.dumps(config), encoding="utf-8")
            command.extend(
                [
                    "--",
                    "promptfoo",
                    "eval",
                    "--config",
                    str(config_path),
                    *forwarded_args(selected),
                ]
            )
            return subprocess.run(
                command, check=False, cwd=directory, env=env
            ).returncode
    except (OSError, subprocess.SubprocessError, ValueError, RuntimeError) as error:
        print(f"promptfoo runner: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
