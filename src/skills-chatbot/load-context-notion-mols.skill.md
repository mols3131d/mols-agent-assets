---
name: load-context-notion-mols
description: >-
  Add mols-specific Notion conventions on top of load-context-notion when the target
  is clearly the user's personal Notion space or another Notion area explicitly
  identified as personally managed. Do not activate for another person's workspace,
  a team/company workspace, or a shared project merely because the user can access it.
---

# Load Mols Notion Context

This Skill is a **personal overlay** for `load-context-notion`.

Never use it instead of the base loader. When this Skill applies, load both:

1. `load-context-notion`
2. `load-context-notion-mols`

## Activation Boundary

Activate only when both conditions hold:

- `load-context-notion` applies to the task;
- the target is evidenced as the user's personal Notion space.

Strong evidence includes an explicit user statement that the workspace/page/database is
their own or current Notion evidence showing that the target belongs to a personal space
the user governs.

Do **not** infer personal scope from edit access, workspace membership, page authorship,
shared access, familiarity, or permission level. Team, company, shared-project, and other
people's Notion spaces use only the base loader unless the user explicitly identifies the
target as personally governed.

## Personal Conventions

### Personal Guidance Entry Point

When a personal Notion space contains an explicit chatbot/agent guidance page such as
`CHATBOT`, treat it as a high-signal personal instruction source for Notion operations.
Load it when its scope can affect the current task.

Do not assume such a page exists, and do not treat `CHATBOT` as a general Notion
standard. If the personal workspace defines a different guidance entry point or explicit
precedence, follow the live workspace evidence instead.

### Preserve Personal Information Architecture

For personal spaces, prefer existing canonical pages, databases, relations, and navigation
structures over creating parallel structures from generic Notion practice.

Before structural mutation, identify whether the target participates in a user-maintained
hub, resource database, project database, relation graph, or other canonical structure.
Load only the portion needed to preserve that structure.

Do not copy this personal information architecture into team or external workspaces.

## Boundary

This overlay owns only the user's cross-workspace personal conventions. Page-specific,
database-specific, and project-specific rules still come from the live Notion target
through `load-context-notion`.

It does not own writing, database design, knowledge capture, page creation, or mutation.
Those remain downstream capabilities.
