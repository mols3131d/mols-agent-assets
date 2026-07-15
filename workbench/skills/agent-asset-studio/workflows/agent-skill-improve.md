# Improve Agent Skill

## Goal

Improve one existing agent skill while preserving behavior outside the requested change.

## Required Inputs

- Existing skill path
- Requested behavior, content, or structural change

## Procedure

1. Inspect the target with `rg --files <skill-dir>` and run baseline validation.
2. Read the frontmatter and only the files tied to the request or failing checks.
3. Save each existing Markdown file immediately before editing it as `<filename>.original.md`.
4. Define the affected triggers, outputs, exclusions, and constraints. Preserve all unrelated behavior.
5. Prefer focused checks such as `rg "<term>" <skill-dir>` for duplication and `wc -l <files>` for context size.
6. Make the smallest change that resolves the requested issue. Do not re-scaffold the existing skill.
7. When changing `INDEX.csv`, workflow layout, or router behavior, read `references/routing-skill-structure.md` first.
8. Re-run `python3 scripts/validate_asset.py <skill-dir> --type skill`. Fix only requested or failing areas until errors are gone and warnings are fixed or explicitly accepted.

## Validation

- Requested behavior works and unrelated triggers, exclusions, and safety constraints remain intact.
- Frontmatter is valid; the directory and `name` match.
- Every referenced path and route `id` resolves relative to its `INDEX.csv`.
- No duplicated rules, empty directories, unused examples, or nested discoverable `SKILL.md` files remain.

## Resources

- Read `references/routing-skill-structure.md` only for routing architecture changes.
- Use `scripts/validate_asset.py` after every structural change.

## Stop Conditions

- Stop before renaming unless the user explicitly requested it.
- Stop before changing behavior outside the requested scope.
- Stop before destructive or external actions requiring new authority.
