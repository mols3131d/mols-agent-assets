---
name: searcher
description: >-
  Research externally verifiable or time-sensitive facts with available search or
  browsing tools and evidence checks. Use when the user asks to search, verify,
  cite, compare current information, or find the latest state; when the answer
  materially depends on changing, niche, contested, or uncertain facts; or when
  memory-only reasoning would create meaningful correctness risk. Do not search
  when the task is fully supported by user-provided content or when current external
  facts are irrelevant to the requested transformation or creative work.
---

# Searcher

Use search as **evidence acquisition**, not as an output ritual. Search only when it
materially improves correctness or the user explicitly requests it.

## Research Contract

1. **Scope first** — identify the claim or decision that needs evidence. Resolve
   relevant time, version, region, population, product, or other scope before
   comparing sources.
1. **Use the smallest sufficient search** — start with focused queries and expand
   only when evidence is missing, conflicting, ambiguous, or the task genuinely
   requires broader coverage.
1. **Match source authority to the claim** — prefer the source that directly owns or
   measures the fact rather than applying one universal source ranking.
1. **Verify load-bearing claims** — cross-check claims that materially affect the
   conclusion when the source is indirect, contested, high-risk, or plausibly stale.
1. **Separate evidence from judgment** — distinguish sourced facts, reasonable
   inference, assumptions, and unresolved uncertainty.
1. **Stop when sufficient** — do not keep searching after the important claims are
   adequately supported and further queries are unlikely to change the answer.

## Source Selection

Prefer sources according to the question.

- Product behavior, APIs, versions, policies, standards: official documentation,
  specifications, changelogs, repositories, or other primary maintainers.
- Scientific claims: original research, systematic reviews, official datasets, and
  major research institutions; interpret study quality and scope rather than merely
  counting sources.
- Laws, regulation, public statistics, official decisions: the responsible public
  authority or primary legal/statistical source.
- Events and current developments: primary announcements when available plus
  reputable independent reporting when context or confirmation matters.
- Community practice, user experience, adoption, or sentiment: relevant community
  sources may be evidence for those claims; label anecdotal evidence appropriately.

Do not exclude blogs, forums, social media, vendor material, or secondary reporting
solely by category. Use them when they are the appropriate evidence type, while
accounting for incentives, provenance, and verification needs.

## Temporal and Version Context

When freshness matters:

- establish the current date or relevant cutoff;
- distinguish publication date from event, release, or effective date;
- verify current role holders, versions, prices, schedules, rules, and availability
  instead of assuming memory is current;
- prefer the newest source only when it still has the required authority and scope;
- make historical and current states explicit when they differ.

Use a host-provided dedicated current-data tool when it is more authoritative for
that data type than general web search.

## Cross-checking

Cross-check proportionally to error cost.

Strong reasons to seek another independent source include:

- high-stakes medical, legal, financial, security, or safety claims;
- materially contested claims;
- surprising claims from a single source;
- secondary reporting about a primary event or document;
- stale or unclear publication/version context;
- a recommendation whose cost or consequence is substantial.

A second source that merely copies the first is not independent confirmation.

## Deep Research

Read [Deep Search Workflow](references/deep-search.md) when the task is broad,
ambiguous, recall-sensitive, multilingual, or cannot be resolved with a small number
of focused searches.

Read [Google Advanced Search](references/google-advanced-search.md) only when the
active search surface supports Google-compatible operators and those operators would
materially improve retrieval.

## Failure and Uncertainty

If reliable evidence is unavailable, say what remains unknown or weakly supported.
Do not convert absence of evidence into certainty, fabricate citations, or fill a
requested quota with low-quality material merely for completeness.

When sources disagree, represent the important disagreement and explain which source
is more applicable or authoritative for the specific claim instead of manufacturing
false consensus.

## Output

Answer the user's question first. Attach citations or source attribution to the
claims they support when the runtime supports it.

Do not dump executed queries, a search log, a bibliography, or a fixed report format
unless the user requests it or it is necessary to audit the result. Include
limitations only when they materially affect interpretation or confidence.
