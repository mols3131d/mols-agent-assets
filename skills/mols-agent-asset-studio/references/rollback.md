# Rollback and Recovery

Establish recovery readiness before rename, replacement, consolidation, broad
refactor, deletion, or other destructive work.

## Git Workspace

1. Inspect current branch and working-tree changes.
1. Do not overwrite unrelated uncommitted work.
1. Use an existing commit, a dedicated branch, or an explicitly scoped stash as
   the rollback point.
1. Record the rollback command in `templates/rollback-plan.yaml`.

## Non-Git Workspace

Create a bounded snapshot only for the approved target set. Record source paths,
checksums, destination, creation time, and cleanup condition. Never create an
unbounded permanent `.tmp/` archive.

## Rules

- new assets normally need no backup
- backups and snapshots are not packaged with runtime assets
- secrets and credential files are excluded from snapshots unless the user
  explicitly owns and requests a secure backup mechanism
- verify recovery instructions before mutation; do not test destructive recovery
  on the only copy
