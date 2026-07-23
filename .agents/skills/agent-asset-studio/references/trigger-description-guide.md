# Writing Agent Asset Trigger Descriptions

> A Trigger Description is an intent classifier, not a feature summary.

## Purpose

`description` decides whether an Agent Asset activates. Write classification criteria for user requests, not a feature introduction.

- Too narrow increases false negatives.
- Too broad increases false positives.

## Principles

1. Start with `USE WHEN...`.
2. Describe the user's goal and intent, not internal implementation.
3. Cover implicit requests without exact keywords in `USE WHEN`; add `INCLUDES` only when a separate clarification helps.
4. State both scope and exclusions.
5. Stay concise and within 1024 characters.

## Recommended Template

```text
USE WHEN: [core goal, representative tasks, and implicit requests].
INCLUDES: [optional clarification only when needed].
EXCLUDES: [excluded scope and near misses].
```

## Example

```text
USE WHEN: the user wants to analyze structured data, investigate metric changes, compare segments, derive quantitative insights, or identify drivers behind drops, spikes, or performance gaps.
EXCLUDES: file conversion, ETL implementation, or database administration without an analytical objective.
```

## Checklist

- [ ] Starts with an imperative trigger
- [ ] Focuses on user intent
- [ ] Covers implicit requests
- [ ] Uses `INCLUDES` only when it adds information beyond `USE WHEN`
- [ ] States scope and exclusions
- [ ] Distinguishes adjacent Skills
- [ ] Stays within 1024 characters
