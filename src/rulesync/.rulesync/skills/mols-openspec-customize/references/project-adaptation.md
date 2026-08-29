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
navigation surface. Put durable supporting detail in `docs/` only when it would
overload the README. Keep repository-wide or harness-specific agent instructions in
their existing authority.

Do not create companion files as ceremony. A simple schema may need none of them.

## Apply dogfood evidence

When tuning is part of the goal, choose a small representative set from real project
work. Select cases for information value rather than a quota, then apply the
dogfooding and tuning method in [Patterns](patterns.md).

Preserve only project evidence future maintainers need to understand or reproduce a
material decision. Keep transient run logs and disposable experiments in the
project's existing working-artifact surface when one exists.

## Project stop conditions

Stop adapting the customization when project evidence no longer exposes a material
gap, remaining failures belong to another owner, or further OpenSpec-specific
changes would mainly duplicate existing project guidance.

For a durable custom schema, the selected maintenance surfaces should make its
purpose and meaningful project-specific differences understandable without creating
a second project handbook.

## Evidence handoff

Use the verification method in [Patterns](patterns.md) for claims about resolved
behavior. This reference only adds project-specific evidence and uncertainty: which
repository state was inspected, which representative cases informed the decision,
and which project facts could not be verified.

The parent Skill owns final separation of **Official**, **Pattern**, and **Project**
conclusions.
