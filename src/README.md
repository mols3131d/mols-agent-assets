# Source Workspace (`src/`)

`src/` contains only Agent Asset profiles **outside the current portable AgentsMesh contract**.

Portable coding-agent Rules and Skills live in `.agentsmesh/rules/` and `.agentsmesh/skills/`. Repository tooling lives in root `scripts/`.

| Directory | Role |
| --- | --- |
| `agents/` | Target-specific subagents/custom agents whose current semantics are not safely portable through the active AgentsMesh target set |
| `prompts/` | Explicit invocation prompts and hosted-service orchestration prompts |
| `skills-chatbot/` | Self-contained single-file hosted-chatbot Skills |
| `skills-chatbot-runtime/` | Bundled/runtime hosted-chatbot Skills |
| `rules/` | Hosted-chatbot-specific Rules outside AgentsMesh |

Do not recreate `src/skills/` as a second portable Skill source. `.agentsmesh/skills/` is authoritative for portable coding-agent Skills.

The peer Agent Asset types remain **Rule, Skill, Prompt, and Agent**. Supporting resources and repository tooling are not peer asset types.

The hosted-chatbot Skill profiles are repository-local deployment profiles, not categories defined by the Agent Skills specification. The same capability may have a portable AgentsMesh Skill and a hosted-chatbot projection when their target payloads genuinely differ.

For portable coding-agent Rule projection, use AgentsMesh. The repository-local chatbot fallback `CHATBOT.md → AGENTS.md → README.md` remains a separate hosted-chatbot convention documented under `docs/references/rules/`.
