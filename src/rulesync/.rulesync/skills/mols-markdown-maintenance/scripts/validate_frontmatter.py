#!/usr/bin/env python3
# /// script
# dependencies = [
#   "pyyaml>=6.0.2",
# ]
# ///
"""Validate markdown YAML frontmatter."""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path
from typing import Any, Sequence

from frontmatter import read_frontmatter

TYPE_NAMES = {
    "bool": bool,
    "dict": dict,
    "float": float,
    "int": int,
    "list": list,
    "str": str,
}


def _validate_value(value: Any, spec: dict) -> bool:
    """Helper to validate value against a spec dictionary."""
    if "type" in spec and not isinstance(value, spec["type"]):
        return False

    if "allowed_values" in spec and value not in spec["allowed_values"]:
        return False

    if "min_length" in spec and isinstance(value, (str, list, dict)):
        if len(value) < spec["min_length"]:
            return False
    if "max_length" in spec and isinstance(value, (str, list, dict)):
        if len(value) > spec["max_length"]:
            return False

    if "min_items" in spec and isinstance(value, list):
        if len(value) < spec["min_items"]:
            return False
    if "max_items" in spec and isinstance(value, list):
        if len(value) > spec["max_items"]:
            return False

    if spec.get("is_date"):
        if isinstance(value, datetime.date):
            pass
        elif isinstance(value, str):
            try:
                datetime.date.fromisoformat(value)
            except ValueError:
                return False
        else:
            return False

    if "pattern" in spec:
        if not isinstance(value, str) or not re.match(spec["pattern"], value):
            return False

    if "item_type" in spec and isinstance(value, list):
        item_type = spec["item_type"]
        if not all(isinstance(item, item_type) for item in value):
            return False

    if "schema" in spec:
        if not isinstance(value, dict):
            return False
        nested_schema = spec["schema"]
        if spec.get("strict") and any(k not in nested_schema for k in value):
            return False
        for k, v_spec in nested_schema.items():
            if k not in value or not _validate_value(value[k], v_spec):
                return False

    return True


def validate_frontmatter(
    file_path: Path,
    required_fields: set[str] | None = None,
    schema: dict | None = None,
    expected_values: dict[str, Any] | None = None,
) -> bool:
    """Validate YAML frontmatter against required fields or a schema.

    Schema rules:
        - type: Allowed data type (e.g., str, list, dict).
        - required: Whether the field must exist. Defaults to True.
        - allowed_values: Allowed set/list of values.
        - min_length / max_length: Min/max size for str, list, dict.
        - min_items / max_items: Min/max length of lists.
        - is_date: ISO 8601 date string or datetime.date object.
        - pattern: Regex string pattern matching.
        - item_type: Expected type for list elements.
        - schema: Sub-schema for nested dict values.
        - strict: Disallow undefined fields (use '__strict__' for root).
    """
    if not file_path.is_file():
        return False

    parsed = read_frontmatter(file_path)
    if parsed is None:
        return False
    data, _ = parsed

    if required_fields is not None and not required_fields.issubset(data.keys()):
        return False

    if schema is not None:
        is_strict = schema.get("__strict__", False)
        schema_keys = {k for k in schema.keys() if k != "__strict__"}

        if is_strict and any(k not in schema_keys for k in data):
            return False

        for key in schema_keys:
            spec = schema[key]
            if key not in data:
                if spec.get("required", True):
                    return False
                continue
            if not _validate_value(data[key], spec):
                return False

    if expected_values is not None:
        for key, value in expected_values.items():
            if data.get(key) != value:
                return False

    return True


def _load_schema(path: Path) -> dict[str, Any]:
    """YAML schema를 읽고 type 이름을 Python type으로 변환한다."""
    try:
        import yaml
    except ImportError as error:
        raise ImportError("dependency 'yaml' is missing") from error

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("schema root must be a mapping")

    def convert(value: Any) -> Any:
        if isinstance(value, list):
            return [convert(item) for item in value]
        if not isinstance(value, dict):
            return value
        converted = {key: convert(item) for key, item in value.items()}
        for key in ("type", "item_type"):
            type_name = converted.get(key)
            if isinstance(type_name, str):
                if type_name not in TYPE_NAMES:
                    raise ValueError(f"unsupported {key}: {type_name}")
                converted[key] = TYPE_NAMES[type_name]
        return converted

    return convert(data)


def _parse_expected(items: Sequence[str]) -> dict[str, str]:
    expected: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"--expect must use key=value: {item}")
        key, value = item.split("=", 1)
        if not key:
            raise ValueError(f"--expect key is empty: {item}")
        expected[key] = value
    return expected


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--required", nargs="+", default=[])
    parser.add_argument("--schema", type=Path)
    parser.add_argument(
        "--expect",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Require an exact scalar value; repeat for multiple fields",
    )
    args = parser.parse_args(argv)

    try:
        schema = _load_schema(args.schema) if args.schema else None
        expected = _parse_expected(args.expect)
        results = {
            str(path): validate_frontmatter(
                path,
                required_fields=set(args.required),
                schema=schema,
                expected_values=expected,
            )
            for path in args.files
        }
    except (ImportError, OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
