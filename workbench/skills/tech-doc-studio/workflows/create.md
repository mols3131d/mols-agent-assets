---
name: create
description: Scaffold and initialize a new technical document.
---

# Create Document

## Goal

Scaffold and initialize a new technical document.

## When to Use

Use when creating a brand new technical document.

## When NOT to Use

Do not use to modify an existing document (use update workflow).

## Instructions

- Read `references/<doc_type>.md` for type-specific sections and methodology.

## Workflows

### Arguments from Context

- Target directory
- Document title and type (e.g., adr, prd, spec, design, tasks, kanban)

### Procedure

1. Identify the requested document type.
2. If applicable, run the initialization script: `python3 scripts/init_document.py <name> --type <doc_type> --path <dir>` (or `kanban.py init` for kanban).
3. Populate the initial structure based on user requirements.

### Validation

- The document is successfully created in the target directory.
