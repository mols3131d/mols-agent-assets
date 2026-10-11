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
    "mols-loops": (
        ("mols-loops",),
        "mols-loops-native.yaml",
    ),
    "asset-routing": (
        ("mols-agent-asset", "mols-agent-asset-find"),
        "agent-asset-routing-native.yaml",
    ),
}


def stage_skills(workspace: Path, skills: tuple[str, ...]) -> None:
    """Stage canonical packages, including references, without editing the source."""
    for name in skills:
        source = ROOT / "src" / "rulesync" / ".rulesync" / "skills" / name
        if not (source / "SKILL.md").is_file():
            raise FileNotFoundError(f"canonical Skill missing: {source}")
        shutil.copytree(source, workspace / ".agents" / "skills" / name)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Local Codex SDK Agent Skill eval")
    parser.add_argument("profile", choices=sorted(PROFILES))
    parser.add_argument("--repeat", type=int, default=1)
    args = parser.parse_args(argv)
    if args.repeat < 1:
        parser.error("--repeat must be a positive integer")

    skills, config = PROFILES[args.profile]
    staging_root = ROOT / ".tmp" / "native-agent-eval"
    staging_root.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=f"{args.profile}-", dir=staging_root) as temp:
        workspace = Path(temp)
        stage_skills(workspace, skills)
        prior = os.environ.get("CODEX_SKILLS_WORKING_DIR")
        os.environ["CODEX_SKILLS_WORKING_DIR"] = str(workspace)
        try:
            return promptfoo_run.main(
                ["eval", "-c", str(ROOT / "evals" / "promptfoo" / config), "--repeat", str(args.repeat)]
            )
        finally:
            if prior is None:
                os.environ.pop("CODEX_SKILLS_WORKING_DIR", None)
            else:
                os.environ["CODEX_SKILLS_WORKING_DIR"] = prior


if __name__ == "__main__":
    sys.exit(main())
