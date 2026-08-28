# Project-specific OpenSpec Adaptation

Use this reference only when adapting OpenSpec to a concrete project or repository.
The target repository is evidence and authority for project-specific decisions.

## Inspect first

Resolve the target repository and relevant ref, then load only context that can
change the customization decision:

- applicable repository or directory instructions;
- existing `openspec/` configuration and project schemas;
- current OpenSpec integration or generated workflow surfaces when relevant;
- canonical development, testing, architecture, documentation, security, or
  contribution guidance the requested workflow must respect;
- existing specs or workflow artifacts when they reveal established project intent.

Stop when more repository context is unlikely to change the decision.

## Derive project deltas

For each requested behavior, record:

1. the repository evidence that requires it;
1. the current canonical owner of that policy or fact;
1. whether OpenSpec actually needs to consume it;
1. the concrete project value or rule OpenSpec needs.

Then use the canonical OpenSpec customization pattern to choose the smallest
supported customization surface. Confirm exact fields and commands in current
official OpenSpec material.

If OpenSpec does not need the information, leave it with the existing repository
owner instead of creating another copy.

## Adapt minimally

- Improve an existing OpenSpec owner before adding a parallel config or schema.
- Preserve canonical repository policy owners.
- Add only the OpenSpec delta needed for the workflow to consume project policy.
- Keep concrete project values project-specific; do not promote them into the
  reusable pattern without evidence from repeated cases.

## Verify

Match evidence to the changed surface:

- inspect resolved instructions when configuration should change agent input;
- validate a changed schema before relying on it;
- inspect schema or template resolution when precedence matters;
- compare resulting instructions or artifacts with the repository policy the
  customization was meant to preserve.

Use exact CLI syntax from the current official documentation or installed version.

## Report

Keep three kinds of reasoning separable when they are material:

- **Official** — the supported OpenSpec mechanism used;
- **Pattern** — the reusable reason for choosing that mechanism;
- **Project** — the repository evidence that determines the concrete value or rule.

Record unresolved repository or OpenSpec-version uncertainty instead of inventing a
default.
