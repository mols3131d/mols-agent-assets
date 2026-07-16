# Optimize Agent Asset

## Goal

Optimize one or more agent assets (skills, workflows, references) to maximize model efficiency and safety.

## Required Inputs

- Target asset path(s)
- Desired optimization outcome (compress size, refactor structure, format cleanup)

## Procedure

1. Read [references/zen-of-agent-assets.md](../references/zen-of-agent-assets.md) and [references/agent-asset-compress.md](../references/agent-asset-compress.md).
2. Choose optimization strategy:
   - **Size Reduction**: Apply rules in [references/agent-asset-compress.md](../references/agent-asset-compress.md) to prune filler words, hedging, and redundant prose.
   - **Structure Alignment**: Flatten deep directories, avoid empty scaffolds, and extract passive logic into shared references following `zen-of-agent-assets`.
   - **Formatting & Links**: Ensure all cross-references use explicit paths and links, and resolve any markdown lint warnings.
3. Save backup of modified files as `<filename>.original.md` before making edits.
4. Apply minimal behavior-preserving changes. Avoid massive rewrites.
5. Validate modified assets using `python3 scripts/validate_asset.py`.

## Validation

- The meaning, capabilities, triggers, and safety constraints are fully preserved.
- Code blocks, commands, and numeric configurations remain identical to original.
- The overall context size (lines, tokens) is reduced without losing precision.
- All internal and relative links resolve correctly.

## Resources

- Read [references/zen-of-agent-assets.md](../references/zen-of-agent-assets.md) for core optimization philosophies.
- Read [references/agent-asset-compress.md](../references/agent-asset-compress.md) for detailed prose compression rules.
- Use `scripts/validate_asset.py` for structural and validation checks.

## Stop Conditions

- Stop before executing optimizations that mutate behavior or violate safety bounds.
- Stop if the target asset is not a valid markdown or natural-language file.
- Do not compress or modify files that are not part of the active workspace without explicit authorization.
