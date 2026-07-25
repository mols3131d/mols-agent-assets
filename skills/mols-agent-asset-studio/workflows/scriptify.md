---
name: scriptify
description: >-
  Script deterministic agent-asset procedures to reduce token cost and execution
  uncertainty. Use for evaluating, planning, or applying repetitive mechanical
  steps. Not for LLM reasoning, ambiguity resolution, or flexible text generation.
---

# Scriptify Agent Asset

## Goal

Convert deterministic natural language workflows into scripts to minimize LLM token cost and execution uncertainty.

## When to Use

Use this workflow to optimize repetitive or mechanical procedures by replacing natural language instructions with executable scripts.

## When NOT to Use

- Tasks requiring flexible text generation or LLM reasoning.
- When natural language is simpler to maintain than a script.

## Instructions

- Evaluate, plan, and apply scriptification using the sibling workflow modules.

## Workflow: Scriptify Agent Asset

### Arguments from Context

- Target workflow path
- Steps to scriptify
- Target language (default: Python)
- Target script path

### Procedure

1. **Evaluate**: Check [scriptify-evaluate.md](scriptify/scriptify-evaluate.md). Exit if scriptification is not recommended.
2. **Plan**: Check [scriptify-plan.md](scriptify/scriptify-plan.md). Outline language, path, and edits. Obtain user approval.
3. **Apply**: Check [scriptify-apply.md](scriptify/scriptify-apply.md). Write script, update markdown, and validate execution.

### Validation

- Script exists at target path and executes cleanly.
- Workflow correctly references script without forcing LLM reasoning into code.
