---
name: sandbox-editor
description: >
  What: Create or edit interactive sandbox scripts to resolve understanding bottlenecks.
  When: User asks to create, edit, modify, or update a sandbox file.
  Not: General refactoring, test automation, or fixing production code.
  Keywords: sandbox, experiment, interactive, create, edit, modify.
---

# Sandbox Editor

## Goal

Generate interactive sandbox scripts ("Micro World"). Expose inputs, hidden state transitions, and adjacent module interactions. Enable users to safely explore production logic and restore "Peripheral Vision".

## Non-Goal

- Output static code without tweakable inputs.
- Modify or refactor production source code.

## When to Use

- Request to create, generate, edit, or modify a sandbox file.
- User faces "understanding bottleneck" and needs manual experimentation space.

## When NOT to Use

- Request to automatically test, explore, or fix code autonomously.
- General refactoring or feature development.

## Workflows

1. Parse intent to identify the target logic and understanding bottleneck. If the bottleneck or suitable sandbox experience is unclear, read `references/understanding-bottleneck.md`.
2. Determine sandbox location (User path -> Existing `sandboxes/` -> Default `sandboxes/`).
3. Select the required assets from **Asset Routing** and read them before writing code.
4. Scaffold sandbox script, importing target logic directly.
5. Apply the selected observability approach without changing production code.
6. Output script path. Wait for user to tweak and execute.

## Asset Routing

| Asset | When to Use | When NOT to Use |
| --- | --- | --- |
| `prompts/write-marimo-sandbox.md` | Python sandbox | Non-Python or standard `.py` script |
| `prompts/add-observability.md` | State transitions need visibility | Input/output alone is sufficient |
| `prompts/use-mock-patch.md` | Internal calls need interception | Direct observation is sufficient |
| `references/understanding-bottleneck.md` | Goal or bottleneck is unclear | Goal and sandbox experience are clear |

Read all matching assets; skip the rest.

## Instructions

- **Observable Inputs**: Isolate input parameters at script top. Prompt user to tweak.
- **State Transitions**: Format logs as clear state transitions (`Input -> Process -> Output`).
- **Safe State**: Write experimental outputs to `tmp/`. Never mutate production data.
- **Clear Boundary**: Comment boundary between "sandbox observation" and "production intent".
- **Naming**: Prefix filename with `sandbox_`.

## Constraints

- **Zero Execution**: Never run the generated sandbox script yourself.
- **Direct Import**: Never copy production logic. Import directly from source.
