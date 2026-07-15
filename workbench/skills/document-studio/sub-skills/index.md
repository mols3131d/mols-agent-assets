---
name: index
description: >
  Create or update folder-local INDEX.csv files from markdown frontmatter. Use
  when user asks to index a document folder, refresh INDEX.csv, or organize docs
  by metadata.
---

# Document Index

## Overview

- **Goal**: Create and update folder-local `INDEX.csv` files from markdown frontmatter.

## Triggers

- User asks to create/update `INDEX.csv`.
- User names a folder to index.
- Folder docs need sortable/searchable metadata.

## Exclusions

- Do not index sibling/parent folders unless user asks.
- Do not use fixed fields when docs need different metadata.
- Do not manually summarize files if frontmatter has required data.

## Workflow

1. Confirm target folder.
2. Generate/update index:

   ```bash
   python3 scripts/update_index.py <folder> --fields file,id,title,status --sort status,id,file
   ```

3. Sort existing index when only order changes:

   ```bash
   python3 scripts/sort_index.py <folder>/INDEX.csv --fields status,id,file
   ```

4. Report missing frontmatter fields instead of inventing values.
5. Report the target folder, updated `INDEX.csv`, fields used, and missing fields or skipped files.

## Resources

- `scripts/update_index.py`: Script to generate/update the index.
- `scripts/sort_index.py`: Script to sort the index.

### Field Selection Examples

| Need | Field examples |
| --- | --- |
| identity | `id`, `title`, `name`, `file` |
| lifecycle | `status`, `created`, `updated`, `deprecated` |
| ownership | `owner`, `team`, `reviewer` |
| relation | `prd`, `adr`, `spec`, `supersedes`, `depends_on` |
| routing | `overview`, `trigger`, `exclusion` |

---

## Rules

- Target is a folder, not whole repo.
- `adr/INDEX.csv` indexes only `adr/*.md`, `prd/INDEX.csv` indexes only `prd/*.md`, etc.
- Ignore `INDEX.csv`, `README.md`, archive folders unless user includes them.
- Source of truth: markdown frontmatter.
- CSV format rules:
  - Header = chosen fields.
  - One row per indexed markdown doc.
  - Keep values short.
  - Preserve existing field order unless user asks to change.
  - Add new field only if needed.
- Always include a file/path field if frontmatter lacks stable ID.

## Constraints

- Use script generation/update. LLM should not hand-maintain rows.
- If required field missing:
  - Leave cell empty, or
  - Use filename for `file`/`id`, and
  - Report missing fields after update.
- Do not infer owner/status/date from prose unless user asks.
- Do not duplicate the same fact under multiple fields.
