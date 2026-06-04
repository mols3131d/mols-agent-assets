---
name: design
description: >
  Create or improve design notes for UX, UI, flows, interaction, or system
  structure. Use when user asks for design documentation, wireframe notes,
  screen flow, or design rationale.
---

# Design Notes

Goal: capture design intent and usable decisions.

## Use When

- UI/UX flow needs documentation.
- Screen, component, or interaction behavior needs clarity.
- Design tradeoff must be preserved before implementation.

## Frontmatter (Metadata)

| Field | Type | Required | Description |
| :--- | :--- | :---: | :--- |
| `id` | String | Y | Unique ID (e.g. `design-001`) |
| `title` | String | Y | Document title |
| `description` | String | N | Detailed explanation or summary |
| `categories` | Array | N | Categories list |
| `tags` | Array | N | Tags list for classification |

## Structure

| Path | Description |
| :--- | :--- |
| `INDEX.csv` | Index of active design notes in the main folder |
| `design-*.md` | Individual design note markdown files |
| `archive/` | Archive folder for deprecated or superseded design notes |
| `archive/INDEX.csv` | Index of archived design notes |

## Write

| Section | Content |
| --- | --- |
| Context | problem, users, constraints |
| Goals | desired user/system outcome |
| Flow | steps, states, navigation |
| Decisions | chosen design + why |
| Open Questions | unresolved choices |

Keep visual notes textual unless user provides assets.

## Constraints

- **No Implementation Details**: Do not write low-level implementation details (data schemas, API response structures, or business logic code) in design notes. Use `spec.md` instead.
- **No Duplicate Requirements**: Do not copy functional or non-functional requirements from PRD. Cross-reference the PRD document via links.
- **Avoid Vague Flows**: Do not write abstract flows. Clearly specify concrete screen steps, navigation transitions, triggers, and states.
- **Document Unresolved Choices**: Do not hide unresolved decisions. Document open questions and design trade-offs explicitly.
- **Describe Visuals Textually**: Do not rely solely on visual assets (wireframes/images). Describe screen structures and interaction behavior textually.
- **Preserve History**: Do not make destructive edits to existing design notes. Save `<filename>.original.md` before making major changes.
