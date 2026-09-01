from __future__ import annotations

import shutil
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "src" / "rulesync"


def rulesync_command() -> list[str]:
    rulesync = shutil.which("rulesync")
    if rulesync is None:
        raise RuntimeError("rulesync is required; install repository tools with mise")
    return [rulesync]


def run(args: list[str], cwd: Path) -> None:
    subprocess.run([*rulesync_command(), *args], cwd=cwd, check=True)


def doctor(args: list[str]) -> None:
    run(["doctor", "--strict", *args], WORKSPACE)


def preview(args: list[str]) -> None:
    run(["generate", "--dry-run", *args], WORKSPACE)


def main() -> None:
    commands: dict[str, Callable[[list[str]], None]] = {
        "doctor": doctor,
        "preview": preview,
    }
    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        expected = "|".join(commands)
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} <{expected}> [rulesync args...]")

    commands[sys.argv[1]](sys.argv[2:])


if __name__ == "__main__":
    main()
