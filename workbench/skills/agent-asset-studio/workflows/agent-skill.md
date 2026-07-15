# Agent Skill

## Goal

Create, improve, evaluate, or validate one effective skill with low context cost and preserved behavior.

## Required Inputs

- Mode: create, improve, or evaluate
- Target path or requested destination
- Intended job, triggering requests, outputs, and near-miss exclusions

## Procedure

1. Choose the mode and inspect only the required files.

   | Mode | Condition | First action |
   | --- | --- | --- |
   | Create | Target absent | Confirm path, then scaffold |
   | Improve | Target exists | Inspect files and baseline validation |
   | Evaluate | Review only | Run checks and report findings |

2. Prefer scripts and focused commands.

   | Need | Command |
   | --- | --- |
   | Files | `rg --files <skill-dir>` |
   | Duplicate rules | `rg "<term>" <skill-dir>` |
   | Size | `wc -l <files>` |
   | Validate | `python3 scripts/validate_asset.py <skill-dir> --type skill` |
   | Scaffold | `python3 scripts/init_asset.py <name> --type skill --path <dir>` |
   | Scaffold router | `python3 scripts/init_asset.py <name> --type skill --path <dir> --routing-skill` |

3. Define or refine the job.

   - `name`: kebab-case, matching the folder name
   - trigger: user intent and concrete activation contexts
   - output: files, edits, checks, or decisions produced
   - exclusion: nearby requests the skill must skip

4. Use the minimum structure required.

   | Path | Add when |
   | --- | --- |
   | `SKILL.md` | Always |
   | `references/` | Long or conditional knowledge |
   | `scripts/` | Deterministic logic repeated at least twice |
   | `assets/` | Files copied or reused in outputs |
   | `INDEX.csv` + `workflows/` | Multiple workflows share one domain and usually load selectively |

5. Write only `name` and `description` in frontmatter unless the target client requires more.

   - `name`: lowercase letters, numbers, single hyphens; maximum 64 characters
   - `description`: capability, activation contexts, and exclusions; maximum 1024 characters

6. Keep `SKILL.md` focused on the common execution path, global constraints, resource load conditions, and validation. Move passive knowledge to `references/`, deterministic repeated logic to `scripts/`, and output material to `assets/`.

7. Match instruction freedom to task risk.

   - High freedom: state goals and completion criteria.
   - Medium freedom: provide a preferred procedure and parameters.
   - Low freedom: fix commands, order, approvals, and validation for fragile operations.

8. Run the improve loop: validate, edit only the failing or requested area, re-run the same check, and stop when errors are gone and warnings are fixed or accepted.

## Validation

- Frontmatter contains valid `name` and `description`; folder and name match.
- Description triggers correct requests and excludes near misses.
- `SKILL.md` stays under 500 lines or delegates conditional detail.
- Every referenced path resolves and every script is non-interactive with clear exit behavior.
- No duplicated rules, empty directories, unused examples, or nested discoverable `SKILL.md` files.

## Resources

- For routing architecture, read `references/routing-skill-structure.md` before changing `INDEX.csv`, workflow layout, or router behavior.
- Use `scripts/init_asset.py` only for new assets; do not re-scaffold existing skills.
- Use `scripts/validate_asset.py` after every structural change.

## Stop Conditions

- Ask for the destination only when creating a skill and no path is given.
- Stop before renaming an existing skill unless the user explicitly requested the rename.
- Stop before destructive or external actions that require new authority.
