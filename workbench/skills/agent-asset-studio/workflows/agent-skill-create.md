---
name: agent-skill-create
description: USE WHEN: the user wants to create a focused agent skill with minimum structure. EXCLUDES: overwriting an existing skill, renaming without request, or external actions.
---

# Create Agent Skill

## Goal

Create one focused agent skill with the minimum structure and context cost required for its job.

## When to Use

Use this workflow to scaffold and initialize a new agent skill.

## Instructions

- Read [references/agent-skill-frontmatter.md](../references/agent-skill-frontmatter.md) for frontmatter requirements.
- Read `references/routing-skill-structure.md` and `references/routing-skill-algorithm.md` before creating a routing skill.
- Keep `INDEX.csv` under `workflows/` unless the user requests another location.
- Use `scripts/init_asset.py`; do not reconstruct scaffolding manually.
- Stop before overwriting an existing target; route existing-skill changes to `agent-skill-improve`.
- Stop before renaming an existing skill unless explicitly requested.
- Stop before destructive or external actions requiring new authority.

## Workflows

### Arguments

- Target path or destination
- Intended job, triggering requests, outputs, and near-miss exclusions

### Procedure

1. Confirm the target does not exist. If no destination is given, ask for it.
2. Define the skill's single job, triggers, outputs, and exclusions.
3. Scaffold the target with `python3 scripts/init_asset.py <name> --type skill --path <dir>`. Add `--routing-skill` only when multiple workflows share one domain and usually load selectively.
4. Keep only the required structure following [references/agent-skill-directories.md](../references/agent-skill-directories.md).
5. Write frontmatter following [references/agent-skill-frontmatter.md](../references/agent-skill-frontmatter.md).
6. Put the common execution path and constraints in `SKILL.md`; move passive knowledge, repeated logic, and reusable output material to their matching resource directories.
7. Match instruction freedom to risk: goals for flexible work, preferred procedures for bounded work, and exact commands or order for fragile work.
8. Validate with `python3 scripts/validate_asset.py <skill-dir> --type skill`.

### Validation

- Frontmatter matches the specification in [references/agent-skill-frontmatter.md](../references/agent-skill-frontmatter.md).
- Triggers select intended requests and reject near misses.
- Every referenced path resolves; no empty directories, unused examples, duplicated rules, or nested discoverable `SKILL.md` files remain.
