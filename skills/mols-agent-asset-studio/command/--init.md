---
name: init
description: Initialize workspace configuration and directories for mols-agent-asset-studio.
---

# Initialize Skill Workspace

## Goal

Initialize `.configs/mols-agent-asset-studio.cfg.json` and required workspace directory structures for `mols-agent-asset-studio`.

## Required Inputs

- Target workspace path (default: current workspace)

## Procedure

1. **Verify or Create Config**:
   - Check if `.configs/mols-agent-asset-studio.cfg.json` exists.
   - If missing, copy default template from `src/skills/mols-agent-asset-studio/assets/default/config.json` to `.configs/mols-agent-asset-studio.cfg.json`.
2. **Verify or Create Temporary Directory**:
   - Read `backup_dir` from config (default: `.tmp/`).
   - Ensure the temporary backup directory exists.
3. **Detailed Options**:
   - For detailed initialization options, load [workflows/--init--help.md](--init--help.md).

## Validation

- `.configs/mols-agent-asset-studio.cfg.json` exists and is valid JSON.
- Configured `backup_dir` exists.
