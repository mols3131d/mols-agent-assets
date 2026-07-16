# Asset Markdown Headers Specification

Core body concepts, formatting rules for agent assets.

| Header | Optional | Description |
| --- | --- | --- |
| **Overview** | ✅ | Brief context, background summary of asset. |
| **Goal** | ❌ | Core purpose, scope of responsibility of asset. |
| **Non-Goal** | ✅ | Areas excluded to prevent scope creep. |
| **When to Use** | ❌ | Specific scenarios, activation contexts, user trigger conditions. |
| **When NOT to Use** | ✅ | Excluded scenarios, conditions to delegate to other asset. |
| **Workflows** | ✅ | Sequential steps, task execution flows. Omit if asset only has rules. |
| **Instructions** | ❌ | Positive rules, guidelines agent must follow. |
| **Constraints** | ✅ | Strict negative constraints agent must never violate. |

## Workflows Structure

When defining workflows, use `## Workflows` for a single workflow, or `## Workflow: <Workflow Name>` to support multiple workflows in a single file. Structure each using the following sub-headers (Level 3).

| Header | Optional | Description |
| --- | --- | --- |
| **Arguments from Context** | ✅ | Inputs extracted from context (e.g., chat, active files, environment). Describe them as semantic concepts or intents, not strict schemas or CLI flags. This helps the LLM parse context fluidly without forcing rigid data structures. Can include defaults. |
| **Procedure** | ❌ | Ordered sequential steps to accomplish goal. Can include conditional branching, termination steps. Explicit early termination on negative conditions is preferred to ensure safety. Can reference or delegate to other assets (rules, workflows) for efficient modular expansion. |
| **Validation** | ✅ | Specific checks to verify the outcome is correct. |
