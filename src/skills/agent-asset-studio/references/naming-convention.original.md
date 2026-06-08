# Naming Convention

Terse style guide for agent asset naming conventions.

## 1. Domain Prefixing (도메인 접두사)

- **Purpose**: Since nested folders are not supported in all execution environments, prefixes are used as tags/directories for categorization.
- **Rule**: Place **1 to 2 domain tokens** at the front of the filename to group related assets.
- **Examples**:
  - `openspec-apply-change.md` (Domain: `openspec`)
  - `agent-asset-studio.md` (Domains: `agent`, `asset`)

## 2. Naming Types (이름의 유형)

Based on the scope and design of the skill, choose one of the three naming structures:

### A. 동사형 (Verb Type)
- **Scope**: Single-purpose, action-oriented procedural workflows.
- **Format**: `<domain>-<verb>-<details>.md`
- **Example**: `coder-generate-code.md`, `compress-file.md`

### B. 객체형 (Object Type)
- **Scope**: Multi-purpose skills that manage multiple actions and rules grouped around a specific domain object.
- **Format**: `<domain>-<object>.md`
- **Example**: `task-manager.md`, `agent-reviewer.md`

### C. 장소형 (Place Type)
- **Scope**: Interactive routing hubs, workspaces, or portals where multiple domain objects and capabilities are consolidated.
- **Format**: `<domain>-<details>-<place>.md` (where `<place>` is a place-like word such as `studio`, `console`, `hub`, `portal`, `workspace`, etc.)
- **Example**: `agent-asset-studio.md`, `reviewer-console.md`
