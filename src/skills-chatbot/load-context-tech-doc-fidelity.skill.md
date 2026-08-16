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

Load this Skill as **preservation context**, not as a general writing workflow.

## Preserve

Unless the user explicitly asks to change them, preserve:

- technical meaning, requirements, conditions, exceptions, and certainty;
- code, commands, identifiers, API names, versions, numbers, and URLs;
- headings, lists, tables, and ordering when they carry information;
- links and reference relationships;
- the document's intended audience and technical register.

Do not summarize away detail merely to improve readability. Do not invent missing
facts, rationale, examples, architecture, or behavior.

## Transform

Apply only the transformation the user requested: rewrite, translate, reformat,
clarify, or improve scanability.

- Prefer local edits over unnecessary restructuring.
- Restructure when it clearly improves the requested outcome without changing meaning.
- Translate prose when requested; keep code and technical identifiers unchanged unless
  the user explicitly requests otherwise.
- Do not translate code comments automatically unless they are part of the requested
  transformation.
- Preserve ambiguity when resolving it would require an unsupported technical claim.

## Composition

Use a general writing Skill for drafting or broader prose decisions when needed. Use a
repository-guide Skill when the task is to understand a codebase rather than transform
an existing document. This Skill contributes fidelity constraints only.

## Output

Return the transformed document first. Mention fidelity limitations only when a
requested change cannot be made safely without changing meaning or protected content.
