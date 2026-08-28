# Project-specific OpenSpec Adaptation

Use this reference only when adapting OpenSpec to a concrete project or repository.
The target repository is evidence and authority for project-specific decisions.

## Inspect first

Resolve the target repository and relevant ref, then load only project context that
can change the customization decision:

- applicable repository or directory instructions;
- existing `openspec/` configuration and project schemas;
- current OpenSpec integration or generated workflow surfaces when relevant;
- canonical development, testing, architecture, documentation, security, or
  contribution guidance that the requested workflow must respect;
- existing specs or workflow artifacts when they reveal established project intent.

Do not crawl the repository just to collect context. Stop when additional files are
unlikely to change the customization choice.

## Classify each project need

For every requested behavior, decide who should own it before editing OpenSpec.
Use the current official contract to confirm exact field names and supported
mechanics.

| Project need | Preferred owner |
| --- | --- |
| Which OpenSpec workflows or delivery surfaces are installed | Profile |
| Planning fact that should affect broadly applicable workflow runs | Project context |
| Extra requirement for one planning artifact | Artifact-scoped project rule |
| Guidance for applying or archiving work | Operation guidance |
| Project-level schema selection | Project configuration |
| Different artifacts, dependencies, templates, or schema instructions | Project schema |
| Repository policy OpenSpec does not need to inject | Existing repository authority |

If a need does not clearly belong in OpenSpec, leave it outside OpenSpec rather than
creating a new synchronization burden.

## Adapt minimally

1. Preserve the repository's existing canonical policy owners.
1. Add only the OpenSpec delta needed for the workflow to consume that policy.
1. Prefer project configuration when it can express the requirement additively.
1. Use a project-local schema when the workflow structure itself must differ.
1. Keep project values concrete and repository-specific; do not generalize them
   back into the reusable pattern without evidence from repeated cases.

When a repository already has an OpenSpec customization, improve its current owner
instead of adding a parallel config or schema that competes with it.

## Verify

Use evidence that matches the changed surface:

- inspect the resolved instructions when configuration should change agent input;
- validate a changed schema before relying on it;
- inspect schema or template resolution when shadowing or precedence matters;
- compare the resulting artifacts or instructions against the repository policy the
  customization was meant to preserve.

Use the exact current CLI commands from the official documentation or installed
version rather than relying on remembered syntax.

## Report the adaptation

When the result mixes several kinds of reasoning, keep the handoff separable:

- **Official** — which supported OpenSpec mechanism is being used;
- **Pattern** — why that mechanism is the smallest or safest fit;
- **Project** — which repository evidence determines the concrete rule, value, or
  schema change.

Record unresolved repository or OpenSpec-version uncertainty instead of filling it
with a generic default.
