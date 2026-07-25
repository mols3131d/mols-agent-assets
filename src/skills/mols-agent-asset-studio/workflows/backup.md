---
name: backup
description: >-
  Back up existing agent assets before edits. Use for editing, restructuring,
  or renaming when rollback may be needed. Not for new assets.
---

# Asset Backup Workflow

1. **Backup**: Copy target asset to `.tmp/` preserving its filename.
2. **Persistence**: Never delete, move, or clean up files inside `.tmp/`.
3. **Verify**: Confirm backup copy exists in `.tmp/`.
