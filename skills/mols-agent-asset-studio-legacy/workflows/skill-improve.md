---
name: skill-improve
description: >-
    Improve existing agent skills while preserving intended behavior. Use for
    scoped workflow, structure, trigger, or instruction changes. Not for
    unrelated behavior, renaming, or broad rewrites.
---

# Improve Agent Skill

## Goal

Improve an existing agent skill while preserving unrelated behavior.

## When to Use

Use this workflow to apply fixes, modify behavior, or update content/structure for an existing skill.

## Instructions

- Read [frontmatter.md](../references/agent-skill/frontmatter.md) for frontmatter rules.
- Read [trigger-guide.md](../references/trigger-guide.md) for trigger updates.
- Read [architecture.md](../references/agent-skill/architecture.md) for structure.
- Follow [backup.md](backup.md) before edits.

## Workflow: Improve Agent Skill

### Arguments from Context

- Existing skill path
- Requested change (behavior, content, or structure)

### Procedure

1. Inspect target with `rg --files <skill-dir>` and run baseline validation.
1. Follow [backup.md](backup.md).
1. Update frontmatter following [trigger-guide.md](../references/trigger-guide.md).
1. Apply minimal changes resolving the request while preserving unrelated behavior.
1. Run [frontmatter-validate.md](frontmatter-validate.md).
1. If workflows changed, run [router-asset-maintain.md](router-asset-maintain.md).

### Validation

- Requested behavior works while unrelated triggers, exclusions, and safety bounds are preserved.
- Structure complies with [architecture.md](../references/agent-skill/architecture.md).
- Each `INDEX.csv` `name` resolves to `workflows/<name>.md`.
