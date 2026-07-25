---
name: naming
description: >-
  Name agent assets by project convention. Use for new assets or explicitly
  requested renames of skills, rules, agents, or workflows. Not for automatic
  renaming.
---

# Asset Naming

1. **Detect Convention**: Inspect active workspace naming rules (default: [naming-convention.md](../references/naming-convention.md)).
2. **Verify Intent**: Confirm explicit user request before renaming existing files.
3. **Backup & Rename**: Execute [backup.md](backup.md) before modifying existing asset names.
4. **Apply & Sync**: Rename file, align frontmatter `name`, and update internal references.

## Rules

- **Explicit Authorization**: Never rename an existing asset without explicit user request.
