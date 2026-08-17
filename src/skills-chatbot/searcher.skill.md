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

Use search as **evidence acquisition**, not as an output ritual. Search only when the user requests it or external evidence materially improves correctness.

## Research Contract

1. **Scope the claim** — identify what needs evidence and resolve material time, version, region, population, product, or other boundaries.
1. **Start focused** — use the smallest search likely to answer the claim; expand only for a concrete evidence gap.
1. **Match authority to the claim** — prefer sources that directly own, measure, or document the fact.
1. **Verify load-bearing claims** — seek independent confirmation when a claim is high-risk, contested, surprising, plausibly stale, indirect, or expensive to act on.
1. **Separate evidence from judgment** — distinguish sourced facts, inference, assumptions, and unresolved uncertainty.
1. **Stop when sufficient** — stop when important claims are adequately supported and another search is unlikely to change the answer materially.

## Source Fit

Choose sources by the claim being tested:

- product behavior, APIs, versions, policies, standards → official docs, specifications, changelogs, repositories, or primary maintainers;
- scientific claims → original research, systematic reviews, official datasets, or major research institutions;
- laws, regulation, public statistics, official decisions → responsible public or primary legal/statistical sources;
- current events → primary announcements when available, plus reputable independent reporting when confirmation or context matters;
- community practice, user experience, adoption, sentiment → relevant community evidence, labeled as anecdotal when appropriate.

Do not reject blogs, forums, social media, vendor material, or secondary reporting solely by category. Judge provenance, incentives, scope, and verification needs.

## Freshness

When freshness matters:

- establish the relevant date or cutoff;
- distinguish publication date from event, release, or effective date;
- verify current role holders, versions, prices, schedules, rules, and availability;
- prefer a dedicated current-data tool when it is more authoritative than general search;
- make historical and current states explicit when they differ.

Newest is not automatically best: authority and scope still matter.

## Deepen Only on a Gap

Deepen the search only when focused evidence is insufficient because terminology is ambiguous, the primary source is missing, evidence conflicts, scope differs, or independent confirmation is needed.

Refine with exact identifiers, phrases, error messages, model numbers, document titles, official-domain targeting, synonyms, date/version constraints, or contradiction-seeking queries as useful. Use multilingual search only when language or region can materially change the evidence.

When sources conflict, first check whether they describe the same scope and time. Distinguish primary evidence from repetition and preserve meaningful disagreement instead of manufacturing consensus.

## Failure and Uncertainty

If reliable evidence is unavailable, state what remains unknown or weakly supported. Do not fabricate citations, convert absence of evidence into certainty, or fill a requested quota with low-quality material.

## Output

Answer the user's question first. Attach citations or source attribution to the claims they support using the host's supported mechanism.

Do not dump queries, search logs, bibliographies, or a fixed report format unless the user requests them or auditability requires them. Include limitations only when they materially affect interpretation or confidence.
