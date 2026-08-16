# Rule Placement

Use this reference only when mapping an already resolved scope and authoritative source to editable rule containers.

## Direct Runtime Rules

When the authoritative source is a directly loaded runtime rule, use the exact representation produced by the scope decision:

- Project-wide segment -> root `AGENTS.md`.
- Directory-subtree segment -> the highest `AGENTS.md` whose subtree still matches that segment exactly.
- Cross-cutting file, extension, path, or repeated-directory segment -> a matching pattern rule asset.

If the scope decision requires multiple exact segments, place each segment in the smallest suitable editable container. Do not recompute or broaden the intended scope here.

Do not introduce a new owner file when an existing editable owner already represents the same exact segment.

## Precedence

Treat runtime precedence as part of effective behavior. Directory depth, selector specificity, file order, or source type may change how rules combine.

Do not move a rule across a precedence boundary unless the effective rule set remains unchanged for both intended targets and nearby non-targets.

## Generated or Canonical Input Layers

If the authoritative source is a generator input, canonical configuration, or another layer that produces runtime rule files, preserve that layer's native structure. Do not apply the root/nested/pattern mapping to generated outputs.

Do not relocate or hand-edit generated runtime copies merely to make their physical layout DRY.

If changing the authoritative source would require derived copies to be regenerated and that regeneration is outside the current task, preserve the current state and report the synchronization boundary instead of leaving required copies stale.
