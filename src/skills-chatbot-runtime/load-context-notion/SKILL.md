---
name: load-context-notion
description: >-
  Load current Notion workspace context before concrete work on a Notion page,
  database, data source, view, property, relation, template, or connected Notion
  object. Use before Notion connector/tool actions and when existing Notion structure
  can affect the requested result. Do not use for generic Notion explanations with no
  concrete workspace target.
metadata:
  - target:
      - "OpenAI ChatGPT"
---

# Load Context: Notion

Use this Skill as a **Notion context loader**, not as a Notion editing workflow. Read the
smallest live workspace state needed to understand the target and structural constraints,
then hand execution to the relevant writing, knowledge, planning, or Notion capability.

## Trigger Boundary

Activate when either condition is true:

- a concrete Notion page, database, data source, view, property, relation, template, or
  workspace object is being read or changed;
- a Notion connector, plugin, or tool will be called for task-level work.

A narrow read used only to identify the target may happen first. Complete relevant context
loading before mutation or before making structural assumptions about the object.

## Core Contract

1. **Resolve the live target** — identify the exact object and the parent, container, data
   source, or view only when that relationship can affect the task. Do not rely on remembered
   workspace state.
2. **Separate content from structure** — page body, properties/schema, relations, templates,
   views, and layout are different context surfaces. Load only those the next action needs.
3. **Preserve typed semantics** — do not flatten properties, relations, repeated structure,
   or view configuration into prose merely because prose is easier to generate.
4. **Use workspace evidence** — names, types, relation targets, schema, view state, and
   structure come from current Notion evidence, not generic Notion conventions.
5. **Treat incomplete reads as incomplete** — pagination, truncation, permissions, plan
   limits, unsupported fields, or connector/API differences can hide relevant state. Do not
   convert a partial read into evidence of absence.
6. **Load progressively and stop** — expand from the target only when another object or
   structural surface can materially change the next action. Do not crawl the workspace.

## Conditional Loading

For a straightforward existing-page task, read the current page content and only the
properties or parent context that constrain the requested change.

Read only the relevant section of `references/structured-context.md` when the task depends
on any of these:

- database or data-source schema;
- typed properties, relations, formulas, or rollups;
- a specific database view or linked projection;
- repeated page templates;
- completeness of a potentially bounded or truncated structured read.

For restructuring or navigation work, inspect parent/child placement and nearby canonical
pages only when the information architecture actually depends on them.

Do not load every row, relation target, data source, view, template, sibling page, or parent
object by default.

## Recheck Before Task Action

Before handing off to a task-level mutation, confirm only the facts that could make the next
action target the wrong object or damage existing structure:

- the resolved object is the intended target;
- any property names/types or relation targets used by the action come from current evidence;
- view-specific behavior is not being mistaken for underlying schema;
- the visible result is complete enough for the conclusion being made;
- structure that must be preserved is known;
- material ambiguity is surfaced instead of guessed.

## Boundary

This Skill is read-oriented context discovery. It does not create, edit, move, archive,
delete, comment on, or otherwise mutate Notion content. It does not own prose quality,
document layout, knowledge-capture workflow, database/view design methodology, or final
output format. Those belong to the relevant downstream capability.
