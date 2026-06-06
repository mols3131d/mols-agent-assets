---
name: asset-naming
description: >
  WHAT: Suggest, validate, or apply agent asset names.
  WHEN: User asks to name, rename, suggest, or check naming conventions of skills/rules.
  WHEN NOT: General coding or non-naming tasks.
  KEYWORDS: name, naming, naming-convention, rename, suggest-name
---

# asset-naming

Ensure agent assets follow correct naming conventions.

## Goal & Done Criteria

- **Goal**: Apply or validate asset names according to conventions.
- **Done Criteria**:
  - Suggested/applied names comply with [naming-convention.md](../references/naming-convention.md).
  - Existing skill names are NEVER changed unless the user explicitly instructs to do so.

## Workflow

1. **Inspect Target**:
   - Determine if target is a new or existing asset.
   - If existing, enforce the safety constraint: **NEVER rename unless user explicitly commanded it**.
2. **Apply Naming Convention**:
   - Refer to [naming-convention.md](../references/naming-convention.md).
   - Format: `<domain>-<verb>-<details>.md` for standard skills, `<domain>-<details>-<location>.md` for routing skills.
