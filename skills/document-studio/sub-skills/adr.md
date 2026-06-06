---
name: adr
description: >
  Manage Architecture Decision Records (ADR). Use when documenting technical
  decisions, architecture patterns, stack choices, or system trade-offs.
---

# Architecture Decision Records (ADR)

## Overview

- **Goal**: Record architecture decisions, context, consequences, and lifecycle to preserve technical choices.

## Triggers

- User asks for an ADR, architecture decision, tech choice, or trade-off record.
- Core stack, pattern, dependency, data store, API style, or platform changes.
- Existing decision needs a status update, supersession, or deprecation.

## Exclusions

- Product/user requirement only -> use `prd.md`.
- Implementation/API/data detail only -> use `spec.md`.
- Task tracking only -> use `tasks.md` or `kanban.md`.

## Workflow

1. Run the initialization script to scaffold the document automatically:
   `python3 scripts/init_document.py <name> --type adr --path <dir>`
2. Name files as `adr-[ID]-[Title].md`, e.g. `adr-001-database.md` (automatically formatted by the script).
3. Document context, decision rationale, consequences, and status.
4. Reference relevant SPEC documents where implementation details exist.
5. Update `INDEX.csv` (via `update_index.py`) when the ADR is created, archived, or its status changes.

## Resources

- `INDEX.md`: Active document index.
- `INDEX.csv`: Metadata index of active documents.
- `archive/INDEX.md`: Inactive/archived document index.
- `archive/INDEX.csv`: Metadata index of archived documents.

### Document Sections

| Section Title | Required? | Purpose & Description |
| :--- | :---: | :--- |
| `## Context (배경)` | **Y** | Explains background and problem context. |
| `## Decision (결정)` | **Y** | Explains selection and rationale. |
| `## Consequences (결과)` | **Y** | Explains consequences, trade-offs, and risks. |

Custom sections (e.g., `## Alternatives Considered`, `## Implementation Plan`) can be added freely depending on complexity.

---

## Rules

- Use the initialization script to maintain auto-incrementing ID assignment.
- Link related SPEC docs when implementation details exist.
- Keep the metadata index synced after lifecycle state changes.

### Lifecycle Statuses

| Status | Active | Use when |
| --- | --- | --- |
| `proposed` | yes | under review |
| `accepted` | yes | approved, not fully active |
| `active` | yes | implemented/current |
| `deprecated` | no | obsolete/removing |
| `superseded` | no | replaced by newer ADR |
| `rejected` | no | not approved |

Lifecycle path: `proposed -> accepted|rejected -> active|superseded|deprecated`.

## Constraints

- Do not write ADR for minor implementation details.
- Do not hide trade-offs; record negative consequences.
- Do not change existing accepted/active ADR without preserving original.
- Before editing an existing ADR, save `<filename>.original.md`.
