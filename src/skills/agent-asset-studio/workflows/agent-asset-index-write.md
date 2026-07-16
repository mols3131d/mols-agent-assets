---
name: agent-asset-index-write
description: USE WHEN: the user wants to create or update an asset index as CSV, Markdown file, or Markdown table. EXCLUDES: replacing unrelated content or making structural changes beyond the index.
---

# Write Asset Index

## Goal

Create or update one asset index as routing CSV, standalone Markdown, or an index table inside an existing Markdown file.

## When to Use

Use this workflow when you need to create or update an index of agent assets. The index can be a routing CSV, a standalone Markdown file, or a Markdown table inside an existing file.

## Instructions

- For `csv`, read `references/routing-skill-structure.md` before choosing location or route semantics.
- No reference is required for Markdown modes.
- Ask one targeted question when mode, target, or source scope is missing and cannot be inferred safely.
- Stop before replacing an existing hand-written table whose ownership or boundary is unclear.
- Do not invent route conditions or document descriptions when source content provides no evidence.

## Workflow: Write Asset Index

### Arguments from Context

- Mode: `csv`, `markdown-file`, or `markdown-table`
- Target index or host Markdown path
- Files or workflow modules to index

### Procedure

1. Confirm the mode, target, source scope, and ordering rule. Inspect existing content before writing.
2. Build entries from explicit sources. Use relative paths, deterministic path order, and concise descriptions derived from source headings or metadata.
3. Apply the selected mode:

   | Mode | Output | Rules |
   | --- | --- | --- |
   | `csv` | `INDEX.csv` | Use `id,use_when,excludes`; default to `workflows/INDEX.csv`; resolve each `id` from the index directory |
   | `markdown-file` | `INDEX.md` | Add a title and one link table; preserve useful introduction or manually maintained sections |
   | `markdown-table` | Existing `.md` file | Add or update one clearly titled link table without rewriting unrelated content |

4. For `csv`, keep one workflow per row. Put positive and implicit selection conditions in `use_when`; put near misses and out-of-scope requests in `excludes`.
5. For Markdown modes, use descriptive link labels and relative links. Exclude the index itself, hidden files, generated backups, and unrelated artifacts.
6. Update an existing entry in place instead of appending a duplicate. Do not synchronize CSV and Markdown indexes unless the user requests both.

### Validation

- `csv`: header is exact, IDs are unique safe relative paths, required fields are non-empty, and each ID resolves inside the skill.
- Markdown: every link resolves, entries are unique and deterministically ordered, and unrelated content is unchanged.
- The result contains only the requested index mode or explicitly requested combination.
