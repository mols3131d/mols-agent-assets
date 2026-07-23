---
name: scriptify-apply
description: USE WHEN: the user wants to execute an approved scriptification plan. EXCLUDES: planning, evaluation, or arbitrary script generation without a plan.
---

# Apply Agent Asset Scriptification

## Goal

Execute an approved scriptification plan by writing the script and updating the corresponding natural language workflow.

## Non-Goal

- Re-evaluating the feasibility of the scriptification.
- Altering the approved plan significantly without user consultation.

## When to Use

Use this workflow to write the actual code and modify the markdown file once an implementation plan has been established and approved.

## When NOT to Use

- When there is no clear plan detailing the target path, scripting language, and exact sections to replace.

## Instructions

- Write clean, deterministic, and self-contained scripts.
- Ensure the modified markdown workflow invokes the script using explicit syntax (e.g., `run_command`).
- Maintain the original intent and goal of the workflow.

## Workflow: Apply Agent Asset Scriptification

### Arguments from Context

- Approved implementation plan
- Target workflow or asset path
- Target script path and language

### Procedure

1. Write and test the script at the specified target path using the designated language.
2. Verify the script functions correctly and covers all intended mechanical steps.
3. Update the target markdown workflow:
   - Insert the explicit command invocation for the script.
   - Remove the obsolete natural language instructions.
4. Run standard validation (e.g., `validate_asset.py`) to ensure the updated markdown remains structurally sound.

### Validation

- The script exists at the target path and executes without errors.
- The workflow correctly references the script.
- No LLM reasoning logic is forced into the script.
