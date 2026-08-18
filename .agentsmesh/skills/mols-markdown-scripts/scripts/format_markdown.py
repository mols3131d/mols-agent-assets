#!/usr/bin/env python3
# /// script
# dependencies = [
#   "rumdl>=0.2.6",
# ]
# ///
"""Format markdown files using rumdl."""

from __future__ import annotations

import shlex
import subprocess
from pathlib import Path


def format_markdown(file_paths: Path | list[Path], executable: str = "rumdl") -> bool:
    """Format markdown files using the specified formatting executable.

    Args:
        file_paths: Single Path or list of Paths to format.
        executable: Command or path to the formatter binary.

    Returns:
        True if formatting succeeded, otherwise False.
    """
    paths = [file_paths] if isinstance(file_paths, Path) else list(file_paths)
    if not paths or any(not p.is_file() for p in paths):
        return False

    try:
        cmd = shlex.split(executable) + ["fmt"] + [str(p) for p in paths]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def main() -> None:
    """CLI execution entrypoint."""
    import sys

    args = sys.argv[1:]
    if not args:
        print("Usage: format_markdown.py <file1.md> [file2.md ...]")
        sys.exit(1)

    paths = [Path(arg) for arg in args]
    success = format_markdown(paths)
    if success:
        print("Formatting succeeded for all files.")
        sys.exit(0)
    else:
        print("Formatting failed or some files do not exist.")
        sys.exit(1)


if __name__ == "__main__":
    main()
