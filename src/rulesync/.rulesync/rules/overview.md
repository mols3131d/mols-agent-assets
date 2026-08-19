---
root: true
targets:
  - "*"
description: Repository-wide contract for mols-agent-assets agent work when this Rule is deliberately projected into a runtime workspace.
---

# Repository Contract

## Authority

- `src/rulesync/` is the isolated native Rulesync workspace for distributable Rulesync-managed assets.
- `src/rulesync/rulesync.jsonc` selects projection targets and features.
- `src/rulesync/.rulesync/` is the canonical source for Rules, Skills, and Subagents represented through Rulesync.
- Repository-root `.rulesync/`, `rulesync.jsonc`, and generated harness-native Skill/Rule/Agent surfaces are not canonical and must not be committed.
- `tests/` owns deterministic repository verification; Skill-specific tests use `tests/skills/<skill-name>/`.
- `evals/` owns behavioral, model, and cross-asset evaluation contracts; Skill-specific evals use `evals/skills/<skill-name>/`.
- Do not place repository verification assets such as `tests/`, `evals/`, `scenarios/`, or generated `results/` inside deployable `src/rulesync/.rulesync/skills/<name>/` packages.
- `docs/` owns human-facing standards and references.

## Language

- Use natural Korean for user-facing prose by default. Keep established IT terms in English or parallel when that is clearer or more precise.

## Asset Doctrine

- Primary Agent Asset types are Rule, Skill, Prompt, and Agent. Supporting resources are not peer asset types.
- Prefer one authoritative owner per durable behavior or policy.
- Prefer Skill for reusable capabilities or situation-specific context that should load on demand rather than globally.
- Do not classify Skills by chatbot vs agent or flat vs runtime. A Skill package starts at `src/rulesync/.rulesync/skills/<name>/SKILL.md`; add supporting resources only when needed.
- Repository Agent assets represented through Rulesync live under `src/rulesync/.rulesync/subagents/`.
- Preserve target-specific behavior only when the target actually supports it; do not claim semantic parity from format conversion alone.

## Development

- Follow repository branch, commit, PR, and validation rules in `docs/development.md` and applicable repository instructions.
- Do not commit ordinary change work directly to `main`.
- Run read-only Rulesync diagnostics and preview from `src/rulesync/`; run write-producing generation checks only against a temporary copy of that native workspace.
- Use the smallest relevant repository test/eval after deterministic validation.
- Do not claim runtime behavioral parity, trigger quality, or target execution success without runtime evidence.
