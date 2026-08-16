#!/usr/bin/env python3
"""Validate and package a skill as ZIP, including docs/."""

from __future__ import annotations

import argparse
import subprocess
import sys
import zipfile
from pathlib import Path

EXCLUDED_PARTS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".git"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    root = args.skill.resolve()
    validator = Path(__file__).resolve().parent / "validate_skill.py"
    result = subprocess.run([sys.executable, str(validator), str(root)], check=False)
    if result.returncode:
        return result.returncode

    if not (root / "docs").is_dir():
        print("error: docs/ must be packaged", file=sys.stderr)
        return 2

    args.output.mkdir(parents=True, exist_ok=True)
    archive = args.output / f"{root.name}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(root.rglob("*")):
            if path.is_dir():
                continue
            relative = path.relative_to(root.parent)
            if any(part in EXCLUDED_PARTS for part in relative.parts):
                continue
            if path.suffix in EXCLUDED_SUFFIXES or path == archive:
                continue
            zf.write(path, relative.as_posix())

    print(archive)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
