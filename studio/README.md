---
title: "Studio Root"
type: "doc"
description: "Primary environment for agent-driven content generation"
created: 2026-02-27
updated: 2026-02-27
tags: ["studio", "workspace"]
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: true
---

# 🎨 Studio

> The Agent's Creative Workspace.

This directory is the primary environment for agent-driven content generation, refinement, and assessment. Unlike the `.agents` directory which contains the agent's "OS" (rules and protocols), the `studio` is where the actual "work" happens.

## 📂 Structure

- **`drafts/`**: The creative phase. New files are drafted and improved here through iterative cycles.
- **`evaluation/`**: The critique phase. Files are objectively assessed based on predefined metrics and agent rules.
- **`outputs/`**: The delivery phase. **Finalized assets are categorized here** (e.g., `rules`, `workflows`) once they pass evaluation.

## 🛠 Workflow

1.  **Drafting**: Create initial low-fidelity content in `drafts/`.
2.  **Iterating**: Refine content using `/test` or improvement protocols.
3.  **Evaluating**: Run evaluation scripts to ensure high-density logic and adherence to `rules`.
4.  **Exporting**: Move confirmed high-quality assets to the appropriate category in `outputs/` (e.g., `outputs/rules/`).
