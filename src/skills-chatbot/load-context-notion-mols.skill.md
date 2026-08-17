---
name: load-context-notion-mols
description: >-
  Use with load-context-notion for task-level work in the user's explicitly personal or
  unambiguously personally governed Notion workspace or object. Continue on follow-ups
  to the same target and re-evaluate when the target changes. Do not use for team,
  company, shared-project, or another person's spaces, and do not infer personal scope
  from edit access, membership, authorship, familiarity, or elevated permission. In
  mixed-target tasks, apply only to personal targets.
---

# Load Mols Notion Context

This Skill contributes **personal mols conventions** for the Notion target. Live target
context remains owned by `load-context-notion`.

## Personal Conventions

### Guidance Entry Point

If the personal space contains an applicable chatbot/agent guidance page such as
`CHATBOT`, treat it as a high-signal instruction source and load it when it can affect
the current task.

Do not assume the page exists or export this convention to other workspaces. If live
workspace evidence defines a different guidance entry point or precedence, follow it.

### Preserve Personal Information Architecture

Before structural mutation, prefer existing canonical pages, databases, relations, and
navigation over creating parallel structures from generic Notion practice.

Load only enough surrounding structure to determine whether the target belongs to a
user-maintained hub, resource/project database, relation graph, or other canonical structure.

## Boundary

This overlay owns only cross-workspace personal conventions. Page-, database-, and
project-specific rules still come from the live target through `load-context-notion`.
It does not own writing, database design, knowledge capture, page creation, or mutation.
