---
name: document-console
description: >
  Document workspace console. Use when user asks to create, improve, index,
  validate, or organize ADR, PRD, SPEC, design notes, tasks, kanban, or document
  collections.
---

# Document Console

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

1. Read `sub-skills/INDEX.csv`.
2. Pick one sub-skill.
3. Read only picked sub-skill.
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

## Output

Report changed files, skipped docs, and any missing input.
