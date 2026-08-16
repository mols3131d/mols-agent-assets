---
name: mols-instruction-ownership
description: >-
  Place, move, split, and deduplicate agent instructions so each atomic rule has
  one canonical owner at the narrowest exact scope. Use when reorganizing
  instruction ownership across root or nested AGENTS.md files and provider,
  harness, or vendor rule assets with path or glob matching. Optimize context
  injection without changing rule meaning or inventing new project rules.
---

# Instruction Ownership

Assign each existing agent instruction to one canonical owner. Optimize only
ownership and placement.

## Assumptions

Assume the target agent runtime correctly loads:

- applicable `AGENTS.md` instructions from the directory hierarchy; and
- provider, harness, or vendor rule assets when their path or glob selector
  matches the current work.

Do not redesign or validate that loading mechanism. Use it as the context-injection
contract.

## Objective

Optimize in this order:

1. **Exact scope**: every intended target receives the rule and unrelated targets
   do not.
2. **Single ownership**: one semantic rule has one canonical owner.
3. **Minimum context**: inject the rule only where it is needed.
4. **Simple topology**: use the fewest owners that preserve the first three goals.

Never trade scope correctness for fewer files.

## Ownership Model

Use the owner whose native scope best matches the rule:

- **Root `AGENTS.md`**: rules that apply across the whole project.
- **Nested `AGENTS.md`**: rules whose scope is one directory subtree. Place the
  rule at the highest directory that covers the entire intended subtree without
  covering unrelated work.
- **Pattern rule asset**: rules whose scope is naturally expressed by path, glob,
  extension, file class, or repeated directory pattern across otherwise separate
  subtrees.

Treat concrete rule-asset paths and selector syntax as runtime-specific. Discover
and preserve the project's supported provider or harness format instead of
assuming `.agents/rules/*` is universal.

## Invariants

- One semantic rule has one canonical owner.
- Child `AGENTS.md` files do not repeat inherited parent rules.
- A parent does not own a rule that only some descendants need.
- A pattern rule does not duplicate an equivalent directory-owned rule.
- Precedence is not a substitute for DRY. Keep a parent/child override only when
  the difference is an intentional scope-specific rule.
- Preserve rule meaning. Relocation may make only the minimal wording adjustment
  required to remove obsolete location references.
- Do not create new engineering policy, improve rule content, or redesign project
  structure.

## Resolve Ownership

For each instruction:

1. **Atomize**
   - Split mixed instruction blocks only when different statements have different
     scopes.
   - Treat paraphrases with the same operational meaning as one semantic rule.

2. **Map targets**
   - Identify the files or directories where the rule is intended to apply.
   - Distinguish project-wide, contiguous subtree, and cross-cutting pattern scope.

3. **Choose the canonical owner**
   - Use root `AGENTS.md` only for truly project-wide rules.
   - Use the nearest exact subtree owner when directory ancestry expresses the
     scope without over-injection.
   - Use one pattern rule when a glob or selector expresses a disjoint or
     file-class scope more exactly than directory inheritance.

4. **Deduplicate**
   - Remove inherited repetitions from descendants.
   - Promote identical sibling rules only when the promoted scope remains exact.
   - If promotion would affect unrelated siblings, prefer an exact pattern owner
     instead of broadening the directory scope.
   - Demote an over-broad parent rule when only a narrower subtree needs it.

5. **Verify projection**
   - For representative target files, derive the instruction set that the runtime
     would load from ancestors plus matching pattern rules.
   - Confirm each semantic rule appears once from its canonical owner.
   - Confirm no intended target loses the rule and no unrelated target gains it.

## Boundary Cases

- **Same rule in every child**: move it upward only to the highest exact common
  scope.
- **Same rule in selected siblings only**: use a pattern owner when their common
  ancestor would also cover unrelated siblings.
- **File-type rule inside many directories**: prefer a file-pattern owner over
  repeating the rule in each subtree.
- **Subtree-specific exception**: keep the common rule at its common owner and the
  genuinely different exception at the narrower owner; do not duplicate the
  parent text in the child.
- **Unsupported exact union scope**: preserve correctness first. Do not broaden a
  rule merely to force single-file ownership.

## Output

When reporting work, state only:

- canonical owner changes;
- duplicates removed or rules split by scope; and
- any scope that could not be represented exactly by the available instruction
  mechanisms.

Do not expand the task into general instruction authoring, style review, runtime
evaluation, or agent architecture work.
