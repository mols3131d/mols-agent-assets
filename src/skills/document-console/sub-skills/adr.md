---
name: adr
description: >
  Manage Architecture Decision Records (ADR). Use when documenting technical
  decisions, architecture patterns, stack choices, or system trade-offs.
---

## Overview

- Goal: record architecture decisions, context, consequences, and lifecycle.
- Output: ADR file plus index/status update when needed.

## Triggers

- User asks for ADR, architecture decision, tech choice, or trade-off record.
- Core stack, pattern, dependency, data store, API style, or platform changes.
- Existing decision needs status update, supersession, or deprecation.

## Exclusions

- Product/user requirement only -> use `prd.md`.
- Implementation/API/data detail only -> use `spec.md`.
- Task tracking only -> use `tasks.md` or `kanban.md`.

## Rules

- Use initialization script: `python3 scripts/init_document.py <name> --type adr --path <dir>`.
- Name files as `adr-[ID]-[Title].md`, e.g. `adr-001-database.md` (automatically formatted by the script).
- Include context, decision, consequences, and status.
- Link related SPEC docs when implementation detail exists.
- Update `INDEX.md` when ADR is created, archived, or status changes.

| Status | Active | Use when |
| --- | --- | --- |
| `proposed` | yes | under review |
| `accepted` | yes | approved, not fully active |
| `active` | yes | implemented/current |
| `deprecated` | no | obsolete/removing |
| `superseded` | no | replaced by newer ADR |
| `rejected` | no | not approved |

Lifecycle: `proposed -> accepted|rejected -> active|superseded|deprecated`.

## Constraints

- Do not write ADR for minor implementation detail.
- Do not hide trade-offs; record negative consequences.
- Do not change existing accepted/active ADR without preserving original.
- Before editing existing ADR, save `<filename>.original.md`.
