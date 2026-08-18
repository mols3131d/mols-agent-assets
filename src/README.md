# Hosted Chatbot Compatibility (`src/`)

`src/` keeps hosted-chatbot Agent Assets that are outside the current AgentsMesh coding-target surface.

Portable coding-agent Rules, Skills, and Agents belong in `.agentsmesh/`. Repository tooling belongs in root `scripts/`.

| Directory | Current role |
| --- | --- |
| `skills-chatbot/` | Self-contained single-file hosted-chatbot Skills |
| `skills-chatbot-runtime/` | Bundled/runtime hosted-chatbot Skills |
| `rules/` | Hosted-chatbot-specific Rules outside the current AgentsMesh contract |

Do not recreate `src/skills/`, `src/agents/`, or `src/prompts/` as parallel portable sources. Use `.agentsmesh/` when the active coding-agent contract can own the asset.

The peer Agent Asset types remain **Rule, Skill, Prompt, and Agent**. Supporting resources and repository tooling are not peer asset types.

The repository-local chatbot fallback `CHATBOT.md → AGENTS.md → README.md` remains a separate hosted-chatbot convention documented under `docs/references/rules/`.
