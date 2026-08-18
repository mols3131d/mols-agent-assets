# Refactor

Use this workflow when restructuring an existing agent asset is itself the primary
objective. Small structural edits that merely support another improvement stay in
[improve.md](improve.md).

## Orient

- Read the target, applicable project authority, nearby owners, and relevant
  checks.
- State the structural problem and the write boundary.
- Capture behavior, authority, ordering, activation, and public-surface invariants
  that must survive unless the request explicitly changes them.

## Reshape

Choose the smallest structural move that resolves the problem. Typical moves
include splitting or merging files, moving supporting context between `SKILL.md`,
`workflows/`, and `references/`, reducing duplicated ownership, consolidating
overlap, and simplifying load paths.

For a Skill, use an applicable project-owned Skill authoring specification as the
preferred target shape. Do not create directories or files solely to satisfy a
preferred structure.

Read [../references/change-safety.md](../references/change-safety.md) for broad,
destructive, replacement, or consolidation work.

## Preserve

- Preserve declared invariants and project or host authority.
- Avoid accidental trigger, tool, permission, or behavioral changes.
- Remove obsolete structure after its responsibility has moved.
- Keep intentional behavior changes distinguishable from structural cleanup.

## Finish

Check for duplicated or orphaned responsibility, unnecessary indirection, stale
paths, hidden sibling dependencies, and taxonomy without a concrete loading or
ownership benefit.

Use [review.md](review.md) or [validate.md](validate.md) when required. Static
inspection and deterministic validation do not prove runtime behavioral parity.

Report the structural problem addressed, structure changed, invariants preserved
or intentionally changed, checks performed, and unresolved findings.
