---
name: mols-agent-asset-dry
description: >-
  Make natural-language agent assets DRY without changing behavior. Use when skills, rules, prompts, or agent profiles repeat responsibilities, instructions, context, or authoritative content across files or scopes. Route through common duplication and ownership checks plus the matching asset-type reference. Do not use for executable assets such as hooks or tools, policy rewriting, cross-harness synchronization, or abstraction for its own sake.
---

# Agent Asset DRY

Remove avoidable repetition from skills, rules, prompts, and agents while preserving behavior and ownership.

## Contract

This Skill handles four natural-language asset types: **skill**, **rule**, **prompt**, and **agent**. Embedded metadata or frontmatter is in scope when it controls discovery, activation, scope, permissions, tools, or other behavior of those assets. Standalone hooks, tools, executable configuration, and general documentation are out of scope.

Classify an asset by responsibility, activation, load timing, and authority rather than filename, Markdown shape, or prompt-like text. If one file genuinely serves multiple asset roles and those roles cannot be separated safely, preserve it and report the ambiguity.

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

Load one matching reference for each asset type present in the requested work:

| Asset | Runtime role | Reference |
| --- | --- | --- |
| Skill | Repeatable workflow loaded on demand | [skill.md](references/skill.md) |
| Rule | Persistent or scoped policy loaded automatically | [rule.md](references/rule.md) |
| Prompt | Explicit reusable task entrypoint | [prompt.md](references/prompt.md) |
| Agent | Specialist role, isolated context, or scoped tools | [agent.md](references/agent.md) |

Read [duplication.md](references/duplication.md) when semantic equivalence, specialization, or repeated responsibility is unclear. Read [ownership.md](references/ownership.md) when source authority, generated copies, external ownership, competing owners, or harness-specific projections are involved.

## Workflow

### 1. Find Candidates

Inspect the requested assets and enough surrounding context to find repeated requirements, responsibilities, procedures, context, or projections. Do not classify similarity as duplication yet.

### 2. Preserve Type Semantics

Classify each candidate by runtime role, then load every matching asset reference needed for the requested set. Capture the behavior that must remain unchanged. If an asset type is ambiguous, preserve the current structure and report the ambiguity.

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
- When deduplication across harnesses requires reuse, generation, conversion, or synchronization, report that boundary instead of implementing it here.

## Completion

Complete when avoidable repetition is removed without changing behavior, authority, or intentional asset boundaries. Report consolidated responsibilities or requirements, preserved exceptions or projections, unresolved DRY issues, and verification limits.
