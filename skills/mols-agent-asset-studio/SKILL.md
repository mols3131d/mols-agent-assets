---
name: mols-agent-asset-studio
description: >
  USE WHEN: managing, creating, improving, validating, naming, compressing, optimizing for agents, or routing agent assets (AGENTS.md, agent rules, workflows, skills, or bundled resources).
  EXCLUDES: general code changes, merely invoking an existing skill, or modifying human-facing documentation.
compatibility: "Requires Agent Skill `mols-markdown-scripts`, Python >=3.13, rumdl, pyromark, pyyaml"
---

## Goal

Manage agent assets.

## When to Use

- Creating, modifying, validating, or organizing agent configurations, rules, workflows, or skills.
- Optimizing existing agent assets to be more agent-friendly (e.g., reducing context cost).
- Structuring routing boundaries or standardizing agent asset formats.
- Naming, compressing, or consolidating assets.

## When NOT to Use

- Writing or refactoring general application code.
- Merely invoking an existing agent skill to perform its intended job.
- Creating or modifying human-facing documentation (e.g., `README.md`).

## How to Route

1. Confirm that the request belongs to this skill's domain.
2. If it does, load `command/--route.md`.
3. Follow the route selected by `command/--route.md`.
