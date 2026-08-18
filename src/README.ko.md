# Hosted Chatbot 호환 영역 (`src/`)

`src/`는 현재 AgentsMesh coding-target surface 밖의 hosted-chatbot Agent Asset만 둡니다.

portable coding-agent Rule, Skill, Agent는 `.agentsmesh/`에 둡니다. 저장소 도구는 root `scripts/`에 둡니다.

| 디렉터리 | 현재 역할 |
| --- | --- |
| `skills-chatbot/` | self-contained single-file hosted-chatbot Skill |
| `skills-chatbot-runtime/` | bundled/runtime hosted-chatbot Skill |
| `rules/` | 현재 AgentsMesh contract 밖의 hosted-chatbot-specific Rule |

`src/skills/`, `src/agents/`, `src/prompts/`를 parallel portable source로 다시 만들지 않습니다. active coding-agent contract가 소유할 수 있는 자산은 `.agentsmesh/`를 사용합니다.

Rule, Skill, Prompt, Agent가 peer Agent Asset type이며 supporting resource와 repository tooling은 peer asset type이 아닙니다.

repository-local chatbot fallback `CHATBOT.md → AGENTS.md → README.md`은 `docs/references/rules/`에 문서화된 별도 hosted-chatbot convention으로 유지합니다.
