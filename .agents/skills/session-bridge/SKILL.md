---
name: "session-bridge"
description: "Protocol for session-bridging and task management using Markdown (MD)."
---

# Session-Bridge (Minimal)

This skill ensures continuity between agent sessions using a simplified checkbox-driven Markdown file.

## When to use

- **Session End**: Summarize the current state and list the next steps.
- **Session Start**: Read `.agents/brain/bridge.md` to restore context.

## How to use

### 1. Update the Bridge File

Maintain `.agents/brain/bridge.md` with the following minimalist structure:

#### **Context**

- [ ] ID: `[HASH]`
- [ ] Intent: `[High-level goal]`
- [ ] Status: `[DONE | PARTIAL | BLOCKED]`

#### **Narrative**

- [x] `[Event]` -> `[Reasoning]`

#### **Todo**

- [x] `[Completed Task]`
- [-] `[In Progress Task]`
- [ ] `[Pending Task]`

#### **Hurdles**

- [ ] `[Issue]`: `[Description]`

## Principles

- **Minimalism**: No tables, no complex priorities. Just checkboxes.
- **Delta Only**: Focus on the immediate logical delta.
- **Single Source**: Combined narrative and todo in one file.

## Assets

- Template: `.agents/skills/session-bridge/assets/session-bridge.md`
