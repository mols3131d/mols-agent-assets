#!/usr/bin/env python3
# /// script
# dependencies = [
#   "rumdl>=0.2.6",
# ]
# ///
"""Validate markdown links using rumdl check command."""

from __future__ import annotations

import shlex
import subprocess
from pathlib import Path


def validate_links(file_paths: Path | list[Path], executable: str = "rumdl") -> bool:
    """Validate markdown links temporarily using rumdl CLI check command.

    Args:
        file_paths: Single Path or list of Paths to check.
        executable: Command or path to the rumdl binary.

    Returns:
        True if all links are valid, otherwise False.
    """
    paths = [file_paths] if isinstance(file_paths, Path) else list(file_paths)
    if not paths or any(not p.is_file() for p in paths):
        return False

    try:
        # Override rules temporarily via CLI arguments
        cmd = (
            shlex.split(executable)
            + ["check"]
            + [
                "--config",
                "MD051.enabled = true",
                "--config",
                "MD052.enabled = true",
            ]
            + [str(p) for p in paths]
        )
        subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def main() -> None:
    """CLI execution entrypoint."""
    import sys

    args = sys.argv[1:]
    if not args:
        print("Usage: validate_links.py <file1.md> [file2.md ...]")
        sys.exit(1)

    paths = [Path(arg) for arg in args]
    success = validate_links(paths)
    if success:
        print("All markdown links are valid.")
        sys.exit(0)
    else:
        print("Link validation failed or some files do not exist.")
        sys.exit(1)


if __name__ == "__main__":
    main()
