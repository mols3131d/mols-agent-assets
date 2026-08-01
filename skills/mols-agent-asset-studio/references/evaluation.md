# Evaluation

Evaluation proves useful behavior, not only valid files.

## Layers

| Layer | Purpose |
| --- | --- |
| Structural | Frontmatter, schema, paths, links, and syntax |
| Trigger | Activation precision and recall |
| Behavior | Observable outputs, actions, and forbidden effects |
| Regression | Candidate versus legacy or no-skill baseline |
| Safety | Hostile input, path escape, secret handling, and authority |
| Portability | Runtime discovery and metadata behavior |
| Efficiency | Entry context, duplicate content, duration, and exposed token use |

## Trigger Sets

For a high-value general skill, maintain at least 20 fresh cases with 45-65%
positive cases. Include ordinary phrasing, implicit positives, sibling routing,
near misses, malformed requests, and requests that mention the asset type without
requesting asset lifecycle work.

Validate the case file:

```bash
python scripts/validate_eval_set.py <cases.json>
```

## Runtime Execution

Create a result sheet for each runtime and configuration:

```bash
python scripts/init_runtime_eval.py <cases.json> \
  --runtime github-copilot \
  --configuration candidate \
  --output candidate-results.json
```

Execute every case in isolated sessions and record observed activation. Create a
second sheet for `legacy` or `baseline`, then grade them:

```bash
python scripts/grade_runtime_eval.py <cases.json> candidate-results.json \
  --baseline legacy-results.json \
  --output comparison.json
```

Incomplete observations return exit code `2` and `Deferred`. Structural checks or
lexical heuristics never substitute for runtime activation evidence.

## Gate Rules

- Major behavior changes require runtime behavior evaluation when a supported
  runtime is available.
- Minor or Medium changes may skip with a concrete non-behavior reason.
- Candidate and baseline must use the same cases and runtime version.
- Record runtime, model, version, evidence, duration, and token data only when the
  host exposes them.
- Missing runtime access produces `Deferred`, not Pass.
