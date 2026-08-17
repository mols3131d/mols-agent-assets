---
name: load-context-tech-doc-fidelity
description: >-
  Load technical-document fidelity constraints when rewriting, translating,
  reformatting, or improving an existing technical document while preserving its
  meaning, code, identifiers, URLs, and meaningful structure. Use when preservation
  is a primary requirement. Do not use for repository onboarding, architecture
  explanation, new-document authoring, or general writing without fidelity needs.
---

# Load Context: Technical Document Fidelity

Load this Skill as **preservation context**. It does not perform the writing workflow;
the active writing or transformation capability owns execution and output.

## Preserve

Unless the user explicitly asks to change them, treat these as protected:

- technical meaning, requirements, conditions, exceptions, and certainty;
- facts, numbers, versions, identifiers, API names, commands, and URLs;
- code and code-adjacent literal content;
- headings, lists, tables, ordering, and links when they carry information;
- reference relationships;
- intended audience and technical register.

Do not resolve ambiguity by inventing technical claims. Do not summarize away required
detail merely to improve readability.

## Allowed Change Boundary

The downstream transformation may restructure or reword content only as far as the
requested outcome allows without violating protected information.

- Prefer local edits when broad restructuring adds no value.
- Restructure when it clearly improves the requested result and preserves meaning.
- Translate prose when requested; keep code and technical identifiers unchanged unless
  the user explicitly requests otherwise.
- Do not translate code comments automatically unless they are part of the requested
  transformation.
- Preserve uncertainty, modality, conditions, exceptions, and scope.

## Composition

Combine this context with the relevant writing, translation, formatting, or document
capability. Use repository-understanding capability when the task is to understand a
codebase rather than transform an existing document.

## Boundary

This Skill contributes fidelity constraints only. It does not own drafting, rewriting,
translation, repository analysis, validation workflow, or final output structure.
