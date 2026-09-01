# Common Authoring

Use this reference for authoring decisions shared by Skill, Rule, and subagent work. Type-specific authoring references own the details of each asset type.

## Responsibility

Resolve the responsibility before choosing a file, format, or asset type.

- Prefer extending an established owner to creating a competing owner.
- For new or materially changed behavior, check the abstraction against at least one concrete intended use.
- When selection or scope is easy to confuse with a nearby case, identify a representative non-use or near-miss.
- If ownership or asset type remains materially ambiguous after reading applicable authority and nearby accepted assets, preserve the ambiguity rather than guessing.

## Authority

Authority is concern-specific.

1. User and project guidance own the requested outcome and allowed scope.
1. The source framework owns canonical representation.
1. The target runtime owns target-specific behavior.
1. Repository conventions own local deltas.
1. The individual asset may own requirements intentionally narrower than those authorities.

Do not mirror fast-changing vendor fields, paths, discovery, packaging, permissions, or runtime behavior into portable guidance. Read the current authoritative target source when those details affect the change.

## Write boundary

Set the write boundary before mutation. Reading outside it for authority, dependencies, or nearby examples does not grant write authority.

- Do not normalize unrelated assets while changing one target.
- Treat generated or projected outputs as derived unless the governing source explicitly makes them editable authority.
- Preserve required attribution, license terms, and upstream revision when reused source material depends on them.

## Precision

Use the least restrictive mechanism that is reliable enough for the failure cost.

- Prefer outcomes, constraints, and heuristics when multiple approaches are valid.
- Add stronger structure when a preferred pattern materially improves consistency.
- Use deterministic mechanics or narrowly specified sequences when ordering, reproducibility, or failure cost makes free-form judgment unsafe.
- Do not restate general model knowledge unless repeated failures show that the missing instruction matters.
- Do not add an abstraction layer only to make unlike assets look structurally uniform.

## Change

Make the smallest coherent change that preserves the requested behavior and established valid intent.

- State what should change and what must remain true before substantial mutation.
- Prefer deletion, simplification, clearer ownership, or project-native mechanisms over another abstraction layer.
- Add files only when they provide a concrete loading, ownership, runtime, or deterministic-mechanics benefit.
- Re-read the result against the request, preserved invariants, source/target boundary, and affected links or paths.
