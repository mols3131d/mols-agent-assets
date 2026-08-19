# Rule Placement

Use this reference only when mapping an already resolved application and ownership status to editable rule containers and metadata.

## Established Source

When authority is bound to a specific source file or canonical input layer, preserve that source location unless project authority explicitly permits relocation. Remove redundant runtime copies only when they are not required projections or independent scoped rules.

Do not use DRY as a reason to migrate an established source of truth into a more convenient container.

## Peer Canonicalization

When ownership marks equivalent editable peer copies as eligible for canonicalization, discover the project's supported rule mechanisms and choose the smallest native representation that preserves the resolved application exactly. Do not assume `AGENTS.md`, a particular rule directory, or one selector schema is universal.

Examples include:

- a project-wide rule owner for always-applied project guidance;
- the highest directory-scoped owner whose inherited subtree remains exact;
- a path or glob rule whose selector matches the intended targets exactly;
- a relevance-selected or manually invoked rule with its attachment metadata preserved.

If the application decision requires multiple native segments or mechanisms, keep the smallest correct set. Do not recompute, broaden, or narrow intended application here.

Do not introduce a new owner file when an existing editable peer already represents the full resolved application exactly.

## Attachment Mode

Preserve the existing attachment mode. Do not convert always-applied, path-scoped, relevance-selected, agent-requested, or manual rules into another mode merely to reduce repeated text.

If consolidation would require an attachment-mode change, preserve the current modes and report that candidate as blocked by an application-migration boundary. This Skill does not perform that migration.

## Precedence

Treat runtime precedence, directory depth, selector specificity, file order, or source type as behavior when the runtime uses them.

Do not move or consolidate a rule across a precedence boundary unless the effective guidance remains unchanged for intended and nearby non-intended situations. If the relevant behavior cannot be determined, preserve the current placement and report the uncertainty.

## Generated Outputs

When the authoritative source is a generator input, canonical configuration, or another layer that produces runtime rule files, preserve that source model. Do not apply direct-runtime placement logic to generated outputs.

Do not relocate or hand-edit generated runtime copies merely to make their physical layout DRY.

If changing the authoritative source would require derived copies to be regenerated and that regeneration is outside the current task, preserve the current state and report the synchronization boundary instead of leaving required copies stale.
