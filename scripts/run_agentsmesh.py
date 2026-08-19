from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT / "src" / "agentsmesh"
COMMANDS = frozenset({"lint", "preview", "validate"})


def agentsmesh_executable() -> Path:
    suffix = ".cmd" if os.name == "nt" else ""
    local = ROOT / "node_modules" / ".bin" / f"agentsmesh{suffix}"
    if local.exists():
        return local

    discovered = shutil.which("agentsmesh")
    if discovered:
        return Path(discovered)
    raise RuntimeError("agentsmesh executable not found; run npm ci first")


def invoke(workspace: Path, *args: str) -> None:
    subprocess.run([str(agentsmesh_executable()), *args], cwd=workspace, check=True)


def run(command: str) -> None:
    if command not in COMMANDS:
        raise ValueError(f"unsupported command: {command}")

    if command == "lint":
        invoke(WORKSPACE, "lint")
        return

    if command == "preview":
        invoke(WORKSPACE, "diff")
        return

    # The source is already a native AgentsMesh workspace. Copy it verbatim only
    # for write-producing validation so generated target projections and lock state
    # never become repository files.
    with TemporaryDirectory(prefix="mols-agentsmesh-") as temporary:
        workspace = Path(temporary) / "workspace"
        shutil.copytree(WORKSPACE, workspace)
        invoke(workspace, "generate")
        invoke(workspace, "generate", "--check")
        invoke(workspace, "check")


if __name__ == "__main__":
    try:
        run(sys.argv[1] if len(sys.argv) == 2 else "")
    except (RuntimeError, ValueError, subprocess.CalledProcessError) as exc:
        raise SystemExit(str(exc)) from exc
