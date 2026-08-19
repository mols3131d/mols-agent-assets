from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT / "src" / "rulesync"
RULESYNC_VERSION = "16.14.0"


def rulesync_command() -> list[str]:
    local = ROOT / "node_modules" / ".bin" / ("rulesync.cmd" if sys.platform == "win32" else "rulesync")
    if local.is_file():
        return [str(local)]

    npx = shutil.which("npx")
    if npx is None:
        raise RuntimeError("npx is required to run the pinned Rulesync toolchain")
    return [npx, "--yes", f"rulesync@{RULESYNC_VERSION}"]


def run(args: list[str], cwd: Path) -> None:
    subprocess.run([*rulesync_command(), *args], cwd=cwd, check=True)


def doctor() -> None:
    run(["doctor", "--strict"], WORKSPACE)


def preview() -> None:
    run(["generate", "--dry-run"], WORKSPACE)


def validate() -> None:
    with tempfile.TemporaryDirectory(prefix="rulesync-validate-") as temp_dir:
        workspace = Path(temp_dir) / "rulesync"
        shutil.copytree(WORKSPACE, workspace)
        run(["doctor", "--strict"], workspace)
        run(["generate"], workspace)
        run(["generate", "--check"], workspace)


def main() -> None:
    commands = {
        "doctor": doctor,
        "preview": preview,
        "validate": validate,
    }
    if len(sys.argv) != 2 or sys.argv[1] not in commands:
        expected = "|".join(commands)
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} <{expected}>")
    commands[sys.argv[1]]()


if __name__ == "__main__":
    main()
