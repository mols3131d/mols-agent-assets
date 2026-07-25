---
name: skill-create
description: >-
    Create focused agent skills with minimum structure and context cost. Use to
    scaffold a new skill from its job, triggers, outputs, and exclusions. Not for
    overwriting skills, unrequested renames, or external actions.
---

# Create Agent Skill

## Instructions

- Read [frontmatter.md](../references/agent-skill/frontmatter.md) for frontmatter rules.
- Read [architecture.md](../references/agent-skill/architecture.md) for routing skills.
- Create only the minimum required files; do not add unused scaffold resources.
- Stop before overwriting or renaming an existing target.

## Workflow: Create Agent Skill

### Arguments from Context

- Target path and intended job
- Triggers, outputs, and exclusions

### Procedure

1. Confirm target path does not exist.
2. Define skill job, triggers, outputs, and exclusions.
3. Create `SKILL.md` with the minimum structure in [architecture.md](../references/agent-skill/architecture.md).
4. Write frontmatter following [frontmatter.md](../references/agent-skill/frontmatter.md).
5. Put execution rules in `SKILL.md`; move passive knowledge to `references/` or `assets/`.
6. Run [frontmatter-validate.md](frontmatter-validate.md).
7. For routing skills, run [router-asset-maintain.md](router-asset-maintain.md).

### Validation

- Frontmatter complies with [frontmatter.md](../references/agent-skill/frontmatter.md).
- Referenced paths resolve; no empty directories or unused examples.
