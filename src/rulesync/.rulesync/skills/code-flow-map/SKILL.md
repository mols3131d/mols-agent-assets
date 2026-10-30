---
name: code-flow-map
description: Trace a code path, function call chain, or data flow in a repository, distinguish observed/static/inferred relationships, and create an evidence-linked Markdown code map with Mermaid diagrams and collapsible inline HTML. Use for understanding unfamiliar code, following entry points, and bounded impact analysis. Not a replacement for runtime debugging or a general code review.
argument-hint: "[entry point, symbol, or flow question]"
---

# Code Flow Map

Produce a **navigable, evidence-backed Markdown report** for a specific code path. Use the host coding agent's existing repository tools. Use existing repository inspection tools and do not invent execution evidence.

## Inputs and scope

- Determine the question, entry point, relevant repository/worktree, and boundaries. Reuse constraints already given by the user.
- If no symbol is supplied, investigate likely entry points and state the scope you selected. Avoid claiming whole-repository completeness.
- Read repository instructions and respect workspace security/permissions. Analysis is read-only by default; **only create the requested report**. Do not change application code, execute untrusted code, or send source externally without authorization.
- Report the inspected Git commit/ref when available, or mark it `unknown`. Do not silently treat a working-tree snapshot as a committed revision.

## Analyze

1. **Resolve nodes.** Locate entry points and relevant concrete symbols using search, file reads, definitions, references, call hierarchy, AST or language tools available in this runtime. Record paths and line ranges.
2. **Resolve edges.** For every connection, inspect its actual call site, invocation target, data propagation, event subscription/publication, or runtime trace. Record **direction and relationship kind** (`call`, `data`, `event`, `dependency`). Never infer execution order from mere dependency or textual proximity.
3. **Classify evidence**, independently for each edge:
   - `OBSERVED`: a runtime trace or test demonstrates this connection **in the stated scenario**; record how/when it was observed. It does not prove all runs follow it.
   - `STATIC`: a concrete source-level relationship is resolved (e.g., direct call/definition/reference); it does not establish runtime execution.
   - `INFERRED`: plausible relation proposed by analysis/AI but not independently established; state the hypothesis and missing proof.
   - `UNRESOLVED`: available evidence cannot decide the target or direction; do not draw a solid edge.
   - `CONTRADICTED`: available evidence directly conflicts with the proposed connection; exclude it from the accepted flow and explain the contradiction.
4. **Track evidence.** Assign an `E1`, `E2`, … ID to each proposed edge and cite a file **and exact line range** (or trace identifier) where available. Record alternative routes, dispatch/DI, callbacks, queues, error branches and missing coverage when material.
5. **Check claims.** Reopen sources to confirm files, line numbers, symbol names and the edge claim. A real file/line does **not** prove its relationship to the next node. Do not invent tests, traces, coverage, accuracy scores, or certainty.

## Produce the report

- Load [templates/report.md](./templates/report.md) when writing a report. Replace every `{{PLACEHOLDER}}`; remove irrelevant example nodes/sections rather than inventing values.
- Default output: `docs/code-flows/<short-kebab-topic>.md` relative to the repository root **when the user wants a file**. Otherwise answer inline. Check before overwriting an existing report.
- Use portable Markdown for headings, evidence tables, source links and Mermaid `flowchart TD` blocks. Prefer small overview diagrams (roughly 9 nodes or fewer); split large flows into an overview and focused sections.
- Use **inline HTML only for `<details>`, `<summary>`, `<strong>`, `<code>` and optional explicit anchors**. Keep critical caveats and evidence status visible even when details are collapsed.
- Use solid `-->` lines for `OBSERVED` or `STATIC` edges (but **label each status**), dashed `-.->` for `INFERRED` or `UNRESOLVED`. Do not draw `CONTRADICTED` edges as accepted flow. Label connections with evidence IDs. Do not depict mere dependencies as chronological calls.
- Prefer relative links to real source files **from the report's directory**; record line ranges in adjacent text. Avoid editor-specific URI schemes. When a link cannot be resolved, use plain path text and mark it unverified.
- Escape source-derived text before embedding it into HTML attributes or Mermaid node/edge labels; never interpolate raw code, paths or comments as HTML/diagram syntax. Place optional source snippets and detailed rationale in collapsible HTML `<details>` blocks with blank lines around nested Markdown. Never use JavaScript, inline event handlers, remote scripts, iframes, or require lowering Markdown preview security.
- Report the exact limits: static analysis coverage, unexamined branches, missing runtime traces, generated code, external services and any unavailable tooling.

## Self-check before finishing

- Each displayed edge has a unique evidence ID, type, status and source or an explicit `no direct evidence` explanation.
- Every `STATIC` connection has a real source-level relationship; every `OBSERVED` connection has an actual observed trace/test with scope.
- No inferred edge appears as verified; no claim of complete runtime sequence comes from static source alone.
- File links are relative to the output Markdown and point to existing files when checked. Mermaid node labels and legend agree with the evidence table.
- The report requires no executable HTML or lowered Markdown preview security. Renderer-specific compatibility is not asserted unless actually tested. If renderer validation was not performed, explicitly say so.
- Deliver the report location, a short finding, and the top unresolved relation. Do not claim tests or previews were run unless they were.

## Usage example

`/code-flow-map Trace the request handler through authentication and persistence. Include uncertainty and evidence.`

For a **small synthetic example**, see [examples/demo-report.md](./examples/demo-report.md). It is demonstration data, not a finding about the user's repository.
