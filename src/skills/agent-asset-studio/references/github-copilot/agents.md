# Copilot Custom Agents Spec

## Paths

- **WS**: `.github/agents/*.agent.md`
- **User**: `{{VSCODE_USER_PROMPTS_FOLDER}}/agents/*.agent.md`

## Frontmatter Schema

```yaml
---
name: string
description: string
tools: [read|edit|search|execute|web|todo]
model: string
user-invocable: boolean
disable-model-invocation: boolean
agents: [string]
hooks:
  PreToolUse:
    - type: command
      command: string
---
```
