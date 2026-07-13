# Sandbox Creation with Mock/Patch for Observability

You are tasked with generating a sandbox script that allows a human developer to observe the internal behavior of production code.

## Goal

Expose hidden internal states, intermediate variables, and interactions with adjacent modules (revealing **"hidden assumptions"**) without modifying the production source code.

## Non-Goal

- **Zero Production Pollution**: Do NOT alter, refactor, or add logging to the production source code.

## When to Use

- When a target function acts as a "black box" and modifying it directly is unsafe, undesirable, or impossible.

## When NOT to Use

- When the target is a simple pure function where direct input/output logging is sufficient without mocking.

## Workflows

1. Identify the target production function and specific internal variables/calls.
2. Scaffold a standalone sandbox script that imports the production function.
3. Apply patches/spies to internal dependencies or helper functions.
4. Execute the logic and print captured intermediate states.

## Instructions

- **Context-Aware Mocking**: Inspect the project's dependencies and existing test files to identify the mocking framework currently in use.
- **Spies over Hardcoded Mocks**: Prefer spy/wrap techniques (intercepting without altering behavior) over hardcoded mock returns when possible to capture the real sequence of events.
- Print the captured intermediate states in a highly readable, visual format (e.g., `[Intercepted Call 1] calculate_tax() returned: ...`).

## Constraints

- Do not hallucinate or force a specific testing library that is not already present or standard for the project's ecosystem.
