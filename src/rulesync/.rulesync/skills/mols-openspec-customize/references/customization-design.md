---
description: >-
  Reusable guidance for deciding which surface should own an OpenSpec
  customization. Load for config-versus-schema decisions, choosing the narrowest
  owner, or reducing unnecessary OpenSpec context. Do not use for exact vendor
  contract lookup, schema-package maintenance, dogfood methodology, or
  project-specific evidence.
---

# OpenSpec Customization Design

Use this reference to decide **what should own a customization**. It provides
reusable design judgment, not exact OpenSpec fields, commands, paths, or
version-specific behavior.

## Choose the lightest sufficient owner

Prefer an existing supported surface when it can express the required behavior
without changing the workflow's artifact structure. Use a custom schema when the
artifact set, dependency flow, templates, or schema-level instructions must
materially differ.

| Needed effect | First owner to consider |
| --- | --- |
| Change which workflows are installed or how they are delivered | Profile |
| Add guidance that should shape planning broadly | Project configuration |
| Add guidance for one planning artifact | Artifact-scoped project rule |
| Guide apply or archive behavior | Operation guidance |
| Select which project schema is used | Project configuration |
| Change artifacts, dependencies, templates, or schema-level instructions | Custom schema |
| Preserve policy OpenSpec does not need to inject | Existing repository authority |

This table is a selection heuristic, not a frozen vendor contract. If exact support,
precedence, or field semantics can change the answer, use
[Official contract](official-contract.md).

A custom schema introduces another workflow definition to own and maintain. Do not
create one merely to add guidance that a lighter supported surface can express.

## Keep OpenSpec context delta-only

Do not turn OpenSpec configuration into a second project handbook. Keep only context
that should materially change OpenSpec output or workflow behavior, and put narrow
guidance on the narrowest surface that consumes it.

Repository policy should remain with its existing authority unless OpenSpec needs a
deliberate operational projection of that concern. If the same rule appears in
repository instructions, OpenSpec configuration, and a schema template, identify the
real owner and remove accidental copies.

For a concrete repository, use
[Project customization](project-customization.md) to derive the actual project delta
from live evidence rather than guessing it here.

## Continue only when another concern applies

- Existing or chosen custom schema needs package or long-term maintenance guidance →
  [Schema maintenance](schema-maintenance.md)
- Existing or candidate customization needs empirical evaluation or tuning →
  [Dogfood and tuning](dogfood-and-tuning.md)
- Exact OpenSpec behavior can change the decision →
  [Official contract](official-contract.md)

Do not load another reference merely because it is linked here.
