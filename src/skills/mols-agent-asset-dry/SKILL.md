---
name: mols-agent-asset-dry
description: >-
  Make natural-language agent assets DRY without changing behavior. Use when skills, rules, prompts, or agent profiles repeat responsibilities, instructions, context, or authoritative content across files or scopes. Route through common duplication and ownership checks plus the matching asset-type reference. Do not use for executable assets such as hooks or tools, policy rewriting, cross-harness synchronization, or abstraction for its own sake.
---

# Agent Asset DRY

Remove avoidable repetition from skills, rules, prompts, and agents while preserving behavior and ownership.

## Contract

This Skill handles four natural-language asset types: **skill**, **rule**, **prompt**, and **agent**. Treat reusable command or workflow prompts as prompts. Do not extend this workflow to hooks, tools, executable configuration, or general documentation.

Classify an asset by its runtime role and activation model, not by filename, Markdown shape, or the fact that it contains prompt-like text. If one file genuinely serves multiple asset roles and those roles cannot be separated safely, preserve it and report the ambiguity.

Set the write boundary from the request. Read outside that boundary only when needed to establish inheritance, references, activation, source authority, or generated projections. Do not mutate outside the write boundary without explicit authority.

Preserve every behavior-relevant distinction that applies to the asset, including purpose, discoverability, activation or load timing, scope, authority, permissions or tools, outputs, precedence, dependencies, and release lifecycle.

Apply DRY in this order:

1. **Behavior correctness**: the asset still activates, loads, delegates, and produces results as intended.
2. **Source of truth**: preserve the authoritative source and keep projections derived.
3. **Single ownership**: one responsibility or requirement has one owner when the asset model can represent that safely.
4. **Minimum context**: avoid loading or repeating content where inheritance, references, or routing already provide it.
5. **Simple structure**: do not add indirection merely to remove text.

Never trade behavior or authority for textual DRYness.

## Routing

Load the matching asset reference before changing structure:

| Asset | Reference |
| --- | --- |
| Skill | [skill.md](references/skill.md) |
| Rule | [rule.md](references/rule.md) |
| Prompt or reusable command prompt | [prompt.md](references/prompt.md) |
| Agent or subagent profile | [agent.md](references/agent.md) |

Read [duplication.md](references/duplication.md) when semantic equivalence, specialization, or repeated responsibility is unclear. Read [ownership.md](references/ownership.md) when source authority, generated copies, or competing owners are involved.

## Workflow

### 1. Find Candidates

Inspect the requested assets and enough surrounding context to find repeated requirements, responsibilities, procedures, context, or projections. Do not classify similarity as duplication yet.

### 2. Preserve Type Semantics

Classify each candidate by runtime role, then load the matching asset reference and capture the behavior that must remain unchanged. If the asset type is ambiguous, preserve the current structure and report the ambiguity.

### 3. Decide Duplication

Compare the smallest independently meaningful units. Use the common duplication reference when equivalence or specialization is uncertain. Content shared across different asset types is not automatically duplication because activation and authority may differ.

### 4. Resolve Ownership

Identify the authoritative source for content that is safe to consolidate. Use the ownership reference when authority is not already explicit.

### 5. Apply the Smallest DRY Move

Prefer deletion of redundant restatements, reuse of an existing canonical owner, or type-native composition. Keep intentional specialization, independent entrypoints, required projections, and physical repetition needed to preserve behavior.

### 6. Verify

Re-derive the affected assets' discoverability, activation, loaded context, authority, permissions, outputs, dependencies, and lifecycle as applicable. Verify the complete affected set when feasible; otherwise test representative boundaries and report the check as sampled.

## Guardrails

- Preserve meaning; do not improve wording or invent policy as part of deduplication.
- Do not merge assets solely because they share text.
- Do not migrate content between asset types merely to make it DRY unless the request explicitly includes that migration and behavior remains equivalent.
- Do not create hidden cross-package dependencies, shared schemas, inheritance layers, or new frameworks merely to remove repetition.
- Do not hand-edit generated or derived copies merely to make them physically DRY.
- Preserve ambiguous cases and report them instead of guessing.
- Do not perform cross-harness generation, conversion, or synchronization.

## Completion

Complete when avoidable repetition is removed without changing behavior, authority, or intentional asset boundaries. Report consolidated responsibilities or requirements, preserved exceptions or projections, unresolved DRY issues, and verification limits.
