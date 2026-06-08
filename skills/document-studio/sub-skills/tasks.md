---
name: tasks
description: >
  Create or improve task lists. Use when user asks for todos, checklists,
  implementation steps, or action item extraction from docs.
---

# Tasks

## Overview

- **Goal**: Break down work into clear, actionable todo items and checklists.

## Triggers

- User asks for a todo list or checklist.
- Existing documentation needs action items extracted.
- Work does not require kanban board tracking.

## Exclusions

- Work that requires complex stages (e.g. backlog, review, in-progress) -> use `kanban.md`.

## Workflow

1. Create a markdown file or section with task items.
2. Check off items as they are completed.
3. Keep context in linked documentation.

## Resources

- Checklists inside markdown documents.

---

## Rules

- Start tasks with a verb.
- One task = one action.
- Group by milestone only when list exceeds ~10 items.
- Task item format:

  ```markdown
  - [ ] Action verb + object. Owner/date if known.
  ```

## Constraints

- Do not store detailed prose or implementation notes in task list files; keep them in linked documents.
