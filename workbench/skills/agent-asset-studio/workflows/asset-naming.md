# Asset Naming

## Goal

Suggest, validate, or apply a clear agent asset name without changing existing names implicitly.

## Required Inputs

- Asset type and purpose
- Existing or new asset status
- Target path when applying a rename

## Procedure

1. Determine whether naming is the primary request.
2. If the asset exists, confirm that the user explicitly requested a rename.
3. Read `references/naming-convention.md`.
4. Propose or validate the shortest name that identifies the domain and job.
5. Apply the rename only when explicitly authorized, then update internal references.

## Validation

- Skill directory and frontmatter `name` match.
- Names use lowercase letters, numbers, and single hyphens.
- Internal paths resolve after an applied rename.

## Resources

Read `references/naming-convention.md` for naming patterns and examples.

## Stop Conditions

Never rename an existing asset unless the user explicitly requested it.
