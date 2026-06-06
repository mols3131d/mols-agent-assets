---
name: agent-asset-studio
description: >
  Agent asset management studio. Use when user asks to create, edit, validate,
  route, compress, or improve agent skills, rules, agents, or related assets.
---

# Agent Asset Studio

## Overview

- Manage, create, evaluate, route, and compress agent assets (Skills, Rules, Agents).

## Triggers

- User asks to create, edit, validate, or improve agent skills, rules, or agents.
- Structural changes/management of `AGENTS.md` or `/.agents/` files.

## Exclusions

- General dev tasks (code, bug fix) not targeting asset files.
- Simply using a skill to solve a problem without editing it.

## Sub Skills

See `sub-skills/INDEX.csv`

## Rules

- Scope: agent assets only (`AGENTS.md`, `/.agents/**`, `src/skills/**`).
- Asset criteria:
  - **Agent**: Role/persona combining skills and rules.
  - **Skill**: Action-oriented procedural workflow (how-to).
  - **Rule**: Constraint-oriented cross-cutting protocol (what to enforce).

## Constraints

- Before edit, save original as `<filename>.original.md`.
- Route sub-skills by evaluating `keywords`, `trigger`, and `exclusion` in `sub-skills/INDEX.csv`.
