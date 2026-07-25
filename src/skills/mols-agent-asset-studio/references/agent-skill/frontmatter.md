---
name: agent-skill-frontmatter
description: >-
  Define or validate Agent Skill frontmatter properties such as name, description, and user-invocable. Use when creating or modifying skill metadata. Not for directory structure, naming, or route tables.
---

# Skill Frontmatter

Frontmatter specification for agent skills.

## Fields

### `name`

- Required: ✅
- Format: Lowercase kebab-case, match skill folder name.
- Length: Max 64 chars.

### `description`

- Required: ✅
- Content: Clearly state capability, activation contexts, exclusions.
- Length: Max 1024 chars.

### `argument-hint`

- Required: ❌
- Format: Parameter hint string shown in slash command UI.
- Support: VS Code Copilot, Claude Code.

### `user-invocable`

- Required: ❌
- Format: Boolean (`true` | `false`). Controls visibility in slash command menu.
- Support: VS Code Copilot, Cursor.

### `disable-model-invocation`

- Required: ❌
- Format: Boolean (`true` | `false`). Prevents automatic model discovery/invocation.
- Support: VS Code Copilot, Claude Code, Cursor.

### `license`

- Required: ❌
- Format: SPDX license identifier string (e.g. `MIT`, `Apache-2.0`).
- Support: agentskills.io Spec.

### `compatibility`

- Required: ❌
- Format: Environment compatibility details (e.g. OS, tools, dependencies).
- Support: agentskills.io Spec.

### `metadata`

- Required: ❌
- Format: Key-value dictionary for arbitrary custom metadata.
- Support: agentskills.io Spec.

### `allowed-tools`

- Required: ❌
- Format: Space-delimited string or list of pre-approved tool names/aliases.
- Support: agentskills.io Spec.

## Client Support Matrix

| Field | VS Code Copilot | Claude Code | Cursor | OpenAI Codex | Google Antigravity | agentskills.io Spec |
|---|---|---|---|---|---|---|
| `name` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `description` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `argument-hint` | ✅ | ✅ | ❌ | ❌ | ❌ | |
| `user-invocable` | ✅ | ❌ | ✅ | ❌ | ❌ | |
| `disable-model-invocation` | ✅ | ✅ | ✅ | ❌ | ❌ | |
| `license` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| `compatibility` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| `metadata` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| `allowed-tools` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

## Rules

- Write only `name`, `description` unless target client requires more.
