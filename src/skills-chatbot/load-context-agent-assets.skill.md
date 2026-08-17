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

Use this Skill as **design context** for agent-facing behavioral assets. The active workflow owns creation, editing, validation, packaging, publication, and final output.

## Resolve First

Resolve only dimensions that can change the asset:

- target model, agent, harness, or platform;
- asset type and primary consumer;
- activation scope and lifetime;
- authority relative to user, project, platform, and tool instructions;
- tools, permissions, files, connectors, and runtime capabilities actually available;
- required behavior, non-behavior, failure boundary, and deployment surface.

Do not import one platform's filenames, precedence, tools, or packaging rules as universal conventions.

## Repository Doctrine

When this repository's doctrine matters, use:

1. `docs/references/agent-asset-standard-baseline.md` for standards-adjacent external/common concepts.
1. `docs/references/agent-asset-boundaries.md` as the **Personal Agent Asset Standard** and authority for repository-specific extensions.

Do not project repository-specific decisions back into the external/common baseline.

This repository uses these peer behavioral asset types:

- **Rule** — persistent policy or constraint for an applicable scope.
- **Skill** — reusable capability or context activated when relevant.
- **Prompt** — current invocation goal and one-off context.
- **Agent** — distinct runtime role, authority, tools, delegation, and behavior surface.

Supporting resources are not peer asset types. If knowledge needs model-directed activation, let a Skill own that activation.

Repository-specific Rule projections may include root/nested `AGENTS.md`, glob-scoped instructions, and `CHATBOT.md`. Preserve evidenced local conventions without presenting them as universal standards.

## Skill Package Surfaces

For directory-based Skills in this repository:

- non-dot directories such as `references/`, `scripts/`, and `assets/` may contain runtime resources;
- dot-prefixed directories are maintainer-only, non-runtime surfaces;
- use `.docs/` for maintainer documentation and `.docs/baseline/` for durable purpose, requirements, invariants, major decisions, and recovery directives;
- never make runtime behavior depend on `.docs/`, `.evals/`, `.tests/`, or another dot directory;
- exclude dot directories from deployment/package output by default.

If existing maintainer documentation contains runtime-required material, move that material to a runtime surface before changing the directory role. Flat single-file Skills do not gain an internal bundle merely to mirror directory-based packages.

## Design Rules

### Activation and ownership

- Give every reusable asset a recognizable situation in which loading it changes behavior.
- Discovery metadata should say **what** the asset contributes and **when** it should activate; add a negative boundary only when nearby capabilities are easy to confuse.
- Keep one coherent responsibility and reason to change. Split only when activation, authority, permission, success criteria, or distribution materially diverges.
- A context-only Skill loads judgment and stops; downstream workflows retain mutation, validation, and presentation ownership.

### Context economy

- Spend context on behavior the model would not reliably infer from the task, platform, or repository.
- Put selection-critical information in metadata or discovery surfaces.
- Keep stable policy in durable instructions; keep run-, user-, environment-, or time-varying state in task input, tools, retrieval, or another runtime context surface.
- Distinguish model-visible context from runtime state. Data available to tools or application code is not automatically model context.
- Prefer progressive disclosure when the target supports it, but keep non-obvious activation triggers discoverable before they are needed.
- Preserve independent target variants when they cannot share runtime context. Do not create hidden dependencies merely to remove textual overlap.

### Behavioral contract

Expose observable boundaries:

- when the asset should and should not activate;
- which action or non-action matters;
- which invariants must survive adaptation;
- which failure, handoff, or validation state must remain visible.

Match precision to task fragility: use principles when multiple approaches are valid and explicit constraints or deterministic mechanisms when errors are materially costly.

When evaluating an asset, distinguish static inspection, model simulation, and actual runtime evidence. Prefer the smallest sufficient instruction set that remains discoverable and robust.

## Boundary

This Skill contributes agent-asset design judgment only. Repository rules and the active platform's real authority model outrank this general context.