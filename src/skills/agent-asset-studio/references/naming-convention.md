# Naming Convention

## 1. Domain Prefixing

- **Purpose**: Categorization/tagging (since folders are not always nested).
- **Rule**: Place 1-2 domain tokens at the front.
- **Example**: `openspec-apply-change.md`, `agent-asset-studio.md`

## 2. Naming Types by Skill Complexity

| Type | Target Skill | Format | Example |
| --- | --- | --- | --- |
| **Verb** | Simple skill (single action) | `<domain>-<verb>-<details>.md` | `coder-generate-code.md` |
| **Object** | Complex skill (multi-action object) | `<domain>-<object>.md` | `task-manager.md` |
| **Place** | Routing/Hub skill (consolidates capabilities) | `<domain>-<details>-<place>.md` | `reviewer-console.md` |

*Note: `<place>` must be a location-based word (e.g., `studio`, `console`, `hub`, `portal`, `workspace`).*
