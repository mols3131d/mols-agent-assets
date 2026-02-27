---
title: "ADR 002: ADR Management via Scalable Minimalism"
description: Adoption of a simplified ADR management structure prioritizing clarity over complexity.
author: mols--Antigravity
categories:
  - ADR
draft: false
id: adr-002
adr-status: accepted
adr-keyword: ADR-Management
date: 2026-02-28
lastmod: 2026-02-27T17:08:10.039Z
tags:
  - adr
  - management
  - minimalism
  - en
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: true
---

# ADR 002: ADR Management via Scalable Minimalism

## Status

**Accepted** (2026-02-28)

## Context

As the project grows, efficient management of Architecture Decision Records (ADRs) became necessary. While initial discussions proposed automated indexing and complex reference layers, concerns were raised about premature optimization and overhead for the current project scale.

## Decision

Based on the consensus in [`/docs/rfc/2026/002--ADR-Management`](/docs/rfc/2026/002--ADR-Management), we adopt the **"Scalable Minimalism"** approach.

1.  **Structural Simplicity**: ADRs are stored in yearly folders (`/docs/adr/YYYY/`) with filenames using the `[Number]--[Keyword].md` format, excluding dates.
2.  **Data Standardization**: We maintain standardized, prefixed frontmatter keys (`adr-id`, `adr-status`, `adr-keyword`) to ensure the data remains exportable (e.g., to CSV) if scaling is required later.
3.  **Manual Indexing**: The `README.md` serves as a simple index, updated manually by human users as needed.
4.  **No AOS Coupling**: We avoid complex hierarchical reasoning rules in the AOS to keep the agent's operating context clean.

## Consequences

- **Positives**: Minimal overhead, high discoverability through clean naming/folders, and future-proof data via standardized metadata.
- **Trade-offs**: Requires manual synchronization between the index and files; relies on the agent's ability to locate and parse latest decisions.

---

**Reference**: [ADR Repository Guide](/docs/adr/README.md)
