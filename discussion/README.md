---
title: Discussion Governance
description: Protocols for collaborative reasoning and synthesis
categories: ["governance", "discussion"]
draft: false
date: 2026-02-27
lastmod: 2026-02-27T11:53:00.000Z
tags: ["discussion", "PDD", "TAS", "WWH", "governance"]
author: "mols--Rin"
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: true
---

# OVERVIEW

discussion ::= {Proposal | Reasoning | Decision_Making} | Lifecycle_Management

# PROTOCOL

1. **PDD** ([/docs/methods/PDD.md](/docs/methods/PDD.md)): Macro-pipeline for decision flow.
2. **TAS** ([/docs/methods/TAS.md](/docs/methods/TAS.md)): Persona-driven dialectical reasoning.
3. **WWH** ([/docs/methods/WWH.md](/docs/methods/WWH.md)): Document-level information density control.

# SEQUENCE

Logic_Evolution ::= 0 -> [1..6] -> 7 -> 8 -> 9

- **0**: **Proposal** (Initial Thesis / Problem Definition)
- **1-6**: **Dialectics** (Iterative Reasoning)
  - 1-3: TAS Discussion (Idea expansion & mapping)
  - 4-6: TAS Debate (Stress testing & critique)
- **7**: **Thesis_Final** (Proposer's consolidated stance)
- **8**: **Antithesis_Final** (Critic's unresolved risks)
- **9**: **Decision** (Synthesized outcome & action lock)

# DIRECTORY STRUCTURE

- `<Discussion-ID>/` :: Project-specific reasoning space.
- `<Discussion-ID>/<0-9>--<TITLE>.md` :: Atomic steps of logic progression.

---

_EOF: Discussion Governance_
