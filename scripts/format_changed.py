#!/usr/bin/env python3
"""Format modified and untracked repository files without touching unrelated files."""

from __future__ import annotations

import subprocess
from collections.abc import Iterable
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIOME_SUFFIXES = {
    ".json",
    ".jsonc",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".mjs",
    ".cjs",
    ".mts",
    ".cts",
}


def _git_paths(root: Path, *args: str) -> set[str]:
    result = subprocess.run(
        ["git", *args, "-z", "--"],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
    )
    return {
        item.decode("utf-8", errors="surrogateescape")
        for item in result.stdout.split(b"\0")
        if item
    }


def changed_paths(root: Path = ROOT) -> tuple[str, ...]:
    changed = _git_paths(
        root,
        "diff",
        "HEAD",
        "--name-only",
        "--no-renames",
        "--diff-filter=ACMR",
    )
    changed |= _git_paths(root, "ls-files", "--others", "--exclude-standard")
    return tuple(sorted(path for path in changed if (root / path).is_file()))


def select_paths(paths: Iterable[str], suffixes: set[str]) -> list[str]:
    return [f"./{path}" for path in paths if Path(path).suffix.lower() in suffixes]


def _run(root: Path, *args: str) -> None:
    subprocess.run(args, cwd=root, check=True)


def format_changed(root: Path = ROOT) -> tuple[str, ...]:
    paths = changed_paths(root)
    python = select_paths(paths, {".py"})
    markdown = select_paths(paths, {".md"})
    biome = select_paths(paths, BIOME_SUFFIXES)

    if python:
        _run(root, "ruff", "format", *python)
        _run(root, "ruff", "check", "--fix", *python)
    if markdown:
        _run(root, "rumdl", "fmt", *markdown)
        _run(root, "rumdl", "check", "--fix", *markdown)
    if biome:
        _run(root, "biome", "format", "--write", *biome)

    return paths


def main() -> None:
    paths = format_changed()
    print(f"formatted changed files: {len(paths)}")


if __name__ == "__main__":
    main()
