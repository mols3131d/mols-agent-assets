---
name: prd
description: >
  Manage Product Requirement Documents (PRD). Use for product goals, target
  users, user stories, and feature requirements.
version: 1.0.0
---

# Product Requirement Documents (PRD)

## Overview

- **Goal**: Define product value, target users, user scenarios, and features to align stakeholders.

## Triggers

- User asks to define a new product, service, or major feature.
- Clarify what to build and why it matters.
- Align Product, Design, Dev, QA stakeholders.

## Exclusions

- Architectural decisions or tech stack trade-offs -> use `adr.md`.
- Low-level implementation details, code specifics, database schemas, or API designs -> use `spec.md`.

## Workflow

1. Run the initialization script to scaffold the document automatically:
   `python3 scripts/init_document.py <name> --type prd --path <dir>`
2. Clearly identify the target audience and business objectives.
3. Document user journeys and structured user stories.
4. Define functional and non-functional requirements in a prioritized table.
5. Detail layout expectations and interaction navigation.
6. Specify measurable KPIs and success criteria.
7. Update `INDEX.csv` (via `update_index.py`) when the PRD is created, archived, or updated.

## Resources

- `INDEX.csv`: Index of active PRDs in the main folder.
- `prd-*.md`: Individual PRD markdown files.
- `archive/`: Archive folder for deprecated, superseded, or rejected PRDs.
- `archive/INDEX.csv`: Index of archived PRDs.

### Frontmatter Metadata

| Field | Type | Required | Description |
| :--- | :--- | :---: | :--- |
| `id` | String | Y | Unique ID (e.g. `001`, padded to 3 digits) |
| `title` | String | Y | Document title |
| `status` | Enum | Y | Current status (`draft`, `proposed`, `approved`, `developing`, `released`, `rejected`, `deprecated`, `superseded`) |
| `description` | String | N | Detailed explanation or summary |
| `categories` | Array | N | Categories list |
| `tags` | Array | N | Tags list for classification |

### PRD Lifecycle Statuses

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

### Document Sections

| Section Title | Required? | Purpose & Description |
| :--- | :---: | :--- |
| `## 1. 개요 (Overview)` | **Y** | Definition, Target Audience, Goals & Non-Goals. |
| `## 2. 기획 배경 및 가치 (Rationale)` | **Y** | Problem definition, core value, assumptions, risks. |
| `## 3. 사용자 시나리오 및 스토리 (User Stories)` | N | User stories and user journeys/flows. |
| `## 4. 기능 및 비기능 요구사항 (Requirements)` | **Y** | Functional and non-functional requirement tables. |
| `## 5. UI/UX 요구사항 (User Experience)` | N | Mermaid diagrams, screen layout specs. |
| `## 6. 인수 조건 (Acceptance Criteria)` | **Y** | Final criteria (Given-When-Then format) for DoD. |
| `## 7. 성공 지표 및 모니터링 (Success Metrics)` | N | Quantitative KPIs and logs to track. |
| `## 8. 제약 사항 및 출시 계획 (Constraints & Release Plan)` | **Y** | Tech constraints and phasing plans. |

Custom sections (e.g., `## Security Concerns`, `## Out of Scope`) can be added freely depending on complexity. Optional sections can be omitted or simplified if not applicable.

---

## Rules

- Every PRD must contain valid frontmatter metadata.
- Cross-reference related SPEC or ADR documents.
- Follow the defined lifecycle progression path: `draft -> proposed -> approved|rejected -> developing -> released`.

## Constraints

- **No Implementation Specifics**: Do not specify architectural details, code libraries, database schemas, or low-level API responses. Use `spec.md` instead.
- **Measurable Goals Only**: Avoid vague product success metrics (e.g. "make it fast"). Define clear, quantifiable KPIs.
- **Cross-Reference Dependencies**: Ensure external team or system dependencies are called out and linked.
- **Save Original on Rewrite**: Do not overwrite or delete existing specifications without preserving history. Save `<filename>.original.md` before making major changes.
