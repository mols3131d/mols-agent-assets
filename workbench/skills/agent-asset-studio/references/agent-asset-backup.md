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

- `tmp-dir`: Directory path to save the backup file. Default is `.tmp`.
- `extension`: Extension to inject into the filename. For files with multiple extensions, it is added at the leftmost extension position. Default is `backup`.

### Procedure

1. Resolve the destination directory using `tmp-dir`. Create the directory if it does not exist.
2. Compute the backup filename by injecting `extension` into the original filename at the leftmost extension position (e.g., `file.spec.md` becomes `file.backup.spec.md`).
3. Copy the source file to the computed destination path.

### Validation

- The backup file is successfully created in the correct location.
- The contents of the backup exactly match the original file before any edits.
