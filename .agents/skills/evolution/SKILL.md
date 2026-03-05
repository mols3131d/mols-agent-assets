---
name: "evolution"
description: "Protocol for recording and managing agent rule candidates (Direct MD editing)."
---

# Rule Evolution

> **EVOLUTION_LOG**: `.agents/brain/evolution.md`

High-density protocol for continuous agent self-improvement.

## Activation

- **Pattern Detected**: When a recurring operational pattern is identified.
- **Rule Proposal**: When logic dictates replacing or adding to existing `.agents/rules/`.
- **Lesson Learned**: To record a critical failure mechanism and its behavioral fix.

## Execution Protocol

Do NOT use scripts. Append directly to `EVOLUTION_LOG` using the following HDS format:

```markdown
- `[H | M | L]` **`[Topic/Pattern]`**: `[Logic & Reasoning]`
```

### Evaluation Levels

- **H (High/상)**: Core architectural or integrity rules. Must be formalized.
- **M (Medium/중)**: Useful patterns for specific modules.
- **L (Low/하)**: Experimental or personal agent preference.

## Maintenance

1. **Promotion**: If a candidate is proven and moved to `AGENTS.md` (or explicit rule file), **delete** it from `EVOLUTION_LOG`.
2. **Cleanup**: Maintain max **10 items**. FIFO (First-In, First-Out) if exceeded.
3. **Relative Paths**: Always use paths relative to the project root (no leading slashes).
