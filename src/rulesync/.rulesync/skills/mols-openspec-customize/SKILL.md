---
name: mols-openspec-customize
description: >-
  Design, review, dogfood, tune, or adapt OpenSpec customization. Use for choosing
  or changing OpenSpec profiles, project configuration, custom schemas, templates,
  schema maintenance, or customization behavior, especially when reusable design
  judgment or project-specific tuning is required. Separate exact OpenSpec vendor
  contract, reusable customization patterns, and concrete project decisions. Do not
  use for ordinary OpenSpec workflow usage such as applying or implementing a
  change, writing a specific proposal or spec, or unrelated repository guidance.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
---

# Mols OpenSpec Customize

Design and maintain OpenSpec customization without mixing vendor facts, reusable
design guidance, and project-local decisions.

## Responsibilities

Keep these three concerns separate even when one task needs more than one:

1. **Official OpenSpec contract** — exact supported behavior, commands, fields,
   paths, precedence, version-specific semantics, and authoritative sources.
1. **Customization patterns** — reusable judgment for choosing, maintaining,
   dogfooding, tuning, and verifying customization surfaces.
1. **Project customization** — decisions derived from a concrete repository,
   existing OpenSpec state, project policy, and observed work.

OpenSpec owns its runtime contract. This Skill owns reusable customization judgment.
The target repository owns project-specific policy and evidence.

Do not copy fast-changing OpenSpec contracts into local guidance. Do not turn one
project's policy or one successful dogfood case into a reusable pattern by default.

## Reference routing

Load only the references whose role actually applies.

| Reference | Load when | Do not load merely because... |
| --- | --- | --- |
| [Official customization](references/official-customization.md) | The answer depends on exact OpenSpec support or behavior: commands, fields, paths, precedence, schema semantics, experimental status, version differences, or authoritative vendor sources | the task mentions OpenSpec or needs general customization design |
| [Customization patterns](references/customization-patterns.md) | Choosing the narrowest customization surface, deciding config vs schema, maintaining a schema, dogfooding, tuning, or verifying a customization | an exact vendor-contract lookup is the only need |
| [Project customization](references/project-customization.md) | A concrete repository's current `openspec/` state, policy, workflow integration, representative work, or dogfood evidence affects the decision | the task is generic or has no project-specific evidence |

Load multiple references only when their responsibilities independently apply.

For a concrete repository, inspect its applicable live instructions and current
OpenSpec state before making project-specific recommendations or mutations.

## Workflow

1. Identify which responsibility the request needs: official contract, reusable
   pattern, project customization, or a combination.
1. Load only the matching references and authorities.
1. Keep sourced OpenSpec facts, reusable design judgment, and project evidence
   distinguishable.
1. For a concrete repository, inspect only context that can change the decision.
1. Choose or change the smallest coherent customization surface.
1. When tuning matters, use representative project work to find material friction
   and change its owning surface instead of stacking compensating instructions.
1. Verify runtime-dependent claims with evidence appropriate to that claim.
1. When several concerns matter, report **Official**, **Pattern**, and **Project**
   conclusions separately.

## Self-check

- Exact OpenSpec behavior is supported by current official or target-version
  evidence when exact behavior matters.
- The official reference was not loaded only because the task mentioned OpenSpec.
- Reusable patterns are not presented as OpenSpec requirements.
- Project choices come from repository or dogfood evidence.
- OpenSpec receives only context or structure it actually needs.
- Tuning changes an observed owner instead of accumulating duplicate guidance.
- Verification claims do not exceed what was inspected or run.

## Boundary

This Skill does not own ordinary OpenSpec change authoring, change implementation,
generic repository instruction authoring, or OpenSpec installation unless one is
directly required by a customization task.
