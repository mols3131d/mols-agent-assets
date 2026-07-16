---
name: agent-asset-naming
description: USE WHEN: the user wants to suggest, validate, or apply a clear agent asset name. EXCLUDES: renaming an existing asset without an explicit request.
---

# Asset Naming

## Goal

Suggest, validate, or apply a clear agent asset name without changing existing names implicitly.

## When to Use

Use this workflow to determine appropriate names for new agent assets or to validate and apply names for existing assets when explicitly asked.

## Instructions

- Read `references/naming-convention.md` for naming patterns and examples.
- Never rename an existing asset unless the user explicitly requested it.

## Workflows

### Arguments from Context

- Asset type and purpose
- Existing or new asset status
- Target path when applying a rename

### Procedure

1. Determine whether naming is the primary request.
2. If the asset exists, confirm that the user explicitly requested a rename.
3. Read `references/naming-convention.md`.
4. Propose or validate the shortest name that identifies the domain and job.
5. Apply the rename only when explicitly authorized, then update internal references.

### Validation

- Skill directory and frontmatter `name` match.
- Names use lowercase letters, numbers, and single hyphens.
- Internal paths resolve after an applied rename.
