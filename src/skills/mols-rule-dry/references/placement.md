# Rule Placement

Use this reference only when choosing where an authoritative rule should live after its intended scope and source of truth are known.

## Placement

Choose the smallest editable rule container that represents the intended scope exactly:

- Project-wide scope -> root `AGENTS.md`.
- One directory subtree -> the highest `AGENTS.md` whose subtree still matches exactly.
- Cross-cutting file, extension, path, or repeated-directory scope -> a matching pattern rule asset.

Do not choose a common ancestor when it would load the rule for unrelated descendants.

## Multiple Placements

If one owner cannot represent the intended scope exactly, keep the smallest set of correct placements. Physical repetition is acceptable when it is required for scope correctness.

Do not introduce a new owner file when an existing editable owner already represents the same exact scope.

## Derived Runtime Files

Choose placement only in the authoritative editable layer. Do not relocate or hand-edit generated or derived runtime copies merely to make their physical layout DRY.

If changing the authoritative source would require derived copies to be regenerated and that regeneration is outside the current task, preserve the current state and report the synchronization boundary instead of leaving required copies stale.
