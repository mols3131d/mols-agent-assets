---
name: news-table
description: >-
  Curate recent news or developments into compact topic-grouped tables by selecting,
  deduplicating, prioritizing, and summarizing distinct developments. Use for news
  roundups, trend briefs, or topic-by-topic current-events tables, especially when the
  user requests item counts or recurring topic cadences. Do not use when news is only
  supporting evidence for broader research or when one development needs a deep dive.
---

# News Table

This Skill owns **news selection, deduplication, ranking, and presentation**. The active research capability owns evidence acquisition and source verification.

# Arguments

The user may specify the following naturally. Interpret omitted values from the request and current context only when doing so is useful; do not force a structured input format.

- **Topics** — one or more news subjects.
- **Count** — the desired number of distinct developments for each topic.
- **Interval** — how often each topic should be generated or refreshed, using an hourly or coarser cadence.
- **Freshness** — how far back to consider candidate developments for each topic.
- **Region** — a geographic or market scope when relevant.
- **Ranking** — the user's preferred emphasis, such as relevance, impact, novelty, or recency.
- **Score** — whether a visible relevance score would help comparison.
- **Grouping** — topic-grouped tables or another grouping requested by the user.

The values may differ by topic. For example: `AI agents every 6 hours, 10 developments from the last 48 hours; data engineering daily, 5 developments from the last week.`

`Count` means distinct developments after deduplication unless the user explicitly asks for articles or sources. `Interval` and `Freshness` are independent: a topic may refresh every few hours while considering a wider evidence window.

`Interval` expresses requested cadence at a minimum granularity of one hour; sub-hour recurrence is outside this Skill's contract. Actual repeated execution belongs to the active scheduler, automation capability, or harness. If no interval is requested, treat the topic as one-shot rather than inventing a recurrence.

# Curation

1. Follow the user's topics, scope, freshness window, region, requested counts, and cadence when provided.
1. Prefer actual new developments over evergreen background or repeated commentary.
1. Merge duplicate coverage of the same development. Keep a later update separate when it materially changes the state, availability, impact, or implications.
1. Count each distinct development once and place it in the single most useful topic. Secondary relevance may be mentioned without duplicating the item into another topic count.
1. Use the most meaningful date of the development rather than automatically using article publication date; distinguish event, release, publication, or effective dates when the difference matters.
1. Preserve material uncertainty or disagreement from the evidence.
1. Return fewer items rather than padding a requested count with weak, stale, or redundant developments, and make a material shortfall visible.

# Ranking

Prioritize items from the user's perspective. Relevance or significance usually matters more than raw publication recency; novelty and recency can break otherwise close choices. Respect a different emphasis when the user requests one.

Use `Score` only when it helps comparison. It is an ordinal relevance signal, primarily meaningful within the current topic, not a truth or confidence score. When useful, score `1` to `5` using likely impact, novelty, relevance, and actionability. Omit the column when the score would be arbitrary.

# Output

Group items by topic unless the request calls for another shape. Keep each row delta-first and easy to scan: state **what changed** before explaining why it matters, then include uncertainty only when material.

Default shape:

```markdown
## <Topic>

| Date | News |
| --- | --- |
| MM-DD | **<what changed>** — <why it matters> |
```

Add `Score` when it helps comparison. Adapt other columns to the request. Attach citations or source attribution with the host's supported mechanism; do not create a separate bibliography or source log unless requested or required.

# Boundary

Do not duplicate search, source-ranking, or cross-checking procedures here. When fresh evidence is needed, combine this Skill with the appropriate research capability.

Do not implement waiting, timers, or recurrence inside this Skill. When recurring delivery is requested, pass the interpreted topic cadence to the available scheduling or automation capability.
