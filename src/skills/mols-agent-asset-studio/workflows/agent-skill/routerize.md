---
name: agent-skill-routerize
description: USE WHEN: consolidating multiple related existing skills into one routing skill. EXCLUDES: merging skills with unrelated domains or lifecycles.
---

# Routerize Skills

## Goal

Consolidate related skills into one routing skill with route IDs relative to `INDEX.csv`.

## When to Use

Use this workflow to migrate separate related skills into a single routing skill (`lite` or `full` mode).

## Instructions

- Read [routing-skill-migration.md](routing-skill-migration.md) before migration.
- Use `scripts/routerize_skills.py` for filesystem transformations.
- Use `scripts/validate_asset.py` for validation.

## Workflow: Routerize Skills

### Arguments from Context

- Source skill directories (2+)
- Target routing skill directory
- Migration mode (`lite` | `full`)

### Procedure

1. Read [routing-skill-migration.md](routing-skill-migration.md).
2. Confirm source skills share domain, trigger scope, and lifecycle.
3. Run transformation:

   ```bash
   python3 scripts/routerize_skills.py --mode <lite|full> --target <path/to/router> <path/to/skill1> <path/to/skill2>
   ```

4. Replace generated route conditions with semantic `use_when` and `excludes` in `INDEX.csv`.
5. Validate target and confirm route `id` resolution.

### Validation

- Target contains single `SKILL.md`, `workflows/INDEX.csv`, and workflow modules.
- Index schema uses `id,use_when,excludes`.
- Every `id` resolves to a valid workflow file; no nested `SKILL.md` files exist under `workflows/`.
