# 개발 워크스페이스 (`src/`)

`src/`는 AI 에이전트 자산의 source workspace입니다.

| 디렉터리 | 역할 |
| --- | --- |
| `agents/` | subagent 및 custom agent |
| `skills/` | workspace를 다루는 agent skill |
| `skills-chatbot/` | 4,000-token flat budget 안에서 한 파일로 완결되는 chatbot skill |
| `skills-chatbot-runtime/` | 큰 context 또는 bundled resource/runtime 기능이 필요한 chatbot skill |
| `rules/` | 재사용 가능한 행동 규칙 |
| `scripts/` | 개발 및 검증 도구 |

세 Skill 디렉터리는 **계층이 아니라 target profile**입니다. 같은 capability가 여러 profile에 존재할 수 있으며, 각 harness가 지원하는 규격과 기능을 최대한 활용하도록 서로 다른 형태로 최적화합니다. 따라서 profile 간 의미 중복은 독립 배포와 target-specific 최적화를 위한 의도적 중복일 수 있습니다.
