# Agent Asset Backup Protocol

## Goal

Preserve Markdown asset state before edits for rollbacks and diffs.

## When to Use

When a workflow or rule modifies an existing Markdown asset.

## Instructions

- Save a source copy before making edits.
- Backup path follows arguments or defaults.

## Workflow: Agent Asset Backup Protocol

### Arguments

- Target file path (Required): Source Markdown asset path.
- `mode`: Backup method (`extension` | `tmp-dir`). Default: `extension`.
- `tmp-dir`: Directory path for `tmp-dir` mode. Default: `.tmp`.
- `extension`: Filename extension to inject at leftmost extension position for `extension` mode. Default: `backup`.

### Procedure

1. Determine backup mode.
2. If `mode` is `extension`:
   - Compute filename by injecting `extension` at leftmost extension position (e.g., `file.spec.md` -> `file.backup.spec.md`).
   - Copy source file to computed filename in same directory.
3. If `mode` is `tmp-dir`:
   - Resolve destination directory (`tmp-dir`), creating if needed.
   - Copy source file preserving original filename.

### Validation

- Backup file is created at correct path.
- Contents match original file before edits.
