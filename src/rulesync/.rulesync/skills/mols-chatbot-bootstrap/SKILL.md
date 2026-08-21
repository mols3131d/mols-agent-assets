---
name: mols-chatbot-bootstrap
description: >-
  Bootstrap or update a repository for mols CHATBOT.md compatibility. Use when a
  repository should support chat runtimes that may not automatically load applicable
  AGENTS.md guidance, task-relevant Skills, or path-scoped Rules, including route
  metadata, generation, tuning, or drift validation.
---

# Mols Chatbot Bootstrap

Establish or repair the smallest repository-local compatibility harness that lets a chat
runtime reach the repository guidance and Agent Assets it cannot discover natively.

# Lifecycle

This is a low-frequency provisioning Skill, not baseline operational context.

- Reuse it across repositories when chatbot compatibility must be established or repaired;
  one repository may need it only once or occasionally.
- Keep it discoverable in a Skill source or catalog instead of persistently installing or
  loading it merely for possible future use.
- Prefer this consumer lifecycle when the runtime supports it: discover/select → temporary
  load → bootstrap or repair → release from active context.
- Persist or preinstall this Skill only when repeated access is explicitly useful in the
  target runtime or across repositories.
- After bootstrap, repository-local compatibility assets own the resulting harness. Normal
  repository work must not depend on this Skill remaining loaded or installed.
- Reinvoke it when the compatibility harness becomes missing or stale, or when runtime or
  repository architecture materially changes.

# Contract

- Inspect the target before changing it. A review-only request stays read-only, and an
  already-sufficient harness is a valid no-op result.
- Reuse native runtime behavior and established repository mechanisms before adding a
  compatibility layer.
- Recover only behavior the target chat runtime is actually missing. Treat missing
  `AGENTS.md`, Skill, and Rule discovery responsibilities independently; partial native
  support is a valid target state.
- When the runtime does not natively discover the repository entrypoint, connect a
  guaranteed runtime-side instruction surface to that entrypoint. If that surface cannot
  be changed or verified with current authority, return the exact required handoff and do
  not claim end-to-end compatibility is complete.
- Keep `AGENTS.md`, Skills, Rules, and other canonical assets authoritative; compatibility
  entrypoints and route metadata only connect the runtime to those owners.
- Preserve established target conventions. Do not impose one route layout, filename,
  metadata schema, generator, or CI model on every repository.
- Keep the harness independent of this Skill after provisioning.
- Preserve approved routing intent and user customization unless the requested repair
  explicitly supersedes them.
- Do not create route files, generators, validators, or CI merely because this Skill or a
  bundled resource makes them available.

# CHATBOT.md

For mols `CHATBOT.md` compatibility, keep one root `CHATBOT.md` and treat it as a minimal
repository entry/router, not another policy owner.

It should connect the runtime to the smallest useful existing or repository-local routing
surface needed to recover missing behavior such as:

- applicable `AGENTS.md` guidance;
- task-relevant Skill discovery and loading;
- target-path Rule discovery and loading.

Do not copy project policy, Skill bodies, Rule bodies, catalogs, or static path tables into
`CHATBOT.md`.

# Workflow

1. Inspect caller intent and the target runtime/repository state only as far as they can
   affect the compatibility decision: native discovery, guaranteed runtime instruction
   surfaces, existing guidance, entrypoints, routing surfaces, generators, validators, and
   CI.
1. Determine the exact missing or stale compatibility behavior. If native or existing
   mechanisms already cover it, reuse them and stop adding structure.
1. Establish or repair the smallest repository-side entrypoint and routing surface that
   closes the repository gap. Use the target's established representation when one exists.
1. If the runtime does not natively discover that entrypoint, establish the smallest
   runtime-side bootstrap that explicitly points to it and requires loading its routing
   guidance. When the runtime-side surface is outside current write authority, provide the
   exact handoff instead of pretending the first hop exists.
1. When no established route convention exists and a separate route surface is justified,
   use [Fallback route convention](references/routes.md) as the mols fallback rather than
   as a universal schema.
1. Use generation only when deterministic regeneration or drift checking provides concrete
   value. Prefer target-native or existing tooling; otherwise use the bundled reference
   generator only when its assumptions fit or a small adaptation is justified.
1. Tune routing metadata only when selection materially improves. Do not duplicate asset
   bodies or redefine authoritative applicability.
1. Add or adapt validation proportional to the created drift risk. Reuse existing local or
   CI checks before introducing another persistent mechanism.
1. Verify authority boundaries, preservation of intentional tuning, and that the resulting
   repository works without this Skill remaining active.

# Resources

Load only the resource needed for the current decision:

- [Fallback route convention](references/routes.md) — when a separate routing surface is
  needed and the target has no stronger established representation.
- [Generation and tuning](references/tuning.md) — when generation, regeneration, semantic
  route tuning, or drift validation is materially justified.
- `scripts/generate_routes.py` — when a compatible deterministic baseline generator or
  checker provides more value than a direct edit.
- `examples/github-actions-route-check.yml` — only when persistent CI validation is
  justified and the target lacks an equivalent check.

Bundled resources are reference implementations for this compatibility procedure, not
installation side effects or universal target assets.

# Validation

Verify only claims relevant to the resulting harness:

- when native discovery is insufficient, a guaranteed runtime-side bootstrap identifies the
  repository entrypoint and its loading expectation;
- the repository entrypoint is stable and actionable, and routing can reach the required
  repository guidance and Agent Assets without duplicating their bodies;
- missing `AGENTS.md`, Skill, and Rule discovery responsibilities are recovered only where
  the runtime lacks them;
- Skill selection remains semantic and Rule applicability preserves authoritative selector
  meaning;
- any generated metadata is deterministic for the assumptions actually used;
- validation checks factual drift without erasing approved semantic tuning;
- target-specific paths, formats, permissions, and CI behavior came from observable target
  authority rather than assumption;
- if the runtime-side first hop could not be established or observed, that limitation is
  reported rather than counted as completed compatibility;
- normal repository work no longer depends on this Skill being loaded or installed.

Prefer the smallest valid result over a uniform repository layout.

# Boundary

- This Skill provisions compatibility; it does not become the ongoing owner of repository
  guidance, Skill behavior, Rule behavior, routing semantics owned elsewhere, or routine
  repository work.
- It does not define a portable chatbot standard or guarantee automatic discovery of
  `CHATBOT.md` or any route path.
- It does not grant authority to modify runtime-side project, system, workspace, plugin, or
  harness configuration merely because such a bootstrap would complete the chain.
- It does not justify a separate Skill for bootstrap, repair, review, generation, tuning,
  or validation merely because those workflow branches exist inside the same outcome.
