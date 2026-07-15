# Routerize Skills

## Goal

Consolidate related existing skills into one shallow routing skill with a semantic route index and exact workflow entrypoints.

## Required Inputs

- Two or more source skill directories
- Target routing skill directory
- Migration mode: `lite` or `full`

## Procedure

1. Read `references/routing-skill-structure.md`.
2. Verify that source skills share one domain, top-level trigger, resources, and release lifecycle. Keep unrelated skills separate.
3. Choose a mode.

   - `lite`: Move each skill into `workflows/<id>/`, rename `SKILL.md` to `WORKFLOW.md`, and preserve isolated resources.
   - `full`: Flatten each `SKILL.md` to `workflows/<id>.md`, merge shared resource files, and rewrite affected relative paths.

4. Run:

   ```bash
   python3 scripts/routerize_skills.py --mode <lite|full> --target <path/to/router> <path/to/skill1> <path/to/skill2>
   ```

5. Replace generated route conditions with semantic `use_when` and `avoid_when` values based on real user intent.
6. Validate the target and confirm every exact entrypoint resolves.

## Validation

- Target contains one `SKILL.md`, root `INDEX.csv`, and `workflows/`.
- Index schema is `id,use_when,avoid_when,entrypoint` with unique IDs.
- Every entrypoint exists inside the target skill.
- No nested `SKILL.md` remains under `workflows/`.
- A clear request loads one minimum workflow; near misses and ambiguous requests route correctly.

## Resources

- Read `references/routing-skill-structure.md` before migration.
- Use `scripts/routerize_skills.py` for the filesystem transformation.
- Use `scripts/validate_asset.py` for structural validation.

## Stop Conditions

- Stop if source skills have unrelated permissions, ownership, triggers, or release lifecycles.
- Stop before overwriting an existing target or workflow.
- Ask one targeted question when migration mode materially changes the desired output.
