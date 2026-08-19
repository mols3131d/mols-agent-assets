---
name: update-index
description: Regenerate an existing index after Markdown files or frontmatter change, preserving the target project's output path, format, and field conventions.
---

# Update Markdown Index

## Goal

Update an existing index by regenerating it from the current Markdown source
files. Do not edit generated index rows manually.

## Instructions

1. Inspect the existing index and target project conventions first:
   output path, format, selected fields, grouping, depth, and validation flags.
1. Run the same `scripts/generate_index.py` command used to create the index.
   Change only the target directory or options required by the requested update.
1. If the original command is unavailable, infer options from the existing index
   and project convention. Prefer the existing output path and format.
1. Use `--output <existing-index-path>` to replace the generated index after
   checking the target path.
1. Use `--require-fields` and `--unique-fields` when the target convention
   requires complete and unique frontmatter values.
1. Review the diff and run the Markdown formatter only when the selected format
   is Markdown.

## Recommended command shape

```sh
uv run python scripts/generate_index.py <target-directory> \
  --format <existing-format> \
  --fields <existing-fields> \
  --output <existing-index-path>
```

`INDEX.csv` is only a fallback recommendation when the target project has no
existing filename convention. It is never a fixed requirement.

## Validation

- Existing index path and format are preserved unless explicitly requested.
- Index content reflects current Markdown frontmatter.
- No generated rows are manually patched.
