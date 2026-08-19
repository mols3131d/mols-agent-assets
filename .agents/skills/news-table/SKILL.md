---
name: news-table
description: Curate recent news or developments into compact topic-grouped tables with deduplication, prioritization, dates, and a simple relevance score. Use when the user asks for a news roundup, trend brief, or topic-by-topic current-events table, especially with requested item counts. Do not use for general research without a news-curation output.
---

# News Table

This Skill owns **news selection, deduplication, ranking, and presentation**. The active research capability owns evidence acquisition and source verification.

## Selection

1. Follow the user's topics, scope, freshness window, region, and requested counts.
1. Prefer actual new developments over evergreen background or repeated commentary.
1. Deduplicate reports about the same underlying event and place each item in the single most useful topic.
1. Distinguish event, release, or effective date from publication date when recency could be misleading.
1. Preserve material uncertainty or disagreement from the evidence.
1. Stop before filling a quota with weak, stale, or redundant items.

## Ranking

Use `Score` only when it helps comparison. It is a relevance signal, not a truth or confidence score.

When useful, score `1` to `5` from the user's perspective using likely impact, novelty, relevance, and actionability. Omit the column when the score would be arbitrary.

## Output

Group items by topic and keep each row easy to scan while still stating why the development matters.

Default shape:

```markdown
## <Topic>

| Date | News | Score |
| --- | --- | ---: |
| MM-DD | **<development>** — <what changed and why it matters> | 5 |
```

Adapt columns to the request. Attach citations or source attribution with the host's supported mechanism; do not create a separate bibliography or source log unless requested or required.

## Boundary

Do not duplicate search, source-ranking, or cross-checking procedures here. When fresh evidence is needed, combine this Skill with the appropriate research capability.