from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src/agentsmesh"
FEATURE_DIRS = ("rules", "skills", "agents")


def stage_workspace(destination: Path) -> None:
    shutil.copy2(SOURCE / "agentsmesh.yaml", destination / "agentsmesh.yaml")
    canonical = destination / ".agentsmesh"
    canonical.mkdir()
    for name in FEATURE_DIRS:
        source = SOURCE / name
        if source.exists():
            shutil.copytree(source, canonical / name)


def agentsmesh_executable() -> Path:
    suffix = ".cmd" if os.name == "nt" else ""
    local = ROOT / "node_modules" / ".bin" / f"agentsmesh{suffix}"
    if local.exists():
        return local

    discovered = shutil.which("agentsmesh")
    if discovered:
        return Path(discovered)
    raise RuntimeError("agentsmesh executable not found; run npm ci first")


def run(command: str) -> None:
    if command not in {"lint", "check", "generate-check", "diff"}:
        raise ValueError(f"unsupported command: {command}")

    with TemporaryDirectory(prefix="mols-agentsmesh-") as temporary:
        workspace = Path(temporary)
        stage_workspace(workspace)
        executable = str(agentsmesh_executable())

        def invoke(*args: str) -> None:
            subprocess.run([executable, *args], cwd=workspace, check=True)

        if command == "lint":
            invoke("lint")
            return

        # Commands below need a projection to compare or inspect, but that projection
        # must stay outside the asset-library repository.
        invoke("generate")
        if command == "check":
            invoke("check")
        elif command == "generate-check":
            invoke("generate", "--check")
        else:
            invoke("diff")


if __name__ == "__main__":
    try:
        run(sys.argv[1] if len(sys.argv) == 2 else "")
    except (RuntimeError, ValueError, subprocess.CalledProcessError) as exc:
        raise SystemExit(str(exc)) from exc
