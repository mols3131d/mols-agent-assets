#!/usr/bin/env python3
"""Sync or validate committed repository projections through one CLI."""

from __future__ import annotations

import argparse
import sys

from scripts import generated_artifacts_sync as sync
from scripts import generated_artifacts_validate as validation


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    sync_command = commands.add_parser("sync", help="Regenerate committed projections")
    sync_command.add_argument(
        "--staged",
        action="store_true",
        help="Regenerate staged-impact projections and stage their outputs",
    )

    validate_command = commands.add_parser(
        "validate", help="Check committed projections without writing"
    )
    validate_command.add_argument(
        "--local-only",
        action="store_true",
        help="Limit checks to local indexes and distribution routes",
    )
    impact = validate_command.add_mutually_exclusive_group()
    impact.add_argument("--all", action="store_true", help="Check all projections")
    impact.add_argument(
        "--changed-from", metavar="REV", help="Check changes from REV to HEAD"
    )

    args = parser.parse_args(argv)
    if args.command == "sync":
        try:
            names = sync.sync_staged() if args.staged else sync.sync_all()
        except sync.GeneratedArtifactSyncError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        for name in names:
            print(f"generated: {name}")
        return 0

    paths = None
    if args.changed_from:
        paths = validation.changed_paths(args.changed_from)
        if paths is None:
            print(
                f"WARN unable to resolve changes from {args.changed_from}; "
                "validating all projections.",
                file=sys.stderr,
            )
    projections = validation.select_for_validation(
        paths, local_only=args.local_only
    )
    return validation.validate(projections)


if __name__ == "__main__":
    raise SystemExit(main())
