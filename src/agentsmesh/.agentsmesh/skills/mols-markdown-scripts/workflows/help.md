---
name: help
description: Help guide and usage instructions for the markdown skill.
---

# Markdown Skill Help Guide

Help instructions for users (Commanders) and agents (Executors).

## Goal

Explain skill capabilities and guide execution flow.

## 1. Overview (For Commanders)

Use this skill to check or fix markdown files.

- **Check Frontmatter**: Validate YAML keys, types, list elements, nesting, date format, strict modes.
- **Check Headings**: Validate H1 single constraint, sequential levels (no gaps).
- **Check Links**: Validate fragment anchors, reference links via rumdl check.
- **Format**: Clean up trailing whitespaces, extra empty lines via rumdl fmt.

To start, ask agent to perform check or format: e.g., "Check headers on index.md".

## 2. Execution (For Executors)

Read `INDEX.csv` to select the right workflow.

- If YAML metadata checks → Run `validate-frontmatter.md`
- If Heading sequence checks → Run `validate-headers.md`
- If Link/Anchor validity checks → Run `validate-links.md`
- If Format/Cleanup needed → Run `format-markdown.md`

## 3. Resilience Fallback (For Executors)

If dependencies fail, delegate to manual parsing:

- **Missing pyyaml**: Extract frontmatter between `---`, parse lines via regex/split.
- **Missing pyromark**: Collect `#` prefix counts via regex `^#+\s` to find levels.
- **Missing rumdl**: Extract links via regex `\[.*?\]\((.*?)\)` and check target file/anchor.
