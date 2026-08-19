# `AGENTS.md`

## Authority

- `src/rulesync/` is the isolated native Rulesync workspace for distributable Rulesync-managed assets.
- `src/rulesync/rulesync.jsonc` configures projection targets and features.
- `src/rulesync/.rulesync/` is the canonical Rulesync source.
- Current Rulesync schema, file formats, feature names, target namespaces, and adapters are authoritative for Rulesync-managed assets.
- Repository-local documentation must not redefine Rulesync contracts that can be referenced directly.

Repository-specific integration conventions live in `docs/references/common/standards/rulesync-repository-conventions.md`.

## Repository Boundary

- Repository-root `.rulesync/` and `rulesync.jsonc` are forbidden. Distribution assets must not auto-activate for this repository itself.
- Generated target surfaces such as `.github/skills/`, `.github/agents/`, `.github/copilot-instructions.md`, `.agents/skills/`, `.agents/rules/`, and `.agents/agents/` are not distribution source.
- `.agents/AGENTS.md` is a repository-local guard outside the distribution source.
- `route/` is derived cross-runtime discovery metadata, not Rulesync canonical source. Follow `route/README.md` for its contract.
- Keep non-Rulesync custom source as an explicit peer of `src/rulesync/` only when a real required semantic cannot be represented by Rulesync.

## Authoring

Use Rulesync feature terminology directly. The currently configured features are `rules`, `skills`, and `subagents`.

- Author distributable Rules only when they are actual reusable/distributable Rules. Do not copy repository-maintenance policy into `src/rulesync/.rulesync/rules/`.
- Canonical Skills live at `src/rulesync/.rulesync/skills/<name>/SKILL.md`. Follow `docs/references/skills/skill-authoring-conventions.md` only for repository-local authoring conventions not owned by Rulesync or the target contract.
- Canonical Subagents live under `src/rulesync/.rulesync/subagents/`; use target-specific sections only for behavior the target actually supports.
- Do not create repository-local superset schemas or manual projection rules for fields Rulesync already models.
- Do not claim semantic parity when a target adapter cannot express a canonical capability.

Supporting resources are not separate Rulesync features unless Rulesync defines them as such. Put runtime resources with the asset that consumes them and repository verification under `tests/` or `evals/`.

## Asset Pipeline

1. **Author**: edit canonical source under `src/rulesync/.rulesync/`; edit `src/rulesync/rulesync.jsonc` only for Rulesync configuration.
1. **Validate read-only**: run native diagnostics or dry-run preview directly from `src/rulesync/`.
1. **Validate writes**: copy the native workspace to a temporary directory before generation/idempotence checks.
1. **Verify**: run the smallest applicable repository tests/evals.
1. **Deploy**: merge canonical source changes only. Do not commit generated target projection or Rulesync lock state.

The physical isolation is intentional: this repository develops distributable configuration assets and must not implicitly consume every asset it stores.
