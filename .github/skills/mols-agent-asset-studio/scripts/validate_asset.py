from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from validators.dispatch import PROFILES, detect_profile, validate_target


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate an agent asset using a runtime-specific profile."
    )
    parser.add_argument("target", type=Path)
    parser.add_argument(
        "--profile", choices=("auto", *sorted(PROFILES)), default="auto"
    )
    parser.add_argument(
        "--boundary", type=Path, help="Allowed root for relative links in file assets"
    )
    parser.add_argument("--strict", action="store_true", help="Reject unknown fields")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    target = args.target.resolve()
    profile = args.profile
    if profile == "auto":
        try:
            profile = detect_profile(target)
        except ValueError as exc:
            if args.as_json:
                print(
                    json.dumps(
                        {"profile": None, "errors": [str(exc)], "warnings": []},
                        indent=2,
                    )
                )
            else:
                print(f"ERROR: {exc}")
            return 1
    result = validate_target(
        target,
        profile=profile,
        strict=args.strict,
        boundary=args.boundary.resolve() if args.boundary else None,
    )
    if args.as_json:
        print(
            json.dumps(
                {
                    "target": str(target),
                    "profile": profile,
                    "errors": result.errors,
                    "warnings": result.warnings,
                    "passed": result.ok,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        for warning in result.warnings:
            print(f"WARN: {warning}")
        for error in result.errors:
            print(f"ERROR: {error}")
        if result.ok:
            print(f"PASS: {target} ({profile})")
    return 0 if result.ok else 1


if __name__ == "__main__":
    sys.exit(main())
