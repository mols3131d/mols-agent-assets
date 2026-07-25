---
name: modular
description: >
  Decompose a primary asset into independent, single-responsibility module assets to optimize context and maintainability.
  Use when decomposing complex domain procedures or multi-step workflows into functional building blocks.
  Does not apply to attaching simple auxiliary/optional sub-help or single-file assets.
---

# Modular Asset Pattern

Decompose complex domain procedures into independent, single-responsibility modules to reduce context bloat and simplify maintenance.

## Essence

- **Domain Decomposition**: Split large or multi-step workflows into focused, single-responsibility units.
- **Selective Assembly**: Root asset conditionally orchestrates or references modules as needed for execution.

## Structure

```mermaid
graph LR
    Root[Root Asset] --> ModA[Module Asset A]
    Root --> ModB[Module Asset B]
    ModA --> Shared[Shared Spec]
    ModB --> Shared
```

## Rules

- **Single Responsibility**: Each module handles exactly one step or focused sub-task.
- **Clean Interfaces**: Define explicit inputs, outputs, and execution boundaries for each module.
