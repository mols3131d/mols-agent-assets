# `AGENTS.md`

## Authority

Rulesync-managed assets use two intentionally separate workspaces.

- Repository workspace: root `.rulesync/` + `rulesync.jsonc`, only for Rulesync assets that configure or maintain this repository itself.
- Library workspace: `src/rulesync/.rulesync/` + `src/rulesync/rulesync.jsonc`, for reusable assets this repository stores and distributes.
- The library workspace must never be treated as this repository's runtime configuration.
- Current Rulesync schema, file formats, feature names, target namespaces, and adapters are authoritative for Rulesync-managed assets.
- Repository-local documentation must not redefine Rulesync contracts that can be referenced directly.

Repository-specific integration conventions live in `docs/references/common/conventions/rulesync-repository-conventions.md`.

## Repository Boundary

- Repository-level Rulesync assets, when needed, belong only in the root Rulesync workspace. Do not place them in `src/rulesync/.rulesync/`.
- Reusable/distributable Rulesync assets belong only in `src/rulesync/.rulesync/`. Do not copy the whole library into the root workspace.
- Root Rulesync workspace is optional. Do not create it merely to mirror the library.
- Generated target surfaces such as `.github/skills/`, `.github/agents/`, `.github/copilot-instructions.md`, `.agents/skills/`, `.agents/rules/`, and `.agents/agents/` are not canonical source and must not be committed as projection output.
- `.agents/AGENTS.md` is a repository-local guard outside both Rulesync canonical workspaces.
- `route/` is derived cross-runtime discovery metadata for the library, not Rulesync canonical source. Follow `route/README.md` for its contract.
- Keep non-Rulesync custom source as an explicit peer of `src/rulesync/` only when a real required semantic cannot be represented by Rulesync.

## Target Scope

This repository does not define a supported vendor/target matrix. Select targets only for the projection or validation operation that needs them.

Target-specific sections in individual assets may remain when they are meaningful for past, current, or plausible future use. Do not remove valid metadata merely because a target is not selected for a current projection.

## Authoring

Use Rulesync feature terminology directly.

For the library workspace, the committed feature set is `rules`, `skills`, and `subagents`.

- Author library Rules only when they are actual reusable/stored Rules. Repository-maintenance Rules belong in the root workspace instead.
- Canonical library Skills live at `src/rulesync/.rulesync/skills/<name>/SKILL.md`. Follow `docs/references/skills/skill-authoring-conventions.md` only for repository-local authoring conventions not owned by Rulesync or the target contract.
- Canonical library Subagents live under `src/rulesync/.rulesync/subagents/`; use target-specific sections only for behavior the target actually supports.
- Do not create repository-local superset schemas or manual projection semantics for fields Rulesync already models.
- Do not claim semantic parity when a target adapter cannot express a canonical capability.

Supporting resources are not separate Rulesync features unless Rulesync defines them as such. Put runtime resources with the asset that consumes them and repository verification under `tests/` or `evals/`.

## Asset Pipeline

For reusable library assets:

1. **Author**: edit canonical source under `src/rulesync/.rulesync/`; edit `src/rulesync/rulesync.jsonc` only for the library workspace configuration.
1. **Validate canonical**: run native diagnostics against `src/rulesync/`.
1. **Validate projection when needed**: choose targets at invocation time and use a temporary workspace for write-producing generation/idempotence checks.
1. **Verify**: run the smallest applicable repository tests/evals.
1. **Keep canonical only**: do not commit generated target projection or Rulesync lock state.

For repository-level Rulesync assets, use only the root Rulesync workspace and validate it independently from the library workspace.

The physical separation is intentional: this repository may consume a small repository-local Rulesync configuration while storing a much larger reusable asset library without implicitly activating that library.
