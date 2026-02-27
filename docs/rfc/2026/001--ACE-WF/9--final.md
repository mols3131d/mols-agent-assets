---
title: "ACE-WF Decision: Integrated RFC-ADR Lifecycle"
description: Final decision on the Agent Context Engineering Workflow
author: mols--Rin
categories:
  - RFC
draft: false
id: rfc-001
date: 2026-02-28
lastmod: 2026-02-27T17:06:21.986Z
tags:
  - ACE
  - workflow
  - RFC
  - ADR
  - decision
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: true
---

# DECISION: The RFC-ADR Driven ACE Workflow

Following the TAS discussion between Leni (Thesis), Kana (Antithesis), and Rin (Synthesis), we officially adopt the **Integrated RFC-ADR Lifecycle** for all agentic asset engineering within `mols-agent`.

## 1. The Core Lifecycle

The workflow transitions from a linear waterfall to an iterative, experience-driven loop centered on architectural decisions and project reuse.

1.  **Alignment (Proposal & RFC)**:
    - Any new logic or change starts as a **Proposal** (Thesis).
    - It undergoes an **RFC (Request for Comments)** phase where personas (Leni, Kana, Rin) critique and refine the logic.
2.  **Crystallization (ADR & REQ)**:
    - The conclusion of the RFC is codified into an **ADR (Architecture Decision Record)**.
    - Based on the ADR, formal **Requirements** are drafted.
3.  **Forge (Studio & Insight)**:
    - Implementation occurs in the **Studio**.
    - Logic is discovered during the forge; requirements are updated if the implementation reveals a more optimal path.
4.  **Verification (Subjective Approval & Assetization)**:
    - The asset is moved to **Outputs/Assets** only after subjective approval.
    - **The Bench**: The ultimate test is whether the asset can be successfully reused or "brought back" for a different project without breaking intent.

## 2. Key Principles

- **Subjectivity over Automation**: We acknowledge that Context Engineering cannot be objectively tested like software. Final authority rests with the User's feel and successful application in-situ.
- **Traceability**: The ADR serves as the permanent record of _Why_ a logic exists, preventing knowledge drift.
- **Draft Efficiency**: Work can begin with **Draft Requirements** to ensure development velocity isn't stalled by formal bureaucracy.

## 3. Operational Map

- **Discussion**: `/discussion/` -> Where RFCs happen.
- **Records**: `/docs/methods/RFC-ADR.md` -> Guidelines.
- **Decisions**: Linked or stored near the relevant assets.

---

**ADOPTED**: 2026-02-28
**STAKEHOLDERS**: Leni (Thesis), Kana (Antithesis), Rin (Synthesis), User.
