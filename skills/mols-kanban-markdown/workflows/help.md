---
name: help
description: Help guide and usage instructions for the mols-kanban-markdown skill.
---

# Mols Kanban Markdown Help Guide

Help instructions and reference guide for managing markdown-based Kanban boards.

## 1. Overview (For Commanders)

Use this skill to create, manage, validate, and organize markdown-based Kanban boards.

- **Initialize Kanban (`initialize`)**: Set up standard directory structure (`.configs/`, `backlog/`, `active/`, `archive/`) and default configuration files (`config.jsonc`, `template.md`, `AGENTS.md`).
- **Validate Directory (`validate-directory`)**: Check if all required directories and configuration files exist.
- **Validate Frontmatter (`validate`)**: Verify card frontmatter fields (id, title, status, priority, tags, etc.) against `.configs/config.jsonc` schema rules.
- **Move Cards (`move`)**: Move cards to appropriate subdirectories based on their `status` field (`backlog/`, `active/`, `archive/`) and automatically update internal/inbound relative links.

To start, ask the agent to perform actions: e.g., "Initialize kanban in ./my-kanban", "Validate kanban cards", or "Move cards based on status".

## 2. Key Assets & Reference Links

- **`AGENTS.md`** (`<kanban_path>/AGENTS.md`): Primary instruction guide for agents operating inside the Kanban workspace.
- **`config.jsonc`** (`<kanban_path>/.configs/config.jsonc`): Schema definition for card frontmatter validation and path configurations.
- **`template.md`** (`<kanban_path>/.configs/template.md`): Markdown card creation template.

## 3. Workflows & Execution Routes (For Executors)

Read `workflows/INDEX.csv` to select the right workflow route:

- `initialize`: Run `scripts/initialize.py` to bootstrap workspace.
- `validate-directory`: Run `scripts/validate_directory.py` to check folder/file integrity.
- `validate`: Run `scripts/validate_frontmatter.py` to validate card frontmatters.
- `move`: Run `scripts/move_cards.py` to organize cards by status and fix relative links.

## 4. Resilience Fallback (For Executors)

If python scripts or dependencies are missing or fail:

- **Directory Creation & Setup**: Manually create `.configs/`, `backlog/`, `active/`, `archive/` and copy reference files from `assets/default/`.
- **Card Moving**: Manually move `.md` card files matching `status` to `backlog/` (backlog), `active/` (todo, in_progress, review), `archive/` (done).
- **Link Updating**: Parse and update `[text](../path)` links to ensure relative path accuracy after file movements.
