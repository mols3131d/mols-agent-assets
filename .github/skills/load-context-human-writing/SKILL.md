---
name: load-context-human-writing
description: Load human-centered writing and document context for reader-facing prose, reports, guides, briefs, explanations, README-style documentation, and other content meant primarily for people. Use when structure, readability, information hierarchy, scanability, audience fit, or cognitive load materially affects the result. Do not use for agent-facing behavioral instructions or when only literal transformation is requested.
---

# Load Context: Human Writing

This Skill contributes **reader-centered writing context**. The active writing or document capability owns drafting, rewriting, research, rendering, publication, and final output.

## Resolve the Reader

Resolve only what can change the writing:

- who the intended reader is and what they need to learn, decide, or do;
- what they can reasonably be expected to know already;
- the document's purpose and likely next action;
- the reading surface and constraints when material;
- what must be preserved exactly versus what may be reorganized.

Do not invent a detailed persona when the available context already supports a reasonable audience assumption.

## Structure for Retrieval

- Put the conclusion, decision, task, or most useful orientation early.
- Organize around the reader's questions and decisions, not the author's discovery order.
- Use headings as navigation. Add one only when it creates a real information boundary.
- Use lists, tables, callouts, or diagrams when they reduce search or comparison cost, not as decoration.
- For long material, establish the core answer first and disclose detail where it becomes useful.
- Remove duplicate or stale explanations instead of adding another competing version.

## Reduce Cognitive Load

- Prefer concrete, direct language over avoidable abstraction and ceremony.
- Keep terminology stable. Define specialized terms only when the intended reader may need it; preserve standard domain terms when substitution would reduce precision.
- Make actor, action, condition, exception, and consequence explicit when ambiguity matters.
- Keep paragraphs and sections focused on one useful job without enforcing arbitrary length limits.
- Front-load distinguishing information in headings and important paragraphs when it improves scanning.
- Remove preambles that only announce that an explanation is coming.
- Preserve necessary uncertainty and nuance instead of simplifying a claim into something less accurate.

## Preserve Fidelity and Voice

The requested purpose and audience determine how much restructuring is appropriate. Preserve facts, required constraints, citations, quotations, identifiers, and user-specified voice.

When technical or other preservation-critical material is being transformed, combine this context with the relevant fidelity context. For mixed artifacts, apply this Skill only to the human-facing layer; use agent-asset context for behavioral instructions.

## Boundary

This Skill contributes audience, information architecture, readability, and cognitive-load judgment. It does not own factual verification, style-guide enforcement, or the writing workflow itself.
