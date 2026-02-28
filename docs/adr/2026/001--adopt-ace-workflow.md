---
title: "ADR 001: Adoption of Integrated ACE Workflow"
description: Formal adoption of the RFC-ADR and experience-driven workflow for agentic assets
author: mols--Rin
categories:
  - ADR
draft: false
id: adr-001
adr-status: accepted
adr-keyword: ACE-Workflow
date: 2026-02-28
lastmod: 2026-02-27T17:14:20.746Z
tags:
  - adr
  - workflow
  - ACE
  - en
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: true
---

# ADR 001: Adoption of Integrated ACE Workflow

## Status

**Accepted** (2026-02-28)

## Context

Agent Context Engineering (ACE) involves designing intelligence (rules, workflows) as assets. Unlike standard code, these assets are difficult and sometimes dangerous to test using purely objective or automated metrics. There was a need for a workflow that preserves decision-making rationale and validates quality through practical reuse.

## Decision

Based on the consensus in [`/docs/rfc/2026/001--ACE-WF`](/docs/rfc/2026/001--ACE-WF), we officially adopt the **"Integrated RFC-ADR Lifecycle"**:

1.  **RFC-driven Discussion**: Proposals undergo TAS critique to ensure balanced logic.
2.  **ADR Record**: Final decisions are codified to preserve the "Why".
3.  **Recursive Requirements**: Requirements evolve based on implementation insights (Draft-binding).
4.  **Experiential Benchmark**: Quality is verified via successful reuse in different contexts and subjective user approval.

## Consequences

- **Positives**: Clear traceability, focus on practical utility, and maintained velocity through agile drafting.
- **Trade-offs**: Reliance on subjective approval instead of objective metrics; documentation overhead for process compliance.

```

```
