# Custom Agent Assets (`src/`)

`src/` is reserved for repository-local **custom or non-standard Agent Assets** that intentionally remain outside the current AgentsMesh contract.

Normal Rules, Skills, and Agents belong in `.agentsmesh/` whenever AgentsMesh can represent them. Repository tooling belongs in root `scripts/`.

There is currently no required custom Agent Asset under `src/`. Create a subdirectory only when a real target or format requirement cannot be represented by the current AgentsMesh contract.

Do not recreate `src/skills/`, `src/skills-chatbot/`, `src/skills-chatbot-runtime/`, `src/agents/`, `src/prompts/`, or a parallel Skill-routing Rule surface. A Skill that can use the normal `<name>/SKILL.md` package belongs in `.agentsmesh/skills/`, whether it is single-file or bundled.

The peer Agent Asset types remain **Rule, Skill, Prompt, and Agent**. Supporting resources and repository tooling are not peer asset types.
