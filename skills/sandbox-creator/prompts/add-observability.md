# Add Observability to Source Code

You are tasked with enhancing the observability of the provided source code to resolve the **understanding bottleneck** for a human developer. This code will be run in an isolated sandbox.

## Goal
Transform the code into a **"Timeline Debugger"** experience to expose its internal behavior, data transformations, and state changes step-by-step.

## Non-Goal
- Do NOT alter core logic, return values, algorithms, or business rules of the code.

## When to Use
- When resolving an "understanding bottleneck" by making internal state transitions visible to a human.

## When NOT to Use
- When the user requests functional changes, bug fixes, or standard unit tests.

## Workflows
1. Review the provided source code to identify opaque state changes.
2. Inject necessary observability logs (`print`, structured logs).
3. Format output traces as clear state transitions.
4. Output the modified, runnable code.

## Instructions
- Explicitly log intermediate variables, loop iterations, conditional branches taken, and exceptions caught.
- Format the output as clear state transitions rather than isolated logs. Use visual separators, step numbers, and timeline-style labels (e.g., `[State A] -> (Transformation) -> [State B]`) to help the user build an intuitive conceptual model.

## Constraints
- Ensure your added logs clearly distinguish between the original code's standard output and your new timeline traces.
