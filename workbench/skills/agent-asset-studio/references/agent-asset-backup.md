# Agent Asset Backup Protocol

## Goal

Preserve the original state of an existing Markdown asset before modification to allow for clean rollbacks and diff comparisons.

## When to Use

Use this protocol whenever a workflow or rule requires modifying an existing Markdown asset in the workspace.

## Instructions

- Always save a copy of the source before making any edits.
- Use one of the two backup modes based on the requested arguments.

## Workflows

### Arguments

- Target file path
- Backup mode: `extension` (default) or `tmp-folder`

### Procedure

1. Determine the backup mode.
2. If `extension`:
   - Copy the target file to `<filename>.original.md` in the same directory.
3. If `tmp-folder`:
   - Copy the target file into a `.tmp/` directory, creating the directory if it does not exist.

### Validation

- The backup file is successfully created in the correct location.
- The contents of the backup exactly match the original file before any edits.
