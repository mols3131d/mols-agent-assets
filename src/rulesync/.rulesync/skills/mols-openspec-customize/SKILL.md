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

Keep these concerns distinct even when one task needs all three:

1. **Official OpenSpec mechanisms** — what OpenSpec currently supports and the
   authoritative documentation for exact behavior.
1. **Customization patterns** — reusable design guidance for choosing and composing
   those mechanisms.
1. **Project adaptation** — decisions derived from the concrete repository,
   existing OpenSpec state, and local authority.

Official OpenSpec sources own fields, commands, paths, precedence, and runtime
semantics. Patterns in this Skill are advisory. Project instructions and repository
state own project-specific choices.

Do not copy fast-changing OpenSpec contracts into local guidance when a current
official source can own them. Do not promote one project's policy into a reusable
pattern merely because it worked once.

## Route

Read only the reference needed for the current request:

- [Official](references/official.md) — use when the task asks what OpenSpec supports,
  how a customization mechanism works, or when exact current commands, fields,
  paths, or semantics matter.
- [Patterns](references/patterns.md) — use when designing or reviewing a reusable
  OpenSpec customization approach.
- [Project adaptation](references/project-adaptation.md) — use when a concrete
  project or repository must be inspected and OpenSpec should be fitted to it.

Load multiple references when their responsibilities independently apply. When a
concrete repository is involved, load its applicable live instructions and current
OpenSpec files before making project-specific recommendations or mutations.

## Decide

Choose the smallest OpenSpec customization surface that owns the requested effect.
Use the current official documentation to confirm exact mechanics.

As a decision boundary:

- workflow selection or delivery belongs to the profile surface;
- additive project context, artifact-specific rules, operation guidance, and schema
  selection belong to project configuration when the official contract supports
  them;
- artifact set, dependency flow, templates, or workflow instructions that require
  structural replacement belong to a custom schema;
- repository policy that does not need OpenSpec injection should remain with its
  existing project owner.

Prefer an additive configuration change before a schema fork when both can express
the same intent. Prefer the repository's existing authority over duplicating policy
inside OpenSpec.

## Workflow

1. Classify the request as official mechanism, reusable pattern, project adaptation,
   or a combination.
1. Load only the corresponding references and current authority.
1. Separate sourced OpenSpec facts from local design judgment.
1. For project adaptation, inspect the repository before choosing a customization
   surface.
1. Make or recommend the smallest coherent change that satisfies the requested
   behavior.
1. Verify the affected OpenSpec output or schema with the current CLI when runtime
   evidence is available and the claim depends on it.
1. Report official behavior, reusable pattern decisions, and project-specific
   decisions separately when more than one is material.

## Self-check

Before finalizing, verify that:

- exact OpenSpec behavior is supported by a current official source or observed CLI
  evidence;
- reusable patterns are not presented as official OpenSpec requirements;
- project-specific choices are grounded in the target repository rather than
  assumed from this Skill;
- configuration contains only context OpenSpec actually needs;
- schema customization is used only when lighter configuration cannot express the
  required structural change;
- canonical repository policy has not been duplicated without a concrete OpenSpec
  need;
- verification claims do not exceed what was actually inspected or run.

## Boundary

This Skill does not own ordinary OpenSpec change authoring, implementation of an
OpenSpec change, generic repository instruction authoring, or installation of
OpenSpec itself unless those tasks are directly required to complete a
customization request.
