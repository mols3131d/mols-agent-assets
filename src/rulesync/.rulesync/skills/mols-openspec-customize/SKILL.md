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

Customize OpenSpec without mixing vendor contract, reusable pattern, and
project-local decisions.

## Contract

Keep three concerns distinct even when one task needs all of them:

1. **Official OpenSpec mechanisms** — what OpenSpec currently supports and where
   its authoritative documentation lives.
1. **Customization patterns** — reusable design guidance owned by the repository's
   canonical pattern library.
1. **Project adaptation** — choices derived from the concrete repository, existing
   OpenSpec state, and local authority.

OpenSpec owns its commands, fields, paths, precedence, and runtime semantics. The
pattern library owns reusable design guidance. The target repository owns
project-specific policy and values.

Do not copy fast-changing OpenSpec contracts into this Skill. Do not turn one
project's policy into a reusable pattern by default.

## Route

Load only what the request needs:

- [Official](references/official.md) — current OpenSpec mechanisms and official
  source map.
- [OpenSpec Customization Pattern](https://raw.githubusercontent.com/mols3131d/mols-agent-assets/refs/heads/main/catalog/patterns/workflow/openspec-customization.md)
  — reusable customization pattern. Treat that catalog document as canonical.
- [Project adaptation](references/project-adaptation.md) — how to fit OpenSpec to a
  concrete project or repository.

Load multiple sources when their responsibilities independently apply. For a
concrete repository, load its applicable live instructions and current OpenSpec
state before making project-specific recommendations or mutations.

## Decide

Choose the smallest surface that owns the requested effect, then confirm exact
mechanics in the current official documentation:

- workflow selection or delivery → profile;
- additive context, artifact rules, operation guidance, or schema selection →
  project configuration when supported;
- different artifacts, dependencies, templates, or schema-level instructions →
  custom schema;
- repository policy OpenSpec does not need to inject → existing repository owner.

Prefer configuration before a schema fork when both can express the same intent.
Prefer existing repository authority over policy duplication inside OpenSpec.

## Workflow

1. Classify the request as official mechanism, reusable pattern, project adaptation,
   or a combination.
1. Load only the corresponding authority.
1. Separate sourced OpenSpec facts from reusable design judgment.
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
- OpenSpec configuration contains only context OpenSpec actually needs.
- Schema customization is not used when lighter configuration is enough.
- Verification claims do not exceed what was inspected or run.

## Boundary

This Skill does not own ordinary OpenSpec change authoring, implementation of a
change, generic repository instruction authoring, or OpenSpec installation unless
one is directly required by a customization request.
