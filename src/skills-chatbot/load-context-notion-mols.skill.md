---
name: load-context-notion-mols
description: >-
  Add mols-specific Notion conventions after load-context-notion when the target is
  evidenced as the user's personal Notion space. Do not activate for another person,
  team, company, or shared project merely because the user has access, authorship,
  membership, or elevated permission.
---

# Load Mols Notion Context

This Skill is a **personal overlay**. Apply it only after `load-context-notion`.

## Activation

Activate only when the base loader applies and the target is explicitly identified or
unambiguously evidenced as the user's personally governed Notion space.

Edit access, workspace membership, page authorship, shared access, familiarity, or
permission level do not establish personal scope. Otherwise use only the base loader.

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