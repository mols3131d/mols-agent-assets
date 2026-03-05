---
name: "kanban"
description: "Atomic task management and project state synchronization via a structured Kanban Toon file."
---

# Kanban (Toon Edition)

This skill manages the project's task lifecycle using a structured `.toon` file. It ensures atomic task tracking and automated context optimization.

## When to use this skill

- **Task Creation**: When starting a new feature or logical unit of work.
- **Status Update**: When completing a task or encountering a blocker.
- **Pruning**: When the number of completed tasks exceeds the limit (10 items), to maintain context efficiency.

## How to use it

### 1. Update the Kanban

Modify `.agents/brain/kanban.toon` to reflect the current state of tasks using the following schema:

```toon
kanban:
  meta:
    last_updated: "[ISO-8601]"
    active_tasks: [INTEGER]
    total_completed: [INTEGER]

  tasks[N]{id,status,priority,task,note}:
    [id],[BACKLOG|IN_PROGRESS|DONE|BLOCKED],[high|med|low],[Task objective],[Ref/Context]
```

### 2. Principles

- **Atomic Tasks**: Keep tasks small and verifiable.
- **Single Source of Truth**: All progress must be recorded here.
- **FIFO Cleanup**: When `DONE` tasks exceed 10, remove the oldest entries.

## Assets

- Template: `.agents/skills/kanban/assets/kanban_template.toon`
