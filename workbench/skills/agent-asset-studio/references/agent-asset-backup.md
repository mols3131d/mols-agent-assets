# Agent Asset Backup Protocol

## Goal

Preserve the original state of an existing Markdown asset before modification to allow for clean rollbacks and diff comparisons.

## When to Use

Use this protocol whenever a workflow or rule requires modifying an existing Markdown asset in the workspace.

## Instructions

- Always save a copy of the source before making any edits.
- The backup path is determined by the provided arguments or their defaults.

## Workflows

### Arguments

- Target file path (Required): The path of the source Markdown asset to be backed up.
- `mode`: Backup method to use (`extension` or `tmp-dir`). Default is `extension`.
- `tmp-dir`: Directory path to save the backup file (used if mode is `tmp-dir`). Default is `.tmp`.
- `extension`: Extension to inject into the filename (used if mode is `extension`). For files with multiple extensions, it is added at the leftmost extension position. Default is `backup`.

### Procedure

1. Determine the backup mode.
2. If `mode` is `extension`:
   - Compute the backup filename by injecting `extension` into the original filename at the leftmost extension position (e.g., `file.spec.md` becomes `file.backup.spec.md`).
   - Copy the source file to the computed filename in the same directory.
3. If `mode` is `tmp-dir`:
   - Resolve the destination directory using `tmp-dir`. Create the directory if it does not exist.
   - Copy the source file into the destination directory, preserving its original filename.

### Validation

- The backup file is successfully created in the correct location.
- The contents of the backup exactly match the original file before any edits.
