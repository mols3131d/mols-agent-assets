---
name: optimize
description: >-
  Optimize agent assets for context cost, clarity, efficiency, and safety without
  behavior changes. Use for compression, refactoring, or formatting. Not for
  changing behavior, triggers, or safety bounds.
---

# Optimize Asset Package Orchestrator

Package entry point and orchestrator for agent asset optimization workflows.

## Execution

1. **Backup Target**: Execute [backup.md](backup.md) for target asset(s).
2. **Determine Strategy**:
   - **Size Compression**: Execute [optimize-compress.md](optimize/optimize-compress.md) to prune filler prose and redundancies.
   - **Asset Package Refactoring**: Execute [optimize-refactor.md](optimize/optimize-refactor.md) for folder and file structure changes.
   - **Asset Document Restructuring**: Execute [optimize-restructure.md](optimize/optimize-restructure.md) for one asset's headings, sections, prose layout, or Markdown format.
3. **Audit & Validate**: Compare diff against backup to verify zero unintended content or behavior loss.
