---
name: validate-frontmatter
description: Validate YAML frontmatter keys and values.
---

# Validate Frontmatter

## Goal

Validate markdown YAML frontmatter structure and schema.

## Instructions

- Call `scripts/validate_frontmatter.py` to validate.
- If `pyyaml` dependency missing:
  1. Try install via `pip install pyyaml` or `uv pip install pyyaml`.
  2. If install fails, delegate to manual parsing: read content, extract lines between first `---` markers, parse key-value lines via string split or regex, validate types/constraints manually.
