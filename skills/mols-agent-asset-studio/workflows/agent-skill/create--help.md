---
name: agent-skill-create-help
description: Create progressive disclosure help guide for single or routing skills.
---

# Create Skill Help Guide

Scaffold progressive disclosure help guide for single or routing agent skills.

## Goal

Establish a structured help framework for Commanders (users) and Executors (agents).

## Instructions

- Determine target skill path and type (single vs. routing).
- **Single Skill**: Add `## Help` section in `SKILL.md` (Overview → Execution → Fallback).
- **Routing Skill**: Create `workflows/help.md` or `workflows/--help.md`, and register in `INDEX.csv`.

## Procedure

1. Inspect target skill structure.
2. If single skill, insert `## Help` section in `SKILL.md`.
3. If routing skill, create `workflows/--help.md` (or `workflows/help.md`) and add entry to `INDEX.csv`.
4. Validate help resolution.

## Validation

- Help content is accessible and properly mapped in `SKILL.md` or `INDEX.csv`.
