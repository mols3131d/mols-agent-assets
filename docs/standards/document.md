---
title: Documentation Pairing Standard (DPS)
description: Mandatory dual-target pairing protocol for all project documentation
categories:
  - standards
draft: false
date: 2026-02-27
lastmod: 2026-02-27T11:49:32.787Z
tags:
  - standards
  - documentation
  - dual-target
  - agent-friendly
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: true
---

# OVERVIEW

DPS ::= {Primary_Agent_Specs (.md) | Secondary_Human_Manual (.ko.md)}

Pair ::= {Logic_Density | Linguistic_Clarity}

# PROTOCOL

## 1. Universal Pairing Rule

Every discrete knowledge or requirement document MUST exist as a synchronized pair.

- **Agent-Target (`{filename}.md`)**:
  - **Primary**: Reference for all Agent reasoning and execution.
  - **Language**: English (Global Portability).
  - **Format**: Logic-dense, symbolic headers, token-optimized.
- **Human-Target (`{filename}.ko.md`)**:
  - **Secondary**: Reference for human review, context, and intuition.
  - **Language**: Korean (High Fidelity for USER).
  - **Format**: Narrative, descriptive, user-friendly.

## 2. Naming & Location

- Pairs MUST reside in the same directory.
- Root filename MUST be identical (e.g., `rule.md` and `rule.ko.md`).

## 3. Content Separation

- **Logic for Agent**: Technical specs, schemas, and algorithmic steps stay in `.md`.
- **Context for Human**: Rationale, background stories, and detailed "Why" explanations stay in `.ko.md`.

# SYNCHRONIZATION OBLIGATION

- When the Agent updates the Logic (`.md`), it is MANDATORY to update the Corresponding Human Context (`.ko.md`) to prevent "Knowledge Drift".
- Failure to sync constitutes a violation of AOS (Agent Operational Standard).

# CONSTRAINT

- **Primary Source**: In case of logical conflict, the Agent-Target (`.md`) is the final authority.
- **Format Compliance**: All pairs must follow the layout defined in `/docs/standards/markdown.md`.
- **Blueprints**: Use the standardized templates in **[`/templates/`](/templates/README.md)** for initializing new pairs.
