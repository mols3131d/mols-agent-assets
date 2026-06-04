---
name: prd
description: >
  Manage Product Requirement Documents (PRD). Use for product goals, target
  users, user stories, and feature requirements.
version: 1.0.0
---

# Product Requirement Documents (PRD)

Goal: define product value, users, and requirements.

## Use When

- Define product, service, or major feature.
- Clarify what to build and why it matters.
- Align Product, Design, Dev, QA.

## Frontmatter (Metadata)

| Field | Type | Required | Description |
| :--- | :--- | :---: | :--- |
| `id` | String | Y | Unique ID (e.g. `001`, padded to 3 digits) |
| `title` | String | Y | Document title |
| `status` | Enum | Y | Current status (`draft`, `proposed`, `approved`, `developing`, `released`, `rejected`, `deprecated`, `superseded`) |
| `description` | String | N | Detailed explanation or summary |
| `categories` | Array | N | Categories list |
| `tags` | Array | N | Tags list for classification |

## Structure

| Path | Description |
| :--- | :--- |
| `INDEX.csv` | Index of active PRDs in the main folder |
| `prd-*.md` | Individual PRD markdown files |
| `archive/` | Archive folder for deprecated, superseded, or rejected PRDs |
| `archive/INDEX.csv` | Index of archived PRDs |

## Lifecycle Management

### Status

| Status | Active | Description |
| :--- | :--- | :--- |
| `draft` | ✅ | Requirement definition is in early drafting stage. |
| `proposed` | ✅ | Requirement is proposed and under review/alignment. |
| `approved` | ✅ | Requirement is approved by stakeholders and ready for dev. |
| `developing` | ✅ | Requirement is currently in active implementation. |
| `released` | ✅ | Feature is deployed to production and under evaluation. |
| `rejected` | ❌ | Requirement was reviewed and not approved. |
| `deprecated` | ❌ | Requirement/feature is obsolete or removed. |
| `superseded` | ❌ | Requirement has been replaced by a newer PRD. |

Lifecycle: `draft -> proposed -> approved|rejected -> developing -> released`.

## Authoring Instructions

- **Initialization Script**: Run `python3 scripts/init_document.py <name> --type prd --path <dir>` to scaffold the document automatically.
- **Overview & Goals**: Clearly identify the target audience and business objectives.
- **User Scenarios**: Document user journeys and structured user stories.
- **Requirements**: Define functional and non-functional requirements in a prioritized table.
- **UI/UX Flow**: Detail layout expectations and interaction navigation.
- **Metrics**: Specify measurable KPIs and success criteria.
- **Cross-Reference**: Link related SPEC or ADR documents.

## Constraints

- **No Implementation Specifics**: Do not specify architectural details, code libraries, database schemas, or low-level API responses. Use `spec.md` instead.
- **Measurable Goals Only**: Avoid vague product success metrics (e.g. "make it fast"). Define clear, quantifiable KPIs.
- **Cross-Reference Dependencies**: Ensure external team or system dependencies are called out and linked.
- **Save Original on Rewrite**: Do not overwrite or delete existing specifications without preserving history. Save `<filename>.original.md` before making major changes.
