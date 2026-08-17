---
name: load-context-agent-assets
description: >-
  Load agent-facing authoring and design context for Skills, Rules, Prompts, Agents,
  subagents, tool guidance, guardrails, templates, and related behavioral assets
  consumed primarily by AI agents. Use when activation, authority, context cost,
  routing, tool boundaries, portability, packaging, or evaluability materially affects
  the asset. Do not use for ordinary human-facing prose or product code that does not
  define agent behavior.
---

# Load Context: Agent Assets

Load this Skill as **agent-facing design context**. It does not create, refactor, validate,
package, or publish assets; the active agent-asset workflow owns execution and output.

## Runtime Contract

Resolve only dimensions that can change the asset:

- target agent, model, harness, or platform;
- asset type and primary consumer;
- activation scope and lifetime;
- authority relative to user, project, platform, and tool instructions;
- tools, permissions, files, connectors, and runtime capabilities actually available;
- expected behavior, non-behavior, failure boundary, and deployment surface.

Do not import one platform's filenames, precedence, tool semantics, or packaging rules as
universal conventions.

## Repository Standards

When this repository's asset doctrine matters, distinguish two layers:

1. `docs/references/agent-asset-standard-baseline.md` — standards-adjacent external/common baseline.
1. `docs/references/agent-asset-boundaries.md` — **Personal Agent Asset Standard**, which owns this repository's intentional non-standard extensions and operating decisions.

Use the baseline to understand external/common concepts. Use the Personal Standard as the
repository authority for local taxonomy, naming, projections, fallback, placement, packaging,
and non-runtime package conventions. Do not copy personal extensions back into the baseline
as if they were external standards.

## Asset Boundary

Treat these as peer behavioral asset types when the repository uses this taxonomy:

- **Rule** — persistent policy or constraint for an applicable scope;
- **Skill** — reusable capability or context activated when relevant;
- **Prompt** — current invocation goal and one-off context;
- **Agent** — distinct runtime role, authority, tools, delegation, and behavior surface.

Supporting resources are not peer Agent Asset types. If supporting knowledge needs its own
model-directed activation boundary, let a Skill own that activation and load the resource
conditionally.

Repository-specific projections may be intentionally non-standard. In this repository,
Rule can be projected through root/nested `AGENTS.md`, glob-scoped instructions, or
`CHATBOT.md` for text I/O chatbot surfaces. Preserve evidenced repository conventions;
do not promote them into universal platform standards.

## Skill Package Surfaces

For directory-based Skills in this repository, distinguish runtime and maintainer surfaces.

- **non-dot directories** such as `references/`, `scripts/`, and `assets/` may be runtime
  resources when the Skill actually needs them;
- **dot-prefixed directories (`.*`) are non-runtime maintainer surfaces**;
- use `.docs/` instead of Skill-internal `docs/` for maintainer documentation;
- use `.docs/baseline/` to preserve original purpose/essence, requirements, invariants,
  major decisions, and recovery directives;
- do not make runtime behavior depend on `.docs/`, `.evals/`, `.tests/`, or another dot
  directory;
- deployment/package logic should exclude dot directories by default.

A baseline may use `DIRECTIVE.md`, `intent.md`, `requirements.md`, `decisions.md`, or another
clear file split. The filenames are not the contract; **preservation of original intent and
requirements is**. Baseline material should be durable enough to detect semantic regression
after repeated refactors, but it is not runtime context and does not outrank the user's
current explicit instruction.

When an existing `docs/` contains material that the runtime actually reads, do not hide it
by renaming the directory. Move the runtime-required material to `references/` or another
runtime surface, and move only maintainer material to `.docs/`.

Flat single-file Skill projections do not gain an internal `.docs/` bundle merely to follow
this convention.

## Context Economy

Agent context is an execution resource, not a documentation archive.

- Put selection-critical information in metadata or discovery surfaces.
- Keep activated instructions focused on behavior the agent would not reliably infer from
  the task, platform, or surrounding project context.
- Move conditional detail behind explicit load conditions when the runtime supports
  progressive disclosure.
- For Agent Skills-compatible targets, use the target's disclosure layers deliberately:
  discovery metadata first, `SKILL.md` on activation, bundled resources only when needed.
  Do not project this loading model onto platforms that implement a different contract.
- Keep stable behavioral policy in durable instructions. Keep run-, user-, environment-,
  or time-varying state in task input, dynamic instructions, tools, retrieval, or another
  runtime context surface when the target supports one.
- Preserve the distinction between model-visible context and local runtime state. Data
  available to tools, hooks, or application code is not automatically model context.
- Keep authority, permission, routing, and non-obvious activation boundaries discoverable
  before the agent needs them.
- Avoid hidden shared-context dependencies when a target variant must deploy independently.
- Allow intentional semantic overlap between target-specific sibling variants when their
  harness capabilities, authority, packaging, or loading strategies differ. Optimize each
  projection for its target rather than deduplicating across incompatible boundaries.

## Activation and Ownership

- A reusable asset needs a recognizable situation in which loading it changes behavior.
- Discovery metadata should communicate both **what** the asset contributes and **when** it
  should activate; add a negative boundary when nearby capabilities are easy to confuse.
- Keep one coherent responsibility and reason to change. Split when activation, authority,
  permission, success criteria, or distribution genuinely diverges—not merely because a
  file is long.
- Distinguish persistent Rule, conditional Skill, one-off Prompt, and runtime Agent using
  the target platform and repository's actual authority model.
- For a context-only Skill, load context and stop there; downstream workflows retain
  implementation, mutation, validation, and presentation ownership.

## Behavioral Contract

Prefer asset instructions that expose observable boundaries:

- when the asset should and should not activate;
- which action or non-action matters;
- which invariants must survive adaptation;
- which failure or handoff state should be visible.

Match instruction precision to task fragility. Use principles where multiple approaches are
valid; use explicit constraints or deterministic mechanisms where the runtime supports them
and errors are materially costly.

Distinguish static inspection, model simulation, and actual runtime evidence when evaluating
an asset. Optimize for the smallest sufficient instruction set that remains discoverable
and robust; shorter is not better if the condition needed to load critical context becomes
unclear.

## Composition

For concrete repository work, combine this context with repository/GitHub context so the
project's own asset taxonomy and conventions remain authoritative. Add coding context when
implementation code is part of the asset and human-writing context only for human-facing
documentation around it.

## Boundary

This Skill contributes agent-facing design judgment only. It does not own asset creation,
editing, validation loops, runtime evaluation, packaging, deployment, or final output
format.
