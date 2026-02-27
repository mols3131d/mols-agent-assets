---
title: "ADR Management Final: Scalable Minimalism"
description: Official adoption of a simplified management structure prioritizing clarity over complexity
author: User--Rin
categories:
  - RFC
draft: false
id: rfc-002
date: 2026-02-28
lastmod: 2026-02-27T17:07:19.335Z
tags:
  - ADR
  - management
  - minimalism
  - final
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: true
---

# Decision: ADR Management via Scalable Minimalism

## 1. Overview

Based on the TAS discussion and user feedback, we reject complex automation or mandatory indexing that doesn't fit the current project scale. Instead, we adopt **"Scalable Minimalism"**: keep it simple for now, making it flexible for later.

## 2. Final Operational Rules

### 2.1. Eliminating Artificial Complexity

- **No AOS Mirroring**: Decisions will not be duplicated in the AOS. No complex hierarchical reasoning rules are enforced.
- **Manual Indexing**: The `docs/adr/README.md` serves as a simple, manually updated list for human users.

### 2.2. Structural Order

- **Yearly Folders**: Use `docs/adr/2026/` to reduce visual clutter.
- **Standard Filenames**: Maintain `[Number]--[Keyword].md` format. (e.g., `001--...`)
- **Date Management**: Dates are removed from filenames to avoid redundancy. All temporal data is managed via the `date` field in the frontmatter, making the ADR number the primary sorting criterion.

### 2.3. Metadata Safety & Standard

- To avoid conflicts with SSGs (Hugo, Astro, etc.), essential metadata uses prefixes.
- **Required Fields**: `id` (e.g., `adr-001`), `adr-status`, `adr-keyword`.
- This ensures that if the scale increases, we can easily run a script to extract data into **CSV or automated lists**, as suggested.

## 3. Conclusion

Our ADR management focuses on making information discoverable through **clean filenames and folder structures**. We prioritize the preservation of "Why" over the maintenance of over-engineered processes.

---

_This concludes the discussion on ADR management efficiency. Implementation is effective immediately._
