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
  - work: `/.agent/workflows/brain/handover.md`
  - file: `/.agent/brain/handover.md`
- [Kanban]
  - work: `/.agent/workflows/brain/kanban.md`
  - dir: `/.agent/brain/kanban.md`
- [feedback]
  - work: `/.agent/workflows/brain/feedback.md`
  - file: `/.agent/brain/feedback.md` 

### 3. Report

- Report