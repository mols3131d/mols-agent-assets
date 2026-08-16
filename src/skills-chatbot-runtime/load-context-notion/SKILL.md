---
name: load-context-notion
description: >-
  Load current Notion workspace context before concrete work on a Notion page,
  database, data source, property, relation, template, or connected Notion object.
  Use before Notion connector/tool actions and when existing Notion structure can
  affect the requested result. Do not use for generic Notion explanations with no
  concrete workspace target.
metadata:
  - target:
      - "OpenAI ChatGPT"
---

# Load Context: Notion

Use this Skill as a **Notion context loader**, not as a Notion editing workflow. Read the
smallest current workspace state needed to understand the target and its structural
constraints, then hand execution to the relevant writing, knowledge, planning, or Notion
mutation capability.

## Trigger Boundary

Activate when either condition is true:

- a concrete Notion page, database, data source, property, relation, template, or workspace
  object is being read or changed;
- a Notion connector, plugin, or tool will be called for task-level work.

A Notion read used only to identify the target may happen first. Complete the relevant
context loading before mutation or before making structural assumptions about the object.

## Core Contract

1. **Resolve the live target** — identify the exact page/database/object and its parent or
   containing structure when that relationship matters. Do not rely on remembered
   workspace state.
2. **Separate content from structure** — page body content, page/database properties,
   schema, relations, templates, views, and layout are different kinds of context. Load
   only the kinds that can affect the requested operation.
3. **Preserve existing semantics** — do not flatten structured properties, relations, or
   repeated page structure into prose merely because prose is easier to generate.
4. **Respect workspace evidence** — use the current Notion object and its connected
   metadata as the source for names, property types, relation targets, and structure. Do
   not invent a workspace convention from generic Notion practice.
5. **Load progressively** — start with the target object. Expand to its parent, database or
   data-source schema, related objects, or template only when the current task depends on
   them.
6. **Stop when sufficient** — context loading should not become a workspace crawl.

## Notion Object Lens

Preserve these distinctions when the active connector exposes them:

- A database entry is also a page: structured properties and page body content can both
  matter, but they are not interchangeable.
- Database/data-source properties define structured fields used for organization, search,
  filtering, sorting, status, dates, people, relations, formulas, rollups, and similar
  semantics.
- Relation properties connect pages or database items. Treat the relationship itself as
  structured data rather than replacing it with a copied title or URL unless the user
  explicitly asks for a textual projection.
- Templates may encode repeated property defaults and page structure. Inspect the relevant
  template when creating or reshaping a repeated page type and when the connector exposes
  it.
- Views and layouts can change presentation without changing the underlying information
  model. Do not infer a schema change merely from a presentation preference.

## Load Conditions

Load additional Notion context only when one of these conditions is present:

- **Existing page edit** → read the current page content and any properties that constrain
  the edit.
- **Database item work** → read the relevant property/schema definitions before assigning
  or interpreting structured values.
- **Relation or rollup work** → identify the relation target and only the connected fields
  needed to understand the requested relationship.
- **Repeated page creation** → inspect an applicable database template when one is known and
  available.
- **Restructuring** → inspect parent/child placement, existing navigation, and nearby
  canonical pages only when the requested move or information architecture depends on it.

Do not load every relation target, database row, template, sibling page, or view by default.

## Recheck Before Task Action

Before handing off to a task-level mutation, confirm that:

- the resolved Notion object is the intended target;
- property names and types used by the next action come from current workspace evidence;
- relation targets and structured fields have not been reduced to guessed prose;
- existing structure that must be preserved is known;
- unresolved ambiguity that could cause a destructive or structurally incorrect write is
  surfaced rather than guessed.

## Boundary

This Skill is read-oriented context discovery. It does not create, edit, move, archive,
delete, comment on, or otherwise mutate Notion content. It does not own prose quality,
document layout, knowledge-capture workflow, database design methodology, or final output
format. Those belong to the relevant downstream capability.
