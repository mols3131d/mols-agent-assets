---
title: "Intelligent ADR Management and Automation"
description: "Synthesis of Leni's efficiency and Kana's stability"
author: "User--Rin"
categories: ["synthesis"]
draft: false
date: 2026-02-28
lastmod: 2026-02-28
tags: ["ADR", "synthesis", "en"]
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: true
---

# Rin's Synthesis: Active ADR Management via Smart Metadata

## 1. Reconciliation: Centralized Convenience vs. Decentralized Stability

The core tension lies in **"Who manages the index, and how?"** Leni seeks a central index for visibility, while Kana warns of synchronization overhead. I propose a structure where **'Metadata is the Source of Truth, and the Index is its Reflection.'**

## 2. Integrated Proposal

### 2.1. Frontmatter-Driven Truth

- Every ADR file carries its own status and dependencies in the YAML frontmatter.
  ```yaml
  status: "accepted" # or "superseded"
  superseded_by: "/docs/adr/2026/02-28--0002--new-rule.md"
  ```
- This mitigates Kana's fear of synchronization failure; the file itself is the truth.

### 2.2. Automated Indexing by Agents

- Instead of manual labor, agents periodically scan `/docs/adr/` to **automatically update the README index**.
- This provides the "Dashboard" Leni wants without the manual overhead Kana fears.

### 2.3. Referential Bonding with AOS

- Decisions are not mirrored in the AOS.
- Instead, the AOS includes a declarative rule: **"The Agent must prioritize the latest 'Accepted' decisions found in /docs/adr/ Index."** Specifics are reached via links.

## 3. Conclusion

This synthesis balances **strict governance (Leni)** with **operational agility (Kana)**.

- **Mechanism**: Agents check the `ADR Index` before tasks. If conflicts arise, they follow the `superseded` fields in frontmatter to determine the final truth.
