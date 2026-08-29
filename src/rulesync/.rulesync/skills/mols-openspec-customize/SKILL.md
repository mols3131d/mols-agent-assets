---
name: mols-openspec-customize
description: >-
  Design, review, dogfood, tune, or adapt OpenSpec customization while keeping
  three concerns distinct: current official customization mechanisms, reusable
  customization patterns, and adaptation to a concrete project or repository.
  Use when customizing or iterating OpenSpec profiles, project configuration,
  schemas, templates, or workflow behavior, including project-local schema
  maintenance and evidence-driven tuning. Do not use for ordinary OpenSpec
  workflow usage such as applying a change, writing a specific change proposal or
  spec, implementing a change, or general repository guidance unrelated to OpenSpec
  customization.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
---

# Mols OpenSpec Customize

Customize OpenSpec without mixing vendor contract, reusable design judgment, and
project-local decisions.

## Contract

Keep three concerns distinct even when one task needs all of them:

1. **Official OpenSpec mechanisms** — what OpenSpec currently supports and where
   its authoritative documentation lives.
1. **Customization patterns** — reusable guidance for choosing, maintaining, and
   tuning those mechanisms.
1. **Project adaptation** — choices derived from the concrete repository, existing
   OpenSpec state, and observed project use.

OpenSpec owns commands, fields, paths, precedence, and runtime semantics. This
Skill owns reusable customization judgment. The target repository owns
project-specific policy, values, and durable tuning rationale.

Do not copy fast-changing OpenSpec contracts into local guidance. Do not turn one
project's policy or one successful dogfood case into a reusable pattern by default.

## Route

Load only what the request needs:

- [Official](references/official.md) — current OpenSpec mechanisms, official source
  map, and schema package boundaries.
- [Patterns](references/patterns.md) — reusable customization, schema maintenance,
  dogfooding, and tuning patterns.
- [Project adaptation](references/project-adaptation.md) — concrete repository
  adaptation and project-specific evidence.

Load multiple references when their responsibilities independently apply. For a
concrete repository, load its applicable live instructions and current OpenSpec
state before making project-specific recommendations or mutations.

## Workflow

1. Classify the request as official mechanism, reusable pattern, project adaptation,
   or a combination.
1. Load only the corresponding references and authority.
1. Separate sourced OpenSpec facts, reusable design judgment, and project-specific
   evidence.
1. Inspect a concrete repository before choosing or tuning its customization
   surface.
1. Make or recommend the smallest coherent change.
1. When tuning matters, use representative project work to locate material friction
   and change its owning surface rather than layering compensating instructions.
1. Verify the affected instructions, schema, templates, or resolution with current
   OpenSpec tooling when the claim depends on runtime behavior.
1. When several concerns are material, report **Official**, **Pattern**, and
   **Project** decisions separately.

## Self-check

- Exact OpenSpec behavior is backed by current official material or observed CLI
  evidence.
- Reusable patterns are not presented as OpenSpec requirements.
- Project choices and tuning decisions come from repository or dogfood evidence.
- OpenSpec receives only context or structure it actually needs.
- Tuning addresses an observed owner instead of accumulating duplicate guidance.
- Verification claims do not exceed what was inspected or run.

## Boundary

This Skill does not own ordinary OpenSpec change authoring, implementation of a
change, generic repository instruction authoring, or OpenSpec installation unless
one is directly required by a customization request.
