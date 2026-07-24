---
name: agent-skill-create
description: USE WHEN: creating a focused agent skill with minimum structure. EXCLUDES: overwriting existing skills, renaming without request, or external actions.
---

# Create Agent Skill

## Goal

Create one focused agent skill with minimum structure and context cost.

## When to Use

Use this workflow to scaffold and initialize a new agent skill.

## Instructions

- Read [references/agent-skill-frontmatter.md](../../references/skill/agent-skill-frontmatter.md) for frontmatter rules.
- Read [references/routing-skill-structure.md](../../references/router/routing-skill-structure.md) for routing skills.
- Use `scripts/init_asset.py`; do not construct scaffolding manually.
- Stop before overwriting existing target (`agent-skill-improve`) or renaming (`agent-asset-naming`).

## Workflow: Create Agent Skill

### Arguments from Context

- Target path and intended job
- Triggers, outputs, and exclusions

### Procedure

1. Confirm target path does not exist.
2. Define skill job, triggers, outputs, and exclusions.
3. Scaffold using `python3 scripts/init_asset.py <name> --type skill --path <dir>`.
4. Retain minimal structure per [references/skill/agent-skill-directories.md](../../references/skill/agent-skill-directories.md).
5. Write frontmatter following [references/skill/agent-skill-frontmatter.md](../../references/skill/agent-skill-frontmatter.md).
6. Put execution rules in `SKILL.md`; move passive knowledge to `references/` or `assets/`.
7. Validate with `python3 scripts/validate_asset.py <skill-dir> --type skill`.

### Validation

- Frontmatter complies with [references/skill/agent-skill-frontmatter.md](../../references/skill/agent-skill-frontmatter.md).
- Referenced paths resolve; no empty directories or unused examples.
