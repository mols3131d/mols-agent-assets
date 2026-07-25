---
name: skill-validate
description: >-
    Validate agent-skill frontmatter, references, workflow structure, and required
    files without editing. Use before sharing, publishing, or accepting changes.
    Not for fixing failures or evaluating effectiveness.
---

# Validate Agent Skill

## Goal

Validate one skill's required fields and basic file structure without editing it.

## When to Use

Use this workflow to check structural conformance and frontmatter without editing.

## Instructions

- Read [frontmatter.md](../references/agent-skill/frontmatter.md) for frontmatter rules.
- Read [architecture.md](../references/agent-skill/architecture.md) for directory rules.
- Use `mols-markdown-scripts` through the local validation workflows.
- Do not fix validation failures unless explicitly requested.

## Workflow: Validate Agent Skill

### Arguments from Context

- Existing skill directory

### Procedure

1. Run [frontmatter-validate.md](frontmatter-validate.md).
2. Verify structure against [architecture.md](../references/agent-skill/architecture.md).
3. For routing skills, run [router-asset-maintain.md](router-asset-maintain.md) and
   verify each `name` resolves to `workflows/<name>.md`.
4. Report each pass or failure without modifying source files.

### Validation

- Frontmatter command exits with code `0`.
- Every failed check is reported; no files are modified.
