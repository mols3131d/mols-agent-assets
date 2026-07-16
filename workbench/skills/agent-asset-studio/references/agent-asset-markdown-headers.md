# Asset Markdown Headers Specification

Core body concepts, formatting rules for agent assets.

| Header | Required | Description |
| --- | --- | --- |
| **Overview** | ❌ | Brief context, background summary of asset. |
| **Goal** | ✅ | Core purpose, scope of responsibility of asset. |
| **Non-Goal** | ❌ | Areas excluded to prevent scope creep. |
| **When to Use** | ✅ | Specific scenarios, activation contexts, user trigger conditions. |
| **When NOT to Use** | ❌ | Excluded scenarios, conditions to delegate to other asset. |
| **Workflows** | ❌ | Sequential steps, task execution flows. Omit if asset only has rules. |
| **Instructions** | ✅ | Positive rules, guidelines agent must follow. |
| **Constraints** | ❌ | Strict negative constraints agent must never violate. |

## Workflows Structure

When `Workflows` is defined, structure it using the following sub-headers.

| Header | Required | Description |
| --- | --- | --- |
| **Parameters** | ❌ | External inputs, target paths, variables required from user. Can include required/default values. Dynamic parameter discovery by agent is permitted (explicit search steps preferred, implicit allowed). |
| **Procedure** | ✅ | Ordered sequential steps to accomplish goal. Can include conditional branching, termination steps. Explicit early termination on negative conditions is preferred to ensure safety. Can reference or delegate to other assets (rules, workflows) for efficient modular expansion. |
| **Validation** | ❌ | Specific checks to verify the outcome is correct. |
