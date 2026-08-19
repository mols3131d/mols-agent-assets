# `AGENTS.md`

## Directory Roles

- `src/agentsmesh/`: canonical source for Agent Assets represented through AgentsMesh, including Rules, Skills, Agents, and the projection config. It is intentionally **not** named `.agentsmesh/` so this asset-library repository does not auto-activate its own distribution assets.
- `.agentsmesh/`: forbidden at repository root. A runtime-discoverable AgentsMesh workspace may exist only in temporary validation/projection workspaces.
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

Do not classify Skills by chatbot vs agent or flat vs runtime. A canonical Skill lives at `src/agentsmesh/skills/<name>/SKILL.md`. Keep a Skill single-file when `SKILL.md` is sufficient; add supporting resources only when the capability actually needs them.

For Skill authoring, separate external contracts from repository-local extensions:

1. `docs/references/skills/agent-skills-io/agent-skills-io-specification.md` — Tier 1 `agentskills.io` portable specification plus links to official Tier 2 vendor/harness contracts.
1. `docs/references/skills/agent-assets-skills-standard-personal.md` — repository-local **Personal Skill Standard** applied after external contracts.

Do not copy Tier 2 vendor rules into repository-local standards. Read the official target-harness source linked by the specification reference when host-specific behavior matters.

Supporting resources are not peer Agent Asset types alongside Rule, Skill, Prompt, and Agent.

## Asset Pipeline

1. **Author**: Edit `src/agentsmesh/` for every Agent Asset the current AgentsMesh contract can represent.
1. **Stage**: When native AgentsMesh validation or projection is needed, stage `src/agentsmesh/{rules,skills,agents}` as `<temporary-workspace>/.agentsmesh/` and stage `src/agentsmesh/agentsmesh.yaml` at that workspace root.
1. **Validate**: Run applicable AgentsMesh checks in the temporary workspace plus repository tests/evals at the cheapest relevant level.
1. **Deploy**: Merge canonical source changes. Do not commit temporary `.agentsmesh/` state or harness-native generated projections back into this repository.

The physical isolation is intentional: this repository develops Agent Assets; it must not implicitly consume every asset it stores.
