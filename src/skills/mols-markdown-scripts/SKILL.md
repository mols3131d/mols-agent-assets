---
name: mols-markdown-scripts
description: >
  USE WHEN: Markdown quality check, validation, formatting, or generating an index from YAML frontmatter as CSV, Markdown table, or Markdown list. YAML frontmatter schema parsing (key, value, type, list, nesting), heading hierarchy (H1 count, sequential level), link fragment/reference check via rumdl, format syntax via rumdl fmt.
  EXCLUDES: Text gen/template compile without target validation.
---

# Mols Markdown Scripts

Format and validate Markdown files.

## Routing

1. Read `workflows/INDEX.csv` once.
2. Identify requested outcome, operation, object, constraints.
3. Eliminate routes matching `excludes`.
4. Select minimum route set matching `use_when`.
5. Resolve ambiguity with one targeted question.
6. Resolve selected IDs from index directory, load only those files.
7. Load resources only when selected workflow requires.
8. Run workflow validation before completion.

Route by semantic intent, not keyword. Do not scan `workflows/`.

## Ambiguity

- Select one route when it covers request.
- Select multiple routes only when request spans them.
- Ask one targeted question when remaining routes imply different actions.
- If no route matches, state skill not cover request.
