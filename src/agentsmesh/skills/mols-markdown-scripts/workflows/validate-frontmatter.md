---
name: validate-frontmatter
description: Validate YAML frontmatter keys and values.
---

# Validate Frontmatter

## Goal

Validate markdown YAML frontmatter structure and schema.

## Instructions

- Call `scripts/validate_frontmatter.py <files...>` to validate.
- Use `--required <fields...>` for required keys.
- Use `--schema <schema.yaml>` for reusable type, length, pattern, list, or
  nested mapping rules. Schema `type` values are `str`, `int`, `float`, `bool`,
  `list`, or `dict`.
- Use repeatable `--expect KEY=VALUE` when one scalar must match an exact value.
- Exit code `0` means pass, `1` validation failure, and `2` execution/schema error.
- If `pyyaml` dependency missing:
  1. Try install via `pip install pyyaml` or `uv pip install pyyaml`.
  1. If install fails, delegate to manual parsing: read content, extract lines between first `---` markers, parse key-value lines via string split or regex, validate types/constraints manually.
