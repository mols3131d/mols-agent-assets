---
name: spec
description: >
  Manage implementation specifications (SPEC) for features, data structures,
  APIs, and complex logic.
---

# Specifications (SPEC)

## Overview

- **Goal**: Turn approved requirements or architecture designs into buildable, low-level technical implementation specifications.

## Triggers

- Planning the technical implementation details of a feature.
- Designing complex logic, component structures, APIs, or database schemas.
- Expanding an accepted ADR into buildable steps.

## Exclusions

- High-level product requirement definition or user stories -> use `prd.md`.
- High-level architecture decisions or tech stack trade-offs -> use `adr.md`.

## Workflow

1. Run the initialization script to scaffold the document automatically:
   `python3 scripts/init_document.py <name> --type spec --path <dir>`
2. Describe the problem rationale and business value.
3. Design details: document schemas, API endpoints, logic flow, edge cases, and error states.
4. Keep the spec synchronized when code implementation changes.
5. Update `INDEX.csv` (via `update_index.py`) when the SPEC is created, archived, or updated.

## Resources

- `INDEX.csv`: Index of active specifications in the main folder.
- `spec-*.md`: Individual specification markdown files.
- `archive/`: Archive folder for deprecated, superseded, or rejected specifications.
- `archive/INDEX.csv`: Index of archived specifications.

### Frontmatter Metadata

| Field | Type | Required | Description |
| :--- | :--- | :---: | :--- |
| `id` | String | Y | Unique ID (e.g. `001`, padded to 3 digits) |
| `title` | String | Y | Specification title |
| `status` | Enum | Y | Current status (`draft`, `proposed`, `accepted`, `implemented`, `deprecated`, `superseded`, `rejected`) |
| `description` | String | N | Detailed explanation or summary |
| `categories` | Array | N | Categories list |
| `tags` | Array | N | Tags list for classification |

### SPEC Lifecycle Statuses

| Status | Active | Description |
| :--- | :--- | :--- |
| `draft` | ✅ | Specification is in early drafting stage. |
| `proposed` | ✅ | Specification is proposed and under review. |
| `accepted` | ✅ | Specification is approved but pending implementation. |
| `implemented` | ✅ | Specification is implemented and currently in use. |
| `deprecated` | ❌ | Specification is obsolete or slated for removal. |
| `superseded` | ❌ | Specification has been replaced by a newer specification. |
| `rejected` | ❌ | Specification was not approved. |

### Document Sections

| Section Title | Required? | Purpose & Description |
| :--- | :---: | :--- |
| `## 1. 개요 (Overview)` | **Y** | High-level summary and single goal of the spec. |
| `## 2. 기획 의도 (Rationale)` | **Y** | Problem solved, user value, system contribution. |
| `## 3. 기능 명세 (Functional Specs)` | **Y** | Core behavior, normal flows, exception scenarios. |
| `## 4. 기술 설계 (Technical Design)` | **Y** | Data Flow (Mermaid), schemas, interface/classes. |
| `## 5. 제약 사항 및 예외 처리 (Constraints)` | **Y** | Low-level constraints and error handling logic. |
| `## 6. 품질 및 테스트 기준 (QA)` | N | Verification points, test cases, performance floors. |

Custom sections (e.g., `## Performance Impact`, `## Rollback Strategy`) can be added freely depending on complexity. Optional sections can be omitted or simplified if not applicable.

---

## Rules

- Every SPEC must contain valid frontmatter metadata.
- Follow the defined lifecycle progression path: `draft -> proposed -> accepted|rejected -> implemented`.
- Cross-reference originating ADRs or PRDs.

## Constraints

- **No Duplicated Business Requirements**: Do not copy functional user stories from PRD. Reference/link the PRD instead.
- **Keep it Updated**: Update specifications when the implementation changes. The specification must act as the source of truth for the codebase.
- **Do Not Skip Error Design**: Ensure edge cases, validations, error responses, and failure modes are explicitly designed and documented.
- **Save Original on Rewrite**: Do not overwrite or delete existing specifications without preserving history. Save `<filename>.original.md` before making major changes.
