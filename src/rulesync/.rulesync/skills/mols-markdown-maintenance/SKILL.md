---
name: mols-markdown-maintenance
description: >-
  Run deterministic Markdown maintenance for formatting, frontmatter validation,
  heading or link checks, and frontmatter-driven index generation or regeneration.
  Use when correctness depends on repeatable Markdown mechanics rather than prose judgment.
  Prefer established repository-native Markdown tooling when it owns the target behavior;
  otherwise use rumdl for standard Markdown mechanics and bundled utilities only for local
  frontmatter/index behavior. Do not use for general writing, document semantics,
  dashboard design, Mermaid authoring, or manual text cleanup that does not need tooling.
agentsskills:
  compatibility: 'Standard formatting and Markdown lint checks require rumdl. Bundled frontmatter/index utilities require Python and PyYAML.'
  metadata:
    author: 'mols (github.com/mols3131d)'
    version: '0.1.0'
---

# Mols Markdown Maintenance

Use established Markdown tooling directly. Keep custom code only for behavior the backend does not already own.

## Contract

- Inspect the target repository's Markdown commands, config, generated-file conventions, and schemas before selecting an operation.
- Repository-native tooling and configuration win when they already own equivalent behavior.
- Use the minimum operation that proves or produces the requested result.
- Tool failure or a missing required dependency remains explicit; do not replace parser, formatter, or validator semantics with model judgment.
- Generated indexes are projections of source Markdown/frontmatter. Regenerate them instead of hand-patching generated rows.
- Report checks as run only when the corresponding command actually ran.

## Operations

| Need | Operation |
| --- | --- |
| Format Markdown | `rumdl fmt <paths...>` |
| Validate heading hierarchy and single title | `rumdl check --enable MD001,MD025 <paths...>` |
| Validate link fragments and references | `rumdl check --enable MD051,MD052 <paths...>` |
| Validate YAML frontmatter schema | `scripts/validate_frontmatter.py <files...>` |
| Generate or regenerate a frontmatter index | `scripts/generate_index.py <directory>` |

Use the target repository's rumdl configuration when it represents accepted project policy. Use CLI rule selection only when the requested check is intentionally narrower than that policy. Consult current rumdl authority rather than copying its broader rule or configuration reference into this Skill.

## Frontmatter and Index

- `validate_frontmatter.py --help` owns schema, required-field, and exact-value options.
- `generate_index.py --help` owns output format, field, glob, grouping, depth, required-field, unique-field, and output-path options.
- Preserve an existing index path, format, field selection, grouping, and validation flags unless the request changes them.
- Exclude generated index files from their own source set.
- Review generated output and format Markdown output when appropriate.

## Boundary

- Human-readable Markdown composition belongs to `mols-markdown-for-human`.
- Engineering dashboard semantics belong to `mols-markdown-dashboard`.
- Document-level semantics such as decision records belong to `mols-document`.
- Mermaid diagram/chart semantics belong to `mols-mermaid`.

This Skill owns deterministic Markdown maintenance selection and the small local delta not already owned by the Markdown backend.
