---
name: update
description: Edit content, update status, or append information to an existing technical document.
---

# Update Document

## Goal

Edit content, update status, or append information to an existing technical document.

## When to Use

Use when modifying existing content or updating the lifecycle status of a document.

## When NOT to Use

Do not use for a complete structural rewrite (use improve workflow).

## Instructions

- Read `references/<doc_type>.md` to ensure edits comply with the document's specific structure.

## Workflows

### Arguments from Context

- Target file path
- Changes to apply

### Procedure

1. Read the existing document.
2. Apply the requested edits or status updates.
3. If the document lifecycle changes, update the index via `scripts/update_index.py` if needed.

### Validation

- The document meaning and context are preserved while incorporating the new changes.
