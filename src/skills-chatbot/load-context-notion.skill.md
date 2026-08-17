---
name: load-context-notion
description: >-
  Load the live Notion context that governs concrete work on a page, database,
  data source, view, property, relation, template, or connected object. Use before
  task-level Notion actions or connector/tool calls when existing workspace structure
  can affect the result; skip generic Notion explanation with no concrete target.
---

# Load Notion Context

Use this Skill only to resolve the **live Notion context that governs the task**.
Execution belongs to the downstream task capability.

## Trigger

Activate when a concrete Notion object is being read or changed, or when a Notion
connector/tool will be used for task-level work. A narrow read may be used first to
identify the target; finish relevant context loading before mutation or structural assumptions.

## Contract

- Resolve the exact live target and only relationships that can affect the task.
- Keep page body, properties/schema, relations, templates, views, and layout distinct.
- Preserve typed semantics for properties, relations, formulas, rollups, and views.
- Treat pagination, truncation, permissions, plan limits, and unsupported fields as
  possible incompleteness, not evidence of absence.
- Load progressively. Stop when more context is unlikely to change the next action.

## Object Semantics

Preserve distinctions exposed by the active Notion surface:

- a database can contain one or more data sources;
- a data source owns structured properties/schema and rows represented as pages;
- a database entry is also a page, but its properties and page body are distinct;
- a view is a presentation/query surface, not the underlying schema;
- a linked surface may be a projection of another authoritative source.

Prefer returned object identities, types, and relationships over inference from UI appearance.

## Procedure

### 1. Identify the Target

Resolve the target object and only the parent, container, data source, source projection,
or view relationships that can constrain the task.

### 2. Load the Relevant Surface

| Condition | Load |
| --- | --- |
| Page task | page body plus only constraining properties or parent context |
| Database/data-source task | concrete data source and relevant property schema |
| View-specific task | exact view and relevant filters, sorts, grouping, visibility, and view type; keep these distinct from schema |
| Relation/rollup task | relevant property definition and required target; verify returned values are complete enough |
| Repeated creation | applicable template only when defaults or repeated structure matter |
| Linked projection | authoritative source when the active surface distinguishes it |
| Restructuring/navigation | parent/child placement and nearby canonical structures only when information architecture depends on them |

Treat relations as references to other objects, not copied titles or URLs. Resolve only
fields and targets required by the current operation.

### 3. Resolve Incomplete Reads

When completeness matters and the result may be partial, retrieve only the missing
context needed to decide the next action: for example the next page, a specific property,
relation target, authoritative source, or page body.

Do not crawl every row, relation, view, template, sibling, or parent by default.

### 4. Gate and Stop

Before handoff, confirm that:

- the resolved object is the intended target;
- property types and relation targets used by the task come from current evidence;
- view behavior is not being mistaken for source schema;
- the visible result is complete enough for the conclusion;
- structure that must be preserved is known;
- material ambiguity is surfaced instead of guessed.

Then stop loading context.

## Boundary

This Skill is read-oriented context discovery. It does not own writing, page/database
creation, editing, moving, archiving, deletion, commenting, database/view design,
knowledge-capture workflow, personal workspace conventions, or final output format.