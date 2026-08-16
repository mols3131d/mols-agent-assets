# Rule Scope

Use this reference only when deciding where a rule should load or whether rule scopes overlap.

## Exact Scope

Prefer the narrowest structure that gives the rule to every intended target and no unrelated target.

- Project-wide rule -> root `AGENTS.md`.
- One contiguous directory subtree -> the highest `AGENTS.md` whose subtree still matches exactly.
- Cross-cutting file, extension, path, or repeated-directory scope -> a matching pattern rule asset.

Do not move a rule to a common ancestor when that ancestor would also apply it to unrelated descendants.

## Overlapping Scopes

When multiple owners or selectors apply the same rule to overlapping targets, keep only the placement needed to preserve the intended total scope.

A narrower placement is redundant when a broader owner already applies the same rule to all of its targets. A broader placement is wrong when it reaches targets that should not receive the rule.

## Unrepresentable Scope

If the runtime cannot express the intended combined scope exactly with one owner, keep the smallest set of correct owners even when some physical duplication remains.

Scope correctness outranks DRY.

## Verification Boundaries

Check intended targets and nearby non-targets around directory and pattern boundaries. When the complete affected set can be enumerated, verify it completely; otherwise report the check as sampled.
