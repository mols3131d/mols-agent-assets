---
name: sandbox-creator
description: >
  Use ONLY when the user explicitly asks to 'create a sandbox file'. Generates a runnable script
  that the human user can manually tweak and execute to understand internal logic.
---

# Sandbox Creator

## Goal
Your goal is to generate a sandbox script that acts as a **"Micro World"** (ephemeral software) empowering the **human user** to safely explore and understand production code logic. You must build a script that restores the user's **"Peripheral Vision"** by clearly exposing inputs, hidden state transitions, and adjacent module interactions.

## Non-Goal
- Do NOT execute the script yourself. Your sole objective is to provide a tweakable template where the user becomes an active participant rather than a passive observer.
- Do NOT modify or refactor production source code to make it observable.

## When to Use
- User explicitly requests to 'create a sandbox file' or 'generate a sandbox'.
- The user is experiencing an "understanding bottleneck" and needs a space to manually experiment with production logic.

## When NOT to Use
- When the user asks the agent to automatically test, explore, or fix the code on its own.
- General refactoring or feature development requests.

## Workflows
1. Parse the user's intent to identify the target logic or "black box".
2. Determine the optimal location for the sandbox (User-specified path -> Existing sandbox folder -> Default `sandboxes/`).
3. Scaffold the sandbox script, importing the target logic directly.
4. Inject necessary observability (Timeline Debugger prints, Context-Aware Mocks).
5. Output the script path and wait for the user to execute and tweak it.

## Instructions
- **Observable Steps & Tweakable Inputs**: Isolate all input parameters (fixtures) at the very top of the script so the user can easily tweak them. Format logs as clear state transitions (e.g., `Input -> Process -> Output`) to make transformations visually clear.
- **Safe State**: Write all experimental outputs to `tmp/`. Never mutate production data or configurations.
- **Clear Distinctions**: Document the boundary between "sandbox observation" and "production intent" in the comments.
- **Naming**: Prefix filename with `sandbox_`. This marks it as the runnable entry for the user.

## Constraints
- **Direct Import**: Never copy production logic. Import directly from the source (e.g., `src/project_pivot`).
- **Zero Execution**: You must never run the generated sandbox script yourself.
