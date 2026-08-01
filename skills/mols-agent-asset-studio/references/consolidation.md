# Asset Consolidation

Use `consolidate` only when multiple assets overlap materially. Lexical similarity
is a discovery signal, not permission to merge.

## Decisions

| Decision | Use when |
| --- | --- |
| `Merge` | Purpose, authority, owner, runtime, and release lifecycle are compatible |
| `Compose` | Assets share a domain but should remain independently invocable |
| `Route` | One shallow entrypoint should select several bounded workflows |
| `Keep separate` | Permission, ownership, safety, runtime, or release lifecycle differs |
| `Deprecate` | Another accepted asset covers the complete required contract |

## Procedure

1. Inventory candidate assets and run `scripts/analyze_consolidation.py`.
1. Capture each source contract: triggers, near misses, outputs, tools, authority,
   safety, owner, runtime, distribution, and release lifecycle.
1. Choose one decision above. Do not merge solely to reduce file count.
1. For Merge or Route, create `templates/consolidation-plan.md` and map every
   source behavior to its destination or explicit retirement rationale.
1. Preserve source permissions and non-tool capability surfaces unless the approved
   plan changes them.
1. Use a shallow router only when independent workflows remain useful. Prefer a
   direct skill when one coherent workflow covers the job.
1. Evaluate clear positive, near-miss, multi-workflow, collision, and ambiguous
   requests against the candidate and legacy baseline.
1. Deprecate or remove old assets only after migration evidence passes.

## Optional Route Manifest

Do not require a registry for a small fixed workflow set. Consider a generated
`routes.yaml` only when there are at least eight independent workflows or the
entry file becomes mostly routing prose. The manifest must be deterministic,
validated, shallow, and generated from authoritative workflow metadata.
