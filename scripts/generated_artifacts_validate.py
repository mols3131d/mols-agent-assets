#!/usr/bin/env python3
"""Validate committed generated projections without modifying repository files."""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections.abc import Callable, Iterable
from pathlib import Path

from scripts import generated_artifacts_sync as sync
from scripts import docs_indexes_generate
from scripts.agent_assets import routes_distribution_generate as distribution_routes
from scripts.agent_assets import routes_repository_generate as repository_routes

ROOT = sync.ROOT
LOCAL_PROJECTION_NAMES = frozenset({"docs-indexes", "distribution-routes"})
Checker = Callable[[], list[str]]


def _first_line_difference(current: str, expected: str) -> tuple[int, str, str] | None:
    current_lines = current.splitlines()
    expected_lines = expected.splitlines()
    for index in range(max(len(current_lines), len(expected_lines))):
        current_line = current_lines[index] if index < len(current_lines) else "<missing>"
        expected_line = expected_lines[index] if index < len(expected_lines) else "<missing>"
        if current_line != expected_line:
            return index + 1, current_line, expected_line
    return None


def compare_outputs(
    expected: dict[Path, str],
    output_matches: Callable[[str], bool],
    root: Path = ROOT,
    *,
    show_first_difference: bool = False,
) -> list[str]:
    """Compare expected generated files with committed outputs without writing them."""
    expected_by_path = {
        path.relative_to(root).as_posix(): content for path, content in expected.items()
    }
    drift: list[str] = []

    for relative, content in sorted(expected_by_path.items()):
        path = root / relative
        if not path.exists():
            drift.append(f"missing: {relative}")
            continue

        current = path.read_text(encoding="utf-8")
        if current == content:
            continue

        drift.append(f"outdated: {relative}")
        if show_first_difference:
            difference = _first_line_difference(current, content)
            if difference is not None:
                line, current_line, expected_line = difference
                drift.append(f"line {line} current: {current_line}")
                drift.append(f"line {line} expected: {expected_line}")

    existing = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and output_matches(path.relative_to(root).as_posix())
    }
    for relative in sorted(existing - expected_by_path.keys()):
        drift.append(f"stale: {relative}")

    return drift


def check_docs_indexes() -> list[str]:
    return compare_outputs(
        docs_indexes_generate.expected_docs_indexes(),
        sync._is_docs_index_output,
        show_first_difference=True,
    )


def check_distribution_routes() -> list[str]:
    return compare_outputs(
        distribution_routes.generate(),
        sync._is_distribution_route_output,
    )


def check_repository_routes() -> list[str]:
    return compare_outputs(
        repository_routes.generate(),
        sync._is_repository_route_output,
    )


CHECKERS: dict[str, Checker] = {
    "docs-indexes": check_docs_indexes,
    "distribution-routes": check_distribution_routes,
    "repository-routes": check_repository_routes,
}


def changed_paths(
    base: str,
    head: str = "HEAD",
    root: Path = ROOT,
) -> set[str] | None:
    """Return changed paths, or None when impact cannot be determined safely."""
    result = subprocess.run(
        [
            "git",
            "diff",
            "--name-only",
            "--no-renames",
            "--diff-filter=ACMRD",
            "-z",
            base,
            head,
            "--",
        ],
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        return None
    return {
        item.decode("utf-8", errors="surrogateescape")
        for item in result.stdout.split(b"\0")
        if item
    }


def select_for_validation(
    paths: Iterable[str] | None,
    *,
    local_only: bool = False,
    projections: tuple[sync.Projection, ...] = sync.PROJECTIONS,
) -> tuple[sync.Projection, ...]:
    """Select affected projections, falling back to all when impact is unknown."""
    selected = projections if paths is None else sync.select_projections(paths, projections)
    if local_only:
        selected = tuple(
            projection
            for projection in selected
            if projection.name in LOCAL_PROJECTION_NAMES
        )
    return selected


def validate(
    projections: Iterable[sync.Projection],
    checkers: dict[str, Checker] = CHECKERS,
) -> int:
    failed = False
    drift_found = False
    selected = tuple(projections)

    if not selected:
        print("No generated projections affected.")
        return 0

    for projection in selected:
        checker = checkers[projection.name]
        try:
            drift = checker()
        except Exception as exc:  # noqa: BLE001 - report projection failures uniformly
            failed = True
            print(f"FAIL {projection.name}: {exc}", file=sys.stderr)
            continue

        if drift:
            failed = True
            drift_found = True
            print(f"FAIL {projection.name}", file=sys.stderr)
            for item in drift:
                print(f"  {item}", file=sys.stderr)
        else:
            print(f"PASS {projection.name}")

    if drift_found:
        print("Regenerate committed projections with: mise run generated-sync", file=sys.stderr)

    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--local-only",
        action="store_true",
        help="Validate only network-free docs-index and distribution-route projections.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        dest="all_projections",
        help="Validate all selected projection owners explicitly.",
    )
    parser.add_argument(
        "--changed-from",
        metavar="REV",
        help="Validate projections affected by git changes from REV to HEAD.",
    )
    args = parser.parse_args(argv)

    if args.all_projections and args.changed_from:
        parser.error("--all and --changed-from cannot be used together")

    paths: set[str] | None
    if args.changed_from:
        paths = changed_paths(args.changed_from)
        if paths is None:
            print(
                f"WARN unable to resolve changes from {args.changed_from}; validating all projections.",
                file=sys.stderr,
            )
    else:
        paths = None

    projections = select_for_validation(paths, local_only=args.local_only)
    return validate(projections)


if __name__ == "__main__":
    raise SystemExit(main())
