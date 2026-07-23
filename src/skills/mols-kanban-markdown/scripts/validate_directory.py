#!/usr/bin/env python3
"""Validate Kanban directory integrity."""

from __future__ import annotations

import sys
from pathlib import Path


def validate_directory_integrity(kanban_path: str) -> list[str]:
    """Validate directory integrity of Kanban workspace."""
    errors = []
    path = Path(kanban_path).resolve()

    # Check root directory
    if not path.is_dir():
        errors.append(f"Root path '{path}' does not exist or is not a directory.")
        return errors

    # Check essential folders
    required_dirs = [
        path / ".configs",
        path / "backlog",
        path / "active",
        path / "archive",
    ]
    for rd in required_dirs:
        if not rd.is_dir():
            errors.append(
                f"Required sub-directory '{rd.relative_to(path.parent)}' is missing."
            )

    # Check essential configuration files
    required_files = [
        path / ".configs" / "config.jsonc",
        path / ".configs" / "template.md",
        path / "AGENTS.md",
    ]
    for rf in required_files:
        if not rf.is_file():
            rel = rf.relative_to(path.parent)
            errors.append(f"Required configuration file '{rel}' is missing.")

    return errors


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python validate_directory.py <kanban_path>", file=sys.stderr)
        sys.exit(1)

    errors = validate_directory_integrity(sys.argv[1])
    if errors:
        print("Directory integrity validation failed:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("Kanban directory integrity is valid!")
        sys.exit(0)


if __name__ == "__main__":
    main()
