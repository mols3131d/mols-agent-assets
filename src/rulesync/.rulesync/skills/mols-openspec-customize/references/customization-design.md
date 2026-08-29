---
description: >-
  Reusable guidance for deciding where an OpenSpec customization belongs. Load
  when choosing between profile, project configuration, artifact or operation
  guidance, a custom schema, or existing repository authority; when deciding
  config versus schema; or when reducing unnecessary OpenSpec context. Do not use
  for exact OpenSpec contract lookup, custom-schema package maintenance, dogfood
  and tuning, or project-specific evidence.
---

# OpenSpec Customization Design

Use this reference to decide **what should own a customization**. It provides
reusable design judgment across projects; it does not define OpenSpec's exact
current fields, commands, paths, or version-specific behavior.

Consult [Official customization](official-customization.md) only when the decision
depends on exact OpenSpec support or semantics.

## Start with the lightest sufficient surface

Prefer an existing supported surface over a custom schema when it can express the
required behavior without changing the workflow's artifact structure.

A custom schema is justified when the artifact set, dependency flow, templates, or
schema-level instructions must materially differ. It introduces another workflow
definition to own and maintain, so do not create one merely to add guidance that
project configuration can already express.

## Choose the narrowest owner

Put a customization on the smallest surface that actually needs it.

| Needed effect | First owner to consider |
| --- | --- |
| Change which workflows are installed or how they are delivered | Profile |
| Add guidance that should shape planning broadly | Project configuration |
| Add guidance for one planning artifact | Artifact-scoped project rule |
| Guide apply or archive behavior | Operation guidance |
| Select which project schema is used | Project configuration |
| Change artifacts, dependencies, templates, or schema-level instructions | Custom schema |
| Preserve policy OpenSpec does not need to inject | Existing repository authority |

This is a selection heuristic, not a frozen vendor contract. If exact support,
precedence, or field semantics can change the answer, verify them through
[Official customization](official-customization.md).

## Keep OpenSpec context delta-only

Do not turn OpenSpec configuration into a second project handbook.

Keep only context that should materially change OpenSpec output or workflow
behavior. Put narrow guidance on the narrowest surface that consumes it.

When the active agent can reliably obtain repository guidance from its existing
authority, keep that guidance canonical there and inject only the delta OpenSpec
actually needs.

## Preserve repository authority

OpenSpec customization should adapt to repository policy, not become a competing
owner of testing, architecture, security, documentation, language, contribution,
or other project rules.

If the same concern appears in repository instructions, OpenSpec configuration, and
a schema template, identify the real owner. Remove accidental copies unless OpenSpec
needs a deliberate operational projection of that concern.

For a concrete repository, use [Project customization](project-customization.md) to
derive the actual project delta from live evidence rather than guessing it here.

## Hand off after the ownership decision

- If a custom schema is already chosen and its long-term package or documentation
  needs design, use [Schema maintenance](schema-maintenance.md).
- If an existing customization needs real-work evaluation, regression checking, or
  evidence-driven iteration, use [Dogfood and tuning](dogfood-and-tuning.md).
- If exact OpenSpec behavior affects the decision, use
  [Official customization](official-customization.md).

Do not load those references merely because they exist; load them only when their
separate concern becomes material.
