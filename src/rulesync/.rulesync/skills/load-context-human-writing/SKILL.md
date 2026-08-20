---
name: load-context-human-writing
description: >-
  Mandatory human-comprehension baseline context for substantive reader-facing writing or
  document work. Always load when the active work includes creating or materially
  restructuring prose, reports, guides, briefs, explanations, README-style documentation,
  or other human-facing content where comprehension, information architecture, scanability,
  decision or action clarity, future re-entry, or understanding debt can materially affect
  the result. Apply as a shared judgment layer inside the owning workflow. Do not use for
  agent-facing behavioral instructions, literal transformations, or tasks where human
  comprehension is not a material concern.
---

# Contract

This Skill contributes **human-comprehension judgment** to reader-facing work. The active
writing or document capability still owns research, drafting, rewriting, rendering,
publication, and final output. Apply this context even when human-facing writing is only one
subtask inside a broader workflow.

Optimize for **reader work**, not merely text length or visual polish. A shorter document is
not automatically easier to understand, and a more formatted document is not automatically
easier to use.

> Reduce the work a reader must do to orient, find, understand, decide, act, and re-enter.

Apply these principles continuously inside the active workflow rather than as a separate
writing procedure.

# Reader Model

Resolve only what can materially change the writing:

- who the intended reader is and what they need to learn, decide, or do;
- what they can reasonably be expected to know already;
- the document's purpose and likely next action;
- the reading surface and constraints when material;
- what must be preserved exactly versus what may be reorganized.

Do not invent a detailed persona when the available context already supports a reasonable
audience assumption. Widening the audience usually increases the amount of context that
must be made explicit.

# Reader Work

Use the following costs as a compact quality lens:

- **Orientation cost** — how much work is required to know what this is, why it matters,
  and where to start.
- **Retrieval cost** — how much searching is required to find the needed fact, decision,
  instruction, or constraint.
- **Interpretation cost** — how much unstated context, terminology, or relationship must be
  reconstructed.
- **Decision cost** — how difficult it is to compare alternatives, evidence, tradeoffs,
  status, or risk.
- **Action cost** — how difficult it is to determine what should happen next and under what
  conditions.
- **Re-entry cost** — how much context a reader must reconstruct when returning later.

Do not optimize one cost by materially increasing another. For example, aggressive
compression that removes rationale can lower reading time while increasing interpretation
and re-entry cost.

# Information Architecture

- Put the conclusion, decision, task, status, or most useful orientation where the reader
  can find it early.
- Organize around the reader's questions and decisions rather than the author's discovery
  order, implementation order, or internal process.
- Use headings as navigation boundaries. Add one only when it creates a real information
  boundary; avoid decorative sectioning and label-only fragmentation.
- Front-load distinguishing information in headings and important paragraphs when it
  improves scanning.
- For long material, disclose detail progressively: establish the core answer first and
  place supporting depth where it becomes useful.
- Keep sections and paragraphs focused on one useful job without enforcing arbitrary
  length limits.
- Keep terminology stable. Define specialized terms when the intended reader may need it;
  preserve standard domain terms when substitution would reduce precision.
- Make actor, action, condition, exception, consequence, and authority explicit when
  ambiguity would materially increase reader work.

# Understanding Debt

Treat **understanding debt** as future human cost created when readers must repeatedly
reconstruct context that the artifact should make recoverable.

Common sources include:

- duplicated or competing explanations with unclear authority;
- stale summaries or status that no longer match the underlying source;
- terminology drift for the same concept;
- hidden prerequisites, assumptions, ownership, or decision state;
- missing rationale for durable decisions and constraints;
- excessive fragmentation that forces unnecessary cross-document traversal;
- decorative structure or visuals that obscure rather than expose information shape.

Prefer one clear owner for durable knowledge. Remove duplicate or stale explanations rather
than adding another competing version. Preserve rationale, constraints, exceptions, and
uncertainty when removing them would force future readers to rediscover why the current
state exists.

# Representation

Choose the representation that reduces the reader's required cognitive operation.

- Use prose for explanation, reasoning, nuance, and narrative relationships.
- Use lists for sibling items, conditions, checks, or ordered actions when sequence matters.
- Use tables for repeated attributes or direct comparison across the same dimensions.
- Use diagrams when relationships, boundaries, flow, state, or architecture are the main
  question.
- Use charts when quantitative magnitude, trend, distribution, or proportion is the main
  question.
- Use callouts only when a note, warning, exception, or constraint needs unusual salience.
- Use exact code, commands, paths, identifiers, or syntax in a representation that
  preserves their literal form.

Do not duplicate the same information across prose, tables, callouts, diagrams, and charts
without a distinct reader need. A visual is justified by reduced search, comparison, or
interpretation cost, not by decoration.

When Markdown is the actual output surface and its representation details matter, read
[Markdown for Human](references/markdown.md). Specialized diagram, chart, or dashboard
capabilities own their own syntax and domain rules; this Skill supplies only the
reader-centered selection criterion.

# Fidelity and Re-entry

Preserve facts, required constraints, citations, quotations, identifiers, user-specified
voice, and necessary uncertainty. Never improve readability by making a claim less true.

For durable or repeatedly revisited material, preserve enough orientation to make later
re-entry cheap when those elements are relevant:

- purpose and scope;
- current state or decision;
- rationale and material constraints;
- authoritative pointers instead of duplicated bodies;
- next action, owner, or trigger when the artifact is action-bearing.

Do not turn every document into a status template. Include re-entry anchors only when they
reduce likely future reconstruction cost.

When technical or other preservation-critical material is being transformed, combine this
context with the relevant fidelity context rather than weakening protected content for
readability.

# Composition

This Skill is a cross-workflow context layer. Compose it with research, reporting,
technical-document, repository, Notion, or other capabilities when their responsibilities
independently apply.

For mixed artifacts, apply these principles only to the human-facing layer. Agent-facing
behavioral instructions use agent-asset context even when they coexist with README prose or
other human-facing material.

# Boundary

This Skill owns general human-comprehension principles: audience fit, information
architecture, reader work, understanding debt, representation judgment, readability, and
re-entry quality.

It does **not** own factual verification, research methodology, drafting workflow,
publication, target-specific style-guide enforcement, diagram or chart syntax, or final
output format. Surface-specific references and downstream capabilities may constrain how
these principles are expressed without becoming a second owner of them.
