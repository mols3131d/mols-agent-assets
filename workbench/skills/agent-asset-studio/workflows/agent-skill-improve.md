---
name: agent-skill-improve
description: USE WHEN: the user wants to improve an existing agent skill's behavior or structure. EXCLUDES: changing unrelated behavior, renaming, or massive rewrites.
---

# Improve Agent Skill

## Goal

Improve one existing agent skill while preserving behavior outside the requested change.

## When to Use

Use this workflow to apply fixes, modify behavior, or update content and structure for an existing skill.

## Instructions

- Read [references/agent-skill-frontmatter.md](../references/agent-skill-frontmatter.md) for frontmatter requirements.
- Read [references/agent-skill-directories.md](../references/agent-skill-directories.md) for structural requirements.
- Read `references/routing-skill-structure.md` only for routing architecture changes.
- Read `references/routing-skill-algorithm.md` only for router behavior changes.
- Use `scripts/validate_asset.py` after every structural change.
- Stop before renaming unless the user explicitly requested it.
- Stop before changing behavior outside the requested scope.
- Stop before destructive or external actions requiring new authority.

## Workflows

### Arguments

- Existing skill path
- Requested behavior, content, or structural change

### Procedure

1. Inspect the target with `rg --files <skill-dir>` and run baseline validation.
2. Read the frontmatter and only the files tied to the request or failing checks.
3. Save each existing Markdown file immediately before editing it as `<filename>.original.md`.
4. Define the affected triggers, outputs, exclusions, and constraints. Preserve all unrelated behavior.
5. Prefer focused checks such as `rg "<term>" <skill-dir>` for duplication and `wc -l <files>` for context size.
6. Make the smallest change that resolves the requested issue. Do not re-scaffold the existing skill.
7. Read `references/routing-skill-structure.md` for index or layout changes. Read `references/routing-skill-algorithm.md` for selection, ambiguity, or loading changes.
8. Re-run `python3 scripts/validate_asset.py <skill-dir> --type skill`. Fix only requested or failing areas until errors are gone and warnings are fixed or explicitly accepted.

### Validation

- Requested behavior works and unrelated triggers, exclusions, and safety constraints remain intact.
- Frontmatter matches the specification in [references/agent-skill-frontmatter.md](../references/agent-skill-frontmatter.md).
- File and directory structure complies with [references/agent-skill-directories.md](../references/agent-skill-directories.md).
- Every referenced path and route `id` resolves relative to its `INDEX.csv`.
