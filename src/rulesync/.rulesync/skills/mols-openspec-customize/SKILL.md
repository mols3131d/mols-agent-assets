---
name: mols-openspec-customize
description: >-
  Design, review, or apply OpenSpec customization while keeping three concerns
  distinct: current official customization mechanisms, reusable customization
  patterns, and adaptation to a concrete project or repository. Use when deciding
  how to customize OpenSpec profiles, project configuration, schemas, templates,
  or workflow behavior, or when fitting OpenSpec to an existing repository. Do not
  use for ordinary OpenSpec workflow usage, writing a specific change proposal or
  spec, or general repository guidance unrelated to OpenSpec customization.
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
1. **Customization patterns** — reusable guidance for choosing and composing those
   mechanisms.
1. **Project adaptation** — choices derived from the concrete repository, existing
   OpenSpec state, and local authority.

OpenSpec owns commands, fields, paths, precedence, and runtime semantics. This
Skill owns its reusable customization patterns. The target repository owns
project-specific policy and values.

Do not copy fast-changing OpenSpec contracts into local guidance. Do not turn one
project's policy into a reusable pattern by default.

## Route

Load only what the request needs:

- [Official](references/official.md) — current OpenSpec mechanisms and official
  source map.
- [Patterns](references/patterns.md) — reusable OpenSpec customization patterns.
- [Project adaptation](references/project-adaptation.md) — how to fit OpenSpec to a
  concrete project or repository.

Load multiple references when their responsibilities independently apply. For a
concrete repository, load its applicable live instructions and current OpenSpec
state before making project-specific recommendations or mutations.

## Workflow

1. Classify the request as official mechanism, reusable pattern, project adaptation,
   or a combination.
1. Load only the corresponding references and authority.
1. Separate sourced OpenSpec facts, reusable design judgment, and project-specific
   evidence.
1. For project adaptation, inspect the repository before choosing a customization
   surface.
1. Make or recommend the smallest coherent change.
1. Verify the affected instructions, schema, or resolution with the current CLI
   when the claim depends on runtime behavior.
1. When several concerns are material, report **Official**, **Pattern**, and
   **Project** decisions separately.

## Self-check

- Exact OpenSpec behavior is backed by current official material or observed CLI
  evidence.
- Reusable patterns are not presented as OpenSpec requirements.
- Project choices come from the target repository, not this Skill.
- OpenSpec receives only context or structure it actually needs.
- Verification claims do not exceed what was inspected or run.

## Boundary

This Skill does not own ordinary OpenSpec change authoring, implementation of a
change, generic repository instruction authoring, or OpenSpec installation unless
one is directly required by a customization request.
