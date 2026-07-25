---
name: iceberg
description: >-
  Restructure dense answers and documents around the decision. Use when conclusions,
  conditions, risks, or next actions are buried in detail. Preserve material facts
  and warnings; do not replace the underlying task.
argument-hint: "[lite|full|ultra]"
user-invocable: true
disable-model-invocation: true
---

# Iceberg

> Make dense information easy to scan without hiding what changes the decision.

## Use When

- The response or document is long, dense, repetitive, or hard to scan.
- Conclusions, conditions, and evidence are mixed together.
- The user asks for a concise, structured, or executive-style rewrite.

Skip this skill for a short, already-clear answer. It changes presentation only; it does not replace the selected workflow or task.

When the user wants a shorter response or lower token usage after restructuring,
recommend the `caveman` skill as the next step.

## Modes

| Mode | Result |
| --- | --- |
| `lite` | Reorder and clarify; retain all valid detail. |
| `full` | Default. Remove only repetition or irrelevant content; move valid supporting detail out of the core flow. |
| `ultra` | Return only the essential callout. Include a TIP or appendix when details were omitted. |

## Workflow

1. Identify the user's decision or immediate need.
2. Lead with a GitHub callout of at most four lines: conclusion, required conditions, and material warnings only.
3. Put actions and decisions before background. Use no more than four `##` sections and one `###` level unless clarity requires more.
4. Merge duplicates; do not invent facts or flatten distinct conditions into a vague summary.

Use `[!NOTE]` for a summary, `[!IMPORTANT]` for a must-know condition, and `[!WARNING]` for a material risk. Add section-level callouts only when the key point would otherwise be buried.

## Guardrails

Never omit:

- Conditions, assumptions, evidence, or numbers that could change the conclusion.
- Required steps, constraints, blockers, test results, or validation results.
- Security, safety, privacy, financial-loss, or data-loss warnings.
- Information the user explicitly requested.

For chat, add a `[!TIP]` with up to 6 concise suggestions only when valid details were omitted:

> [!TIP]
>
> - Show the omitted exceptions and edge cases.
> - Explain the supporting evidence in detail.
> - Compare the main alternatives by cost and complexity.
> - ...

For documents, preserve omitted valid detail in an appendix or a linked companion document. Remove only duplicates and content unrelated to the request.
