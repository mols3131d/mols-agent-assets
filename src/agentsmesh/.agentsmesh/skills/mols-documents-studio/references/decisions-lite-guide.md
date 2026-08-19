# Decisions-Lite Guide

## Rules

- **Template Path**: Use `templates/decisions-lite.template.md`.
- **Compliance**: Follow all placeholders (`{{a-A0-9_}}`) and instruction comments.
- **BLUF**: Put key details first using `### **[{{category}}] {{title}}**`. Keep `{{title}}` as a simple, core summary (max 50 chars).

## Status

- `Proposed`: Under review or discussion.
- `Accepted`: Approved and active.
- `Superseded`: Replaced by a newer decision.
- `Deprecated`: Disowned or no longer recommended.

## Body

- DECISION | **Key Decision** - Detailed explanation of the decision.
- REASON | **Key Motivation** - Context and reason.
- IMPACT | **Key Consequence** - Consequences on the system and workflow.
- RELATED
  - {{related_decision}}
  - Optional. Highly relevant decisions only. Better omitted than complex.
