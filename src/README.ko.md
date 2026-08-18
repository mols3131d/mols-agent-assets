# 개발 워크스페이스 (`src/`)

`src/`는 이제 **현재 AgentsMesh portable contract 밖에 있는 profile과 tooling만** 보관합니다.

portable coding-agent Rule과 Skill의 canonical source는 각각 `.agentsmesh/rules/`, `.agentsmesh/skills/`로 이동했습니다.

| 디렉터리 | 역할 |
| --- | --- |
| `agents/` | active AgentsMesh target set에서 의미를 안전하게 보존할 수 없는 target-specific subagent/custom agent |
| `prompts/` | explicit invocation prompt와 hosted-service orchestration prompt |
| `skills-chatbot/` | self-contained single-file hosted-chatbot Skill |
| `skills-chatbot-runtime/` | bundled/runtime hosted-chatbot Skill |
| `rules/` | AgentsMesh 밖의 hosted-chatbot-specific Rule |
| `scripts/` | 개발 및 검증 도구 |

`src/skills/`를 두 번째 portable Skill source로 다시 만들지 않습니다. portable coding-agent Skill의 authority는 `.agentsmesh/skills/` 하나입니다.

hosted-chatbot Skill profile은 Agent Skills specification의 공식 분류가 아니라 repository-local deployment profile입니다. target payload가 실제로 다를 때 같은 capability가 portable AgentsMesh Skill과 hosted-chatbot projection으로 공존할 수 있습니다.
