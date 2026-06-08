---
name: python-builder
description: >
  Read when creating or modifying Python backend classes, endpoints, or scripts.
  Do not read for data analysis (Pandas/Polars) or distributed Spark pipelines.
---

# Python Code Builder

Generates clean, maintainable, and robust Python logic.

## Goal
Implement Python business logic following object-oriented clean code standards.

## Code Generation Steps
1. **Interface Contract**: Define explicit method contracts. Prefer composition over inheritance.
2. **Defensive Processing**: Guard inputs using Pydantic DTOs or explicit guard clauses.
3. **Safety Limits**: Catch specific exceptions and wrap them with context using `raise ... from`.
4. **Style Enforcement**: Follow PEP 8 rules. Run `python-run-linter` after writing code.

## References Loaded
- [design-principles.md](../../references/design-principles.md) (KISS, SOLID, composition)
- [python-style-guide.md](../../references/python-style-guide.md) (Idioms, EAFP, decorators)
- [robustness-and-safety.md](../../references/robustness-and-safety.md) (Error formats, validation)
