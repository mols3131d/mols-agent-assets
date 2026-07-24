---
name: agent-asset-naming
description: >
    USE WHEN: suggesting, validating, or applying an agent asset name. EXCLUDES: renaming existing assets without explicit user request.
---

# Asset Naming

## Goal

Suggest, validate, or apply a clear agent asset name without implicit renaming.

## When to Use

Determining names for new agent assets or validating and applying names when explicitly requested.

## Instructions

- Follow [references/naming-convention.md](../../references/core/naming-convention.md) for domain-job naming patterns and `kebab-case` rules.
- Require explicit authorization before renaming any existing asset.

## Workflow: Asset Naming

### Arguments from Context

- Asset type and purpose
- Existing or new asset status
- Target path when applying a rename

### Procedure

1. Inspect asset status (new vs. existing).
2. If existing asset, verify explicit rename authorization.
3. Propose or validate the shortest domain-job name following naming conventions.
4. If renaming, execute [agent-asset-backup.md](agent-asset-backup.md), apply rename, update internal links, and diff-check.

### Validation

- Skill directory and frontmatter `name` match.
- Internal paths resolve after rename.
