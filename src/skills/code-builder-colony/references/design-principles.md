---
name: design-principles
description: >
  Read when creating new components/classes, refactoring complex code, or deciding on patterns/interfaces.
  Do not read for simple procedural scripts, static data lists, or declarative config files.
---

# Design & Programming Principles

Essential guidelines for writing simple, clean, and maintainable code.

## Applicability

- **Apply When**: Designing new systems, writing logic modules/classes, refactoring complex code blocks, or when deciding whether to introduce abstractions or patterns.
- **Do Not Apply To**: Declarative configuration formats, static data lists, simple sequential procedural scripts, or duplicate code blocks with fewer than three occurrences (Rule of Three).


## 1. Core Development Philosophies

| Philosophy | Rule & Action |
| --- | --- |
| **KISS** | Keep it simple. Avoid unnecessary abstraction or cleverness. |
| **YAGNI** | Do not implement features until they are actually needed. |
| **DRY** | Do not duplicate logic, knowledge, or business rules. |
| **SoC** | Separate concerns. Divide the application into distinct, focused modules. |
| **Readability** | Write code that is optimized for reading by humans. |
| **Minimal Diff** | Make the smallest focused change necessary to solve the problem. |
| **Existing Patterns** | Align with established project conventions and structures. |

## 2. Object-Oriented Programming (OOP) Concepts

| Concept | Description & Guidelines |
| --- | --- |
| **Encapsulation** | Hide internal state. Expose behavior via a public contract. Prevent direct field manipulation. |
| **Polymorphism** | Use interfaces or protocols to decouple callers from concrete implementations. |
| **Abstraction** | Hide complex execution details behind a simplified API. |
| **Composition** | *Prefer over Inheritance.* Class inheritance depth > 2 is an architectural bug. Use composition instead. |

## 3. SOLID Principles

- **S**RP (Single Responsibility): A class, function, or module should have exactly one reason to change.
- **O**CP (Open-Closed): Open for extension, closed for modification.
- **L**SP (Liskov Substitution): Subtypes must be completely substitutable for their base types.
- **I**SP (Interface Segregation): Clients should not be forced to depend on interface methods they do not use.
- **D**IP (Dependency Inversion): Depend on abstractions (interfaces), not concrete implementations.

## 4. Best Practices & Warnings

- **Tell, Don't Ask**: Encapsulate logic inside the object that holds the state.

  ```python
  # Bad: if account.get_balance() >= amount: account.set_balance(account.get_balance() - amount)
  # Good: account.withdraw(amount)
  ```

- **Avoid Premature Abstraction**: Start concrete. Extract interfaces/protocols only when you have duplication or need dynamic swapping.
- **Separate Data & Behavior**: Keep business logic in domain models, but keep data containers (DTOs, NamedTuples, Pydantic schemas) behavior-free.
- **Avoid Over-Engineering**:
  - Do not wrap stateless functions in utility classes (use top-level module functions instead of static helper classes).
  - Do not abuse design patterns (Factories, Strategies) when conditionals or maps suffice.
