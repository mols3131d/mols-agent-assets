---
name: "session-bridge"
description: "Protocol for session-bridging via narrative context and entry points using the Toon (.toon) format."
---

# Session-Bridge (Toon Edition)

This skill ensures continuity between agent sessions by capturing the logical delta, design intent, and immediate next steps in a structured `.toon` file.

## When to use this skill

- **Session End**: Before finishing a task or being dismissed, to record the current state.
- **Session Start**: To parse the previous session's bridge and resume work immediately.

## How to use it

### 1. Generate the Bridge

Create or update `.agents/brain/bridge.toon` using the following schema:

```toon
bridge:
  meta:
    timestamp: "[ISO-8601]"
    status: "[active|blocked|complete]"

  narrative: >
    [Direct, high-density description of what was achieved,
    the design logic used, and any technical compromises made.]

  hurdles[N]{id,description,impact}:
    [id],[A specific problem encountered],[Effect on progress]

  entry_points[N]{id,priority,task,tool_hint}:
    [id],[high|med|low],[Concrete next action],[Suggested tool]
```

### 2. Principles

- **Delta Only**: Don't repeat what's in the repo or long-term docs. Only record the "hot" logical context.
- **Strict Toon**: Ensure the YAML header and CSV body are correctly formatted for machine parsing.

## Assets

- Template: `.agents/skills/session-bridge/assets/handover.toon`
