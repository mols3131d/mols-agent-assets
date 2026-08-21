---
name: mols-markdown-tooling
description: >-
  Run deterministic Markdown maintenance for formatting, frontmatter validation,
  heading or link checks, and frontmatter-driven index generation or regeneration.
  Use when correctness depends on repeatable Markdown tooling rather than prose judgment.
  Prefer an established repository-native command when it owns the target behavior;
  otherwise use the bundled utilities. Do not use for general writing, document semantics,
  dashboard design, Mermaid authoring, or manual text cleanup that does not need tooling.
agentsskills:
  compatibility: 'Bundled utilities require Python; some operations require pyyaml, pyromark, rumdl, or uv as declared by the package.'
  metadata:
    author: 'mols (github.com/mols3131d)'
    version: '0.1.0'
---

# Mols Markdown Tooling

Use deterministic tools for Markdown mechanics. Do not turn the Skill into a workflow framework.

## Contract

- Inspect the target repository's existing Markdown commands, config, generated-file conventions, and schemas before selecting a bundled utility.
- Repository-native tooling wins when it already owns equivalent behavior.
- Use the minimum operation that proves or produces the requested result.
- Tool failure or a missing required dependency remains an explicit failure; do not silently replace parser, formatter, or validator semantics with model judgment.
- Generated indexes are projections of source Markdown/frontmatter. Regenerate them instead of hand-patching generated rows.
- Report checks as run only when the corresponding command actually ran.

## Operations

| Need | Bundled utility |
| --- | --- |
| Check declared dependencies | `scripts/check_dependencies.py` |
| Format Markdown | `scripts/format_markdown.py` |
| Validate YAML frontmatter | `scripts/validate_frontmatter.py` |
| Validate heading hierarchy | `scripts/validate_headers.py` |
| Validate links and fragments | `scripts/validate_links.py` |
| Generate or regenerate a frontmatter index | `scripts/generate_index.py` |
| Apply an explicit Markdown size guard | `scripts/markdown_size_guard.py` |

Run the selected utility with `--help` when its arguments are not already established by the target repository or task. Do not load a second routing layer just to discover these operations.

## Index Discipline

When using `generate_index.py`:

- preserve an existing index path, format, field selection, grouping, and validation flags unless the request changes them;
- for a new index, choose `csv`, `table`, or `list` from the requested consumer and repository convention;
- use required/unique field checks when the target contract requires them;
- exclude generated index files from their own source set;
- review the generated result and format Markdown output when appropriate.

## Boundary

- Human-readable Markdown composition belongs to `mols-markdown-for-human`.
- Engineering dashboard semantics belong to `mols-markdown-dashboard`.
- Document-level semantics such as decision records belong to `mols-document`.
- Mermaid diagram/chart semantics belong to `mols-mermaid`.

This Skill owns deterministic Markdown mechanics only.
