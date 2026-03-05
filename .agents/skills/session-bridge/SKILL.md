---
name: "session-bridge"
description: "Protocol for session-bridging and task management using Markdown (MD)."
---

# Session-Bridge

> Ensures agent session continuity.

> **TARGET_FILE**: `.agents/brain/session-bridge.md`

## Activation

- **Session End**: Summarize achieved deltas and define the pivot for the next agent.
- **Session Start**: Load `TARGET_FILE` to restore the logical thread.

## Execution Protocol

Maintain `TARGET_FILE` with zero-loss, high-density structure:

```markdown
# Session-Bridge

- Intent: `[High-level goal]`
- Status: `[DONE | PARTIAL | BLOCKED]`

## Narrative

- `[Event / Change]` -> `[Reasoning / Intent]`

## Todo

- [x] `[Atomic Task]`
- [-] `[Current Task]`
- [ ] `[Pending Task]`

## Hurdles

- [ ] `[Issue]`: `[Description/Impact]`
```

## Core Principles

1. **Relative Paths**: Use paths relative to the project root (no leading slashes).
2. **Delta-Only**: Record only what is hot or just changed. Zero-redundancy.
3. **KISS/DRY**: Use concise bullets/checkboxes instead of prose. Be extremely minimal.
4. **Intent-Centric**: Every change must have a `-> [Reason]`.
5. **Single Source**: `TARGET_FILE` is the absolute state reference for the next session.
