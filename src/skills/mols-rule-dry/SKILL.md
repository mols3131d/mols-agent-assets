---
name: mols-rule-dry
description: >-
  Make existing agent rules DRY without changing their meaning. Use when rules are duplicated, repeated across parent and child AGENTS.md files, scattered across overlapping scopes, or copied into path/glob rule assets. Consolidate rule ownership and placement while preserving exact scope and the authoritative source. Do not use to author policy, improve rule wording, redesign runtime loading, or synchronize formats across harnesses.
---

# Rule DRY

Make existing agent rules DRY without changing policy.

## Assumption

Assume the target runtime correctly loads rules from applicable `AGENTS.md` files and matching path/glob rule assets. Treat that behavior as the context-injection contract; do not redesign or validate it.

## Priority

Apply DRY in this order:

1. **Scope correctness**: intended targets receive the rule; unrelated targets do not.
2. **Source of truth**: preserve the authoritative rule source.
3. **Single ownership**: use one canonical owner when the runtime can express the intended scope exactly.
4. **Minimum context**: load the rule only where needed.
5. **Simple structure**: use the fewest owners that preserve the goals above.

Never broaden scope or change policy merely to remove duplication.

## References

Read only the reference needed for the current decision:

| Decision | Reference |
| --- | --- |
| Decide whether rules are actually duplicates, inherited restatements, or genuine exceptions | [duplication.md](references/duplication.md) |
| Decide the exact directory or path/glob scope and resolve overlapping scopes | [scope.md](references/scope.md) |
| Decide the authoritative source, canonical owner, or treatment of generated copies | [ownership.md](references/ownership.md) |

## Workflow

### 1. Find Repetition

Inspect the rule-bearing files inside the requested boundary and identify repeated or overlapping rules. Read [duplication.md](references/duplication.md) when equivalence or exception intent must be decided.

### 2. Resolve Scope

Determine where each repeated rule is intended to load. Read [scope.md](references/scope.md) when choosing between root `AGENTS.md`, nested `AGENTS.md`, or a path/glob rule asset, or when scopes overlap.

### 3. Resolve Ownership

Determine the authoritative source and canonical owner only after scope is known. Read [ownership.md](references/ownership.md) when authority is unclear, multiple owners exist, or generated or derived copies are involved.

### 4. Remove Avoidable Duplication

Keep one authoritative rule where the runtime can represent its scope exactly. Remove inherited restatements and redundant overlapping placements. Keep genuine exceptions and unavoidable physical duplication.

### 5. Verify Loaded Rules

Check that intended targets retain every rule, unrelated targets gain none, and generated copies do not become independent owners. Verify the complete affected set when possible; otherwise check representative boundaries and report the result as sampled.

## Guardrails

- Preserve rule meaning; only remove obsolete location wording required by a move.
- Do not use precedence to justify duplicated ownership.
- Create a new owner file only when no suitable exact owner exists.
- Do not author new policy, improve rule content, redesign project structure or runtime loading, validate runtime behavior, or perform cross-harness synchronization.
- If equivalence, scope, or authority remains ambiguous, preserve the existing rules and report the unresolved DRY issue.

## Completion

Complete when avoidable rule duplication is removed, scope and authority are preserved, and the strongest available loaded-rule check passes. Report owner changes, duplicates removed, scope splits, unresolved DRY issues, and verification limits.
