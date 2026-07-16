# Asset Markdown Headers Specification

Core body concepts, formatting rules for agent assets. This specification defines the standard header structure. Each header can be flexibly added or omitted based on the nature and requirements of the asset.

| Header | Optional | Description |
| --- | --- | --- |
| **Overview** | ✅ | Brief context, background summary of asset. |
| **Goal** | ❌ | Core purpose, scope of responsibility of asset. |
| **Non-Goal** | ✅ | Areas excluded to prevent scope creep. |
| **When to Use** | ❌ | Specific scenarios, activation contexts, user trigger conditions. |
| **When NOT to Use** | ✅ | Excluded scenarios, conditions to delegate to other asset. |
| **Instructions** | ❌ | Positive rules, guidelines agent must follow. |
| **Constraints** | ✅ | Strict negative constraints agent must never violate. |
| **References** | ✅ | References to external information, tools, or related assets that the asset relies on or uses in conjunction. |
| **`Workflow: <Workflow Name>`** | ✅ | Sequential steps, task execution flows. Omit if asset only has rules. |

## Workflow Structure

When defining workflows, use the `## Workflow: <Workflow Name>` header to separate each workflow. Structure each using the following sub-headers.

| Header | Optional | Description |
| --- | --- | --- |
| **Arguments from Context** | ✅ | Inputs extracted from context (e.g., chat, active files, environment). Describe them as semantic concepts or intents, not strict schemas or CLI flags. This helps the LLM parse context fluidly without forcing rigid data structures. Can include defaults. |
| **Procedure** | ❌ | Ordered sequential steps to accomplish goal. Can include conditional branching, termination steps. Explicit early termination on negative conditions is preferred to ensure safety. Can reference or delegate to other assets (rules, workflows) for efficient modular expansion. |
| **Validation** | ✅ | Specific checks to verify the outcome is correct. |

## References

Define external documents or related assets within the `references/` directory used by this asset. Organize using bullet points (`-`) or tables. When using a table, it is recommended to specify columns like `id`, `use_when`, and `excludes` to clarify the purpose of each referenced resource. However, if references are already explicitly specified within the Instructions or Workflow sections, creating a separate `References` header is discouraged to avoid redundancy (DRY principle).
