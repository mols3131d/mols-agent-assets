---
name: mols-markdown-scripts
description: >
  USE WHEN: Markdown quality check, validation, formatting, or generating an index from YAML frontmatter as CSV, Markdown table, or Markdown list. YAML frontmatter schema parsing (key, value, type, list, nesting), heading hierarchy (H1 count, sequential level), link fragment/reference check via rumdl, format syntax via rumdl fmt.
  EXCLUDES: Text gen/template compile without target validation.
agentsskills:
  compatibility: 'Requires `python`, `uv`, `pyyaml`, `pyromark`, `rumdl`'
  metadata:
    author: 'mols (github.com/mols3131d)'
    version: '0.0.1'
---

# Mols Markdown Scripts

Format and validate Markdown files.

## Routing

1. Read `workflows/INDEX.csv` once.
1. Identify requested outcome, operation, object, constraints.
1. Compare the request with each workflow `description`.
1. Select the minimum workflow set covering the request.
1. Resolve ambiguity with one targeted question.
1. Resolve each selected `name` as `workflows/<name>.md`.
1. Load resources only when selected workflow requires.
1. Run workflow validation before completion.

Route by semantic intent, not keyword. Do not scan `workflows/`.

## Ambiguity

- Select one route when it covers request.
- Select multiple routes only when request spans them.
- Ask one targeted question when remaining routes imply different actions.
- If no route matches, state skill not cover request.
