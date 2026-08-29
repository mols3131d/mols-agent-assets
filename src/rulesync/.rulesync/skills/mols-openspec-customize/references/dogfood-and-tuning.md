---
description: >-
  Reusable method for evaluating and improving an existing OpenSpec customization
  with real work. Load when dogfooding, tuning from observed failures, checking for
  overfitting or regressions, comparing against a baseline, or verifying resolved
  customization behavior. Do not use for generic surface selection, schema package
  documentation, exact vendor-contract lookup, or project-specific evidence that
  has not yet been established.
---

# OpenSpec Dogfood and Tuning

Use this reference when a customization already exists or has a concrete candidate
form and the question is **whether it works well enough in practice and how to
improve it from evidence**.

This is a reusable evaluation method, not a catalog of OpenSpec commands and not a
source of project-specific requirements.

## Start from representative work

Do not stabilize a meaningful customization from one convenient example.
Choose a small set for information value rather than quota, usually including:

- ordinary work the customization should handle cleanly;
- a case that stresses the behavior being customized;
- a near-miss or edge case when overfitting is plausible.

For a concrete repository, derive those cases from real project evidence through
[Project customization](project-customization.md).

## Turn friction into an owner-specific hypothesis

For each material problem:

1. capture the observed behavior, artifact problem, workflow friction, or recurring
   maintainer correction;
1. state the expected behavior and why it matters;
1. identify the narrowest owner: project configuration, schema graph, template,
   schema instruction, repository policy, or something outside OpenSpec;
1. make the smallest coherent change at that owner;
1. rerun the affected case and check likely regressions in the representative set.

Do not compensate for a template problem with broad project context, or for a
repository-policy problem with duplicated schema instructions.

If the correct owner is unclear, use [Customization design](customization-design.md)
before changing anything.

## Tune from evidence, not wording preference

Useful tuning signals are observable and repeatable, such as:

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
the actual question.

1. Validate schema or config structure when machine-checkable validation exists.
1. Inspect resolved schema, templates, or instructions when selection, precedence,
   or injected behavior matters.
1. Run representative dogfood cases when judging artifact quality or project fit.
1. Review whether the resulting customization remains understandable and
   maintainable when that is part of acceptance.

When an exact command, field, path, precedence rule, or version-specific runtime
behavior is needed for verification, consult
[Official customization](official-customization.md) rather than freezing that
contract here.

## Stop on convergence, not exhaustion

Stop tuning when:

- representative cases no longer expose a material customization gap;
- remaining failures belong to another owner;
- another OpenSpec-specific change would mainly duplicate existing guidance; or
- further iteration has no credible evidence-backed benefit.

Reopen the loop when new project evidence exposes a material failure or an OpenSpec
upgrade changes the governing contract.

## Keep durable evidence small

Preserve enough evidence to explain a material decision or reproduce an important
comparison. Do not turn transient runs, disposable experiments, or every successful
case into permanent documentation.

The concrete project decides which evidence is worth retaining. Use
[Project customization](project-customization.md) for that project-specific boundary.
