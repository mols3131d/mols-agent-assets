---
name: validate-headers
description: Validate markdown header hierarchy.
---

# Validate Headers

## Goal

Validate H1 constraints and sequential heading levels in markdown.

## Instructions

- Call `scripts/validate_headers.py` to check headings.
- If `pyromark` dependency missing:
  1. Try install via `pip install pyromark` or `uv pip install pyromark`.
  2. If install fails, delegate to manual parsing: read content, search headings via regex (`^#+\s+(.+)$` on non-code block lines), collect heading levels (count of `#`), validate constraints manually.
