---
name: create-index-csv
description: >
  USE WHEN: creating or updating routing INDEX.csv via scripts. EXCLUDES: manual frontmatter parsing or markdown table edits.
---

# Create or Update INDEX.csv

## Goal

Create/update routing `INDEX.csv` via deterministic scripts to prevent token waste.

## Instructions

- Run script adhering to CLI Synopsis.
- Never parse frontmatter manually or construct CSV rows line-by-line using LLM tokens.
- If frontmatter missing, validate and fix target `.md` frontmatter first.
- Schema: `name,description` (standard) or `id,use_when,excludes` (router).

## Workflow: Create INDEX.csv

### Context

- `target_dir`: Path to target markdown directory.
- `output_path`: Target CSV output path (default: `<dir>/INDEX.csv`).

### Procedure

1. Verify target directory contains `.md` files.
2. Run index generation script:

   ```sh
   <python_runner> scripts/generate_index.py <target_dir> --format csv --output <output_path>
   ```

3. If validation fails due to missing frontmatter:
   - Identify missing fields: `<python_runner> scripts/validate_frontmatter.py <target_dir>`
   - Fix `name` & `description` frontmatter in `.md` files.
   - Re-run generation script.

### Validation

- Generated deterministically via script without manual LLM token construction.
- Schema matches `name,description` or `id,use_when,excludes`.
