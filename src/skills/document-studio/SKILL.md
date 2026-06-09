---
name: document-studio
description: >
  Document workspace studio. Use when user asks to create, improve, index,
  validate, or organize ADR, PRD, SPEC, design notes, tasks, kanban, or document
  collections.
---

# Document Studio

Goal: create and maintain project docs with minimal context. Route by doc type.

## Scope

- ADR: architecture decisions.
- PRD: product requirements.
- SPEC: implementation specs.
- Design: UX/UI/system design notes.
- Tasks: actionable work items.
- Kanban: status board.
- Index: document inventory.

## Flow

- Multi-skill routing: If the request spans multiple categories, select and execute matching sub-skills sequentially.
- Workflow: Load instructions for all matched sub-skills → Plan a step-by-step sequence → Execute and report progress.

1. Read `sub-skills/INDEX.csv` to identify all matching sub-skills for the request.
2. If a single sub-skill matches, read only that sub-skill file.
3. If multiple sub-skills match, load all matched sub-skill files, plan a sequential workflow, and execute each step while reporting progress.
4. Use matching template when creating new ADR/PRD/SPEC.
5. Update index/status when doc lifecycle changes.

## Rules

- KISS: one doc, one purpose.
- DRY: do not duplicate source of truth across docs.
- Keep docs actionable: owner, status, date, decision/requirement/task.
- Preserve existing docs unless user asks to rewrite.
- Before editing existing file, save `<filename>.original.md`.
- Prefer tables for status/index data.
- Ask when doc type, target path, or status is unclear.
- If a request matches multiple sub-skills, load and execute all relevant sub-skills in sequence.

## Output

Report changed files, skipped docs, and any missing input.
