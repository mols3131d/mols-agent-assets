---
name: news-table
description: >-
  Curate recent news or developments into compact topic-grouped tables with
  deduplication, prioritization, dates, and a simple relevance score. Use when the
  user asks for a news roundup, trend brief, or topic-by-topic current-events table,
  especially with requested item counts. Pair with an appropriate research Skill
  when fresh external evidence is needed. Do not use for general research without a
  news-curation output.
---

# News Table

Use this Skill as **news curation and presentation context**. Evidence acquisition and
source verification remain the responsibility of the active research capability.

## Selection

- Follow the user's topics, scope, freshness window, region, and requested counts.
- Prefer actual new developments over evergreen background or repeated commentary.
- Deduplicate multiple reports of the same underlying event.
- Place each item in the single topic where it is most useful.
- Do not fill a requested quota with weak, stale, or materially redundant items.
- Distinguish the event, release, or effective date from the publication date when it
  matters to recency.
- Preserve important uncertainty or disagreement from the evidence instead of flattening
  it into a confident summary.

## Ranking

Use `Score` as a compact recommendation signal, not as a truth or confidence score.
Base it on the user's interests and the item's likely impact, novelty, relevance, or
actionability.

Use integers from `1` to `5` only when a score is useful. If scoring would be arbitrary
or the user does not benefit from it, omit the column.

## Output

Group results by topic. Default to a compact table:

```markdown
## <Topic>

| Date | News | Score |
| --- | --- | ---: |
| MM-DD | **<development>** — <what changed and why it matters> | 5 |
```

Adapt columns when the request calls for something else. Keep one item concise enough to
scan, but include the practical significance rather than only a headline.

Attach citations or source attribution using the host's supported mechanism. Do not force
a separate bibliography, superscript numbering scheme, or source log unless the user asks
for it or the runtime requires it.

## Composition

When current external evidence is required, combine this Skill with the appropriate
research Skill rather than duplicating search, source-ranking, or cross-checking rules
here. This Skill owns selection, deduplication, ranking, and presentation only.
