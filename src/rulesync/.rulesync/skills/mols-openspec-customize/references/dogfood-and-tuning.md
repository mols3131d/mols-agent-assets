---
description: >-
  Reusable method for evaluating and improving an existing or candidate OpenSpec
  customization with real work. Load for dogfooding, evidence-driven tuning,
  regression or overfitting checks, baseline comparison, or resolved-behavior
  verification. Do not use for generic owner selection, schema-package
  documentation, exact vendor-contract lookup, or inventing project requirements;
  pair with project-customization.md when repository evidence defines the cases or
  acceptance boundary.
---

# OpenSpec Dogfood and Tuning

Use this reference when a customization already exists or has a concrete candidate
form and the question is **whether it works in practice and how evidence should
change it**.

This is a reusable evaluation method, not a source of project requirements or
OpenSpec command semantics.

## Choose representative work

Do not stabilize a meaningful customization from one convenient example. Choose a
small set for information value rather than quota, usually including:

- ordinary work the customization should handle cleanly;
- a case that stresses the intended customization;
- a near-miss or edge case when overfitting is plausible.

For a concrete repository, derive the cases and acceptance boundary from
[Project customization](project-customization.md).

## Trace each material failure to its owner

For each material problem:

1. capture the observed behavior, artifact problem, workflow friction, or recurring
   maintainer correction;
1. state the expected behavior and why it matters;
1. identify the narrowest owner: project configuration, schema graph, template,
   schema instruction, repository policy, or something outside OpenSpec;
1. make the smallest coherent change at that owner;
1. rerun the affected case and check likely regressions.

Do not compensate for a template problem with broad project context, or for a
repository-policy problem with duplicated schema instructions. If the correct owner
is unclear, use [Customization design](customization-design.md) before changing it.

## Tune from evidence

Useful signals are observable and repeatable, such as:

- recurring omissions;
- irrelevant boilerplate;
- poor dependency timing;
- template editing friction;
- repeated manual correction;
- an improvement in one case that degrades another.

Change one meaningful owner at a time when practical so the effect remains
attributable. Preserve a useful baseline for material comparisons.

Do not keep editing because another wording variant exists. Continue only when a
credible next change can improve a material outcome or close an important
uncertainty.

## Match verification to the claim

Static review proves only static properties. Use the cheapest evidence that answers
the actual question:

1. validate schema or config structure when machine-checkable validation exists;
1. inspect resolved schema, templates, or instructions when selection, precedence,
   or injected behavior matters;
1. run representative dogfood cases when judging artifact quality or project fit;
1. review understandability and maintainability when they are part of acceptance.

When verification depends on an exact command, field, path, precedence rule, or
version-specific behavior, use [Official contract](official-contract.md) instead of
freezing that contract here.

## Stop on convergence

Stop tuning when representative cases no longer expose a material customization gap,
remaining failures belong to another owner, further OpenSpec changes would mainly
duplicate existing guidance, or another iteration has no credible evidence-backed
benefit.

Reopen the loop when new project evidence exposes a material failure or an OpenSpec
upgrade changes the governing contract.

## Keep durable evidence small

Preserve enough evidence to explain a material decision or reproduce an important
comparison. Do not preserve transient runs, disposable experiments, or every
successful case as permanent documentation.

The concrete project decides what evidence is worth retaining. Use
[Project customization](project-customization.md) for that boundary.
