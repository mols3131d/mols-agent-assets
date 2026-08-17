# 04. Optimizing Skill Descriptions

## Core Concept

`description` triggers activation. Too narrow = missed queries (False Negative). Too broad = wrong activations (False Positive). Test systematically with train/val splits; do not rely on intuition.

## Trigger Mechanics

- Agent sees ONLY `name` + `description` initially.
- Body text is invisible until activated.
- Best for domain-specific tasks where standard capabilities fail.

## Writing Guide

- **Imperative**: "Use this skill when..."
- **Intent-focused**: Describe user goal, not internal logic.
- **Contextual**: Cover implicit keywords.
- **Concise**: < 1024 chars.
- **Boundaries**: State what it does AND does not do.

## Eval Query Design

Need realistic `query` + `should_trigger` (bool) pairs.

- **Positive (Should trigger)**: Focus on implicit requests without exact keywords.
- **Negative (Near-misses)**: Use overlapping concepts (e.g., CSV analytics vs. CSV ETL).
- **Realism**: Use real paths, typos, slang, dense contexts.

## Measurement

- Run multiple times per query (models are non-deterministic). Start with 3x.
- Formula: `trigger_rate = triggers / total_runs`.
- Pass: `trigger_rate > threshold` (e.g., 0.5) for positive, `< threshold` for negative.
- Automate via script.

## Iteration Loop

- **Split**: 60% Train (for fixing), 40% Validation (for testing generalization). Fixed split.
- Analyze False Negatives (widen scope) and False Positives (tighten boundaries).
- Target intents, do not just copy-paste failed query words.
- Stop when Train passes or plateaus. Pick best Validation score iteration.
- Approx. 5 iterations max.

## Checklist

- [ ] Imperative trigger phrasing.
- [ ] Describes user intent.
- [ ] Contains near-miss negative queries.
- [ ] Averaged multiple runs for trigger rate.
- [ ] Fixed train/val split without leakage.
- [ ] Final check with fresh holdout queries.
