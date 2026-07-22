#!/usr/bin/env python3
# /// script
# dependencies = [
#   "pyyaml>=6.0.2",
# ]
# ///
"""Validate markdown YAML frontmatter."""

from __future__ import annotations

import datetime
import re
from pathlib import Path
from typing import Any


def _parse_frontmatter(content: str) -> dict | None:
    """Parse YAML frontmatter block from markdown content."""
    try:
        import yaml
    except ImportError as error:
        raise ImportError("dependency 'yaml' is missing") from error

    lines = content.splitlines()
    if not lines or lines[0] != "---":
        return None

    yaml_lines = []
    found_end = False
    for line in lines[1:]:
        if line == "---":
            found_end = True
            break
        yaml_lines.append(line)

    if not found_end:
        return None

    try:
        data = yaml.safe_load("\n".join(yaml_lines))
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def _validate_value(value: Any, spec: dict) -> bool:
    """Helper to validate value against a spec dictionary."""
    # 1. Type validation
    if "type" in spec and not isinstance(value, spec["type"]):
        return False

    # 2. Allowed values validation
    if "allowed_values" in spec and value not in spec["allowed_values"]:
        return False

    # 3. Size constraints (min_length, max_length)
    if "min_length" in spec and isinstance(value, (str, list, dict)):
        if len(value) < spec["min_length"]:
            return False
    if "max_length" in spec and isinstance(value, (str, list, dict)):
        if len(value) > spec["max_length"]:
            return False

    # 4. List item counts (min_items, max_items)
    if "min_items" in spec and isinstance(value, list):
        if len(value) < spec["min_items"]:
            return False
    if "max_items" in spec and isinstance(value, list):
        if len(value) > spec["max_items"]:
            return False

    # 5. Date validation
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

    # 6. Regex pattern validation
    if "pattern" in spec:
        if not isinstance(value, str) or not re.match(spec["pattern"], value):
            return False

    # 7. List elements type validation
    if "item_type" in spec and isinstance(value, list):
        item_type = spec["item_type"]
        if not all(isinstance(item, item_type) for item in value):
            return False

    # 8. Nested schema validation
    if "schema" in spec and isinstance(value, dict):
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
) -> bool:
    """Validate YAML frontmatter against required fields or a schema.

    Args:
        file_path: Path to the target markdown file.
        required_fields: Set of keys that must exist.
        schema: Dictionary defining schema rules.

    Schema Rules:
        - type: Allowed data type (e.g., str, list, dict).
        - allowed_values: Allowed set/list of values.
        - min_length / max_length: Min/max size for str, list, dict.
        - min_items / max_items: Min/max length of lists.
        - is_date: ISO 8601 date string or datetime.date object.
        - pattern: Regex string pattern matching.
        - item_type: Expected type for list elements.
        - schema: Sub-schema for nested dict values.
        - strict: Disallow undefined fields (use '__strict__' for root).

    Returns:
        True if all checks pass, otherwise False.
    """
    if not file_path.is_file():
        return False

    content = file_path.read_text(encoding="utf-8")
    data = _parse_frontmatter(content)
    if data is None:
        return False

    if required_fields is not None:
        if not required_fields.issubset(data.keys()):
            return False

    if schema is not None:
        is_strict = schema.get("__strict__", False)
        schema_keys = {k for k in schema.keys() if k != "__strict__"}

        if is_strict and any(k not in schema_keys for k in data):
            return False

        for key in schema_keys:
            spec = schema[key]
            if key not in data or not _validate_value(data[key], spec):
                return False

    return True


def main() -> None:
    pass


if __name__ == "__main__":
    main()
