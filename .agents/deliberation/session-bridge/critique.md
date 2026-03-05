# Negative Review: Session-Bridge Skill Migration

## Risks and Critiques

### 1. The "Observer's amnesia" (지침 망각 위험)

Rules are persistent constraints. Skills are reactive. By moving the session-bridge protocol into a skill and deleting the rule, an agent might **complete a session without ever realizing they should have called the skill**.

- **Risk**: The session ends abruptly without a handover, breaking the very continuity the protocol aims to save.

### 2. Excessive Modularization (과도한 파편화)

The original rule was a simple, 16-line markdown file. The new skill structure introduces a folder, meta-headers, template files, and (planned) scripts.

- **Critique**: We are trading a lightweight context tax (16 lines) for a high maintenance tax. For a protocol that is essentially "write two paragraphs," a multi-file skill is over-engineered.

### 3. The Automation Fallacy (자동화의 오류)

`scripts/bridge.py` is mentioned. Generating a "Narrative" requires a deep understanding of the logical jumps and hurdles of a session.

- **Risk**: Automation might encourage "lazy summaries" (e.g., "I finished Task A and B") instead of the "Narrative Delta" (e.g., "I encountered a 1-indexed error in tool X which forced a rewrite of Y") that the original protocol demanded.

### 4. Semantic Drift (의미의 변색)

In a rule, "Zero-Base" and "Delta Only" are strict mandates. In a skill instructions (`SKILL.md`), they risk being perceived as "optional suggestions" within a toolkit.

## Conclusion

If we proceed, we **must** have a mechanism to ensure the skill is triggered at the right time (at the start and end of every session), otherwise, we are trading reliability for a slim reduction in token usage.
