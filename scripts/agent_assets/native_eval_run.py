from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.agent_assets import promptfoo_run

ROOT = Path(__file__).resolve().parents[2]
PROFILES = {
    "mols-loops": (("mols-loops",), "mols-loops-native.yaml"),
    "asset-routing": (
        ("mols-agent-asset", "mols-agent-asset-find"),
        "agent-asset-routing-native.yaml",
    ),
}
CODEX_ENV_KEYS = ("CODEX_SKILLS_WORKING_DIR", "CODEX_EVAL_HOME")


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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Local Codex SDK Agent Skill eval")
    parser.add_argument("profile", choices=sorted(PROFILES))
    parser.add_argument("--repeat", type=int, default=1)
    args = parser.parse_args(argv)
    if args.repeat < 1:
        parser.error("--repeat must be a positive integer")

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

        workspace = temp_root / "workspace"
        workspace.mkdir()
        stage_skills(workspace, skills)
        prior = {key: os.environ.get(key) for key in CODEX_ENV_KEYS}
        os.environ["CODEX_SKILLS_WORKING_DIR"] = str(workspace)
        os.environ["CODEX_EVAL_HOME"] = str(home)
        try:
            return promptfoo_run.main(
                [
                    "eval",
                    "-c",
                    str(ROOT / "evals" / "promptfoo" / config),
                    "--repeat",
                    str(args.repeat),
                ]
            )
        finally:
            for key, value in prior.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value


if __name__ == "__main__":
    sys.exit(main())
