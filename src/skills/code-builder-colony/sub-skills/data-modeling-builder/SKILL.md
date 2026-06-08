---
name: data-modeling-builder
description: >
  Read when designing database tables, SQLAlchemy ORM entities, or Pydantic validation schemas.
  Do not read for writing procedural business logic or ETL scheduling.
---

# Data Modeling Builder

Designs relational schemas and validation contracts.

## Goal
Generate clear schema models, indexes, and type validation checks.

## Code Generation Steps
1. **Relational Constraints**: Define keys, nullability, and appropriate indexes (e.g. index foreign keys).
2. **Layer Separation**: Separate database model models (SQLAlchemy) from validation models (Pydantic).
3. **Migration Safe**: Ensure Alembic auto-generation matches target database types exactly.

## References Loaded
- [design-principles.md](../../references/design-principles.md) (Encapsulation, OOP vs Data containers)
- [robustness-and-safety.md](../../references/robustness-and-safety.md) (Pydantic schema validations)
