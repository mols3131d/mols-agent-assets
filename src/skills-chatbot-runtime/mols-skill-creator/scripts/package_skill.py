#!/usr/bin/env python3
"""Validate and package a Skill runtime payload with explicit non-runtime exclusions."""

from __future__ import annotations

import argparse
import subprocess
import sys
import zipfile
from pathlib import Path

EXCLUDED_DIRS = {
    ".docs",
    ".evals",
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".svn",
    ".tests",
    ".venv",
    "__pycache__",
    "evals",
    "node_modules",
}
EXCLUDED_FILES = {".DS_Store"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def in_excluded_dir(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    return any(part in EXCLUDED_DIRS for part in relative.parts[:-1])


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
            if in_excluded_dir(path, root):
                continue
            relative_to_package = path.relative_to(root)
            if path.name in EXCLUDED_FILES:
                continue
            if path.suffix in EXCLUDED_SUFFIXES or path == archive:
                continue
            relative = path.relative_to(root.parent)
            zf.write(path, relative.as_posix())

    print(archive)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
