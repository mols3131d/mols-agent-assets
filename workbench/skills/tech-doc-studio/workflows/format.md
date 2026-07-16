---
name: format
description: Fix markdown syntax, lint errors, and visual formatting issues.
---

# Format Document

## Goal

Fix markdown syntax, lint errors, and visual formatting issues.

## When to Use

Use when fixing structural syntax, whitespaces, or markdown rendering issues.

## When NOT to Use

Do not use if the formatting drastically alters the layout meaning (verify with user first).

## Instructions

- Read `references/<doc_type>.md` if specific table structures are required.

## Workflows

### Arguments from Context

- Target file path

### Procedure

1. Read the document.
2. Fix broken markdown tables, bad links, trailing whitespace, or missing blank lines before lists.
3. Ensure consistent heading hierarchy.

### Validation

- Markdown linter would pass without errors.
