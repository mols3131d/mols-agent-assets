---
name: agent-skill-improve
description: USE WHEN: improving an existing agent skill's behavior or structure. EXCLUDES: changing unrelated behavior, renaming, or massive rewrites.
---

# Improve Agent Skill

## Goal

Improve an existing agent skill while preserving unrelated behavior.

## When to Use

Use this workflow to apply fixes, modify behavior, or update content/structure for an existing skill.

## Instructions

- Read [references/agent-skill-frontmatter.md](../../references/skill/agent-skill-frontmatter.md) for frontmatter rules.
- Read [references/trigger-description-guide.md](../../references/core/trigger-description-guide.md) for trigger updates.
- Read [references/agent-skill-directories.md](../../references/skill/agent-skill-directories.md) for structural requirements.
- Follow backup protocol in [agent-asset-backup.md](../asset/agent-asset-backup.md) before edits.
- Use `scripts/validate_asset.py` after structural edits.

## Workflow: Improve Agent Skill

### Arguments from Context

- Existing skill path
- Requested change (behavior, content, or structure)

### Procedure

1. Inspect target with `rg --files <skill-dir>` and run baseline validation.
2. Follow backup protocol in [agent-asset-backup.md](../asset/agent-asset-backup.md).
3. Update frontmatter (`USE WHEN:`, `EXCLUDES:`) following [references/core/trigger-description-guide.md](../../references/core/trigger-description-guide.md).
4. Apply minimal changes resolving the request while preserving unrelated behavior.
5. Re-run `python3 scripts/validate_asset.py <skill-dir> --type skill`.

### Validation

- Requested behavior works while unrelated triggers, exclusions, and safety bounds are preserved.
- Structure complies with [references/agent-skill-directories.md](../../references/skill/agent-skill-directories.md).
- Referenced paths and route `id` entries in `INDEX.csv` resolve.
