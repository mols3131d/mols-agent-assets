# Rule Placement

Use this reference only when mapping an already resolved application and authoritative source to editable rule containers and metadata.

## Native Placement

Discover the project's supported rule mechanisms before moving anything. Preserve the accepted native format rather than assuming `AGENTS.md`, a particular rule directory, or one selector schema is universal.

When the authoritative source is a directly loaded runtime rule, map the resolved application to the smallest native representation that preserves it exactly. Examples include:

- a project-wide rule owner for always-applied project guidance;
- the highest directory-scoped owner whose inherited subtree remains exact;
- a path or glob rule whose selector matches the intended targets exactly;
- a relevance-selected or manually invoked rule with its attachment metadata preserved.

If the application decision requires multiple native segments or mechanisms, keep the smallest correct set. Do not recompute, broaden, or narrow intended application here.

Do not introduce a new owner file when an existing editable owner already represents the same application exactly.

## Attachment Mode

Preserve the existing attachment mode unless the resolved intended application itself requires a change. Do not convert always-applied, path-scoped, relevance-selected, agent-requested, or manual rules into another mode merely to reduce repeated text.

If consolidation requires changing attachment mode, treat that as a separate application migration. Apply it only when the request authorizes the migration and the resulting behavior can be supported by evidence; otherwise preserve the current modes and report the DRY limit.

## Precedence

Treat runtime precedence, directory depth, selector specificity, file order, or source type as behavior when the runtime uses them.

Do not move a rule across a precedence boundary unless the effective guidance remains unchanged for intended and nearby non-intended situations. If the relevant behavior cannot be determined, preserve the current placement and report the uncertainty.

## Generated or Canonical Input Layers

If the authoritative source is a generator input, canonical configuration, or another layer that produces runtime rule files, preserve that layer's native structure. Do not apply direct-runtime placement rules to generated outputs.

Do not relocate or hand-edit generated runtime copies merely to make their physical layout DRY.

If changing the authoritative source would require derived copies to be regenerated and that regeneration is outside the current task, preserve the current state and report the synchronization boundary instead of leaving required copies stale.
