---
name: agent-skill-validate
description: USE WHEN: validating a skill's required fields and basic file structure. EXCLUDES: fixing validation failures or evaluating effectiveness.
---

# Validate Agent Skill

## Goal

Validate one skill's required fields and basic file structure without editing it.

## When to Use

Use this workflow to check structural conformance and frontmatter using the validation script.

## Instructions

- Read [references/agent-skill-frontmatter.md](../../references/skill/agent-skill-frontmatter.md) for frontmatter rules.
- Read [references/agent-skill-directories.md](../../references/skill/agent-skill-directories.md) for directory structure rules.
- Use `scripts/validate_asset.py` for structural validation.
- Do not fix validation failures unless explicitly requested.

## Workflow: Validate Agent Skill

### Arguments from Context

- Existing skill directory

### Procedure

1. Run `python3 scripts/validate_asset.py <skill-dir> --type skill`.
2. Verify frontmatter matches [references/agent-skill-frontmatter.md](../../references/skill/agent-skill-frontmatter.md) and structure follows [references/skill/agent-skill-directories.md](../../references/skill/agent-skill-directories.md).
3. For routing skills, verify `INDEX.csv` route IDs resolve to valid files.
4. Report pass or fail result with validator output.

### Validation

- Command exits with code `0` (`status: pass`).
- Every failed check is reported; no files are modified.
