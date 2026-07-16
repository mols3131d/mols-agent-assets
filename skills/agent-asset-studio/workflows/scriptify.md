---
name: scriptify
description: USE WHEN: the user wants to convert a deterministic natural language procedure into a script to reduce LLM tokens and uncertainty. EXCLUDES: tasks requiring LLM reasoning, context comprehension, or ambiguity resolution.
---

# Scriptify Agent Asset

## Goal

Convert fully or partially deterministic natural language workflows into scripts to minimize LLM dependency, token cost, and execution uncertainty.

## When to Use

Use this workflow to optimize a repetitive, deterministic, or purely mechanical procedure by replacing its natural language instructions with a script.

## When NOT to Use

- When the task intrinsically requires flexible text generation or LLM reasoning.
- When natural language is sufficient and significantly simpler to maintain than a custom script.

## Instructions

- Ensure all scriptification steps are fully evaluated, planned, and applied by referencing the sub-workflows in `references/`.
- Refer to `references/scriptify-evaluate.md` for evaluation criteria.
- Refer to `references/scriptify-plan.md` for planning requirements.
- Refer to `references/scriptify-apply.md` for execution steps.

## Workflows

### Arguments from Context

- Target workflow or asset path
- Specific steps or procedures to scriptify
- Target scripting languages (multiple allowed, default: Python)
- Target script path (agent infers appropriate location if not explicitly specified)

### Procedure

1. **Evaluate**: Refer to [references/scriptify-evaluate.md](../references/scriptify-evaluate.md). If the evaluation recommends against scriptification, exit.
2. **Plan**: Refer to [references/scriptify-plan.md](../references/scriptify-plan.md). Outline the language, path, and exact edits. Wait for user approval.
3. **Apply**: Refer to [references/scriptify-apply.md](../references/scriptify-apply.md). Write the script, update the markdown, and validate the changes.

### Validation

- The script exists at the target path and executes without errors.
- The workflow correctly references the script.
- No LLM reasoning logic is forced into the script.
