# Copilot Hooks Spec

## Paths
- **WS**: `.github/hooks/*.json`
- **WS Local**: `.claude/settings.local.json`
- **User**: `~/.claude/settings.json`

## Events
- `SessionStart` | `UserPromptSubmit` | `PreToolUse` | `PostToolUse` | `PreCompact` | `SubagentStart` | `SubagentStop` | `Stop`

## Schema
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "type": "command",
        "command": "string",
        "timeout": 15
      }
    ]
  }
}
```

