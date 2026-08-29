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

Design and maintain OpenSpec customization while keeping **vendor facts, reusable
guidance, and project evidence** separate.

## Responsibility

| Concern | Authority | This Skill's role |
| --- | --- | --- |
| Exact OpenSpec contract | Current official sources and the target project's actual OpenSpec version/runtime | Route exact behavior questions to the right evidence |
| Reusable customization guidance | This Skill | Choose an owner, maintain a custom schema, and dogfood or tune customization |
| Project-specific decisions | Target repository | Derive only the OpenSpec delta supported by live project evidence |

Do not copy fast-changing OpenSpec contracts into reusable guidance. Do not promote
one project's policy or one successful dogfood case into a reusable default without
independent justification.

## Reference routing

Load only the references whose independent concern can change the decision.
Reference frontmatter `description` fields help search and discovery; this table owns
the package-level load decision.

| Reference | Load when | Do not load merely because... |
| --- | --- | --- |
| [Official contract](references/official-contract.md) | Exact OpenSpec support or behavior can change the answer | the task merely mentions OpenSpec |
| [Customization design](references/customization-design.md) | Choosing the narrowest owner, config versus schema, or how much context OpenSpec should receive | a custom schema already exists and only maintenance is in question |
| [Schema maintenance](references/schema-maintenance.md) | An existing or chosen custom schema needs package, documentation, ownership, or long-term maintenance guidance | the task merely mentions or creates a schema |
| [Dogfood and tuning](references/dogfood-and-tuning.md) | An existing or candidate customization needs empirical evaluation, tuning, regression checking, or resolved-behavior verification | ownership can be decided without empirical iteration |
| [Project customization](references/project-customization.md) | A concrete repository's current `openspec/` state, policy, integration, representative work, or dogfood evidence can change the decision | the task is generic |

Load multiple references only when their concerns independently apply. Do not follow
a reference chain merely because links exist.

## Workflow

1. Classify the request as exact contract, reusable guidance, project evidence, or a
   combination.
1. Load only references that can materially change the decision.
1. For a concrete repository, inspect applicable live instructions and current
   OpenSpec state before project-specific recommendations or mutations.
1. When ownership is at issue, choose the smallest coherent customization owner.
1. When quality or fit needs empirical evidence, dogfood representative work and
   tune the observed owner instead of stacking compensating instructions.
1. Match verification to the claim; consult the exact OpenSpec contract only when
   exact behavior matters.
1. When the distinction matters, report **Official**, **Reusable**, and **Project**
   conclusions separately.

## Self-check

- Exact OpenSpec claims use current official or target-version evidence when needed.
- References were loaded for their own concern, not by keyword or link-chain habit.
- Reusable guidance is not presented as an OpenSpec requirement, and project
  evidence is not promoted to a reusable default without justification.
- OpenSpec receives only the context or structure it needs; tuning changes the
  observed owner instead of accumulating duplicate guidance.
- Verification claims do not exceed what was inspected or run.

## Boundary

This Skill does not own ordinary OpenSpec change authoring or implementation,
generic repository instruction authoring, or installation unless one is directly
required by customization work.
