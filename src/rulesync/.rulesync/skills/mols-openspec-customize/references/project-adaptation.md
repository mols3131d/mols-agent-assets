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
- existing specs or workflow artifacts when they reveal established project intent;
- prior tuning notes or representative examples when the project already maintains
  them.

Stop when more repository context is unlikely to change the decision.

## Derive project deltas

For each requested behavior, record:

1. the repository or dogfood evidence that requires it;
1. the current canonical owner of that policy, fact, or failure mode;
1. whether OpenSpec actually needs to consume or structurally encode it;
1. the concrete project value or rule OpenSpec needs.

Then use [Patterns](patterns.md) to choose the smallest supported customization
surface. Confirm exact fields and commands through [Official](official.md).

If OpenSpec does not need the information, leave it with the existing repository
owner instead of creating another copy.

## Adapt minimally

- Improve an existing OpenSpec owner before adding a parallel config or schema.
- Preserve canonical repository policy owners.
- Add only the OpenSpec delta needed for the workflow to consume project policy.
- Keep concrete project values project-specific; do not promote them into the
  reusable pattern without evidence from repeated cases.
- When a custom schema becomes a durable team-owned surface, make its purpose and
  maintenance boundary discoverable without turning maintainer documentation into
  runtime instruction.

For a non-trivial project schema, consider a small nearby `README.md`. Add a
schema-local `docs/` directory only when durable tuning rationale, representative
scenarios, or upstream-port notes need more space. Treat both as project convention,
not OpenSpec schema semantics, and re-check current companion-file behavior when
schema tooling changes.

## Dogfood and tune

When the goal includes tuning, establish a small project-representative dogfood set
before repeated edits. Select cases for information value rather than a fixed quota:
normal work, a case that stresses the intended customization, and a near-miss or
edge case when overfitting is plausible.

Iterate as follows:

1. Run or inspect the relevant OpenSpec workflow with the current customization.
1. Capture only material friction: wrong artifact shape, missing project context,
   redundant guidance, dependency problems, repeated manual correction, or
   maintainer confusion.
1. Trace the friction to its narrowest owner using [Patterns](patterns.md).
1. Tune that owner with the smallest coherent change.
1. Validate the changed structure or resolution with the current OpenSpec tooling.
1. Re-run the affected dogfood case and enough of the representative set to detect
   a likely regression.
1. Keep the change only when evidence improves project fit without creating a more
   expensive competing owner.

Do not make every dogfood observation durable. Preserve only rationale, scenarios,
provenance, or constraints that future maintainers need to reproduce a decision.
Transient run logs belong in the project's existing working-artifact surface, if it
has one.

## Stabilize deliberately

Treat a customization as stable enough to hand off when:

- the representative project cases no longer expose a material customization gap;
- remaining failures belong to implementation, repository policy, model/runtime
  behavior, or another owner outside the customization;
- schema/config validation and relevant resolution checks pass when available;
- the customization has not accumulated duplicate project guidance;
- a non-trivial schema's purpose, intentional differences, and meaningful fork
  provenance are understandable to its maintainers.

Do not keep tuning merely because another wording variant exists. Reopen the loop
when new project evidence exposes a material failure or an OpenSpec upgrade changes
the governing contract.

## Verify

Match evidence to the changed surface:

- inspect resolved instructions when configuration should change agent input;
- validate a changed schema before relying on it;
- inspect schema or template resolution when precedence matters;
- compare resulting instructions or artifacts with the repository policy the
  customization was meant to preserve;
- use representative project runs when the claim is about output quality or
  workflow fit rather than parseability.

Use exact CLI syntax from the current official documentation or installed version.

## Report

Keep three kinds of reasoning separable when they are material:

- **Official** — the supported OpenSpec mechanism used;
- **Pattern** — the reusable reason for choosing or tuning that mechanism;
- **Project** — the repository and dogfood evidence that determines the concrete
  value, rule, or schema change.

Record unresolved repository or OpenSpec-version uncertainty instead of inventing a
default.
