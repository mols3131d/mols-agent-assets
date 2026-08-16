---
name: mols-rule-dry
description: >-
  Make existing agent rules DRY without changing their meaning or intended scope. Use when rules are duplicated, repeated through inheritance, applied by overlapping scopes, or copied into generated or path/glob rule assets. Resolve duplicate statements, exact scope, source authority, and placement separately. Do not use to author policy, improve rule wording, redesign runtime loading, or synchronize formats across harnesses.
---

# Rule DRY

Make existing agent rules DRY without changing policy or intended scope.

## Contract

Assume the target runtime correctly loads rules from applicable `AGENTS.md` files and matching path/glob rule assets. Treat that loading behavior as a given; do not redesign or validate it.

Set the write boundary from the request. Read outside that boundary only when needed to understand applicable ancestors, matching selectors, source authority, or generated projections. Do not mutate outside the write boundary without explicit authority.

Apply DRY in this order:

1. **Scope correctness**: intended targets receive the rule and unrelated targets do not.
2. **Source of truth**: preserve the authoritative rule source.
3. **Single ownership**: remove duplicate authority when the runtime and project structure allow it.
4. **Minimum context**: avoid loading repeated rules where inheritance or exact selectors already cover them.
5. **Simple structure**: do not add abstraction merely to reduce repetition.

Never trade policy or scope correctness for DRY.

## Workflow

### 1. Find Candidates

Inspect rule-bearing files in the write boundary and any external rule context needed to understand them. Collect repeated statements, inherited restatements, overlapping selectors, and repeated generated copies. Do not decide that they are duplicates yet.

### 2. Resolve Scope

Determine the intended target set for each candidate before comparing or moving it. Read [scope.md](references/scope.md) when target boundaries, overlap, or runtime representability must be decided.

### 3. Decide Duplication

Compare candidates only after their target sets are known. Read [duplication.md](references/duplication.md) when deciding semantic equivalence, inherited restatement, repeated requirements across scopes, or genuine exception intent.

### 4. Resolve Source of Truth

Determine which source is authoritative for confirmed duplicate rules. Read [ownership.md](references/ownership.md) when authority is unclear, multiple sources claim ownership, or generated or derived copies are involved.

### 5. Choose Placement

Choose where the authoritative editable rule should live after scope and authority are known. Read [placement.md](references/placement.md) to map the resolved scope to root `AGENTS.md`, nested `AGENTS.md`, pattern rules, or multiple exact placements.

### 6. Apply and Verify

Remove only avoidable duplication from authoritative editable rules inside the write boundary. Keep genuine exceptions, required derived copies, and physical repetition needed for exact scope.

Verify that intended targets retain every rule, unrelated targets gain none, precedence-dependent behavior is preserved, and required projections do not become independent sources of truth. Verify the complete affected set when possible; otherwise check representative boundaries and report the result as sampled.

## Guardrails

- Preserve rule meaning. Do not rewrite policy as part of deduplication.
- Preserve ambiguous cases and report them instead of guessing.
- Do not use precedence to justify duplicate authority.
- Do not create a shared schema, indirection layer, or new rule framework merely to eliminate repetition.
- Do not hand-edit generated or derived copies merely to make them physically DRY.
- If a source change would require synchronization outside the current task, preserve the current state and report that boundary.
- Do not author new policy, redesign project structure or runtime loading, validate runtime behavior, or perform cross-harness synchronization.

## Completion

Complete when avoidable rule duplication is removed without changing policy, scope, precedence, or source authority. Report changed owners or placements, removed duplication, preserved exceptions or required copies, unresolved DRY issues, and verification limits.
