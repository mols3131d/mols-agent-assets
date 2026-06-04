#!/usr/bin/env python3
"""Sort INDEX.csv by prioritized fields."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from index_common import (
    read_csv,
    resolve_output_path,
    sort_rows,
    split_csv_arg,
    write_csv,
)

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Sort INDEX.csv by prioritized fields.")
    parser.add_argument("csv_path", help="INDEX.csv path.")
    parser.add_argument(
        "--fields",
        required=True,
        help="Comma-separated sort priority fields, e.g. status,id,file.",
    )
    parser.add_argument("--output", help="Output CSV path. Defaults to input path.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    csv_path = Path(args.csv_path).resolve()
    if not csv_path.is_file():
        raise SystemExit(f"not a file: {csv_path}")

    fieldnames, rows = read_csv(csv_path)

    sort_fields = split_csv_arg(args.fields)
    unknown = [field for field in sort_fields if field not in fieldnames]
    if unknown:
        raise SystemExit(f"unknown sort fields: {', '.join(unknown)}")

    sorted_rows = sort_rows(rows, sort_fields)
    output_path = resolve_output_path(csv_path.parent, args.output, csv_path.name)

    if not args.dry_run:
        write_csv(output_path, fieldnames, sorted_rows)

    payload = {
        "csv": str(csv_path),
        "output": str(output_path),
        "rows": len(rows),
        "sort": sort_fields,
        "dry_run": args.dry_run,
    }
    sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
