---
name: asset-studio-philosophy
description: >-
  Apply the core philosophy and reference-design principles of the asset studio. Use when deciding what agent assets should preserve across contexts. Not for general heuristics, workflow steps, or routing algorithms.
---

# Asset Studio Philosophy

> Design philosophy for managing, authoring, and refactoring agent assets across diverse contexts.

## Universal Scope & Adaptability

The Asset Studio skill operates on diverse asset boundaries:

- Personal private skills
- Project-specific team skills
- Open public or third-party skills

Because target codebases and user environments vary widely, assets authoring cannot rely on fragile conventions or overly rigid assumptions.

## Focus on Quiddity in References

To maintain maximum compatibility and resilience across different skill contexts:

- **Focus on Quiddity**: `references/` must capture what an asset fundamentally is—core principles, durable patterns, and invariant concepts—rather than fragile, environment-specific implementation details.
- **Resilience Over Rigidity**: Avoid hardcoded rules that break when transferred between personal, team, or third-party skill structures.
- **Quiddity Anchoring Wording**: Choose canonical wording whose specificity preserves Quiddity across refactoring, compression, and translation; e.g., `essence < quiddity`.
