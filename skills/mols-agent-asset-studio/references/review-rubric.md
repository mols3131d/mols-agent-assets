# General Review Rubric

Review in fresh context. Read the target, stated purpose, requirements, project
policy, and applicable official specification. Do not read author persuasion.

## Dimensions

| Dimension | Review question |
| --- | --- |
| Scope | Does the artifact solve the stated job without unrelated authority? |
| Trigger | Will ordinary positive cases activate it and near misses avoid it? |
| Architecture | Is each concern in the right asset type and loading layer? |
| Procedure | Are steps ordered, executable, and explicit about inputs and outputs? |
| Evidence | Are factual claims and completion assertions supported? |
| Reliability | Are deterministic parts scripted and behavior-bearing parts evaluated? |
| Safety | Are permissions, secrets, external actions, and destructive effects bounded? |
| Portability | Are host-specific assumptions isolated and disclosed? |
| Maintainability | Is content concise, non-duplicated, linked, and testable? |
| User contract | Is the final result, status, limitation, and next action clear? |

## Finding Format

```markdown
### F-001 — High — Trigger overlaps general documentation work

- Evidence: `<file>:<line or section>`
- Impact: The skill may activate for unrelated prose editing.
- Required change: Narrow the description and add near-miss evaluation cases.
- Acceptance evidence: Trigger eval set passes all positive and negative cases.
```

## Verdict

- `Pass`: no open Critical, High, or acceptance-blocking Medium finding
- `Revise`: actionable findings remain
- `Blocked`: review cannot establish the target, policy, or required evidence
