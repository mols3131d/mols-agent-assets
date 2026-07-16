---
name: scriptify-evaluate
description: USE WHEN: the user wants to evaluate whether a workflow or asset can and should be scriptified. EXCLUDES: generating the script or modifying the original asset directly.
---

# Evaluate Agent Asset Scriptification

## Goal

Evaluate whether a target agent asset or workflow step can and should be converted into a deterministic script, analyzing tradeoffs, ROI, and feasibility.

## Non-Goal

- Generating the actual script or implementation plan.
- Forcing tasks requiring LLM reasoning (context comprehension, intent interpretation, ambiguity resolution) into hardcoded scripts.

## When to Use

Use this workflow to assess scriptification suitability when the user proposes converting natural language instructions into scripts, before any planning or coding begins.

## When NOT to Use

- When the user explicitly requests to skip evaluation and proceed directly to planning or application (though a quick mental check is still required).
- When the task intrinsically requires flexible text generation or LLM reasoning.

## Instructions

- Stop and reject scriptification if the task requires LLM reasoning, context comprehension, intent interpretation, or flexible text generation.
- Stop if scripting introduces unnecessary engineering complexity without a clear return on investment (ROI).
- Read `references/zen-of-agent-assets.md` to cleanly separate Reasoning from Execution.
- Never force a script conversion if natural language is sufficient and efficient.

## Workflow: Evaluate Agent Asset Scriptification

### Arguments from Context

- Target workflow or asset path
- Specific steps or procedures to evaluate

### Procedure

1. Read and analyze the target steps for script suitability.
2. Check for reasoning dependencies: Do these steps require reading implicit context, extracting semantic meaning, or generating non-deterministic text?
3. If reasoning is required, recommend against scriptification and provide specific reasons. Exit the workflow.
4. If reasoning is not required, evaluate the ROI: Will a script be significantly faster, cheaper, or more reliable than natural language? If no, recommend against it.
5. If scriptification is suitable and beneficial, output an affirmative evaluation and recommend moving to the `scriptify-plan` workflow.

### Validation

- The evaluation clearly identifies reasoning boundaries.
- The output explicitly states whether scriptification is recommended or not, with supporting reasons.
