---
description: Formalize session handover and state summary before exit
---

# Exit Workflow

## Steps

### 1. Clean

- clean temp files
  - **EXEC**: run [clean](~/scripts/clean.*)

### 2. Update

- [handover]
  - work: `.agent/workflows/handover.md`
  - file: `~/.agent/brain/handover.md`

- [Kanban]
  - work: `.agent/workflows/kanban.md`
  - dir: `~/docs/dev/features/**`

- [feedback]
  - work: `.agent/workflows/feedback.md`
  - file: `~/.agent/brain/feedback.md`

### 3. Report

- Report
