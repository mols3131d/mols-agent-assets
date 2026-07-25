---
name: naming-convention
description: >
  USE WHEN: naming new agent assets, setting domain prefixes, or using skill complexity patterns.
  EXCLUDES: trigger formatting or routing logic.
---

# Naming Convention

## Domain Prefixing

- Place 1-2 domain tokens at front (e.g., `openspec-apply-change.md`).
- Omit prefix inside routing skill if clear from routing skill name.

## Complexity-based Naming

| Type | Complexity | Format | Example |
| --- | --- | --- | --- |
| **Verb** | Simple (single action) | `<domain>-<verb>-<details>.md` | `coder-generate-code.md` |
| **Object** | Complex (multi-action) | `<domain>-<object>.md` | `task-manager.md` |
| **Place** | Router/Hub (consolidated) | `<domain>-<details>-<place>.md` | `reviewer-console.md` |

*`<place>` must be location word (e.g., `studio`, `console`, `hub`, `portal`, `workspace`).*
