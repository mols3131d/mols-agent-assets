# Template Instructions

## Purpose

Record lightweight technical decisions with the conclusion first, followed by its primary reason and consequence.

## Placement

Place each decision under exactly one status section:

* `Proposed`: Under review or discussion.
* `Accepted`: Approved and active.
* `Superseded`: Replaced by a newer decision.
* `Deprecated`: No longer recommended or supported.

When no status is provided, use `Proposed`.

Replace the corresponding status block with the completed decision. Remove unused status block placeholders.

## Decision format

Use this exact structure:

```markdown
### **[CATEGORY] TITLE**

- DECISION | **KEY DECISION** - DETAILED EXPLANATION
- REASON | **KEY MOTIVATION** - CONTEXT AND REASON
- IMPACT | **KEY CONSEQUENCE** - SYSTEM AND WORKFLOW IMPACT
- RELATED
  - RELATED DECISION
```

## Writing rules

* `category`: Use a short, stable category such as `Architecture`, `Data`, `Tooling`, or `Workflow`.
* `title`: State the core decision in 50 characters or fewer.
* `key decision`: Summarize what was chosen.
* `detailed explanation`: Clarify the scope, boundary, or implementation direction.
* `key motivation`: State the primary reason for the decision.
* `context and reason`: Explain the relevant problem, constraint, or trade-off.
* `key consequence`: Summarize the most important consequence.
* `system and workflow impact`: Explain what changes in the system or working process.
* Avoid repeating the same information across `DECISION`, `REASON`, and `IMPACT`.

## Related decisions

`RELATED` is optional.

Include it only when an existing decision is directly required to understand, constrain, extend, or supersede this decision.

* Use the exact decision title or repository-relative link.
* Include only highly relevant decisions.
* Remove the entire `RELATED` block when no relevant decision exists.
* Never invent a related decision.

## Preservation

When updating an existing decisions document:

* Preserve all existing decisions.
* Preserve status headings and their order.
* Append new decisions after existing entries in the selected section.
* Do not move or rewrite existing decisions unless explicitly requested.
* Do not create a duplicate decision with the same meaning.

## Completion

Before finishing:

* Exclude this `Template Instructions` section.
* Exclude the `TEMPLATE CONTENT` boundary.
* Replace or remove every `<<block:...>>`.
* Leave no unresolved `<<slot:...>>`.
* Preserve all fixed headings and existing decisions.
* Do not invent approval status, implementation results, or supporting evidence.

--- TEMPLATE CONTENT ---

# Decisions

## Proposed

<[block:proposed-decisions](block:proposed-decisions)>

## Accepted

<[block:accepted-decisions](block:accepted-decisions)>

## Superseded

<[block:superseded-decisions](block:superseded-decisions)>

## Deprecated

<[block:deprecated-decisions](block:deprecated-decisions)>
