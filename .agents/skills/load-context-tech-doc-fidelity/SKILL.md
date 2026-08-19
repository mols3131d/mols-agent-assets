---
name: load-context-tech-doc-fidelity
description: Load technical-document fidelity constraints when rewriting, translating, reformatting, or improving an existing technical document while preserving its meaning, code, identifiers, URLs, and meaningful structure. Use when preservation is a primary requirement. Do not use for repository onboarding, architecture explanation, new-document authoring, or general writing without fidelity needs.
---

# Load Context: Technical Document Fidelity

This Skill contributes **preservation context** for transforming an existing technical document. The active writing or transformation capability owns execution and output.

## Protected Content

Unless the user explicitly requests a change, preserve:

- technical meaning, requirements, conditions, exceptions, scope, and certainty;
- facts, numbers, versions, identifiers, API names, commands, and URLs;
- code and code-adjacent literal content;
- headings, lists, tables, ordering, links, and reference relationships when they carry information;
- intended audience and technical register.

Do not resolve ambiguity by inventing technical claims or remove required detail merely to improve readability.

## Transformation Rules

- Prefer local edits when broad restructuring adds no material value.
- Restructure only when it clearly improves the requested result without changing protected content.
- Translate prose when requested; keep code and technical identifiers unchanged unless explicitly included in the transformation.
- Do not translate code comments automatically unless the user requests it.
- Preserve modality, uncertainty, conditions, exceptions, scope, and ordering when they affect meaning.

## Fidelity Check

Before finalizing, compare the result against the source for the protected content above. If a requested style improvement conflicts with fidelity, preserve the protected content and expose the limitation rather than guessing.

## Boundary

This Skill contributes fidelity constraints only. Use repository-understanding capability when the task is to understand a codebase rather than transform an existing document.
