# Transitional Source Exceptions (`src/`)

`src/` keeps Agent Assets that are **not yet migrated to `.agentsmesh/` or cannot be represented faithfully by the current AgentsMesh contract**.

It is a transitional exception surface, not the preferred long-term canonical root. Repository tooling belongs in root `scripts/`.

| Directory | Current role |
| --- | --- |
| `agents/` | Target-specific subagents/custom agents whose current semantics are not safely portable through the active AgentsMesh target set |
| `prompts/` | Explicit invocation prompts and hosted-service orchestration prompts |
| `skills-chatbot/` | Current self-contained single-file hosted-chatbot Skill exception |
| `skills-chatbot-runtime/` | Current bundled/runtime hosted-chatbot Skill exception |
| `rules/` | Hosted-chatbot-specific Rules outside the current AgentsMesh contract |

Do not recreate `src/skills/` as a second portable Skill source. Prefer `.agentsmesh/` whenever an asset can be represented there without semantic loss, and treat existing `src/` profiles as migration candidates rather than permanent taxonomy.

The peer Agent Asset types remain **Rule, Skill, Prompt, and Agent**. Supporting resources and repository tooling are not peer asset types.

For portable coding-agent Rule projection, use AgentsMesh. The repository-local chatbot fallback `CHATBOT.md → AGENTS.md → README.md` remains a separate hosted-chatbot convention documented under `docs/references/rules/`.
