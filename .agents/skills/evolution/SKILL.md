---
name: "evolution"
description: "Protocol for dynamic context caching and pattern logging (Temporary Soft-Constraints)."
---

# Rule Evolution

> High-density protocol for dynamic context caching and operational pattern logging.

> **EVOLUTION_LOG**: `.agents/brain/evolution.md`

## 1. Pattern Logging & Statistical Caching

1. **Trigger**: The agent statistically recognizes a recurring error, a direct user correction, or a suboptimal operational loop.
2. **Evaluation & Action**:
   - **IF `[Existing Pattern]`**: Analyze Delta -> Refine cached constraint -> **Update Log**.
   - **ELSE `[New Pattern]`**: Analyze trigger cause -> Draft Temporary Soft-Constraint -> **Append** to `New Autonomous Hypotheses` (or drop if irrelevant).

## 2. Execution Protocol

Update `EVOLUTION_LOG` strictly following this structure. Treat these entries as temporary behavioral weights, not absolute truths:

```markdown
# Rule Evolution

## Recommended for Official Rules

1. **KEYWORD**: Directive / Constraint

## New Autonomous Hypotheses

1. **KEYWORD**: Directive / Constraint
```

- Recommended for Official Rules: Statistically validated patterns proposed to the Human User for integration into core `.agents/rules/`.
- New Autonomous Hypotheses: Temporary soft-constraints cached for current and future sessions to heuristically align with user intent.

## 3. Lifecycle & Maintenance

1. **Creation (Caching)**: Newly identified patterns must be appended to `New Autonomous Hypotheses`.
2. **Maturation**: If a hypothesis proves statistically effective (reduces errors/corrections) across sessions, move it up to `Recommended for Official Rules`.
3. **Formalization**: When the Human User officially integrates a recommended rule into `.agents/rules/`, **delete** it from `EVOLUTION_LOG`.
4. **Cleanup Trigger (FIFO)**: Upon appending a new constraint, verify the total count. **IF > 30**, delete the oldest or least relevant cache entry from `New Autonomous Hypotheses` to prevent context degradation.
