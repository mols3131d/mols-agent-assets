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

- Target file path (Required): The path of the source Markdown asset.
- Backup strategy (Optional): Choose ONE of the following methods:
  - `extension` (Default): Inject an extension name. You can specify a custom name (default is `backup`, added at the leftmost extension position).
  - `directory`: Save to a specific folder. You can specify a custom path (default is `.tmp/`).

### Procedure

1. Read the requested backup strategy.
2. If the strategy is `extension` or omitted:
   - Inject the extension (default `backup`) into the original filename at the leftmost extension position (e.g., `file.spec.md` becomes `file.backup.spec.md`).
   - Copy the source file to the computed filename in the same directory.
3. If the strategy is `directory`:
   - Resolve the destination directory (default `.tmp/`). Create the directory if it does not exist.
   - Copy the source file into the destination directory, preserving its original filename.

### Validation

- The backup file is successfully created in the correct location.
- The contents of the backup exactly match the original file before any edits.
