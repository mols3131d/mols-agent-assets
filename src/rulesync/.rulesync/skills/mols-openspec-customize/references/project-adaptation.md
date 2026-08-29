# Project-specific OpenSpec Adaptation

Use this reference only when adapting OpenSpec to a concrete project or repository.
The target repository and observed project use are evidence and authority for
project-specific decisions.

## Inspect first

Resolve the target repository and relevant ref, then load only context that can
change the customization decision:

- applicable repository or directory instructions;
- existing `openspec/` configuration and project schemas;
- current OpenSpec integration or generated workflow surfaces when relevant;
- canonical development, testing, architecture, documentation, security, or
  contribution guidance the requested workflow must respect;
- existing specs, workflow artifacts, prior tuning notes, or representative cases
  when they reveal established project intent.

Stop when more context is unlikely to change the decision.

## Derive project deltas

For each requested behavior, identify:

1. the repository or dogfood evidence that requires it;
1. the canonical owner of that policy, fact, or failure mode;
1. whether OpenSpec actually needs to consume or structurally encode it;
1. the concrete project delta OpenSpec needs.

Use [Patterns](patterns.md) to choose the smallest supported surface and
[Official](official.md) to confirm exact mechanics. Leave information outside
OpenSpec when OpenSpec does not need it.

## Adapt minimally

Improve an existing OpenSpec owner before adding a parallel config or schema.
Preserve repository policy owners and add only the delta the workflow needs.

When a custom schema becomes a durable team-owned surface, apply the optional
maintenance surfaces from [Patterns](patterns.md) only when they reduce real cost.
Use `README.md` as the schema package's common human-readable entrypoint and
navigation surface. Put durable maintenance detail in `docs/` when it would overload
the README. Keep repository-wide or harness-specific agent instructions in their
existing authority rather than creating a schema-local instruction file by default.

Do not create companion files as ceremony. A simple schema may need none of them.

## Dogfood and tune

When tuning is part of the goal, establish a small representative dogfood set before
repeated edits. Select cases for information value rather than a quota.

Apply the dogfooding and tuning method in [Patterns](patterns.md) to project evidence.
For project-specific work, preserve only rationale, representative scenarios,
provenance, or constraints future maintainers need to reproduce a decision. Put
transient run logs in the project's existing working-artifact surface when one
exists.

## Stabilize

Stop the tuning loop when:

- representative cases no longer expose a material customization gap;
- remaining failures belong to another owner outside the customization;
- relevant validation and resolution checks pass when available;
- duplicate project guidance has not accumulated;
- users and maintainers can understand a non-trivial schema from its selected
  maintenance surfaces without needing duplicated explanations;
- meaningful fork provenance is discoverable when future upgrades depend on it.

Do not continue tuning merely because another wording variant exists. Reopen it when
new project evidence exposes a material failure or an OpenSpec upgrade changes the
governing contract.

## Verify and report

Match evidence to the claim: inspect resolved instructions for agent input, validate
schema structure, inspect schema/template resolution for precedence, and use
representative project runs for output quality or workflow fit.

Use exact CLI syntax from the current official documentation or installed version.
When several kinds of reasoning matter, keep them separable:

- **Official** — the supported OpenSpec mechanism used;
- **Pattern** — the reusable reason for choosing or tuning it;
- **Project** — the repository and dogfood evidence determining the concrete delta.

Record unresolved repository or OpenSpec-version uncertainty instead of inventing a
default.
