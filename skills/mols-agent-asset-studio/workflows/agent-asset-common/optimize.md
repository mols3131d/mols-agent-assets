---
name: agent-asset-optimize
description: >
   USE WHEN: the user wants to optimize one or more agent assets to maximize model efficiency and safety. EXCLUDES: modifying asset behavior, safety bounds, or non-workspace files.
---

# Optimize Agent Asset

## Goal

Optimize one or more agent assets (skills, workflows, references) to maximize model efficiency and safety.

## When to Use

Use this workflow to compress size, refactor structure, or clean up formatting of agent assets without altering their behavior.

## Instructions

- Read [references/zen-of-agent-assets.md](../../references/core/zen-of-agent-assets.md) for core optimization philosophies.
- Read [agent-asset-compress.md](agent-asset-compress.md) for detailed prose compression rules.
- Use `scripts/validate_asset.py` for structural and validation checks.
- Stop before executing optimizations that mutate behavior or violate safety bounds.
- Stop if the target asset is not a valid markdown or natural-language file.
- Do not compress or modify files that are not part of the active workspace without explicit authorization.

## Workflow: Optimize Agent Asset

### Arguments from Context

- Target asset path(s)
- Desired optimization outcome (compress size, refactor structure, format cleanup)

### Procedure

1. Read [references/zen-of-agent-assets.md](../../references/core/zen-of-agent-assets.md) and [agent-asset-compress.md](agent-asset-compress.md).
2. Choose optimization strategy:
   - **Size Reduction**: Apply rules in [agent-asset-compress.md](agent-asset-compress.md) to prune filler words, hedging, and redundant prose.
   - **Structure Alignment**: Flatten deep directories, avoid empty scaffolds, and extract passive logic into shared references following `zen-of-agent-assets`.
   - **Formatting & Links**: Ensure all cross-references use explicit paths and links, and resolve any markdown lint warnings.
3. Follow the backup protocol in [agent-asset-backup.md](agent-asset-backup.md) before making edits and verify backup file creation.
4. Apply minimal behavior-preserving changes. Avoid massive rewrites.
5. Compare optimized file against the backup file (diff inspection) to perform a content loss audit:
   - Verify frontmatter, triggers, exclusions, and safety constraints are fully preserved.
   - Confirm code blocks, commands, file paths, URLs, identifiers, and numbers match the original exactly.
   - If unintended content loss or behavior mutation is detected, revert using the backup and refine optimization.
6. Validate modified assets using `python3 scripts/validate_asset.py`.

### Validation

- The meaning, capabilities, triggers, and safety constraints are fully preserved.
- Code blocks, commands, and numeric configurations remain identical to original.
- Diff comparison against backup confirms zero unintended content loss.
- The overall context size (lines, tokens) is reduced without losing precision.
- All internal and relative links resolve correctly.
