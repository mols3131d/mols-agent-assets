---
name: "rule-evolution"
description: "Protocol for recording and managing agent rule candidates to enable self-evolution."
---

# Rule Evolution

This skill manages the lifecycle of agent instructions. Instead of keeping every evolving thought in the main rules, use this skill to log candidates, evaluate them, and eventually promote them to formal rules or discard them.

## When to use this skill

- When you identify a recurring pattern or logic that should become a rule.
- When you want to propose a change to existing rules in `.agents/rules/`.
- When you need to record a 'lesson learned' during a session to inform future behavior.

## How to use it

### 1. Register a Candidate

Use the `suggest_evolution.py` script to add a new entry to the evolution log at `.agents/brain/evolution.md`.

### 2. Evaluation Levels

- **High (상)**: Core/Strongly recommended. Critical for system integrity.
- **Medium (중)**: Useful in specific contexts. Good to have.
- **Low (하)**: Experimental or personal preference.

### 3. Maintenance Protocols

- **Promotion**: When a candidate is integrated into `AGENTS.md` or other formal rules, remove it from the log.
- **Cleanup**: The log maintains a maximum of **10 items**. Older items are automatically removed (FIFO) to keep context lean.

## Tooling

- `python .agents/skills/rule-evolution/scripts/suggest_evolution.py --help`
