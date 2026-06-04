---
name: spec
description: >
  Manage implementation specifications (SPEC) for features, data structures,
  APIs, and complex logic.
---

# Specifications (SPEC)

Goal: turn approved intent into implementation detail.

## Use When

- Plan implementation of a feature.
- Design complex logic/component/API/data.
- Expand accepted ADR into buildable detail.

## Frontmatter (Metadata)

| Field | Type | Required | Description |
| :--- | :--- | :---: | :--- |
| `id` | String | Y | Unique ID (e.g. `001`, padded to 3 digits) |
| `title` | String | Y | Specification title |
| `status` | Enum | Y | Current status (`draft`, `proposed`, `accepted`, `implemented`, `deprecated`, `superseded`, `rejected`) |
| `description` | String | N | Detailed explanation or summary |
| `categories` | Array | N | Categories list |
| `tags` | Array | N | Tags list for classification |

## Structure

| Path | Description |
| :--- | :--- |
| `INDEX.csv` | Index of active specifications in the main folder |
| `spec-*.md` | Individual specification markdown files |
| `archive/` | Archive folder for deprecated, superseded, or rejected specifications |
| `archive/INDEX.csv` | Index of archived specifications |

## Lifecycle Management

### Status

| Status | Active | Description |
| :--- | :--- | :--- |
| `draft` | ✅ | Specification is in early drafting stage. |
| `proposed` | ✅ | Specification is proposed and under review. |
| `accepted` | ✅ | Specification is approved but pending implementation. |
| `implemented` | ✅ | Specification is implemented and currently in use. |
| `deprecated` | ❌ | Specification is obsolete or slated for removal. |
| `superseded` | ❌ | Specification has been replaced by a newer specification. |
| `rejected` | ❌ | Specification was not approved. |

Lifecycle: `draft -> proposed -> accepted|rejected -> implemented`.

## Authoring Instructions

- **Initialization Script**: Run `python3 scripts/init_document.py <name> --type spec --path <dir>` to scaffold the document automatically.
- **Rationale**: Describe the problem and business value.
- **Design Detail**: Document schemas, APIs, logic flow, and error states.
- **Source of Truth**: Update this document whenever code logic shifts.
- **Cross-Reference**: Explicitly link originating ADRs or PRDs.

## Constraints

- **No Duplicated Business Requirements**: Do not copy functional user stories from PRD. Reference/link the PRD instead.
- **Keep it Updated**: Update specifications when the implementation changes. The specification must act as the source of truth for the codebase.
- **Do Not Skip Error Design**: Ensure edge cases, validations, error responses, and failure modes are explicitly designed and documented.
- **Save Original on Rewrite**: Do not overwrite or delete existing specifications without preserving history. Save `<filename>.original.md` before making major changes.
