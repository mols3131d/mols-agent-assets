---
name: asset-studio-philosophy
description: >
  USE WHEN: understanding the core philosophy and reference design approach of the asset studio skill.
  EXCLUDES: general agent asset heuristics, workflow steps, or specific file routing algorithms.
---

# Asset Studio Philosophy

> Design philosophy for managing, authoring, and refactoring agent assets across diverse contexts.

## Universal Scope & Adaptability

The Asset Studio skill operates on diverse asset boundaries:

- Personal private skills
- Project-specific team skills
- Open public or third-party skills

Because target codebases and user environments vary widely, assets authoring cannot rely on fragile conventions or overly rigid assumptions.

## Focus on Essence in References

To maintain maximum compatibility and resilience across different skill contexts:

- **Focus on Essence**: `references/` must capture core principles, essential patterns, and invariant concepts rather than fragile, environment-specific implementation details.
- **Resilience Over Rigidity**: Avoid hardcoded rules that break when transferred between personal, team, or third-party skill structures.
