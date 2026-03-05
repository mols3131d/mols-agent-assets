# Synthesis: Integration of Kanban into Session Bridge

## Decision

The redundant `kanban` skill has been merged into the `session-bridge` skill. This creates a consolidated **"Session Bridging & Task Management"** protocol.

## Why this works

1. **Single Source of Truth**: Instead of alternating between separate task and bridge files, the agent maintains one `bridge.toon` which includes the narrative, tasks, and hurdles.
2. **Context Density**: All aspects of session continuity are represented in a single, high-density File.
3. **Atomic Management**: Tasks are now part of the session's overall narrative and logical delta.

## The Integrated Schema

- `meta`: Session identity and intent.
- `narrative`: Logical timeline of what was achieved.
- `tasks`: The actual to-do list (replacing the standalone kanban).
- `hurdles`: Open issues blocking progress.
