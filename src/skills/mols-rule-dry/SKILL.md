---
name: mols-rule-dry
description: >-
  Make existing agent rules DRY without changing their meaning, intended application, or source authority. Use when rule guidance is duplicated, restated through inheritance, applied by overlapping rule mechanisms, or repeated in generated or native rule files. Resolve duplication, application, ownership, and placement separately. Do not use to author policy, improve rule wording, redesign runtime loading, or synchronize formats across harnesses.
---

# Rule DRY

Make existing agent rules DRY without changing policy or intended application.

## Contract

Assume the target runtime honors its supported rule loading, attachment, and precedence model. Discover the project's supported rule containers and metadata before changing placement; do not redesign or validate the runtime itself.

Set the write boundary from the request. Read outside that boundary only when needed to understand applicable ancestors, selectors, attachment metadata, source authority, or generated projections. Do not mutate outside the write boundary without explicit authority.

Apply DRY in this order:

1. **Application correctness**: the rule remains available or applied in every intended situation and no unintended situation gains it.
2. **Source of truth**: preserve the authoritative rule source.
3. **Single ownership**: remove duplicate authority when the runtime and project structure allow it.
4. **Minimum context**: avoid repeated rule context where the runtime already provides the same guidance.
5. **Simple structure**: do not add abstraction merely to reduce repetition.

Never trade policy, application correctness, or source authority for DRY.

## Workflow

### 1. Find Candidates

Inspect rule-bearing files in the write boundary and any external rule context needed to understand them. Collect repeated statements, inherited restatements, overlapping selectors or attachment conditions, and repeated generated copies. Do not decide that they are duplicates yet.

### 2. Resolve Application

Determine when each candidate currently applies and when it is intended to apply before comparing or moving it. Read [application.md](references/application.md) when target boundaries, attachment conditions, overlap, or runtime representability must be decided.

### 3. Decide Duplication

Compare candidates only after their application conditions are known. Read [duplication.md](references/duplication.md) when deciding semantic equivalence, inherited restatement, repeated requirements across scopes or attachment modes, or genuine exception intent.

### 4. Resolve Source of Truth

Determine which source is authoritative for confirmed repeated requirements. Read [ownership.md](references/ownership.md) when authority is unclear, multiple sources claim ownership, or generated or derived copies are involved.

### 5. Choose Placement

Choose where the authoritative editable rule should live after application and authority are known. Read [placement.md](references/placement.md) to map the resolved application to the project's supported rule containers and metadata while preserving precedence.

### 6. Apply and Verify

Remove only avoidable duplication from authoritative editable rules inside the write boundary. Keep genuine exceptions, required derived copies, and physical repetition needed to preserve application behavior.

Verify declared application, attachment metadata, precedence, source authority, and generated relationships statically. When runtime selection or relevance behavior cannot be proven without an evaluation system, report it as unverified rather than claiming behavioral validation.

## Guardrails

- Preserve rule meaning. Do not rewrite policy as part of deduplication.
- Preserve ambiguous cases and report them instead of guessing.
- Do not use precedence to justify duplicate authority.
- Do not assume one provider's rule paths, metadata, or attachment modes are universal.
- Do not create a shared schema, indirection layer, or new rule framework merely to eliminate repetition.
- Do not hand-edit generated or derived copies merely to make them physically DRY.
- If a source change would require synchronization outside the current task, preserve the current state and report that boundary.
- Do not author new policy, redesign project structure or runtime loading, validate runtime behavior, or perform cross-harness synchronization.

## Completion

Complete when avoidable rule duplication is removed without changing policy, intended application, precedence, or source authority. Report changed owners or placements, removed duplication, preserved exceptions or required copies, unresolved DRY issues, and verification limits.
