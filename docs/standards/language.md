---
title: Language Standards
description: Mandatory language policy for MOLS Agent workspace
categories:
  - standards
draft: false
date: 2026-02-27
lastmod: 2026-02-27
tags:
  - standards
  - language
agent-readable: true
agent-editable: false
agent-moveable: false
agent-deletable: false
agent-friendly: true
---

# SYNOPSIS

Language_Policy ::= {Primary_Hu (Korean) | Primary_Ag (English)}

# STANDARDS

## 1. Human Interface (Internal/Fidelity)
- **Primary**: Korean (KR).
- **Scope**: Interaction, reasoning explanations, human-friendly READMEs (`.ko.md`).
- **Goal**: Maximize communication fidelity with the USER.

## 2. Agent Interface (External/Portability)
- **Primary**: English (EN).
- **Scope**: Code, commits, technical assets, agent-friendly READMEs (`.md`), logs.
- **Goal**: Ensure logic portability and token efficiency across LLMs.

# CONSTRAINT

- **Sync Logic**: Cross-lingual token synchronization for continuity.
- **Strict Adherence**: Technical assets MUST remain in English regardless of interaction language.
