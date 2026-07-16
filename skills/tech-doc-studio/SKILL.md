---
name: tech-doc-studio
description: >
  USE WHEN: the user wants to create, edit, improve, format, or validate technical documents such as ADRs, PRDs, SPECs, design notes, technical tasks, or kanban boards.
  EXCLUDES: business or administrative documents like meeting minutes and general status reports.
---

# Tech Doc Studio

## Goal

Create and maintain technical project docs with minimal context. Route by action intent.

## When to Use

Use when user asks to create, update, improve, validate, or format technical ADR, PRD, SPEC, design notes, tech tasks, or kanban.

## When NOT to Use

Do not use for business or administrative documents (e.g., meeting minutes, status reports).

## Instructions

- Exclusively handles technical documents.
- Use matching template when creating new ADR/PRD/SPEC.
- Update index/status when doc lifecycle changes.
- KISS: one doc, one purpose.
- DRY: do not duplicate source of truth across docs.
- Keep docs actionable: owner, status, date, decision/requirement/task.
- Preserve existing docs unless user asks to rewrite.
- Do not create backups by default. If requested, insert `.original`.
- Prefer tables for status/index data.
- Ask when doc type, target path, or status is unclear.

## Workflows

### Arguments from Context

- Requested ACTION (create, update, improve, validate, format)
- Requested DOC TYPE (adr, prd, spec, design, tasks, kanban, index)

### Procedure

1. Read `workflows/INDEX.csv` once.
2. Select the matching action workflow from `INDEX.csv`.
3. Load the corresponding reference file from `references/<doc_type>.md` to understand structural constraints.
4. Run the selected workflow's validation before completion.

### Validation

- Report changed files, skipped docs, and any missing input.
