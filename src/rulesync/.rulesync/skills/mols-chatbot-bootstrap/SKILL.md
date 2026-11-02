---
name: mols-chatbot-bootstrap
description: >-
  Design, establish, repair, or review the smallest chatbot harness when native instruction
  discovery, canonical loading, or required agent execution/delegation semantics need
  compatibility guidance. Use for runtime first-hop and bounded execution adaptation, not
  routine task execution, general agent architecture, route tuning, CI, or ongoing automation.
targets:
  - agentsskills
---

# Mols Chatbot Bootstrap

Design, establish, or repair the smallest effective compatibility path from the active chat
runtime into authoritative repository guidance and applicable agent behavior. If the
required discovery, loading, and execution semantics are already sufficient, leave the
existing harness unchanged.

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
- After bootstrap, the durable runtime-side pointer when needed and repository-local
  entry/router sustain the compatibility path; canonical repository assets retain their own
  authority. Normal repository work must not depend on this Skill remaining loaded or
  installed.
- Reinvoke it when the compatibility harness becomes missing or stale, or when runtime or
  repository architecture materially changes.

# Contract

- Inspect the target before changing it. A review-only request stays read-only, and an
  already-sufficient harness is a valid no-op result.
- Reuse native runtime behavior and established repository mechanisms before adding a
  compatibility layer. A no-op is an acceptable design outcome.
- Judge capabilities from the active runtime's exposed tools, access, and permission
  boundaries, not the product name or advertised features. Inspect only capabilities
  relevant to the missing harness behavior.
- Before changing repository or runtime state, confirm the intended target/ref, writable
  surface, approved scope, and execution identity. Available tools do not by themselves
  authorize side effects; never switch accounts or connections to overcome a denial.
- Recover only behavior the target chat runtime is actually missing. Consider applicable
  instruction, selection, execution/delegation, and authority responsibilities—including
  commands or agents when the target uses them—without assuming a universal asset inventory.
  Partial native support is a valid target state.
- If a required execution capability cannot be reproduced, design an explicit bounded
  adaptation, partial result, optional skip, or user-visible handoff rather than silently
  omitting work or claiming equivalent execution. Put disclosure in the target's normal-task
  instructions when future users will encounter the limitation, not only in the design report.
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

1. Resolve the requested design, provisioning, repair, or review outcome; the relevant
   repository/ref/path, current runtime mode, and authorized change boundary. Reuse
   already-provided facts rather than requiring a full environment questionnaire.
1. Inspect the target's native instruction, asset-selection, and execution paths and
   only the tools/permissions relevant to the requested harness behavior. Follow one
   applicable task from its guaranteed entry surface to its scoped source and required
   action where feasible; do not inventory every asset. Distinguish a configured locator
   from actually reading the authoritative source.
1. Identify missing responsibilities separately: runtime first-hop, applicable repository
   guidance, task-specific source selection and scope/ref resolution, canonical body or
   conditional reference loading, and required execution/delegation semantics. If existing
   mechanisms cover them, select no-op and do not add structure.
1. Compare the smallest viable options without treating them as mandatory stages:
   native/no-op; a runtime-side pointer to an existing entrypoint; a narrow selection
   bridge only for uncovered scope/loading; or bounded reuse of available native tools
   when an actual capability gap prevents access. Prefer the valid option with fewer
   new surfaces, context loads, tool calls, and maintenance obligations. Do not invent
   tools or install adapters as a default response to missing capability.
1. Establish or repair only the missing path within approved authority. Preserve the
   target's routing and customization; keep canonical policies and asset bodies in their
   owners. If no established route is sufficient and a separate route is justified, use
   [Fallback route convention](references/routes.md) only as a mols fallback. For an
   actual execution gap, use [Execution adaptation](references/execution-adaptation.md)
   to decide whether target-owned conditional guidance is needed. Never substitute an
   unauthorized tool or imply independent execution when only sequential work is possible.
   If an essential instruction surface or tool is inaccessible, provide an exact handoff.
1. Generate, tune, or validate routing metadata only where recurring drift or selection
   failure justifies it. Reuse target-native generators and checks before bundled
   [Generation and tuning](references/tuning.md) resources; do not create new CI by default.
1. Verify in evidence tiers: `configured` means the connection exists; `reachable`
   means the active runtime can follow it to the applicable canonical sources; and
   `observed applied` requires an actual task result consistent with their contract.
   For selected instructions/assets, check the applicable path/ref, canonical body and
   needed conditional references, not only route metadata; execution-specific fidelity
   also needs evidence for the actual action or explicitly reported gap. Existing native
   loading evidence may suffice without a redundant fetch. If behavior cannot be
   observed, report `not verified`.
1. Report the selected design/no-op, concrete changes and required user-side settings,
   authority constraints, validated tier, any adapted/partial/skipped/handed-off behavior,
   and relevant cost tradeoffs. Ensure the target's normal-task instructions re-evaluate
   applicable source/scope when the task or ref changes, without keeping this Skill loaded.
   Do not claim equivalence across runtimes.

# Resources

Load only the resource needed for the current decision:

- [Fallback route convention](references/routes.md) — when a separate routing surface is
  needed and the target has no stronger established representation.
- [Execution adaptation](references/execution-adaptation.md) — only when an applicable
  tool, command, script, delegation, or other execution contract is not natively supported
  and chatbot-facing fallback, partial, skip, or handoff guidance must be designed.
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
- applicable canonical instructions/asset bodies and necessary conditional references
  can be consumed at the correct scope/ref, rather than stopping at names or metadata;
- configuration, source reachability, and observed behavior are reported at their actual
  evidence tier; a missing trace is not converted into a successful runtime evaluation;
- any generated metadata is deterministic for the assumptions actually used;
- validation checks factual drift without erasing approved semantic tuning;
- target-specific paths, formats, permissions, and CI behavior came from observable target
  authority rather than assumption;
- if the runtime-side first hop could not be established or observed, that limitation is
  reported rather than counted as completed compatibility;
- any persistent execution fallback is triggered only for a confirmed gap, uses a
  target-owned surface the chatbot reads, and reports meaningful partial, skipped, or
  handed-off work to the task user; required semantics and permissions are not weakened;
- normal repository work no longer depends on this Skill being loaded or installed.

Prefer the smallest valid result over a uniform repository layout.

# Boundary

- This Skill provisions compatibility; it does not become the ongoing owner of repository
  guidance, Skill behavior, Rule behavior, routing semantics owned elsewhere, or routine
  repository work.
- It does not define a portable chatbot standard or guarantee automatic discovery of
  `CHATBOT.md` or any route path. Native sufficiency can require no compatibility files.
- It does not grant authority to modify runtime-side project, system, workspace, plugin, or
  harness configuration merely because such a bootstrap would complete the chain.
- It does not own generic tool provisioning, ongoing task execution, or runtime tool/agent
  contracts. It designs target-specific guidance for unavailable capabilities but cannot
  guarantee behavior parity when the source harness requires unsupported semantics.
- It does not justify a separate Skill for bootstrap, repair, review, generation, tuning,
  or validation merely because those workflow branches exist inside the same outcome.
