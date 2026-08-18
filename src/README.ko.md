# 과도기적 소스 예외 (`src/`)

`src/`는 **아직 `.agentsmesh/`로 이관되지 않았거나 현재 AgentsMesh contract로 의미를 충실히 표현하기 어려운 Agent Asset**을 보관합니다.

장기 canonical root가 아니라 과도기적 예외 surface입니다. 저장소 도구는 root `scripts/`에 둡니다.

| 디렉터리 | 현재 역할 |
| --- | --- |
| `agents/` | active AgentsMesh target set에서 의미를 안전하게 보존할 수 없는 target-specific subagent/custom agent |
| `prompts/` | explicit invocation prompt와 hosted-service orchestration prompt |
| `skills-chatbot/` | 현재 self-contained single-file hosted-chatbot Skill 예외 |
| `skills-chatbot-runtime/` | 현재 bundled/runtime hosted-chatbot Skill 예외 |
| `rules/` | 현재 AgentsMesh contract 밖의 hosted-chatbot-specific Rule |

`src/skills/`를 두 번째 portable Skill source로 다시 만들지 않습니다. 의미 손실 없이 표현 가능한 자산은 `.agentsmesh/`를 우선하고, 기존 `src/` profile은 영구 taxonomy가 아니라 migration candidate로 취급합니다.

Rule, Skill, Prompt, Agent가 peer Agent Asset type이며 supporting resource와 repository tooling은 peer asset type이 아닙니다.
