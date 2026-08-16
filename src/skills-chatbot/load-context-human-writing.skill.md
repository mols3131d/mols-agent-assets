---
name: load-context-human-writing
description: >-
  Load human-centered writing and document context for reader-facing prose, reports,
  guides, briefs, explanations, README-style documentation, and other content meant
  primarily for people. Use when structure, readability, information hierarchy,
  scanability, audience fit, or cognitive load materially affects the result. Do not
  use for agent-facing instructions or when only literal transformation is requested.
---

# Load Context: Human Writing

Load this Skill as **reader-centered context**. It does not draft, rewrite, summarize,
research, format, or publish content; the active writing or document capability owns the
work and final artifact.

## Reader Model

Before making writing decisions, resolve only what materially changes the result:

- who the intended reader is and what they are trying to learn, decide, or do;
- what they can reasonably be expected to know already;
- the document's purpose and expected next action;
- the reading surface and constraints when they matter;
- what information must be preserved exactly versus what may be reorganized.

Do not invent a persona when the available context already supports a reasonable audience
assumption.

## Information Architecture

- Put the conclusion, decision, task, or most useful orientation where the reader can find
  it early.
- Organize around the reader's questions and decisions rather than the author's discovery
  order or internal process.
- Use headings as navigation. Add a heading only when it creates a real information
  boundary; avoid decorative sectioning and label-only fragmentation.
- Use lists, tables, callouts, or diagrams when they reduce search or comparison cost, not
  as mandatory decoration.
- For long material, use progressive disclosure: establish the core answer first and place
  detail where the reader can reach it without carrying all of it at once.
- Remove duplicate or stale explanations instead of adding another competing version.

## Clarity and Cognitive Load

- Prefer concrete, direct language over avoidable abstraction and ceremony.
- Keep terminology consistent. Define specialized terms when the intended reader may not
  know them; preserve standard domain terms when replacing them would reduce precision.
- Make the actor, action, condition, exception, and consequence explicit when ambiguity
  would matter.
- Keep paragraphs and sections focused on one useful job, but do not enforce arbitrary
  sentence or paragraph length limits.
- Front-load distinguishing information in headings and important paragraphs when it
  improves scanning.
- Avoid preambles that explain that an explanation is coming; spend that space on the
  information itself.
- Preserve necessary uncertainty and nuance instead of simplifying a claim into something
  easier to read but less accurate.

## Fidelity and Voice

The requested purpose and audience determine how much restructuring is appropriate.
Preserve facts, required constraints, citations, quotations, identifiers, and user-specified
voice. When technical or other preservation-critical material is being transformed, combine
this context with the relevant fidelity context instead of weakening protected content for
readability.

## Composition

Use research context for external factual support and a writing/document workflow for the
actual artifact. Agent-facing Skills, instructions, prompts, agents, tool guidance, and
similar behavioral assets should use agent-asset context instead of treating the model as a
human reader.

## Boundary

This Skill contributes audience, structure, readability, and cognitive-load judgment only.
It does not own factual verification, drafting workflow, document rendering, publication,
style-guide enforcement, or final output format.
