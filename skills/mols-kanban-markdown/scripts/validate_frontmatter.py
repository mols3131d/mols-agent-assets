#!/usr/bin/env python3
# /// script
# dependencies = [
#   "pyyaml>=6.0.2",
# ]
# ///
"""Validate kanban markdown cards YAML frontmatter against config schema."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

# Allow standalone CLI execution without relative import error
sys.path.insert(0, str(Path(__file__).resolve().parent))

from shared import get_card_files, load_kanban_config, parse_frontmatter


def validate_value(value: Any, spec: dict[str, Any], path_str: str) -> list[str]:
    """Validate a single value against a schema spec. Returns list of error messages."""
    errors = []

    spec_type = spec.get("type")
    required = spec.get("required", False)

    if value is None:
        if required:
            errors.append(f"{path_str} is required but got None or missing.")
        return errors

    # Check type
    if spec_type == "string":
        if not isinstance(value, str):
            errors.append(f"{path_str} must be a string, got {type(value).__name__}.")
            return errors

        # Check validation constraints
        validate = spec.get("validate", {})
        length_min = validate.get("length_min")
        length_max = validate.get("length_max")
        regex_pattern = validate.get("regex")

        if length_min is not None and len(value) < length_min:
            errors.append(
                f"{path_str} length must be at least {length_min}, got {len(value)}."
            )
        if length_max is not None and len(value) > length_max:
            errors.append(
                f"{path_str} length must be at most {length_max}, got {len(value)}."
            )
        if regex_pattern is not None:
            if not re.match(regex_pattern, value):
                errors.append(
                    f"{path_str} '{value}' does not match pattern '{regex_pattern}'."
                )

    elif spec_type == "array":
        if not isinstance(value, list):
            errors.append(f"{path_str} must be an array, got {type(value).__name__}.")
            return errors

        validate = spec.get("validate", {})
        length_min = validate.get("length_min")
        length_max = validate.get("length_max")

        if length_min is not None and len(value) < length_min:
            errors.append(
                f"{path_str} item count must be "
                f"at least {length_min}, got {len(value)}."
            )
        if length_max is not None and len(value) > length_max:
            errors.append(
                f"{path_str} item count must be at most {length_max}, got {len(value)}."
            )

        # Check items if specified
        items_spec = validate.get("items")
        if items_spec and isinstance(items_spec, dict):
            for idx, item in enumerate(value):
                item_errors = validate_value(item, items_spec, f"{path_str}[{idx}]")
                errors.extend(item_errors)

    elif spec_type == "object":
        if not isinstance(value, dict):
            errors.append(f"{path_str} must be an object, got {type(value).__name__}.")
            return errors

        # If there's a nested schema for the object, check it here if needed,
        # but config.jsonc frontmatter_schema only defines string/array
        # types at top-level.

    # Check enum (if specified in spec)
    allowed_enum = spec.get("enum")
    if allowed_enum is not None:
        if value not in allowed_enum:
            errors.append(f"{path_str} '{value}' must be one of {allowed_enum}.")

    return errors


def validate_card_file(file_path: Path, schema: dict[str, Any]) -> list[str]:
    """Validate a markdown card file against the config frontmatter_schema."""
    errors = []
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        return [f"Failed to read file {file_path}: {e}"]

    # Basic markdown layout check (should have frontmatter)
    frontmatter = parse_frontmatter(content)
    if frontmatter is None:
        return [
            f"File {file_path.name} does not have valid YAML frontmatter "
            f"(needs to start and end with '---')."
        ]

    # Validate each key in the schema
    for key, spec in schema.items():
        val = frontmatter.get(key)
        val_errors = validate_value(val, spec, key)
        errors.extend(val_errors)

    # Check for extraneous keys if we want strict mode
    # Check if there are keys in frontmatter that are not defined in schema
    for key in frontmatter:
        if key not in schema:
            # Maybe warning or error?
            # In mols-kanban-markdown, let's allow it but we can mention it.
            pass

    return errors


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python validate_frontmatter.py <kanban_path>", file=sys.stderr)
        sys.exit(1)

    kanban_path = Path(sys.argv[1]).resolve()

    # 1. Load config.jsonc using shared helper
    config_data = load_kanban_config(kanban_path)
    if not config_data:
        print(f"Error: Failed to load config at {kanban_path}", file=sys.stderr)
        sys.exit(1)

    schema = config_data.get("frontmatter_schema", {})
    if not schema:
        print(
            "Warning: No 'frontmatter_schema' defined in config.jsonc.", file=sys.stderr
        )
        sys.exit(0)

    # 2. Find all markdown files using shared helper
    markdown_files = get_card_files(kanban_path)

    if not markdown_files:
        print("No markdown files found to validate.")
        sys.exit(0)

    # 3. Validate each file
    total_errors = 0
    for file_path in markdown_files:
        # Skip template.md or AGENTS.md or README.md if they happen to be in the folder
        if file_path.name in ["README.md", "AGENTS.md", "template.md"]:
            continue

        errors = validate_card_file(file_path, schema)
        if errors:
            total_errors += len(errors)
            print(
                f"Validation errors in [ {file_path.relative_to(kanban_path.parent)} ]:"
            )
            for err in errors:
                print(f"  - {err}")

    if total_errors > 0:
        print(f"\nValidation failed with {total_errors} errors.", file=sys.stderr)
        sys.exit(1)
    else:
        print("All cards validated successfully!")
        sys.exit(0)


if __name__ == "__main__":
    main()
