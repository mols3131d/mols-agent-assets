---
title: ADR Operational Guide
description: Management and naming conventions for Architecture Decision Records
categories:
  - ADR
  - guidance
draft: false
date: 2026-02-28
lastmod: 2026-02-27T17:01:39.368Z
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: true
---

# ADR Operational Guide

## 1. Structure

- **Yearly**: `docs/adr/[YYYY]/`

## 2. Naming Convention

Format: `[Number]--[Keyword].md`

- Example: `001--adopt-ace-workflow.md`
- Dates are omitted from the filename as they are recorded in the frontmatter (`date`). Sequential numbers ensure chronological sorting and easy identification.

## 3. Metadata Standard (Safety)

To avoid conflicts with SSGs (Hugo, Astro, etc.), use prefixed keys:

- **id**: Unique ADR identifier (e.g., `adr-001`)
- **adr-status**: Decision status (accepted, superseded, etc.)
- **adr-keyword**: Core keyword
- **date**: Decision date (YYYY-MM-DD)

## 4. Rules

- ADRs are immutable records of final decisions from RFC Index 9.
- If a decision changes, create a new ADR to supersede the old one.
