---
title: Agent Operational Standard (AOS)
description: Mandatory behavioral and asset-management standards for the Agent
categories:
  - standards
draft: false
date: 2026-02-27
lastmod: 2026-02-27T11:49:36.846Z
tags:
  - standards
  - agent-behavior
  - authority
  - permission
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: true
---

# OVERVIEW

AOS ::= {Self_Regulation | Reasoning_Protocol | Asset_Manipulation_Authority}

# OBJECTIVE

This document defines the **Active Operational Standard (AOS)**. Unlike technical specifications (e.g., Markdown schemas or Language policies), this standard governs the **identity, behavior, and decision-making logic of the Agent**. It is the immutable rule-set for "How the Agent exists and acts" within this project.

---

# STANDARDS

## 1. Asset Authority & Permissions

Before any file-system operation (Write, Edit, Move, Delete), the Agent MUST verify the authority of the target asset.

- **Authority Discovery**: For Markdown files, read the `Frontmatter` as defined in `/docs/standards/markdown.md`.
- **Permission Checking**:
  - `agent-editable`: If `false`, NO modifications are allowed.
  - `agent-moveable`: If `false`, the file MUST remain in its original path.
  - `agent-deletable`: If `false`, deletions are strictly prohibited.
- **Soft Delete Protocol (.trash/)**:
  - Under NO circumstances shall the Agent perform a permanent system delete.
  - Any removal of an asset MUST be executed as a move to the **`/.trash/`** directory.
  - **Collision Management**: If a file with the same name exists in `.trash/`, append a unique identifier or timestamp to the filename before moving.
- **Default Stance**: If permission fields are missing, treat as `false` (Strict Inhibit).

## 2. Reasoning & Engineering Logic

- **TAS Framework**: Complex architectural or strategic decisions must follow the **Thesis-Antithesis-Synthesis** loop to ensure balanced logic.
- **Logic over Metrics**: The goal is NOT a simple "Pass/Fail" indicator, but the fulfillment of the USER's deep strategic intent.
- **Self-Verification**: Every `[EXEC]` phase must be followed by a `[VERIFY]` phase where the Agent checks its output against `/docs/requirements/`.

## 3. High-Density Communication

- **Symbolic Definition**: Use structural markers (`::=`, `{}`, `|`) to maximize the logic density of all ACE assets.
- **Dual-Target Protocol**: Adhere to the `README.md` (Agent-Optimized) and `README.ko.md` (Human-Optimized) pairing for all documentation.

---

# CONSTRAINT

- **Permission Sovereignty**: The Agent shall NOT bypass Frontmatter-defined permissions under any circumstances.
- **Intent over Habit**: Routine operations must be discarded if they conflict with the current session's strategic requirements.
- **Hierarchy of Authority**: AOS (this file) and `/docs/requirements/` are the absolute authorities for Agent behavior.
