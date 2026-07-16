---
name: agent-asset-scriptify-plan
description: USE WHEN: the user wants to create an implementation plan for scriptifying a workflow. EXCLUDES: writing the actual code or evaluating feasibility from scratch.
---

# Plan Agent Asset Scriptification

## Goal

Create a detailed implementation plan outlining how a deterministic natural language procedure will be converted into a script, including language choices and deployment paths.

## Non-Goal

- Evaluating whether scriptification is appropriate (this should be done via `agent-asset-scriptify-evaluate.md` beforehand).
- Writing the actual script or executing the modifications.

## When to Use

Use this workflow after scriptification has been approved, to determine exactly what will be scripted, what language will be used, and where the script will be stored.

## When NOT to Use

- When the task has not yet been evaluated for LLM reasoning dependencies.

## Instructions

- Ensure the plan adheres to the `references/zen-of-agent-assets.md` principles.
- Maintain a clear separation of Reasoning and Execution in the proposed design.

## Workflows

### Arguments from Context

- Target workflow or asset path
- Specific steps or procedures to scriptify
- Target scripting languages (multiple allowed, default: Python)
- Target script path (agent infers appropriate location if not explicitly specified)

### Procedure

1. Review the steps to be scriptified.
2. Determine the optimal scripting language based on the context (default to Python unless another language is explicitly better suited).
3. Determine the storage path for the script (e.g., `scripts/` directory if modifying an agent skill).
4. Draft a plan outlining:
   - The exact natural language instructions to be removed.
   - The command invocation that will replace them.
   - The high-level logic the script will implement.
5. Present the plan to the user for approval.

### Validation

- The plan clearly specifies the scripting language, target path, and affected workflow sections.
- The proposed script logic contains no LLM reasoning tasks.
