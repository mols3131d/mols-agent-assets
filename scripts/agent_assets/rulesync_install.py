"""Install frozen Rulesync sources with LF clones without replacing Git credentials."""

from __future__ import annotations

import os
import shutil
import subprocess
from collections.abc import Mapping
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def git_lf_environment(parent: Mapping[str, str]) -> dict[str, str]:
    """Append LF checkout configuration after any inherited counted Git settings."""
    env = dict(parent)
    count = int(env.get("GIT_CONFIG_COUNT", "0"))
    if count < 0:
        raise ValueError("GIT_CONFIG_COUNT must not be negative")
    env[f"GIT_CONFIG_KEY_{count}"] = "core.autocrlf"
    env[f"GIT_CONFIG_VALUE_{count}"] = "false"
    env["GIT_CONFIG_COUNT"] = str(count + 1)
    return env


def main() -> None:
    rulesync = shutil.which("rulesync")
    if rulesync is None:
        raise SystemExit("rulesync was not found; run mise install first")
    subprocess.run(
        [rulesync, "install", "--frozen"],
        check=True,
        cwd=ROOT,
        env=git_lf_environment(os.environ),
    )


if __name__ == "__main__":
    main()
