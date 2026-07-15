# Validate Agent Skill

## Goal

Validate one skill's required fields and basic file structure without editing it.

## Required Inputs

- Existing skill directory

## Procedure

1. Run `python3 scripts/validate_asset.py <skill-dir> --type skill`.
2. Confirm `SKILL.md` exists and its YAML frontmatter contains `name` and `description`.
3. Confirm `name` matches the directory, uses lowercase hyphen-case, and is at most 64 characters.
4. Confirm `description` is not empty and is at most 1024 characters.
5. For a routing skill, find its single `INDEX.csv`, confirm route IDs are unique relative paths, and resolve each from the index directory to an existing file inside the skill.
6. Report pass or fail. For each failure, include the field or path and the validator message.

## Validation

- The command exits with code `0` and returns `status: pass`.
- Every failed check is reported; no file is modified.

## Resources

Use `scripts/validate_asset.py`. No reference is required.

## Stop Conditions

- Do not fix validation failures unless the user also requests changes.
- Stop and report when the target directory or validator script is unavailable.
