---
name: format-markdown
description: Format markdown files.
---

# Format Markdown

## Goal

Format markdown document structure and blank lines.

## Instructions

- Call `scripts/format_markdown.py` to format.
- If `rumdl` CLI tool missing:
  1. Run using `uvx --with rumdl rumdl fmt` or `uv run rumdl fmt` as custom executable.
  2. If format fails, delegate to manual format: collapse consecutive empty lines to max of one, strip trailing whitespace, ensure single trailing newline at EOF.
