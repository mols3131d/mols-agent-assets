---
name: "session-bridge"
description: "Consolidated protocol for session continuity and task management using the Toon (.toon) format."
---

# Session-Bridge (Integrated Task & Narrative)

This skill manages the **logical state** of the session. It combines narrative delta reporting with atomic task management (KISS) to ensure seamless continuity between agent sessions.

## When to use this skill

- **Session Start**: Read `.agents/brain/bridge.toon` to understand the current intent and pick up the next task.
- **Session Progress/End**: Update `.agents/brain/bridge.toon` to reflect completed tasks, log new hurdles, and provide a logical narrative for the next agent.

## How to use it

### 1. Update the Session State

Modify or create `.agents/brain/bridge.toon` based on the following unified schema:

```toon
session_bridge:
  meta:
    session_id: "[ISO-TIMESTAMP-SHORT-HASH]"
    intent: "[The high-level goal or 'Why' of this session]"
    status: "[DONE|PARTIAL|BLOCKED]"

  # Log of significant events and their logical rationale
  narrative[N]{id,event,design_logic}:
    [id],[What happened],[The reasoning/logic applied]

  # Atomic tasks (Merging Kanban functionality)
  tasks[N]{id,status,priority,objective}:
    [id],[BACKLOG|IN_PROGRESS|DONE|BLOCKED],[high|med|low],[Concrete task]

  # Blockers or technical debt
  hurdles[N]{id,issue,impact}:
    [id],[The problem],[How it affects progress]
```

### 2. Principles

- **KISS Tasks**: Keep tasks small enough to be completed in one session.
- **Narrative Over Task List**: The `narrative` explains _how_ the tasks were achieved, providing deeper context than a status flag.
- **Context Tax Policy**: Keep the lists concise. Focus on the 'Delta' (what changed) rather than the entire project history.

## Assets

- Template: `.agents/skills/session-bridge/assets/handover.toon`
