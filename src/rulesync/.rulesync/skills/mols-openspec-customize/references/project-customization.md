---
description: >-
  Use only for OpenSpec customization in a concrete project or repository. Load
  when the decision depends on that repository's existing openspec/ state, local
  policy, current workflow integration, representative work, dogfood evidence, or
  project-specific constraints. Do not use for generic customization design,
  schema-maintenance guidance, dogfood methodology, or exact vendor-contract lookup
  without project-specific evidence.
---

# Project-specific OpenSpec Customization

Use this reference for **what a particular project should do differently**. It is
about project evidence and project delta, not generic OpenSpec guidance.

The repository, its current OpenSpec state, and observed project work are the
evidence for these decisions.

## Inspect only what can change the decision

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

For each requested behavior, answer four questions:

1. What repository or dogfood evidence requires it?
1. Which source already owns that policy, fact, or failure mode?
1. Does OpenSpec actually need to consume or structurally encode it?
1. What is the smallest project-specific delta OpenSpec needs?

Use [Customization design](customization-design.md) when the owning customization
surface is not yet settled. Consult
[Official customization](official-customization.md) only when the choice depends on
exact OpenSpec support or behavior.

Leave information outside OpenSpec when OpenSpec does not need it.

## Adapt the existing owner first

Improve an existing OpenSpec owner before adding a parallel config or schema.
Preserve repository policy owners and add only the delta the workflow needs.

If a custom schema becomes a durable team-owned surface, load
[Schema maintenance](schema-maintenance.md) only for the maintenance concerns that
actually arise. Do not create companion files as ceremony.

## Apply project evidence to dogfood

When empirical tuning matters, choose a small representative set from real project
work. Pick cases for information value rather than a quota, then apply the method in
[Dogfood and tuning](dogfood-and-tuning.md).

Preserve only evidence future maintainers need to understand or reproduce a
material project decision. Keep transient run logs and disposable experiments in
the project's existing working-artifact surface when one exists.

## Stop when the project delta is resolved

Stop adapting when project evidence no longer exposes a material customization gap,
remaining failures belong to another owner, or further OpenSpec-specific changes
would mainly duplicate existing project guidance.

## Hand off evidence, not duplicated method

Use [Dogfood and tuning](dogfood-and-tuning.md) for reusable verification and tuning
method. This reference contributes only project-specific evidence and uncertainty:

- which repository state was inspected;
- which representative cases informed the decision;
- which project facts could not be verified.

The parent Skill owns the final separation of **Official**, **Pattern**, and
**Project** conclusions.
