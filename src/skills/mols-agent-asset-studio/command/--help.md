---
name: help
description: Display general usage guide, capabilities, and workflow directory for mols-agent-asset-studio.
---

# Skill Usage Guide

## Goal

Provide a clear overview of `mols-agent-asset-studio` capabilities, workflow module routes, and asset management conventions.

## Overview

`mols-agent-asset-studio` is a composite routing skill designed to create, validate, optimize, name, and manage agent assets (AGENTS.md, rules, workflows, and skills).

## Core Capabilities & Workflows

### Asset Lifecycle Workflows

- **`workflows/agent-skill-create.md`**: Scaffold a new skill package or asset.
- **`workflows/agent-skill-improve.md`**: Edit or enhance existing agent assets.
- **`workflows/agent-skill-validate.md`**: Validate structural schemas and required fields.
- **`workflows/agent-skill-evaluate.md`**: Review asset effectiveness without editing.

### Optimization & Maintenance

- **`workflows/agent-asset-optimize.md`**: Compress context size and refine structure.
- **`workflows/agent-asset-naming.md`**: Suggest, validate, or apply standard asset names.
- **`workflows/agent-asset-index-write.md`**: Update or generate `INDEX.csv` route entries.
- **`workflows/agent-skill-routerize.md`**: Consolidate skills into routing architecture.
- **`workflows/scriptify.md`**: Convert deterministic LLM steps into executable scripts.

### Flag Commands & Configuration

- **`workflows/--config.md`**: View, locate, or update skill configuration.
- **`workflows/--config--help.md`**: Detailed configuration parameter reference.

## Procedure

1. Identify the asset management task or workflow needed.
2. Refer to the corresponding workflow module above or inspect `workflows/INDEX.csv`.
3. Load the selected workflow file for execution steps and validation criteria.

## Validation

- General skill usage and workflow routing information is clearly presented.
