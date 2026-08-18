import argparse
import sys
from pathlib import Path

from .core import sync

DEFAULT_LOCKFILE = "my-assets-lock.json"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sync files from sourceUrl entries in my-assets-lock.json"
    )
    parser.add_argument(
        "--lockfile",
        default=DEFAULT_LOCKFILE,
        help=f"default: {DEFAULT_LOCKFILE}",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print planned changes without writing files",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit 1 if changes, conflicts, or local modifications exist",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite local modifications",
    )

    args = parser.parse_args()

    if args.dry_run and args.check:
        print("error: --dry-run and --check cannot be used together", file=sys.stderr)
        sys.exit(2)

    try:
        code = sync(
            Path(args.lockfile),
            dry_run=args.dry_run,
            check=args.check,
            force=args.force,
        )
        sys.exit(code)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
