---
name: python-run-linter
description: >
  Read when formatting Python files, fixing PEP 8 syntax errors, or validating code styling rules.
  Do not read when styling checks are not required.
---

# Python Linter Runner

Enforces style checks and auto-formats codebase files.

## Steps

1. Run `ruff check . --fix` to clean unused imports and syntax errors.
2. Run `black .` to standardize spacing and line formatting.
