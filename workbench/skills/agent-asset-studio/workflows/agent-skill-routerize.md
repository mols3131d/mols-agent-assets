# Routerize Skills

## Goal

Consolidate related existing skills into one shallow routing skill whose route IDs are workflow paths relative to `INDEX.csv`.

## Required Inputs

- Two or more source skill directories
- Target routing skill directory
- Migration mode: `lite` or `full`

## Procedure

1. Read `references/routing-skill-migration.md`.
2. Verify that source skills share one domain, top-level trigger, resources, and release lifecycle. Keep unrelated skills separate.
3. Choose a mode.

   - `lite`: Move each skill into `workflows/<id>/`, rename `SKILL.md` to `WORKFLOW.md`, and preserve isolated resources.
   - `full`: Flatten each `SKILL.md` to `workflows/<id>.md`, merge shared resource files, and rewrite affected relative paths.

4. Run:

   ```bash
   python3 scripts/routerize_skills.py --mode <lite|full> --target <path/to/router> <path/to/skill1> <path/to/skill2>
   ```

5. Replace generated route conditions with semantic `use_when` and `excludes` values based on real user intent.
6. Validate the target and confirm every route `id` resolves relative to `INDEX.csv`.

## Validation

- Target contains one `SKILL.md`, default `workflows/INDEX.csv`, and workflow modules.
- A different index location is used only when the user explicitly requests it.
- Index schema is `id,use_when,excludes` with unique relative-path IDs.
- Every `id` resolves to a workflow file inside the target skill.
- No nested `SKILL.md` remains under `workflows/`.
- A clear request loads one minimum workflow; near misses and ambiguous requests route correctly.

## Resources

- Read `references/routing-skill-migration.md` before migration.
- Use `scripts/routerize_skills.py` for the filesystem transformation.
- Use `scripts/validate_asset.py` for structural validation.

## Stop Conditions

- Stop if source skills have unrelated permissions, ownership, triggers, or release lifecycles.
- Stop before overwriting an existing target or workflow.
- Ask one targeted question when migration mode materially changes the desired output.
