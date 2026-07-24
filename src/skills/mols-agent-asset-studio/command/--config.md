---
name: config
description: View, locate, or edit skill configuration for mols-agent-asset-studio.
---

# Configure Skill

## Goal

Locate, view, or update the skill configuration file for `mols-agent-asset-studio`.

## Required Inputs

- Target key/value updates, or request to locate/view configuration

## Procedure

1. **Locate Configuration File**:
   - Primary path: `.configs/mols-agent-asset-studio.cfg.json`
   - Fallback path: `src/skills/mols-agent-asset-studio/assets/default/config.json`
2. **If File Missing**:
   - Copy default template from `src/skills/mols-agent-asset-studio/assets/default/config.json` to `.configs/mols-agent-asset-studio.cfg.json`.
3. **View or Edit**:
   - Display current settings if viewing.
   - Apply key/value changes to `.configs/mols-agent-asset-studio.cfg.json` if editing.
4. **Detailed Options**:
   - For complete configuration schemas and parameter descriptions, load [workflows/--config--help.md](--config--help.md).

## Validation

- Configuration file exists at `.configs/mols-agent-asset-studio.cfg.json` and contains valid JSON.
