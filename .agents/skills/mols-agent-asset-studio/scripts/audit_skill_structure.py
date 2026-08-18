from __future__ import annotations

import argparse
import json
from pathlib import Path

from validators.structure import validate_structure


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit Agent Skill structural hygiene."
    )
    parser.add_argument("skill_root", type=Path)
    parser.add_argument("--tests-root", type=Path)
    parser.add_argument("--warnings-as-errors", action="store_true")
    parser.add_argument("--fail-on-generated", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    result = validate_structure(
        args.skill_root.resolve(),
        tests_root=args.tests_root.resolve() if args.tests_root else None,
        fail_on_generated=args.fail_on_generated,
    )
    errors = list(result.errors)
    if args.warnings_as_errors:
        errors.extend(f"warning promoted: {item}" for item in result.warnings)
    if args.as_json:
        print(
            json.dumps(
                {
                    "errors": errors,
                    "warnings": result.warnings,
                    "passed": not errors,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        for item in result.warnings:
            print(f"WARN: {item}")
        for item in errors:
            print(f"ERROR: {item}")
        if not errors:
            print(f"PASS: {args.skill_root}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
