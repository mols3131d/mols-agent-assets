---
name: mols-rule-ownership
description: >-
  Deduplicate and relocate existing agent rules so each rule has one canonical owner whenever the runtime can express its scope exactly. Use for DRY placement across root or nested AGENTS.md files and provider, harness, or vendor path/glob rule assets. Do not use to author policy, review wording, redesign runtime loading, or synchronize formats across harnesses.
---

# Rule Ownership

Optimize only the ownership and placement of existing agent rules.

## Assumption

Assume the target runtime correctly loads rules from applicable `AGENTS.md` files and matching path/glob rule assets. Treat that behavior as the context-injection contract; do not redesign or validate it.

Preserve a source of truth only when project rules or other evidence establish it. A rule's current location is not authority by itself. A generated or derived copy is not a canonical owner unless the project explicitly makes it authoritative.

## Priority

Resolve ownership in this order:

1. **Scope correctness**: intended targets receive the rule; unrelated targets do not.
2. **Source of truth**: preserve the authoritative rule source.
3. **Single ownership**: one rule has one canonical owner when its scope can be represented exactly.
4. **Minimum context**: load the rule only where needed.
5. **Simple structure**: use the fewest owners that preserve the goals above.

Never broaden scope or change policy merely to make the layout more DRY.

## Ownership Rules

- **Root `AGENTS.md`**: use for project-wide rules.
- **Nested `AGENTS.md`**: use for one directory subtree. Place the rule in the highest `AGENTS.md` whose subtree still matches the intended scope exactly.
- **Pattern rule asset**: use for cross-cutting path, glob, extension, file-class, or repeated-directory scope.

Treat concrete rule paths and selector syntax as runtime-specific. Preserve the project's supported format instead of assuming `.agents/rules/*` is universal.

## Workflow

### 1. Separate Rules

Split a mixed block only when its statements have different scopes. Treat two statements as the same rule only when their operational requirement, target scope, and exception or override intent are equivalent.

If equivalence, scope, authority, or override intent is ambiguous, preserve the existing rules and report unresolved ownership. Do not infer policy to achieve DRYness.

### 2. Find Scope

Identify where each rule is intended to load:

- project-wide;
- one contiguous directory subtree; or
- a cross-cutting path/glob scope.

### 3. Assign Owner

- Project-wide -> root `AGENTS.md`.
- Directory subtree -> the highest `AGENTS.md` whose subtree matches the intended scope exactly.
- Cross-cutting pattern -> one matching pattern rule asset.

Do not choose a common ancestor when it would load the rule for unrelated siblings. Do not assign canonical ownership to a generated or derived copy.

### 4. Remove Duplication

- Remove inherited repetitions from descendants.
- Move identical child rules upward only when the parent scope remains exact.
- Prefer one exact pattern rule when moving upward would affect unrelated siblings.
- Move an over-broad parent rule downward when only a narrower subtree needs it.
- Keep genuine scoped exceptions at their narrower owner without copying parent text.

If the runtime cannot express a combined scope exactly, keep the smallest correct owners even when some duplication is unavoidable.

### 5. Verify Loaded Rules

Derive the rules loaded for affected target and non-target files from ancestor `AGENTS.md` files plus matching pattern rules.

When available tools can enumerate every affected file, verify the complete set. Otherwise verify representative boundary cases and report the result as sampled rather than exact.

Confirm that:

- intended targets retain every rule;
- each rule with an exactly representable scope comes from one authoritative owner; and
- unrelated targets do not gain the rule.

## Guardrails

- Preserve rule meaning; only remove obsolete location wording required by a move.
- Do not use precedence to justify duplicated ownership.
- Create a new owner file only when no suitable exact owner exists.
- Do not author new engineering policy, improve rule content, redesign project structure, validate runtime behavior, or perform cross-harness synchronization.

## Completion

Complete when ownership changes preserve the source of truth and the strongest available loaded-rule check preserves the intended scope. Report only owner changes, removed duplicates or scope splits, unresolved ownership, and verification limits.
