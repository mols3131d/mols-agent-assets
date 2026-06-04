---
name: prd
description: >
  Manage Product Requirement Documents (PRD). Use for product goals, target
  users, user stories, and feature requirements.
version: 1.0.0
---

# Product Requirement Documents (PRD)

Goal: define product value, users, and requirements.

## 1. When to use

- Define product, service, or major feature.
- Clarify what to build and why it matters.
- Align Product, Design, Dev, QA.

## 2. Initialization Script

- Script: `python3 scripts/init_document.py <name> --type prd --path <dir>`
- Name: `prd-[ID]-[Title].md`, e.g. `prd-001-user-onboarding.md` (automatically formatted by the script)

## 3. Authoring Instructions

- Overview/goals: audience + objectives.
- Scenarios/stories: user journey + user stories.
- Requirements: prioritized table.
- UI/UX flow: navigation + expectations.
- Metrics: measurable success criteria.
- Cross-reference: related SPEC/ADR docs.

## 4. Lifecycle Management

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
