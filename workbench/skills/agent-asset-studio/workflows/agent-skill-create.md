# Create Agent Skill

## Goal

Create one focused agent skill with the minimum structure and context cost required for its job.

## Required Inputs

- Target path or destination
- Intended job, triggering requests, outputs, and near-miss exclusions

## Procedure

1. Confirm the target does not exist. If no destination is given, ask for it.
2. Define the skill's single job, triggers, outputs, and exclusions.
3. Scaffold the target with `python3 scripts/init_asset.py <name> --type skill --path <dir>`. Add `--routing-skill` only when multiple workflows share one domain and usually load selectively.
4. Keep only the required structure:

   | Path | Add when |
   | --- | --- |
   | `SKILL.md` | Always |
   | `references/` | Knowledge is long or conditional |
   | `scripts/` | Deterministic logic repeats at least twice |
   | `assets/` | Output material is copied or reused |
   | `workflows/INDEX.csv` + workflow modules | Selective workflows share one domain |

5. Write only `name` and `description` in frontmatter unless the target client requires more.
6. Put the common execution path and constraints in `SKILL.md`; move passive knowledge, repeated logic, and reusable output material to their matching resource directories.
7. Match instruction freedom to risk: goals for flexible work, preferred procedures for bounded work, and exact commands or order for fragile work.
8. Validate with `python3 scripts/validate_asset.py <skill-dir> --type skill`.

## Validation

- `name` is lowercase hyphen-case, matches the folder, and is at most 64 characters.
- `description` states capability, activation contexts, and exclusions and is at most 1024 characters.
- Triggers select intended requests and reject near misses.
- Every referenced path resolves; no empty directories, unused examples, duplicated rules, or nested discoverable `SKILL.md` files remain.

## Resources

- Read `references/routing-skill-structure.md` before creating a routing skill.
- Keep `INDEX.csv` under `workflows/` unless the user requests another location.
- Use `scripts/init_asset.py`; do not reconstruct scaffolding manually.

## Stop Conditions

- Stop before overwriting an existing target; route existing-skill changes to `agent-skill-improve`.
- Stop before renaming an existing skill unless explicitly requested.
- Stop before destructive or external actions requiring new authority.
