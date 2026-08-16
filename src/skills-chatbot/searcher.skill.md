---
name: searcher
description: >-
  Research externally verifiable or time-sensitive facts with available search or
  browsing tools and evidence checks. Use when the user asks to search, verify,
  cite, compare current information, or find the latest state; when the answer
  materially depends on changing, niche, contested, or uncertain facts; or when
  memory-only reasoning would create meaningful correctness risk. Do not search
  when the task is fully supported by user-provided content or current external
  facts are irrelevant to the requested transformation or creative work.
---

# Searcher

Use search as **evidence acquisition**, not as an output ritual. Search only when it
materially improves correctness or the user explicitly requests it.

## Research Contract

1. **Scope first** — identify the claim or decision that needs evidence. Resolve
   relevant time, version, region, population, product, or other scope before
   comparing sources.
1. **Use the smallest sufficient search** — start focused and expand only when
   evidence is missing, conflicting, ambiguous, or broader coverage is genuinely
   required.
1. **Match source authority to the claim** — prefer the source that directly owns or
   measures the fact instead of applying one universal source ranking.
1. **Verify load-bearing claims** — cross-check claims that materially affect the
   conclusion when evidence is indirect, contested, high-risk, or plausibly stale.
1. **Separate evidence from judgment** — distinguish sourced facts, reasonable
   inference, assumptions, and unresolved uncertainty.
1. **Stop when sufficient** — do not keep searching after important claims are
   adequately supported and more queries are unlikely to change the answer.

## Source Selection

Choose sources for the claim being tested.

- Product behavior, APIs, versions, policies, standards → official documentation,
  specifications, changelogs, repositories, or primary maintainers.
- Scientific claims → original research, systematic reviews, official datasets, and
  major research institutions; judge methodology and scope rather than source count.
- Laws, regulation, public statistics, official decisions → responsible public
  authority or primary legal/statistical source.
- Current events → primary announcements when available plus reputable independent
  reporting when confirmation or context matters.
- Community practice, user experience, adoption, sentiment → relevant community
  evidence; label anecdotal evidence appropriately.

Do not reject blogs, forums, social media, vendor material, or secondary reporting
solely by category. Account for incentives, provenance, and verification needs.

## Freshness

When freshness matters:

- establish the current date or relevant cutoff;
- distinguish publication date from event, release, or effective date;
- verify current role holders, versions, prices, schedules, rules, and availability;
- prefer the newest source only when it still has the required authority and scope;
- make historical and current states explicit when they differ;
- prefer a host-provided dedicated current-data tool when it is more authoritative
  for that data type than general search.

## Cross-checking

Scale verification to error cost. Seek independent confirmation for high-stakes,
contested, surprising, stale, indirect, or expensive-to-act-on claims. A source that
merely repeats another source is not independent confirmation.

## Deep Search

Use a deeper search only when a small focused search is insufficient.

1. Identify unresolved dimensions: terminology or aliases, time/version/geography,
   primary source owner, competing explanations, or local/global context.
1. Search the highest-value evidence gap first. Expand only when another query can
   materially improve the answer.
1. Refine with exact phrases, identifiers, error messages, model numbers, document
   titles, official-domain targeting, synonyms, date/version constraints, or queries
   designed to find contradiction and independent confirmation.
1. Use multilingual search only when language or region is likely to change the
   available evidence.
1. When evidence conflicts, confirm the sources cover the same scope and time,
   distinguish primary evidence from repetition, inspect methodology/authority/
   incentives/provenance as relevant, and preserve meaningful disagreement.
1. Stop when load-bearing claims are sufficiently supported, important uncertainty
   is represented, and another query is unlikely to change the answer materially.

Do not require a fixed number of query variations. Repeating searches without a new
evidence gap is not deeper research.

## Search Operators

Use advanced operators only when the active search provider supports them and they
reduce retrieval noise. Useful forms may include:

```text
"exact phrase"
-term
site:domain
filetype:ext
intitle:term
inurl:term
after:YYYY before:YYYY
A AROUND(N) B
A OR B
```

Provider-specific syntax is optional; do not depend on it for the capability.

## Failure and Uncertainty

If reliable evidence is unavailable, state what remains unknown or weakly supported.
Do not convert absence of evidence into certainty, fabricate citations, or fill a
requested quota with low-quality material merely for completeness.

When sources disagree, represent the important disagreement and explain which source
is more applicable or authoritative for the specific claim instead of manufacturing
false consensus.

## Output

Answer the user's question first. Attach citations or source attribution to the claims
they support when the runtime supports it.

Do not dump executed queries, a search log, a bibliography, or a fixed report format
unless the user requests it or it is necessary to audit the result. Include
limitations only when they materially affect interpretation or confidence.
