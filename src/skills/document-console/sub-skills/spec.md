---
name: spec
description: >
  Manage implementation specifications (SPEC) for features, data structures,
  APIs, and complex logic.
version: 1.0.0
---

# Specifications (SPEC)

Goal: turn approved intent into implementation detail.

## 1. When to use

- Plan implementation of a feature.
- Design complex logic/component/API/data.
- Expand accepted ADR into buildable detail.

## 2. Initialization Script

- Script: `python3 scripts/init_document.py <name> --type spec --path <dir>`
- Name: `spec-[ID]-[Title].md`, e.g. `spec-001-user-auth.md` (automatically formatted by the script)

## 3. Authoring Instructions

- Rationale: problem + value.
- Design: schema/API/logic/errors.
- Source of truth: update when code changes.
- Cross-reference: originating ADR/PRD.

## 4. Lifecycle Management

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
