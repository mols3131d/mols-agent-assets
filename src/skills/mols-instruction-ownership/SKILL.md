---
name: mols-instruction-ownership
description: >-
  Deduplicate and relocate existing agent instructions so each semantic rule has
  one canonical owner at the narrowest exact load scope. Use for DRY placement
  across root or nested AGENTS.md files and provider, harness, or vendor path/glob
  rule assets. Do not use to author policy, review wording, redesign runtime
  loading, or synchronize formats across harnesses.
---

# Instruction Ownership

Optimize only the ownership and placement of existing agent instructions.

## Contract

Assume the target runtime correctly loads applicable directory-hierarchy
instructions and path/glob rule assets. Treat that behavior as the
context-injection contract; do not redesign or validate it.

Preserve project-declared or otherwise evidenced source authority. Do not treat a
rule's current location as authority by itself. A generated or derived instruction
projection is not a canonical owner unless project authority explicitly makes it
authoritative.

## Priority

Resolve ownership in this order:

1. **Exact scope**: intended targets receive the rule; unrelated targets do not.
2. **Source authority**: preserve the project's authoritative instruction source.
3. **Single ownership**: one representable semantic rule has one canonical owner.
4. **Minimum context**: load the rule only where needed.
5. **Simple topology**: use the fewest owners that preserve the goals above.

Never broaden scope or change policy merely to make the layout more DRY.

## Owners

- **Root `AGENTS.md`**: project-wide rules.
- **Nested `AGENTS.md`**: one directory subtree; use the shallowest exact owner.
- **Pattern rule asset**: cross-cutting path, glob, extension, file-class, or
  repeated-directory scope.

Treat concrete rule paths and selector syntax as runtime-specific. Preserve the
project's supported format instead of assuming `.agents/rules/*` is universal.

## Workflow

### 1. Atomize

Split a mixed block only when its statements have different scopes. Treat two
statements as the same semantic rule only when their operational requirement,
target scope, and exception or override intent are equivalent.

If equivalence, scope, authority, or override intent is ambiguous, preserve the
existing rules and report unresolved ownership. Do not infer policy to achieve
DRYness.

### 2. Map Scope

Identify where each rule is intended to load:

- project-wide;
- one contiguous directory subtree; or
- cross-cutting path/glob scope.

### 3. Assign Owner

- Project-wide -> root `AGENTS.md`.
- Exact subtree -> shallowest exact nested `AGENTS.md`.
- Cross-cutting pattern -> one matching rule asset.

Do not choose a common ancestor when it would inject the rule into unrelated
siblings. Do not assign canonical ownership to a derived projection.

### 4. Deduplicate

- Remove inherited repetitions from descendants.
- Promote identical child rules only when the promoted scope stays exact.
- Prefer one exact pattern owner when promotion would cover unrelated siblings.
- Demote an over-broad parent rule when only a narrower subtree needs it.
- Keep genuine scoped exceptions at their narrower owner without copying parent
  text.

If the runtime cannot represent an exact union scope, keep the smallest correct
owners even when duplication is unavoidable.

### 5. Verify Projection

Derive the instructions loaded for affected target and non-target files from
ancestor `AGENTS.md` files plus matching pattern rules.

When available tools can enumerate the affected set, verify the complete set.
Otherwise verify representative boundaries and report the result as sampled, not
exact.

Confirm that:

- intended targets retain every rule;
- each representable semantic rule comes from one authoritative owner; and
- unrelated targets do not gain the rule.

## Guardrails

- Preserve rule meaning; only remove obsolete location wording required by a move.
- Precedence is not a substitute for DRY.
- Create a new owner file only when no suitable exact owner exists.
- Do not author new engineering policy, improve rule content, redesign project
  structure, validate runtime behavior, or perform cross-harness synchronization.

## Completion

Complete when ownership changes preserve authority and the strongest available
projection check preserves intended scope. Report only owner changes, removed
duplicates or scope splits, unresolved ownership, and verification limitations.
