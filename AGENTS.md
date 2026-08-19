# `AGENTS.md`

## Directory Roles

- `src/rulesync/`: native Rulesync workspace for distributable Rulesync-managed assets.
- `src/rulesync/rulesync.jsonc`: workspace projection configuration.
- `src/rulesync/.rulesync/`: canonical Rulesync source for Rules, Skills, and Subagents. This nested location preserves the native Rulesync layout without exposing the repository root as a Rulesync runtime workspace.
- Repository-root `.rulesync/` and `rulesync.jsonc`: forbidden. Distribution assets must not auto-activate for this repository itself.
- `.github/skills/`, `.github/agents/`, `.github/copilot-instructions.md`, `.agents/rules/`, and `.agents/agents/`: generated runtime projection surfaces. Do not commit generated Rulesync output there.
- `.agents/skills/`: repository runtime Skill surface. Only explicitly repository-local Skills belong here; it is not canonical distribution source and must not receive generated Rulesync projections. Current explicit exceptions are `mols-chatbot-bootstrap` and `mols-ci-design`.
- `.agents/AGENTS.md`: repository-local guard outside the distribution source. Follow its contents.
- `src/`: source tree for distributable Agent Assets. Keep non-Rulesync custom assets as explicit peers of `src/rulesync/` only when a real format or target requires them.
- `scripts/`: repository automation, synchronization, setup, validation, and other development tooling.
- `tests/`: repository-level automated tests for assets and tooling.
- `docs/`: repository-level human-facing documentation and references.

For asset doctrine, distinguish:

1. `docs/references/common/standards/agent-assets-standard-baseline.md` — standards-adjacent external/common baseline.
1. `docs/references/common/standards/agent-assets-standard-personal.md` — **Personal Agent Asset Standard** and repository authority for non-standard extensions.

Prefer Skill as the portable reusable unit when a capability or situation-specific context should be activated on demand by the model rather than loaded globally.

Do not classify Skills by chatbot vs agent or flat vs runtime. A canonical Skill lives at `src/rulesync/.rulesync/skills/<name>/SKILL.md` and follows the current Rulesync canonical schema. Keep a Skill single-file when `SKILL.md` is sufficient; add supporting resources only when the capability actually needs them.

Repository Agent assets represented through Rulesync live under `src/rulesync/.rulesync/subagents/`; use target-specific sections only for behavior the target actually supports.

For Skill authoring, separate canonical representation from generated target contracts:

1. Current Rulesync schema and adapters — canonical front matter, target namespaces, and projection behavior.
1. `docs/references/skills/agent-skills-io/agent-skills-io-specification.md` — Agent Skills output contract plus links to official vendor/harness contracts.
1. `docs/references/skills/agent-assets-skills-standard-personal.md` — repository-local **Personal Skill Standard** for conventions not owned by Rulesync or a target contract.

Do not copy Tier 2 vendor rules into repository-local standards. Read the official target-harness source linked by the specification reference when host-specific behavior matters.

Supporting resources are not peer Agent Asset types alongside Rule, Skill, Prompt, and Agent.

## Asset Pipeline

1. **Author**: Edit canonical assets under `src/rulesync/.rulesync/`; edit `src/rulesync/rulesync.jsonc` only for workspace projection configuration.
1. **Validate read-only**: Run native diagnostics or preview directly from `src/rulesync/`.
1. **Validate writes**: Copy the native workspace verbatim to a temporary directory before generation/idempotence checks so generated projections and lock state never become repository files.
1. **Verify**: Run applicable repository tests/evals at the cheapest relevant level.
1. **Deploy**: Merge canonical source changes only. Do not commit generated target projections or Rulesync lock state.

The physical isolation is intentional: this repository develops Agent Assets; it must not implicitly consume every distribution asset it stores.
