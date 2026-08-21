---
name: mols-document-decisions
description: >-
  Create or update lightweight project decision records. Use when recording a proposed,
  accepted, superseded, or deprecated technical or project decision and the repository
  does not already provide a more authoritative decision workflow. Preserve an existing
  project decision format when one is established; otherwise use the bundled Decisions-Lite
  structure. Do not use for general prose, Markdown styling, dashboards, or agent instructions.
---

# Mols Document Decisions

Create and maintain lightweight decision records without introducing a document framework.

## Contract

- The current repository's established decision format, location, and status semantics outrank this Skill's fallback format.
- Do not create a parallel Decisions-Lite document when an accepted ADR or decision owner already exists.
- Preserve existing decisions unless the user explicitly asks to revise, supersede, or remove them.
- Never invent approval, implementation, validation, ownership, or supporting evidence.
- Prefer one durable decision owner over duplicated decision summaries across documents.

## Write

1. Inspect the target repository for an existing decision document, ADR convention, template, or authoritative instructions.
1. If an existing format is authoritative, follow it and change only the requested decision.
1. Otherwise initialize from `templates/decisions-lite.md` when a new decision document is needed.
1. Put the decision under exactly one status: `Proposed`, `Accepted`, `Superseded`, or `Deprecated`.
1. Record the decision as `DECISION`, `REASON`, and `IMPACT`; add `RELATED` only when an existing decision is directly relevant.
1. Check for semantic duplicates before appending a new decision.
1. Re-read the resulting document for status, preservation, and unresolved placeholders.

## Decisions-Lite

Use the following block when this Skill's fallback format applies:

```markdown
### **[CATEGORY] TITLE**

- DECISION | **KEY DECISION** - DETAILED EXPLANATION
- REASON | **KEY MOTIVATION** - CONTEXT AND REASON
- IMPACT | **KEY CONSEQUENCE** - SYSTEM OR WORKFLOW IMPACT
```

`RELATED` is optional and should be omitted when no existing decision is needed to understand, constrain, extend, or supersede the new one.

## Boundary

This Skill owns decision-record semantics only. Reader-facing prose guidance belongs to the active writing capability; Markdown expression and deterministic Markdown maintenance belong to the `mols-markdown` family; diagrams and charts belong to `mols-mermaid`.
