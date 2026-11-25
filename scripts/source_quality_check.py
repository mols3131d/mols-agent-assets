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


def _git_records(root: Path, *args: str) -> tuple[str, ...]:
    result = subprocess.run(
        ["git", *args, "-z", "--"],
        cwd=root,
        capture_output=True,
        check=True,
    )
    return tuple(
        record.decode("utf-8", errors="surrogateescape")
        for record in result.stdout.split(b"\0")
        if record
    )


def _diff_entries(root: Path, *args: str) -> tuple[tuple[str, str], ...]:
    records = iter(
        _git_records(root, "diff", "--raw", "--no-renames", "--diff-filter=ACMT", *args)
    )
    # With -z and rename detection disabled, the path follows its raw diff header.
    return tuple(
        (path, header.split()[1]) for header, path in zip(records, records, strict=True)
    )


def _check_source_paths(
    entries: Iterable[tuple[str, str]], root: Path
) -> tuple[str, ...]:
    paths = []
    for path, mode in entries:
        if Path(path).suffix.lower() not in QUALITY_SUFFIXES:
            continue
        source = root / path
        if (
            mode not in {"100644", "100755"}
            or source.is_symlink()
            or not source.is_file()
        ):
            raise ValueError(f"Cannot inspect selected source: {path}")
        paths.append(path)
    return tuple(sorted(paths))


def changed_paths(base: str, root: Path = ROOT) -> tuple[str, ...]:
    """Inspect the complete committed range; never silently skip a missing base."""
    return _check_source_paths(_diff_entries(root, base, "HEAD"), root)


def _merge_parents(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "rev-parse", "--git-path", "MERGE_HEAD"],
        cwd=root,
        capture_output=True,
        check=True,
    )
    path = root / result.stdout.decode("utf-8", errors="surrogateescape").rstrip("\r\n")
    try:
        return path.read_text(encoding="ascii").splitlines()
    except FileNotFoundError:
        return []


def staged_paths(root: Path = ROOT) -> tuple[str, ...]:
    """Only inspect staged content when the corresponding worktree file is identical."""
    staged = _diff_entries(root, "--cached")
    for parent in _merge_parents(root):
        parent_changes = set(_diff_entries(root, "--cached", parent))
        staged = tuple(entry for entry in staged if entry in parent_changes)
    unstaged = set(_git_records(root, "diff", "--name-only", "--no-renames"))
    conflicts = sorted(
        path
        for path, _ in staged
        if path in unstaged and Path(path).suffix.lower() in QUALITY_SUFFIXES
    )
    if conflicts:
        raise ValueError(
            "Staged source also has unstaged changes; "
            f"stage or separate before checking: {', '.join(conflicts)}"
        )
    return _check_source_paths(staged, root)


def all_paths(root: Path = ROOT) -> tuple[str, ...]:
    entries = []
    for record in _git_records(root, "ls-files", "--format=%(objectmode) %(path)"):
        mode, path = record.split(" ", 1)
        entries.append((path, mode))
    return _check_source_paths(entries, root)


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
                ("Ruff format", ["ruff", "format", "--diff", *python]),
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
    tool, *args = command
    executable = shutil.which(tool)
    if executable is None:
        raise FileNotFoundError(f"Required source quality tool not found: {tool}")
    if tool == "biome" and Path(executable).suffix.lower() in {".bat", ".cmd"}:
        # npm batch wrappers allow cmd.exe to expand characters in source filenames.
        package_bin = (
            Path(executable).parent.parent / "@biomejs" / "biome" / "bin" / "biome"
        )
        node = shutil.which("node.exe")
        if node is None or not package_bin.is_file():
            raise FileNotFoundError(
                "Required Node.js or npm Biome entry point not found"
            )
        executable = node
        args.insert(0, str(package_bin))
    return subprocess.run([executable, *args], cwd=root, check=False).returncode


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
