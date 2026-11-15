"""Read-only lint and formatting checks for selected repository sources."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from collections.abc import Callable, Iterable
from pathlib import Path

from scripts.changed_files_format import BIOME_SUFFIXES, select_paths

ROOT = Path(__file__).resolve().parents[1]
QUALITY_SUFFIXES = BIOME_SUFFIXES | {".py", ".md"}
CommandRunner = Callable[[list[str], Path], int]


def _git_paths(root: Path, *args: str) -> tuple[str, ...]:
    result = subprocess.run(
        ["git", *args, "-z", "--"],
        cwd=root,
        capture_output=True,
        check=True,
    )
    paths = {
        name.decode("utf-8", errors="surrogateescape")
        for name in result.stdout.split(b"\0")
        if name
    }
    return tuple(sorted(paths))


def _check_source_paths(paths: tuple[str, ...], root: Path) -> tuple[str, ...]:
    for path in paths:
        if Path(path).suffix.lower() not in QUALITY_SUFFIXES:
            continue
        source = root / path
        if source.is_symlink() or not source.is_file():
            raise ValueError(f"Cannot inspect selected source: {path}")
    return paths


def changed_paths(base: str, root: Path = ROOT) -> tuple[str, ...]:
    """Inspect the complete committed range; never silently skip a missing base."""
    return _check_source_paths(
        _git_paths(
            root,
            "diff",
            "--name-only",
            "--no-renames",
            "--diff-filter=ACMRT",
            base,
            "HEAD",
        ),
        root,
    )


def staged_paths(root: Path = ROOT) -> tuple[str, ...]:
    """Only inspect staged content when the corresponding worktree file is identical."""
    staged = _git_paths(
        root, "diff", "--cached", "--name-only", "--no-renames", "--diff-filter=ACMRT"
    )
    unstaged = set(_git_paths(root, "diff", "--name-only", "--no-renames"))
    conflicts = sorted(
        path
        for path in staged
        if path in unstaged and Path(path).suffix.lower() in QUALITY_SUFFIXES
    )
    if conflicts:
        raise ValueError(
            "Staged source also has unstaged changes; "
            f"stage or separate before checking: {', '.join(conflicts)}"
        )
    return _check_source_paths(staged, root)


def all_paths(root: Path = ROOT) -> tuple[str, ...]:
    return _check_source_paths(_git_paths(root, "ls-files"), root)


def checks_for_paths(paths: Iterable[str]) -> list[tuple[str, list[str]]]:
    names = tuple(paths)
    python = select_paths(names, {".py"})
    markdown = select_paths(names, {".md"})
    biome = select_paths(names, BIOME_SUFFIXES)

    checks: list[tuple[str, list[str]]] = []
    if python:
        checks.extend(
            [
                ("Ruff lint", ["ruff", "check", *python]),
                ("Ruff format", ["ruff", "format", "--check", *python]),
            ]
        )
    if markdown:
        checks.extend(
            [
                ("rumdl lint", ["rumdl", "check", *markdown]),
                ("rumdl format", ["rumdl", "fmt", "--check", *markdown]),
            ]
        )
    if biome:
        checks.extend(
            [
                ("Biome lint", ["biome", "lint", "--no-errors-on-unmatched", *biome]),
                (
                    "Biome format",
                    ["biome", "format", "--no-errors-on-unmatched", *biome],
                ),
            ]
        )
    return checks


def _run(command: list[str], root: Path) -> int:
    executable = shutil.which(command[0])
    if executable is None:
        raise FileNotFoundError(f"Required source quality tool not found: {command[0]}")
    return subprocess.run([executable, *command[1:]], cwd=root, check=False).returncode


def verify(
    paths: Iterable[str], root: Path = ROOT, runner: CommandRunner = _run
) -> int:
    checks = checks_for_paths(paths)
    if not checks:
        print("No supported source files affected.")
        return 0

    failed = False
    for name, command in checks:
        print(f"CHECK {name}", flush=True)
        try:
            result = runner(command, root)
        except OSError as exc:
            print(f"ERROR {name}: {exc}", file=sys.stderr)
            return 2
        if result != 0:
            failed = True
            print(f"FAIL {name} (exit {result})", file=sys.stderr)
            if name == "Ruff format":
                print("DIFF Ruff format", flush=True)
                runner(["ruff", "format", "--diff", *command[3:]], root)
    return 1 if failed else 0


def main(argv: list[str] | None = None, root: Path = ROOT) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--changed-from", metavar="BASE")
    scope.add_argument("--staged", action="store_true")
    scope.add_argument("--all", action="store_true")
    args = parser.parse_args(argv)

    try:
        if args.staged:
            paths = staged_paths(root)
        elif args.all:
            paths = all_paths(root)
        else:
            paths = changed_paths(args.changed_from, root)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"ERROR source selection: {exc}", file=sys.stderr)
        return 2

    return verify(paths, root)


if __name__ == "__main__":
    raise SystemExit(main())
