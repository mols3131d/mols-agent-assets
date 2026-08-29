---
name: mols-openspec-customize
description: >-
  Design, review, dogfood, tune, or adapt OpenSpec customization. Use for choosing
  or changing OpenSpec profiles, project configuration, custom schemas, templates,
  schema maintenance, or customization behavior, especially when reusable design
  judgment or project-specific tuning is required. Separate exact OpenSpec vendor
  contract, reusable customization guidance, and concrete project decisions. Do not
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

Keep these concerns distinct even when one task needs several of them:

1. **Official OpenSpec contract** — exact supported behavior, commands, fields,
   paths, precedence, version-specific semantics, and authoritative sources.
1. **Reusable customization guidance** — how to choose an owner, maintain a custom
   schema, and evaluate or tune customization without turning those heuristics into
   vendor requirements.
1. **Project customization** — decisions derived from a concrete repository,
   existing OpenSpec state, project policy, and observed work.

OpenSpec owns its runtime contract. This Skill owns reusable customization judgment.
The target repository owns project-specific policy and evidence.

Do not copy fast-changing OpenSpec contracts into local guidance. Do not turn one
project's policy or one successful dogfood case into a reusable pattern by default.

## Reference routing

Load only the references whose independent concern actually applies. Reference
frontmatter `description` fields summarize applicability for search and discovery;
this section owns the package-level decision about when to load each reference.

| Reference | Load when | Do not load merely because... |
| --- | --- | --- |
| [Official customization](references/official-customization.md) | Exact OpenSpec support or behavior can change the answer | the task merely mentions OpenSpec |
| [Customization design](references/customization-design.md) | Choosing the narrowest owner, config versus schema, or how much context OpenSpec should receive | a custom schema already exists and only maintenance is in question |
| [Schema maintenance](references/schema-maintenance.md) | An existing or chosen custom schema needs package, documentation, fork, or long-term maintenance guidance | the task merely mentions or creates a schema |
| [Dogfood and tuning](references/dogfood-and-tuning.md) | An existing or candidate customization needs real-work evaluation, tuning, regression checking, baseline comparison, or resolved-behavior verification | the ownership decision can be made without empirical iteration |
| [Project customization](references/project-customization.md) | A concrete repository's current `openspec/` state, policy, integration, representative work, or dogfood evidence can change the decision | the task is generic |

Load multiple references only when their responsibilities independently apply. Do
not follow a chain merely because one reference links to another.

For a concrete repository, inspect its applicable live instructions and current
OpenSpec state before making project-specific recommendations or mutations.

## Workflow

1. Identify whether the request needs exact vendor contract, reusable customization
   judgment, project-specific evidence, or a combination.
1. Load only the focused references that can materially change the decision.
1. Keep sourced OpenSpec facts, reusable judgment, and project evidence
   distinguishable.
1. For a concrete repository, inspect only context that can change the decision.
1. Choose or change the smallest coherent customization owner when ownership is at
   issue.
1. If a custom schema becomes a durable maintenance surface, apply only the
   maintenance guidance it actually needs.
1. When quality or fit must be established empirically, dogfood representative work
   and tune the observed owner rather than stacking compensating instructions.
1. Verify runtime-dependent claims with evidence appropriate to that claim; consult
   the exact OpenSpec contract only when exact behavior matters.
1. When several concerns matter, report **Official**, **Pattern**, and **Project**
   conclusions separately.

## Self-check

- Exact OpenSpec behavior is supported by current official or target-version
  evidence when exact behavior matters.
- The official reference was not loaded only because the task mentioned OpenSpec.
- Focused reusable references were loaded for their own concern, not as a bundle.
- Reusable guidance is not presented as an OpenSpec requirement.
- Project choices come from repository or dogfood evidence.
- OpenSpec receives only context or structure it actually needs.
- Tuning changes an observed owner instead of accumulating duplicate guidance.
- Verification claims do not exceed what was inspected or run.

## Boundary

This Skill does not own ordinary OpenSpec change authoring, change implementation,
generic repository instruction authoring, or OpenSpec installation unless one is
directly required by a customization task.
