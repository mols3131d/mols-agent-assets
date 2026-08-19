# 커스텀 Agent Asset (`src/`)

`src/`는 현재 AgentsMesh contract 밖에 의도적으로 남기는 repository-local **커스텀 또는 비표준 Agent Asset**만 둡니다.

AgentsMesh가 표현할 수 있는 일반 Rule, Skill, Agent는 `.agentsmesh/`에 둡니다. 저장소 도구는 root `scripts/`에 둡니다.

현재 `src/` 아래에 반드시 유지해야 하는 커스텀 Agent Asset은 없습니다. 실제 target 또는 format 요구를 현재 AgentsMesh contract로 표현할 수 없을 때만 하위 디렉터리를 만듭니다.

`src/skills/`, `src/skills-chatbot/`, `src/skills-chatbot-runtime/`, `src/agents/`, `src/prompts/` 또는 별도의 Skill-routing Rule surface를 parallel source로 다시 만들지 않습니다. 일반 `<name>/SKILL.md` package로 표현할 수 있는 Skill은 single-file이든 bundled이든 `.agentsmesh/skills/`에 둡니다.

Rule, Skill, Prompt, Agent가 peer Agent Asset type이며 supporting resource와 repository tooling은 peer asset type이 아닙니다.
