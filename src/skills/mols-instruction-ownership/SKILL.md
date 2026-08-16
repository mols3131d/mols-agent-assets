---
name: mols-instruction-ownership
description: >-
  Deduplicate and relocate existing agent instructions so each semantic rule has
  one canonical owner at the narrowest exact load scope. Use for DRY placement
  across root or nested AGENTS.md files and provider, harness, or vendor path/glob
  rule assets, including promoting shared rules, demoting over-broad rules, and
  removing inherited duplicates. Do not use to author new policy, review rule
  wording, redesign runtime loading, or synchronize formats across harnesses.
---

# Instruction Ownership

Optimize only the ownership and placement of existing agent instructions.

## Loading Contract

Assume the target runtime correctly loads:

- applicable `AGENTS.md` instructions from the directory hierarchy; and
- provider, harness, or vendor rule assets when their path or glob selector
  matches the current work.

Do not redesign or validate that loading mechanism. Treat it as the context
injection contract to optimize against.

## Priority

Resolve ownership in this order:

1. **Exact scope**: every intended target receives the rule and unrelated targets
   do not.
2. **Single ownership**: one semantic rule has one canonical owner.
3. **Minimum context**: load the rule only where it is needed.
4. **Simple topology**: use the fewest owners that preserve the first three goals.

Never broaden a rule merely to reduce the number of instruction files.

## Owners

Choose the owner whose native scope most exactly represents the rule:

- **Root `AGENTS.md`** owns project-wide rules.
- **Nested `AGENTS.md`** owns rules for one directory subtree. Place the rule at
  the shallowest directory whose inherited scope is still exact.
- **Pattern rule asset** owns cross-cutting rules naturally expressed by path,
  glob, extension, file class, or repeated directory pattern.

Treat concrete rule-asset paths and selector syntax as runtime-specific. Discover
and preserve the project's supported format instead of assuming
`.agents/rules/*` is universal.

## Invariants

- Child `AGENTS.md` files do not repeat inherited parent rules.
- A parent does not own a rule that only some descendants need.
- A pattern rule does not duplicate an equivalent directory-owned rule.
- Precedence is not a substitute for DRY.
- Keep a parent/child override only when the difference is an intentional
  scope-specific rule.
- Preserve rule meaning. Relocation may make only the minimal wording adjustment
  needed to remove obsolete location references.
- Create an instruction owner file only when the required exact scope has no
  suitable existing owner.
- Do not create new engineering policy, improve rule content, redesign project
  structure, or perform cross-harness format synchronization.

If the available runtime mechanisms cannot represent an intended scope exactly,
preserve scope correctness even when unavoidable duplication remains and report
that limitation.

## Workflow

For each instruction:

### 1. Atomize

Split a mixed block only when its statements have different scopes. Treat
paraphrases with the same operational meaning as one semantic rule.

### 2. Map Scope

Identify where the rule is intended to load. Classify it as:

- project-wide;
- one contiguous directory subtree; or
- cross-cutting path/glob scope.

### 3. Assign Owner

- Project-wide -> root `AGENTS.md`.
- Exact subtree -> the shallowest exact nested `AGENTS.md`.
- Cross-cutting pattern -> one matching rule asset.

Do not use a common ancestor when it would inject the rule into unrelated
siblings.

### 4. Deduplicate

- Remove inherited repetitions from descendants.
- Promote identical child rules only when the promoted scope remains exact.
- If promotion would cover unrelated siblings, prefer one exact pattern owner.
- Demote an over-broad parent rule when only a narrower subtree needs it.
- Keep genuinely different scoped exceptions at their narrower owner without
  copying parent text.

### 5. Verify Projection

For representative target and non-target files, derive the instructions the
runtime would load from ancestor `AGENTS.md` files plus matching pattern rules.
Confirm that:

- every intended rule is present;
- each representable semantic rule comes from one canonical owner; and
- unrelated work does not receive the rule.

## Boundary Cases

- **Same rule in every child**: move upward only to the highest exact common
  directory scope.
- **Same rule in selected siblings**: use a pattern owner when their common
  ancestor would also cover unrelated siblings.
- **Same file-type rule across directories**: prefer a file-pattern owner over
  repeated subtree rules.
- **Subtree-specific exception**: keep the common rule at its common owner and the
  different exception at the narrower owner.
- **Unrepresentable exact union**: keep the smallest correct owners rather than
  broadening context for artificial DRYness.

## Completion

Complete when ownership changes are applied and projection verifies the intended
scope. Report only canonical owner changes, duplicates removed or scope-based
splits, and any scope the runtime cannot represent exactly.
