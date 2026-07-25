---
name: extension-pattern
description: >-
  Attach optional help, edge cases, or advanced options to a complete primary asset through progressive disclosure. Use for secondary extensions. Not for domain decomposition or router indices.
---

# Extension Pattern

Attach auxiliary functionality (sub-help, edge cases, advanced options) to a standalone primary asset to protect initial context.

## Essence

- **Standalone Completeness**: Primary asset functions fully on its own.
- **Auxiliary Attachment**: Extension assets load only when rare, advanced, or optional scenarios are triggered.

## Structure

```mermaid
graph LR
    Primary[Primary Asset] -.->|On-demand Auxiliary| Ext[Extension Asset]
```

## Naming Convention

- **Extension Attachment**: `<asset>-<extension>.md` (e.g. `workflow-help.md`, `config-advanced.md`)
