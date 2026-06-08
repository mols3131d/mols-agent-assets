---
name: review-principles
description: General code review guidelines and principles covering readability, maintainability, safety, and testability.
---

# Code Review Principles

Guidelines for reviewing code changes to ensure high maintainability, correctness, and safety.

---

## 1. Readability & Maintainability

- **Intent-Revealing Names**: Variables, functions, and classes must clearly describe their purpose. Avoid cryptic abbreviations.
- **Single Responsibility (SRP)**: Each function and class should do one thing. Keep functions short (prefer < 30 lines).
- **Control Flow**: Avoid deep nesting (prefer early returns). Minimize complex conditional logic.
- **Structure & Naming**: Refer to the architecture guidelines in [architectural-patterns.md](../../code-builder-colony/references/architectural-patterns.md).

## 2. Defensive Programming & Safety

- **Error Handling**: Never swallow exceptions silently. Use structured error boundaries and log relevant details safely (no secrets/PII).
- **Input Validation**: Validate all inputs at the boundary. Do not trust external data.
- **Null & Boundary Safety**: Guard against null pointer exceptions, index out-of-bounds, and undefined values.

## 3. Testability

- **Decoupling**: Keep business logic separated from external side-effects (DB, API) so it is easy to unit test.
- **Mocking**: Minimize complex mocking setups by keeping interfaces clean and simple.

## 4. Performance & Efficiency

- **Avoid Redundant Work**: Watch out for unnecessary DB queries (e.g., N+1), file I/O inside loops, or redundant API calls.
- **Resource Management**: Ensure files, database connections, and sockets are properly closed or disposed of.
