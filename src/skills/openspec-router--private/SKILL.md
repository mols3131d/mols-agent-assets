---
name: openspec-router
description: >
  OpenSpec routing skill. Use when the user asks to work with the OpenSpec
  framework, including exploring ideas, proposing changes, applying tasks,
  syncing specs, archiving changes, or using OpenSpec add-on workflows such as
  TDD. Routes to one OpenSpec sub-skill to keep indexing and context small.
---

# OpenSpec Router

Goal: route OpenSpec work to one focused sub-skill with low context cost.

## Scope

- OpenSpec change lifecycle: explore, propose, apply, sync specs, archive.
- OpenSpec framework tasks that rely on `openspec` CLI state or artifacts.
- OpenSpec add-ons under `sub-skills/openspec-addon-*`.
- Future generated OpenSpec template skills under `sub-skills/`.

## Triggers

Use this skill for requests mentioning:

- OpenSpec, `openspec`, `/opsx`, spec-driven changes, delta specs, change proposals.
- Creating or continuing an OpenSpec change.
- Implementing tasks from an OpenSpec change.
- Syncing delta specs into main specs.
- Archiving or finalizing an OpenSpec change.
- Exploring requirements or designs before/during an OpenSpec change.
- OpenSpec add-on workflows such as TDD.

## Exclusions

- General coding work with no OpenSpec context.
- Generic documentation, ADR, PRD, or task management not tied to OpenSpec.
- Installing or modifying OpenSpec itself unless the user explicitly asks.
- Broad repository exploration after a concrete OpenSpec route is known.

## Sub Skills

Read `sub-skills/INDEX.csv` to identify all matching sub-skills for the request.
- Multi-skill routing: If the request spans multiple categories, select and execute matching sub-skills sequentially.
- Workflow: Load instructions for all matched sub-skills → Plan a step-by-step sequence → Execute and report progress.

If the index is missing or appears stale, discover candidates by listing
`sub-skills/*/SKILL.md` and reading only their frontmatter. Include add-ons whose
folder starts with `openspec-addon-`.

## Routing

| User intent | Route |
| --- | --- |
| Think through idea, investigate problem, clarify requirements | `openspec-explore/SKILL.md` |
| Create a new change proposal and artifacts | `openspec-propose/SKILL.md` |
| Implement or continue tasks from a change | `openspec-apply-change/SKILL.md` |
| Sync delta specs to main specs without archiving | `openspec-sync-specs/SKILL.md` |
| Finalize/archive a completed change | `openspec-archive-change/SKILL.md` |
| TDD/test-first workflow for OpenSpec | best matching `openspec-addon-tdd/SKILL.md` if present |
| Multiple intents | select and execute matching sub-skills sequentially |

## Rules

- Core workflows require the OpenSpec CLI; add-ons may define extra requirements.
- Do not duplicate sub-skill instructions in this router.
- Prefer CLI-derived paths and state over hardcoded OpenSpec directories.
- Read instructions of all matched sub-skills after routing.
- If a change name is ambiguous, follow the selected sub-skill's selection rules.
- If the user is only exploring, do not edit implementation code unless the
  selected sub-skill permits artifact creation.
- Preserve user edits and existing OpenSpec artifacts unless the selected
  workflow requires a scoped update.
- If a request matches multiple sub-skills, load and execute all relevant sub-skills in sequence.

## Extending

- Add each new OpenSpec workflow as `sub-skills/<name>/SKILL.md`.
- Use `openspec-*` for core OpenSpec workflows.
- Use `openspec-addon-*` for community or project-specific add-ons.
- Add one row to `sub-skills/INDEX.csv` with routing signal only.
- Keep this router stable when generated sub-skills change; update it only when
  route categories or global guardrails change.

## Output

Report selected sub-skill, changed files, validation/checks run, and any skipped
OpenSpec step.
