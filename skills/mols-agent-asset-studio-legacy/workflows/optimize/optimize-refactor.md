---
name: optimize-refactor
description: >-
  Refactor an agent package's folder and file structure without changing asset
  behavior. Use for moving, adding, removing, splitting, merging, or flattening
  asset resources. Not for one-file prose structure, Markdown formatting, or
  token compression.
---

# Refactor Asset Workflow

Refactor the asset package layout without mutating behavior.

## Execution

1. **Backup**: Execute [backup.md](../backup.md) before structural edits.
1. **Package Realignment**:
   - Add, remove, move, merge, or split asset folders and files.
   - Extract passive knowledge into `references/` and scripts into `scripts/`.
   - Flatten unnecessary directory depth.
1. **Verify Integrity**: Perform diff-check to confirm zero behavior mutation.
