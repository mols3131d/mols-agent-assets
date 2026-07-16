---
name: validate
description: Check an existing document against its guidelines and highlight missing or problematic sections.
---

# Validate Document

## Goal

Check an existing document against its guidelines and highlight missing or problematic sections.

## When to Use

Use when reviewing or auditing a document's compliance.

## When NOT to Use

Do not use if the user asked to fix the issues immediately (route to improve or update).

## Instructions

- Read `references/<doc_type>.md` for validation rules.
- Do not modify the document during validation unless explicitly asked.

## Workflows

### Arguments from Context

- Target file path

### Procedure

1. Read the document.
2. Check against the required structure and anti-patterns.
3. List any violations or missing information (e.g., missing Action Item owners).

### Validation

- A clear validation report is provided to the user.
