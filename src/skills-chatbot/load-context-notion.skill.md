---
name: load-context-notion
description: >-
  Load current Notion workspace context before concrete work on a Notion page,
  database, data source, view, property, relation, template, or connected Notion
  object. Use before Notion connector/tool actions and when existing Notion structure
  can affect the requested result. Do not use for generic Notion explanations with no
  concrete workspace target.
---

# Load Context: Notion

Use this Skill as a **Notion context loader**, not as a Notion editing workflow. Read the
smallest live workspace state needed to understand the target and structural constraints,
then hand execution to the relevant downstream capability.

## Trigger Boundary

Activate when either condition is true:

- a concrete Notion page, database, data source, view, property, relation, template, or
  workspace object is being read or changed;
- a Notion connector, plugin, or tool will be called for task-level work.

A narrow read used only to identify the target may happen first. Complete relevant
context loading before mutation or before making structural assumptions.

## Core Contract

1. **Resolve the live target** — identify the exact object and only the parent,
   container, data source, source projection, or view relationships that can affect the task.
1. **Separate content from structure** — page body, properties/schema, relations,
   templates, views, and layout are different context surfaces.
1. **Preserve typed semantics** — do not flatten properties, relations, formulas,
   rollups, or view configuration into prose merely because prose is easier to generate.
1. **Use workspace evidence** — names, types, relation targets, schema, view state, and
   structure come from current Notion evidence, not remembered or generic conventions.
1. **Treat incomplete reads as incomplete** — pagination, truncation, permissions,
   plan limits, unsupported fields, or connector/API differences are not evidence of absence.
1. **Load progressively and stop** — expand from the target only when another object or
   structural surface can materially change the next action. Do not crawl the workspace.

## Structured Context

Preserve the object distinctions exposed by the active Notion surface:

- A **database** is a container that can expose one or more **data sources**.
- A **data source** owns structured properties/schema and rows represented as pages.
- A database entry is also a **page**; structured properties and page body are distinct.
- A **view** is a presentation/query surface over a data source. Filters, sorts,
  grouping, visible properties, and view type can change what the user sees without
  changing the underlying schema.
- A linked database/data-source surface can be a projection of an authoritative source.
  Resolve the source when the active connector distinguishes it.
- A **template** can carry repeated property defaults and page structure. Inspect it only
  when repeated creation or reshaping actually depends on the template.

Prefer object identities, types, and relationships returned by the active connector/API
over inferences from UI appearance.

### Properties and Relations

Before assigning, interpreting, querying, or changing structured values, load the current
relevant property definitions.

- Treat relations as references to other pages/items, not copied titles or URLs.
- Preserve formula, rollup, status, date, people, and other typed-property semantics.
- Resolve only the connected fields and targets required by the current operation.

### Views

When a request targets a specific view, load only view state that can affect the task,
such as filters, sorts, grouping, visible/hidden properties, view type, and relevant
display/query configuration.

Keep view configuration distinct from data-source schema. A view filter is not an
invariant of the underlying source.

### Partial Reads

Treat results as potentially incomplete when the active surface exposes or plausibly
imposes pagination/cursors, bounded relations, truncated properties, inaccessible
sources, permission/plan limits, unsupported fields, or separation between page
properties and body content.

When completeness matters, retrieve only the narrow missing context: the next page,
specific property, relation target, authoritative source, or page body required to resolve it.

## Procedure

1. Resolve the live target.
1. For a straightforward page task, read the page content and only properties or parent
   context that constrain the requested action.
1. For database/data-source work, resolve the concrete data source and relevant property schema.
1. For view-specific work, resolve the exact view and only configuration relevant to the request.
1. For relation/rollup work, resolve the required target and verify the returned value is complete enough.
1. For repeated page creation, inspect a known applicable template only when needed.
1. For linked projections, resolve the authoritative source when the active surface distinguishes it.
1. For restructuring/navigation work, inspect parent/child placement and nearby canonical
   pages only when the information architecture depends on them.
1. Stop when additional context is unlikely to change the next action.

Do not load every row, relation target, data source, view, template, sibling page, or
parent object by default.

## Recheck Before Task Action

Before handing off to a task-level mutation, confirm:

- the resolved object is the intended target;
- property names/types and relation targets used by the action come from current evidence;
- view-specific behavior is not being mistaken for underlying schema;
- the visible result is complete enough for the conclusion;
- structure that must be preserved is known;
- material ambiguity is surfaced instead of guessed.

## Boundary

This Skill is read-oriented context discovery. It does not create, edit, move, archive,
delete, comment on, or otherwise mutate Notion content. It does not own prose quality,
document layout, knowledge-capture workflow, database/view design methodology, or final
output format. Those belong to the relevant downstream capability.
