---
name: agent-skill-validate
description: USE WHEN: the user wants to validate a skill's required fields and basic file structure. EXCLUDES: fixing validation failures or evaluating effectiveness.
---

# Validate Agent Skill

## Goal

Validate one skill's required fields and basic file structure without editing it.

## When to Use

Use this workflow to check structural conformance and frontmatter of a skill using the validation script.

## Instructions

- Read [references/agent-skill-frontmatter.md](../references/agent-skill-frontmatter.md) for frontmatter requirements.
- Read [references/agent-skill-directories.md](../references/agent-skill-directories.md) for structural requirements.
- Use `scripts/validate_asset.py` for structural validation.
- Read `references/routing-skill-validation.md` only for a routing skill.
- Do not fix validation failures unless the user also requests changes.
- Stop and report when the target directory or validator script is unavailable.

## Workflow: Validate Agent Skill

### Arguments from Context

- Existing skill directory

### Procedure

1. Run `python3 scripts/validate_asset.py <skill-dir> --type skill`.
2. Confirm that the frontmatter matches the specification in [references/agent-skill-frontmatter.md](../references/agent-skill-frontmatter.md) and the file/directory structure follows [references/agent-skill-directories.md](../references/agent-skill-directories.md).
3. For a routing skill, find its single `INDEX.csv`, confirm route IDs are unique relative paths, and resolve each from the index directory to an existing file inside the skill.
4. Report pass or fail. For each failure, include the field or path and the validator message.

### Validation

- The command exits with code `0` and returns `status: pass`.
- Every failed check is reported; no file is modified.
