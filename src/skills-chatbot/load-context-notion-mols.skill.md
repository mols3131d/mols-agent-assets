---
name: load-context-notion-mols
description: >-
  Load mols-specific Notion conventions for task-level work in the user's explicitly
  personal or unambiguously personally governed workspace or object. Continue on
  follow-ups to the same target and re-evaluate when the target changes. Do not use for
  team, company, shared-project, or another person's spaces, and do not infer personal
  scope from edit access, membership, authorship, familiarity, or elevated permission.
  In mixed-target tasks, apply only to personal targets.
---

# Load Mols Notion Context

This Skill contributes **personal mols conventions** for the Notion target. Resolve live
target context through `load-context-notion`; this overlay does not replace the base loader.

## Scope Discipline

Keep personal conventions bound to targets that remain evidenced as personally governed.
If newly loaded context shows that a target belongs to a team, company, shared project,
or another person, stop applying this overlay to that target. In mixed-target work, never
carry personal defaults from an in-scope target into another target.

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
