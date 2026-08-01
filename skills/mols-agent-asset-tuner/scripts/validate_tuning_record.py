from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None

REQUIRED_SOURCE = {"name", "location", "revision", "license", "trust_tier"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a provenance YAML record.")
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    if yaml is None:
        print("ERROR: PyYAML is required")
        return 2
    try:
        data = yaml.safe_load(args.record.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"ERROR: invalid YAML: {exc}")
        return 1
    if not isinstance(data, dict) or not isinstance(data.get("source"), dict):
        print("ERROR: record.source must be a mapping")
        return 1
    source = data["source"]
    missing = REQUIRED_SOURCE - set(source)
    errors = [f"missing source fields: {', '.join(sorted(missing))}"] if missing else []
    for field in REQUIRED_SOURCE - {"trust_tier"}:
        if field in source and (
            not isinstance(source[field], str) or not source[field].strip()
        ):
            errors.append(f"source.{field} must be a non-empty string")
    tier = source.get("trust_tier")
    if not isinstance(tier, int) or not 0 <= tier <= 4:
        errors.append("source.trust_tier must be an integer from 0 to 4")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print(f"PASS: {args.record}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
