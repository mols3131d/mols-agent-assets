---
name: reviewer-architecture
description: Audits code directory structure, screaming architecture, module/dependency rules, and naming conventions.
---

# Architecture Auditor Skill

Procedural guidelines for auditing code architecture, boundaries, and structure.

## Goal

Ensure the code layout makes the application's domain and design rules obvious and follows target architectural patterns.

## Review Steps

1. **Check Directory Layout**:
   - Verify if the layout is domain/feature-centric rather than tech-centric.
   - Look for deep nesting of directories (> 4 levels) and suggest flattening.
   - Refer to guidelines in [architectural-patterns.md](../../../code-builder-colony/references/architectural-patterns.md).

2. **Verify Naming Conventions**:
   - Check if class and file names use appropriate architectural suffixes:
     - `Handler` / `Controller` for entry points.
     - `Service` / `UseCase` for business logic.
     - `Repository` / `Dao` for data layers.
     - `Dto` / `Response` / `Request` for data transfer.
     - `Client` / `Gateway` for external integrations.

3. **Audit Dependency Flow**:
   - Inspect imports to check the dependency direction (Infrastructure -> Application -> Domain).
   - Ensure the `domain` (core business rules) contains no imports from outer layers (like database drivers, ORMs, Web/REST frameworks).
   - Check for circular dependencies between components and suggest extracting shared logic if necessary.

4. **Verify Entry Points**:
   - Ensure the entry points (`main.py`, `app.py`, `cli.py`, etc.) are in clear, predictable locations.
