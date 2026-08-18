#!/usr/bin/env python3
"""Validate and package a skill runtime payload, excluding non-runtime dot directories."""

from __future__ import annotations

import argparse
import subprocess
import sys
import zipfile
from pathlib import Path

EXCLUDED_PARTS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".git"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def in_non_runtime_dot_dir(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    return any(part.startswith(".") for part in relative.parts[:-1])


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

    args.output.mkdir(parents=True, exist_ok=True)
    archive = args.output / f"{root.name}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(root.rglob("*")):
            if path.is_dir():
                continue
            if in_non_runtime_dot_dir(path, root):
                continue
            relative_to_package = path.relative_to(root)
            if any(part in EXCLUDED_PARTS for part in relative_to_package.parts):
                continue
            if path.suffix in EXCLUDED_SUFFIXES or path == archive:
                continue
            relative = path.relative_to(root.parent)
            zf.write(path, relative.as_posix())

    print(archive)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
