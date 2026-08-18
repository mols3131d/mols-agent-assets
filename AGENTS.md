# `AGENTS.md`

## Directory Roles

- `.agentsmesh/`: Primary canonical source for Agent Assets represented by AgentsMesh, including Rules, Skills, and Agents. Edit this source, not generated target files.
- `.github/skills/`, `.github/agents/`, `.github/copilot-instructions.md`, `.agents/rules/`, and `.agents/skills/`: AgentsMesh-generated target projections. Do not hand-edit them.
- `.agents/AGENTS.md`: Repository-local guard outside the AgentsMesh generated surfaces. Follow its contents.
- `src/`: Compatibility surface for hosted-chatbot assets that are not managed by the current AgentsMesh target set. Do not create portable coding-agent authority here.
- `scripts/`: Repository automation, synchronization, setup, validation, and other development tooling.
- `tests/`: Repository-level automated tests for assets and tooling.
- `docs/`: Repository-level human-facing documentation and references.

For asset doctrine, distinguish:

1. `docs/references/common/standards/agent-assets-standard-baseline.md` — standards-adjacent external/common baseline.
1. `docs/references/common/standards/agent-assets-standard-personal.md` — **Personal Agent Asset Standard** and repository authority for non-standard extensions.

Prefer Skill as the portable reusable unit when a capability or situation-specific context should be activated on demand by the model rather than loaded globally.

For portable coding-agent Rule deployment, AgentsMesh owns canonical representation and target fan-out from `.agentsmesh/rules/`. `docs/references/rules/agent-assets-rules-projections.md` documents repository-local boundaries, including the hosted-chatbot fallback `CHATBOT.md → AGENTS.md → README.md`, which remains outside AgentsMesh.

For Skill authoring, separate external contracts from repository-local extensions:

1. `docs/references/skills/agent-skills-io/agent-skills-io-specification.md` — Tier 1 `agentskills.io` portable specification plus links to official Tier 2 vendor/harness contracts.
1. `docs/references/skills/agent-assets-skills-standard-personal.md` — repository-local **Personal Skill Standard** applied after external contracts.

Do not copy Tier 2 vendor rules into repository-local standards. Read the official target-harness source linked by the specification reference when host-specific behavior matters.

Target profile and package-surface details are delegated to `docs/references/skills/agent-assets-skills-target-profiles.md`. Hosted-chatbot profiles under `src/` remain explicit compatibility surfaces outside the current AgentsMesh coding-target set.

Supporting resources are not peer Agent Asset types alongside Rule, Skill, Prompt, and Agent.

## Asset Pipeline

1. **Author**: Use `.agentsmesh/` for AgentsMesh-managed canonical Agent Assets. Use an existing `src/` compatibility profile only when the hosted-chatbot target requires it.
1. **Generate**: For AgentsMesh-managed assets, run the pinned AgentsMesh toolchain to project active targets.
1. **Validate**: Run applicable AgentsMesh checks plus repository tests/evals at the cheapest relevant level.
1. **Deploy**: Merge the validated feature branch to the distribution branch.

Generated target files are evidence and distribution artifacts, not independent sources of truth.
