---
name: generate-index
description: Generate an index from Markdown YAML frontmatter as CSV, a Markdown table, or a Markdown list.
---

# Generate Markdown Index

## Goal

Generate an INDEX document from the YAML frontmatter of Markdown files.

## Instructions

1. Run `scripts/generate_index.py` with the target directory.
2. Select one format:
   - `csv`: machine-readable CSV with all fields quoted.
   - `table`: compact Markdown table.
   - `list`: headings and bullet lists for extensible human-readable output.
3. Write the result to the requested output path with `--output`.
4. Review the generated file and run the Markdown formatter if needed.

For `list`, group files by one or more frontmatter fields with `--group-by`.
The first field becomes `##`, the second becomes `###`, and the file title is
rendered below the deepest group. Group labels include field names by default.

```sh
uv run python scripts/generate_index.py docs --format list \
   --group-by status importance \
   --output docs/INDEX.md
```

Grouping options:

- `--group-label` / `--no-group-label`: include or omit field names.
- `--group-missing VALUE`: label missing values; default is `[unset]`.
- `--group-sort alpha|input`: sort groups alphabetically or preserve input order.

Grouping is supported only for the `list` format. Scalar and list frontmatter
values are rendered as text; list values are joined with commas.

Examples:

```sh
uv run python scripts/generate_index.py docs --format csv --output docs/INDEX.csv
uv run python scripts/generate_index.py docs --format table --output docs/INDEX.md
uv run python scripts/generate_index.py docs --format list --output docs/INDEX_LIST.md
```

Only Markdown files with YAML frontmatter are indexed. Existing files whose names
start with `INDEX` are excluded from input discovery.
