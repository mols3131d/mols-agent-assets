---
name: design
description: >
  Create or improve design notes for UX, UI, flows, interaction, or system
  structure. Use when user asks for design documentation, wireframe notes,
  screen flow, or design rationale.
---

# Design Notes

## Overview

- **Goal**: Capture design intent, user/system flows, UI/UX structure, and usable decisions.

## Triggers

- User asks for design documentation, wireframe notes, screen flow, or design rationale.
- UI/UX flow needs documentation.
- Screen, component, or interaction behavior needs clarity.
- Design trade-off must be preserved before implementation.

## Exclusions

- Low-level implementation/API/data details -> use `spec.md`.
- Product/user requirement only -> use `prd.md`.
- Architecture decisions -> use `adr.md`.
- Task tracking only -> use `tasks.md` or `kanban.md`.

## Workflow

1. Run the initialization script to scaffold the document automatically:
   `python3 scripts/init_document.py <name> --type design --path <dir>`
2. Fill out Context, Goals, Flow, Decisions, and Open Questions.
3. Keep visual notes textual unless user provides assets.
4. Update `INDEX.csv` (via `update_index.py`) when the design note is created, archived, or updated.

## Resources

- `INDEX.csv`: Index of active design notes in the main folder.
- `design-*.md`: Individual design note markdown files.
- `archive/`: Archive folder for deprecated or superseded design notes.
- `archive/INDEX.csv`: Index of archived design notes.

### Frontmatter Metadata

| Field | Type | Required | Description |
| :--- | :--- | :---: | :--- |
| `id` | String | Y | Unique ID (e.g. `design-001`) |
| `title` | String | Y | Document title |
| `description` | String | N | Detailed explanation or summary |
| `categories` | Array | N | Categories list |
| `tags` | Array | N | Tags list for classification |

### Directory Structure

| Path | Description |
| :--- | :--- |
| `INDEX.csv` | Index of active design notes in the main folder |
| `design-*.md` | Individual design note markdown files |
| `archive/` | Archive folder for deprecated or superseded design notes |
| `archive/INDEX.csv` | Index of archived design notes |

### Document Sections

| Section Title | Required? | Purpose & Description |
| :--- | :---: | :--- |
| `## Context` | **Y** | Problem context, target users, and constraints. |
| `## Goals` | **Y** | Desired user/system outcomes. |
| `## Flow` | N | Screen steps, transitions, triggers, and states. |
| `## Decisions` | **Y** | Selected design approach and rationale. |
| `## Open Questions` | **Y** | Unresolved choices and design trade-offs. |

Custom sections (e.g., `## Interactive Prototyping`, `## Accessibility (a11y)`) can be added freely depending on complexity. Optional sections can be omitted or simplified if not applicable.

---

## Rules

- Target is a folder, not the whole repo.
- Markdown frontmatter is the absolute source of truth.
- Fill in all required fields (`id`, `title`) in the frontmatter metadata.
- Keep the metadata index synced after lifecycle state changes.

## Constraints

- **No Implementation Details**: Do not write low-level implementation details (data schemas, API response structures, or business logic code) in design notes.
- **Avoid Vague Flows**: Do not write abstract flows. Clearly specify concrete screen steps, navigation transitions, triggers, and states.
- **Document Unresolved Choices**: Do not hide unresolved decisions. Document open questions and design trade-offs explicitly.
- **Describe Visuals Textually**: Do not rely solely on visual assets (wireframes/images). Describe screen structures and interaction behavior textually.
- Before editing an existing design note, save `<filename>.original.md`.
