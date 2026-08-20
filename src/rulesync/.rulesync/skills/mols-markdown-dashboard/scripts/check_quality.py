#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "scripts" / "render_dashboard.py"


@dataclass(frozen=True, slots=True)
class Check:
    name: str
    command: tuple[str, ...]


def main() -> int:
    checks = (
        Check("Ruff lint", ("ruff", "check", ".")),
        Check("Ruff format", ("ruff", "format", "--check", ".")),
        Check("ty", ("ty", "check")),
        Check("rumdl", ("rumdl", "check", ".")),
        Check("Python compile", (sys.executable, "-m", "compileall", "-q", "src", "scripts")),
    )

    for check in checks:
        result = _run(check)
        if result:
            return result

    return _check_rendered_examples()


def _run(check: Check) -> int:
    executable = check.command[0]
    if executable != sys.executable and shutil.which(executable) is None:
        print(
            f"missing quality tool: {executable}; provide it in the active environment",
            file=sys.stderr,
        )
        return 127

    print(f"==> {check.name}")
    return subprocess.run(check.command, cwd=ROOT, check=False).returncode


def _check_rendered_examples() -> int:
    print("==> rendered example drift")
    with tempfile.TemporaryDirectory(prefix="mols-dashboard-") as temporary:
        temp_dir = Path(temporary)
        for source in sorted((ROOT / "examples").glob("*-dashboard.yml")):
            expected = source.with_suffix(".md")
            actual = temp_dir / expected.name
            result = subprocess.run(
                (
                    sys.executable,
                    str(RENDERER),
                    "render",
                    str(source),
                    "-o",
                    str(actual),
                ),
                cwd=ROOT,
                check=False,
            )
            if result.returncode:
                return result.returncode
            if actual.read_text(encoding="utf-8") != expected.read_text(
                encoding="utf-8"
            ):
                print(f"generated example is stale: {expected}", file=sys.stderr)
                return 1

    print("rendered examples are current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
