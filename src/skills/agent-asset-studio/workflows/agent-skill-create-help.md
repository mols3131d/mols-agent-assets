---
name: agent-skill-create-help
description: Create progressive disclosure help guide for single or routing skills.
---

# Create Skill Help Guide

Scaffold progressive disclosure help guide for single or routing agent skills.

## Goal

Establish a structured help framework to guide users (Commanders) and agents (Executors).

## Instructions

- Define target skill directory and skill type (single or routing).
- **For Single Skills**:
  - Add `## Help` section in `SKILL.md` body.
  - Implement progressive disclosure: Overview (User commands) → Execution (Script runs) → Fallback (Resilience).
- **For Routing Skills**:
  - Create separate `workflows/help.md` and map it in `INDEX.csv`.
  - Structure: Overview (User-level) → Execution (Routing map) → Fallback (Dependency resilience/regex parsing).
