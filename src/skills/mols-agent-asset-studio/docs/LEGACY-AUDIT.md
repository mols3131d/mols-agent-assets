# Legacy Audit

## Baseline

The previous Studio used a minimal router `SKILL.md`, a generated
`workflows/INDEX.csv`, and many small workflow modules for backup, naming,
optimization, scriptification, creation, improvement, and validation.

## Findings

| Severity | Finding | Modern response |
| --- | --- | --- |
| High | Validation focused on frontmatter and references, not actual asset behavior | Add behavior, trigger, regression, safety, and portability evaluation |
| High | External source and executable-resource trust was not modeled | Add provenance tiers, quarantine, script/hook/MCP inspection |
| High | No project-specific adaptation lifecycle | Add independent `mols-agent-asset-tuner` |
| Medium | CSV router and micro-workflows add indirection for a small fixed set | Replace with direct mode table and one-level references |
| Medium | Backup to persistent `.tmp/` never cleans up and can accumulate sensitive copies | Prefer Git, explicit snapshots only when rollback evidence is needed |
| Medium | Improve workflow always requests approval in substeps and cannot operate autonomously when scope is clear | Ask only when authority, safety, or contract changes materially |
| Medium | Scriptification is split into ceremonial evaluate/plan/apply files | Integrate degree-of-freedom decisions into lifecycle and keep deterministic scripts |
| Medium | Cross-runtime frontmatter support was documented as a broad matrix without per-version evidence | Keep portable core and verify target runtime adapters |
| Low | Runtime skill included README/process-oriented material | Keep human reports outside runtime skill |
| Low | Similar preserve-behavior rules were repeated across workflows | Centralize in workflow contract and quality standard |

## Preserved Strengths

- concise semantic activation description
- minimal-file preference
- frontmatter name and directory alignment
- references and scripts separated from core instructions
- deterministic index and frontmatter checks
- explicit refusal to overwrite or rename without authority
