from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a balanced trigger evaluation set."
    )
    parser.add_argument("eval_set", type=Path)
    parser.add_argument("--min-cases", type=int, default=20)
    parser.add_argument("--min-positive-ratio", type=float, default=0.45)
    parser.add_argument("--max-positive-ratio", type=float, default=0.65)
    args = parser.parse_args()
    try:
        data = json.loads(args.eval_set.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 1
    if not isinstance(data, list):
        print("ERROR: eval set must be an array")
        return 1
    errors: list[str] = []
    ids: set[str] = set()
    queries: set[str] = set()
    positives = 0
    for index, item in enumerate(data):
        context = f"case {index}"
        if not isinstance(item, dict):
            errors.append(f"{context}: expected object")
            continue
        case_id = item.get("id")
        if not isinstance(case_id, str) or not case_id.strip():
            errors.append(f"{context}: id must be non-empty string")
        elif case_id in ids:
            errors.append(f"{context}: duplicate id {case_id!r}")
        else:
            ids.add(case_id)
        query = item.get("query")
        if not isinstance(query, str) or not query.strip():
            errors.append(f"{context}: query must be non-empty string")
        elif query in queries:
            errors.append(f"{context}: duplicate query")
        else:
            queries.add(query)
        expected = item.get("should_trigger")
        if not isinstance(expected, bool):
            errors.append(f"{context}: should_trigger must be boolean")
        elif expected:
            positives += 1
        if "expected_route" in item and not isinstance(item["expected_route"], str):
            errors.append(f"{context}: expected_route must be string")
        if "rationale" in item and not isinstance(item["rationale"], str):
            errors.append(f"{context}: rationale must be string")
    count = len(data)
    if count < args.min_cases:
        errors.append(f"need at least {args.min_cases} cases, found {count}")
    if count:
        ratio = positives / count
        if not args.min_positive_ratio <= ratio <= args.max_positive_ratio:
            errors.append(
                f"positive ratio {ratio:.2f} must be between "
                f"{args.min_positive_ratio:.2f} and {args.max_positive_ratio:.2f}"
            )
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print(
        f"PASS: {count} cases ({positives} positive, "
        f"{count - positives} negative, ratio={positives / count:.2f})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
