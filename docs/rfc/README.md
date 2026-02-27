---
title: RFC Operational Guide
description: Guide for RFC directory structure and naming conventions
categories:
  - RFC
  - guidance
draft: false
date: 2026-02-28
lastmod: 2026-02-27T17:02:39.908Z
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: true
---

# RFC Operational Guide

This directory manages the lifecycle of proposals and discussions. All official proposals (Index 0) and final versions (Index 9) MUST include a unique `id` field.

## 1. Frontmatter Standard

For managed documents, use the following key:

- **id**: Unique RFC identifier (e.g., `rfc-001`)

## 2. Structure & Naming Convention

- **Yearly**: `docs/rfc/[YYYY]/`
- **Proposal Folder**: `[Num]--[Keyword]/` (e.g., `001--ACE-WF/`)
  - Use a sequential **3-digit number** instead of the `MM-DD` date format for better sorting and shorter references.
- **File Indexing**:
  - `0--proposal.md`: Initial proposal
  - `1-8--[Content].md`: Discussions/Critiques
  - `9--final.md`: Final conclusion

## 2. Rules

- No separate `discussion` folder. All context stays within the proposal folder.
- Once Index 9 is reached, the decision must be recorded in [`/docs/adr/`](/docs/adr/).
