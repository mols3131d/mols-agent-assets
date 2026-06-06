# Deep Search Workflow

## 1. Multi-Lingual Expansion

- Search in the user's native language for localized context.
- Translate query terms to English and execute parallel searches to capture global data, official documentation, and broad consensus.

## 2. Iterative Query Refinement

- Never conclude research after a single search query.
- Generate and execute at least 3 query variations using synonyms, acronyms, or conceptual shifts.
- Extract new keywords from initial results and perform subsequent searches to drill down.

## 3. Query Best Practices (Complex Syntaxes)
- **Authoritative Report Search**: `<query> site:[domain] filetype:[ext] -site:[unreliable_domain]`
- **Precise Error / API Search**: `"<exact_phrase>" <context> -site:[spam/forum_domain]`
- **Consensus & Date Search**: `("<term_A>" OR "<term_B>") site:[domain] after:[year]`
- **Proximity & Context Filter**: `"<term_A>" AROUND(<N>) "<term_B>" -"<noise_phrase>"`
