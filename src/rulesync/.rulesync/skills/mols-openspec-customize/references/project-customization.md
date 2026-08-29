---
description: >-
  OpenSpec customization guidance for a concrete project or repository. Load when
  the decision depends on that repository's current `openspec/` state, local policy,
  workflow integration, representative work, dogfood evidence, or project-specific
  constraints. Do not use for generic customization design, schema maintenance,
  reusable dogfood methodology, or exact vendor-contract lookup without
  project-specific evidence.
---

# Project-specific OpenSpec Customization

Use this reference to decide **what a particular project should do differently**.
The repository, its current OpenSpec state, and observed project work provide the
evidence; generic customization method belongs elsewhere.

## Inspect only context that can change the decision

Resolve the target repository and relevant ref, then inspect the smallest useful
context:

- applicable repository or directory instructions;
- existing `openspec/` configuration and project schemas;
- current OpenSpec integration or generated workflow surfaces when relevant;
- canonical development, testing, architecture, documentation, security, or
  contribution guidance the workflow must respect;
- existing specs, workflow artifacts, prior tuning notes, or representative cases
  when they reveal established project intent.

Stop when more context is unlikely to change the customization decision.

## Derive the project delta

For each requested behavior, answer:

1. What repository or dogfood evidence requires it?
1. Which source already owns that policy, fact, or failure mode?
1. Does OpenSpec actually need to consume or structurally encode it?
1. What is the smallest project-specific delta OpenSpec needs?

If the owning customization surface is unclear, use
[Customization design](customization-design.md). Use
[Official contract](official-contract.md) only when exact OpenSpec support or
behavior can change the choice.

Leave information outside OpenSpec when OpenSpec does not need it.

## Improve the existing owner before adding another one

Prefer changing an existing OpenSpec owner to adding a parallel config or schema.
Keep repository policy with its existing authority and add only the delta the
workflow needs.

If a custom schema becomes a durable team-owned surface, load
[Schema maintenance](schema-maintenance.md) only for maintenance concerns that
actually arise. Do not create companion files as ceremony.

## Apply project evidence to empirical tuning

When tuning matters, derive representative cases and acceptance evidence from real
project work, then use the reusable method in
[Dogfood and tuning](dogfood-and-tuning.md).

Preserve only evidence future maintainers need to understand or reproduce a material
project decision. Keep transient run logs and disposable experiments in the
project's existing working-artifact surface when one exists.

## Stop when the project delta is resolved

Stop adapting when project evidence no longer exposes a material customization gap,
remaining failures belong to another owner, or further OpenSpec changes would mainly
duplicate existing project guidance.

## Report project evidence, not duplicated method

This reference contributes only project-specific evidence and uncertainty:

- which repository state was inspected;
- which representative cases informed the decision;
- which project facts could not be verified.

Use [Dogfood and tuning](dogfood-and-tuning.md) for reusable verification and tuning
method. The parent Skill owns the final separation of **Official**, **Reusable**, and
**Project** conclusions.
