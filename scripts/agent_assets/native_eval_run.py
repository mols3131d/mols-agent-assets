from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.agent_assets import promptfoo_run

ROOT = Path(__file__).resolve().parents[2]
PROFILES = {
    "mols-loops": (("mols-loops", "mols-agent-asset"), "mols-loops-native.yaml"),
    "asset-routing": (
        ("mols-agent-asset", "mols-agent-asset-find"),
        "agent-asset-routing-native.yaml",
    ),
}
CODEX_ENV_KEYS = ("CODEX_SKILLS_WORKING_DIR", "CODEX_EVAL_HOME")
CODEX_SDK_VERSION = "0.156.1"


def stage_skills(workspace: Path, skills: tuple[str, ...]) -> None:
    """Stage canonical packages with references, leaving source untouched."""
    for name in skills:
        source = ROOT / "src" / "rulesync" / ".rulesync" / "skills" / name
        if not (source / "SKILL.md").is_file():
            raise FileNotFoundError(f"canonical Skill missing: {source}")
        shutil.copytree(source, workspace / ".agents" / "skills" / name)


def resolve_codex_home(temp: Path, env: dict[str, str]) -> Path:
    """Avoid personal Skills/config in baseline measurements."""
    configured = env.get("CODEX_EVAL_HOME")
    if configured and (env.get("OPENAI_API_KEY") or env.get("CODEX_API_KEY")):
        raise ValueError(
            "CODEX_EVAL_HOME cannot be combined with API keys; unset "
            "OPENAI_API_KEY and CODEX_API_KEY for a login-based eval"
        )
    if configured:
        path = Path(configured).expanduser().resolve()
        if not path.is_dir():
            raise ValueError(f"CODEX_EVAL_HOME is not a directory: {path}")
        return path
    if not (env.get("OPENAI_API_KEY") or env.get("CODEX_API_KEY")):
        raise ValueError(
            "Native Eval needs OPENAI_API_KEY/CODEX_API_KEY or an explicit "
            "CODEX_EVAL_HOME with authenticated Codex login"
        )
    path = temp / "codex-home"
    path.mkdir()
    return path


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def package_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    for file in sorted(item for item in path.rglob("*") if item.is_file()):
        digest.update(file.relative_to(path).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(file.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def git_head() -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def write_manifest(
    output: Path,
    profile: str,
    suite: str,
    repeat: int,
    skills: tuple[str, ...],
    config: str,
    workspace: Path,
    auth_mode: str,
    exit_code: int,
) -> None:
    """Record comparable inputs without serializing credentials or home paths."""
    manifest = {
        "schema_version": 1,
        "profile": profile,
        "suite": suite,
        "repeat": repeat,
        "git_head": git_head(),
        "model": os.environ.get("CODEX_EVAL_MODEL", "gpt-5.5"),
        "auth_mode": auth_mode,
        "promptfoo_version": promptfoo_run.PROMPTFOO_VERSION,
        "codex_sdk_version": CODEX_SDK_VERSION,
        "config_sha256": file_sha256(ROOT / "evals" / "promptfoo" / config),
        "fixture_sha256": {
            name: file_sha256(ROOT / "evals" / "skills" / name / "cases.json")
            for name in skills
            if (ROOT / "evals" / "skills" / name / "cases.json").is_file()
        },
        "skill_package_sha256": {
            name: package_sha256(workspace / ".agents" / "skills" / name)
            for name in skills
        },
        "runner_sha256": file_sha256(Path(__file__)),
        "adapter_sha256": file_sha256(
            ROOT / "scripts" / "agent_assets" / "skills_promptfoo.py"
        ),
        "grader_provider_sha256": (
            hashlib.sha256(
                promptfoo_run.build_env()["PROMPTFOO_GRADER_PROVIDER"].encode("utf-8")
            ).hexdigest()
            if suite != "trigger"
            else None
        ),
        "result_sha256": file_sha256(output),
        "runner_exit_code": exit_code,
        "evidence_scope": (
            "skill-file-read-heuristic"
            if suite == "trigger"
            else "response-only" if suite == "behavior" else "mixed"
        ),
    }
    output.with_name(output.name + ".manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Local Codex SDK Agent Skill eval")
    parser.add_argument("profile", choices=sorted(PROFILES))
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--suite", choices=("all", "trigger", "behavior"), default="all")
    parser.add_argument("--output", help="Optional persistent local JSON/CSV eval evidence")
    args = parser.parse_args(argv)
    if args.repeat < 1:
        parser.error("--repeat must be a positive integer")
    if args.profile == "asset-routing" and args.suite == "behavior":
        parser.error("asset-routing profile supports trigger only")

    effective_suite = "trigger" if args.profile == "asset-routing" else args.suite
    skills, config = PROFILES[args.profile]
    # Outside the repository: root AGENTS.md and installed project Skills
    # cannot accidentally influence an otherwise isolated measurement.
    with TemporaryDirectory(prefix=f"native-{args.profile}-") as temp:
        temp_root = Path(temp)
        try:
            home = resolve_codex_home(temp_root, os.environ)
        except ValueError as error:
            print(f"native eval: {error}", file=sys.stderr)
            return 2

        output = Path(args.output).expanduser().resolve() if args.output else None
        if output is not None:
            output.parent.mkdir(parents=True, exist_ok=True)
        previous_mtime = (
            output.stat().st_mtime_ns if output is not None and output.is_file() else None
        )

        workspace = temp_root / "workspace"
        workspace.mkdir()
        stage_skills(workspace, skills)
        prior = {key: os.environ.get(key) for key in CODEX_ENV_KEYS}
        os.environ["CODEX_SKILLS_WORKING_DIR"] = str(workspace)
        os.environ["CODEX_EVAL_HOME"] = str(home)
        try:
            command = [
                "eval",
                "-c",
                str(ROOT / "evals" / "promptfoo" / config),
                "--repeat",
                str(args.repeat),
            ]
            if effective_suite != "all":
                name = "native-trigger" if effective_suite == "trigger" else "behavior"
                command.extend(["--filter-metadata", f"suite={name}"])
            if output is not None:
                command.extend(["-o", str(output)])
            exit_code = promptfoo_run.main(
                command,
                extra_packages=(f"@openai/codex-sdk@{CODEX_SDK_VERSION}",),
            )
            if output is not None:
                if not output.is_file() or (
                    previous_mtime is not None
                    and output.stat().st_mtime_ns == previous_mtime
                ):
                    if exit_code == 0:
                        print("native eval: requested output was not written or refreshed", file=sys.stderr)
                        return 2
                else:
                    write_manifest(
                        output,
                        args.profile,
                        effective_suite,
                        args.repeat,
                        skills,
                        config,
                        workspace,
                        "explicit-home" if prior["CODEX_EVAL_HOME"] else "api-key",
                        exit_code,
                    )
            return exit_code
        finally:
            for key, value in prior.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value


if __name__ == "__main__":
    sys.exit(main())
