# `AGENTS.md`

## Directory Roles

- `src/agentsmesh/`: native AgentsMesh workspace for distributable AgentsMesh-managed assets.
- `src/agentsmesh/agentsmesh.yaml`: workspace projection configuration.
- `src/agentsmesh/.agentsmesh/`: canonical AgentsMesh source for Rules, Skills, and Agents. This nested location preserves the native AgentsMesh layout without exposing the repository root as an AgentsMesh runtime workspace.
- Repository-root `.agentsmesh/` and `agentsmesh.yaml`: forbidden. Distribution assets must not auto-activate for this repository itself.
- `.github/skills/`, `.github/agents/`, `.github/copilot-instructions.md`, `.agents/rules/`, and `.agents/skills/`: generated runtime projections. Do not commit them to this repository.
- `.agents/AGENTS.md`: repository-local guard outside the distribution source. Follow its contents.
- `src/`: source tree for distributable Agent Assets. Keep non-AgentsMesh custom assets as explicit peers of `src/agentsmesh/` only when a real format or target requires them.
- `scripts/`: repository automation, synchronization, setup, validation, and other development tooling.
- `tests/`: repository-level automated tests for assets and tooling.
- `docs/`: repository-level human-facing documentation and references.

For asset doctrine, distinguish:

1. `docs/references/common/standards/agent-assets-standard-baseline.md` — standards-adjacent external/common baseline.
1. `docs/references/common/standards/agent-assets-standard-personal.md` — **Personal Agent Asset Standard** and repository authority for non-standard extensions.

Prefer Skill as the portable reusable unit when a capability or situation-specific context should be activated on demand by the model rather than loaded globally.

Do not classify Skills by chatbot vs agent or flat vs runtime. A canonical Skill lives at `src/agentsmesh/.agentsmesh/skills/<name>/SKILL.md`. Keep a Skill single-file when `SKILL.md` is sufficient; add supporting resources only when the capability actually needs them.

For Skill authoring, separate external contracts from repository-local extensions:

1. `docs/references/skills/agent-skills-io/agent-skills-io-specification.md` — Tier 1 `agentskills.io` portable specification plus links to official Tier 2 vendor/harness contracts.
1. `docs/references/skills/agent-assets-skills-standard-personal.md` — repository-local **Personal Skill Standard** applied after external contracts.

Do not copy Tier 2 vendor rules into repository-local standards. Read the official target-harness source linked by the specification reference when host-specific behavior matters.

Supporting resources are not peer Agent Asset types alongside Rule, Skill, Prompt, and Agent.

## Asset Pipeline

1. **Author**: Edit canonical assets under `src/agentsmesh/.agentsmesh/`; edit `src/agentsmesh/agentsmesh.yaml` only for workspace projection configuration.
1. **Validate read-only**: Run native lint or preview directly from `src/agentsmesh/`.
1. **Validate writes**: Copy the native workspace verbatim to a temporary directory before generation/idempotence checks so generated projections and lock state never become repository files.
1. **Verify**: Run applicable repository tests/evals at the cheapest relevant level.
1. **Deploy**: Merge canonical source changes only. Do not commit generated target projections or AgentsMesh lock state.

The physical isolation is intentional: this repository develops Agent Assets; it must not implicitly consume every asset it stores.
