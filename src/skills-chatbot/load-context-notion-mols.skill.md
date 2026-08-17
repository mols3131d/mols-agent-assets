---
name: load-context-notion-mols
description: >-
  Use with load-context-notion to apply mols-specific conventions when the current
  workspace or target is explicitly the user's personal Notion or is unambiguously
  evidenced as personally governed. Continue on follow-ups to that target. Do not
  trigger for team, company, shared-project, or another person's spaces, or from edit
  access, membership, authorship, or elevated permission alone; in mixed-target tasks,
  apply only to personal targets.
---

# Load Mols Notion Context

This Skill is a **personal overlay**. Apply it only with `load-context-notion`.

## Activation

Evaluate personal scope **per Notion workspace/object**, not once for the whole conversation.
Activate when the base loader applies and the current target is explicitly identified or
unambiguously evidenced as the user's personally governed Notion space.

Keep the overlay active for follow-up requests that continue the same personal target,
even when the user does not repeat its name. If a follow-up switches targets, re-evaluate
personal scope before carrying this overlay forward.

Do not infer personal scope from edit access, workspace membership, page authorship,
shared access, familiarity, or permission level. If ownership/governance is unclear, use
only the base loader until evidence establishes personal scope.

If later live context shows that the target belongs to a team, company, shared project,
or another person rather than the user's personal governance, stop applying this overlay
and do not carry its conventions into further action on that target.

When one task spans multiple workspaces or objects, apply this overlay only to the
personal targets. Never export its conventions to team, company, shared-project, or
other people's Notion spaces.

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