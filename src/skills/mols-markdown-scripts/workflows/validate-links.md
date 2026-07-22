---
name: validate-links
description: Validate markdown link fragments and references.
---

# Validate Links

## Goal

Verify internal anchor and reference links in markdown files.

## Instructions

- Call `scripts/validate_links.py` to check links.
- If `rumdl` CLI tool missing:
  1. Run using `uvx --with rumdl rumdl check` or `uv run rumdl check` as custom executable.
  2. If CLI run fails, delegate to manual regex search: extract targets from `\[.*?\]\((.*?)\)`, manually check target validity (file existence or heading anchors in same file).
