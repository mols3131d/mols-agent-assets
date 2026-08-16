# Rule Placement

Use this reference only when choosing where an authoritative rule should live after its intended scope and source of truth are known.

## Direct Runtime Rules

When the authoritative source is a directly loaded runtime rule, choose the smallest editable container that represents the intended scope exactly:

- Project-wide scope -> root `AGENTS.md`.
- One directory subtree -> the highest `AGENTS.md` whose subtree still matches exactly.
- Cross-cutting file, extension, path, or repeated-directory scope -> a matching pattern rule asset.

Do not choose a common ancestor when it would load the rule for unrelated descendants.

## Precedence

Treat runtime precedence as part of effective behavior. Directory depth, selector specificity, file order, or source type may change how rules combine.

Do not move a rule across a precedence boundary unless the effective rule set remains unchanged for both intended targets and nearby non-targets.

## Multiple Placements

If one owner cannot represent the intended scope exactly, keep the smallest set of correct placements. Physical repetition is acceptable when it is required for scope correctness.

Do not introduce a new owner file when an existing editable owner already represents the same exact scope.

## Generated or Canonical Input Layers

If the authoritative source is a generator input, canonical configuration, or another layer that produces runtime rule files, preserve that layer's native structure. Do not apply the root/nested/pattern placement mapping to generated outputs.

Do not relocate or hand-edit generated runtime copies merely to make their physical layout DRY.

If changing the authoritative source would require derived copies to be regenerated and that regeneration is outside the current task, preserve the current state and report the synchronization boundary instead of leaving required copies stale.
