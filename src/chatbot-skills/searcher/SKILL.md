---
name: searcher
description: >-
  Research current facts with search tools and reliability checks. Use when a
  chatbot needs verified, source-backed answers instead of memory-only responses.
metadata:
  - target:
      - "Google Gemini"
---

# Searcher

Use search tools to retrieve verified facts; do not answer solely from memory.

## Reliability

- **Consensus**: Prioritize cross-verified consensus; label minority opinions.
- **Fact/Opinion**: Strictly separate objective facts from subjective opinions.
- **Fallback**: Output "Lack of reliable evidence" if data is scarce; never hallucinate.
- **Sources**: Prefer journals, official statistics, and deep reports. Exclude blogs, SNS, PR, and weakly sourced media when stronger evidence exists.

## Temporal Context

- Check current time when recency matters.
- Prioritize recent, reliable evidence.
- Include source years when useful.
- Separate historical and current evidence when the distinction matters.
- Cross-check new small studies against stronger prior evidence.

## Workflow

For complex searches, use [deep-search.md](references/deep-search.md). For Google operator syntax, use [google-advanced-search.md](references/google-advanced-search.md).

## Output

- List executed search queries as YAML when useful for reproducibility.
- Start with the key conclusion and context.
- Use Markdown structure and visuals only when they improve comprehension.
- State limitations when evidence is incomplete.
