# Full

Load only for **full**.

- Strong n↔m: merge thin same-relation sentences; split multi-relation clauses.
- Hard front-load A (context+core). Trail B (rest).
- One primary relation per sentence after merge.
- Complete grammar. No article/particle strip. No fact deletion for density.
- Re-parse or guessed relation → step down to lite.

**lite:** four short sentences (cause, effect, action, rest).  
**full:** merge cause+effect; action; rest trailing.

> Each request opens a new database connection, so connection cost rises under load and performance falls. Use a connection pool.
> Tune pool size later if traffic requires it.
