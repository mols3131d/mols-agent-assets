---
name: index
description: >
  Create or update folder-local INDEX.csv files from markdown frontmatter. Use
  when user asks to index a document folder, refresh INDEX.csv, or organize docs
  by metadata.
---

# Document Index

Goal: one folder, one `INDEX.csv`. Index only markdown docs in that folder.

## Triggers

- User asks to create/update `INDEX.csv`.
- User names a folder to index.
- Folder docs need sortable/searchable metadata.

## Exclusions

- Do not index sibling/parent folders unless user asks.
- Do not use fixed fields when docs need different metadata.
- Do not manually summarize files if frontmatter has required data.

## Rules

- Target is a folder, not whole repo.
- `adr/INDEX.csv` indexes only `adr/*.md`.
- `prd/INDEX.csv` indexes only `prd/*.md`.
- Ignore `INDEX.csv`, `README.md`, archive folders unless user includes them.
- Source of truth: markdown frontmatter.
- Use script generation/update. LLM should not hand-maintain rows.
- Fields come from indexing need, not a fixed schema.

## Field Selection

Choose minimal fields needed for retrieval/sorting.

| Need | Field examples |
| --- | --- |
| identity | `id`, `title`, `name`, `file` |
| lifecycle | `status`, `created`, `updated`, `deprecated` |
| ownership | `owner`, `team`, `reviewer` |
| relation | `prd`, `adr`, `spec`, `supersedes`, `depends_on` |
| routing | `overview`, `trigger`, `exclusion` |

Always include a file/path field if frontmatter lacks stable ID.

## Script Workflow

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

## CSV Rules

- Header = chosen fields.
- One row per indexed markdown doc.
- Keep values short.
- Preserve existing field order unless user asks to change.
- Add new field only if needed.
- Do not duplicate same fact under multiple fields.

## Missing Data

If required field missing:

- leave cell empty, or
- use filename for `file`/`id`, and
- report missing fields after update.

Do not infer owner/status/date from prose unless user asks.

## Output

Report:

- target folder
- updated `INDEX.csv`
- fields used
- missing fields or skipped files
