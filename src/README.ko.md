# Agent Asset 소스 (`src/`)

`src/`는 배포 가능한 Agent Asset의 canonical source tree입니다.

`src/agentsmesh/`는 AgentsMesh로 표현하는 Rule, Skill, Agent를 위한 격리된 native workspace입니다.

```text
src/agentsmesh/
├── agentsmesh.yaml
└── .agentsmesh/
    ├── agents/
    ├── rules/
    └── skills/
```

이 구조는 AgentsMesh의 native layout을 그대로 유지하면서도 repository root의 `.agentsmesh/` discovery와 분리합니다. 따라서 저장한 distribution asset이 이 저장소 자체의 runtime configuration으로 자동 활성화되지 않습니다.

Read-only native command는 `src/agentsmesh/`에서 직접 실행합니다. `generate`처럼 파일을 쓰는 검증은 workspace 전체를 temporary directory로 복사한 뒤 실행하며, 생성된 target projection과 `.lock`은 canonical repository file이 아닙니다.

AgentsMesh가 표현할 수 없는 실제 custom/non-standard format이 필요할 때만 `src/`에 peer directory를 추가합니다. `skills-chatbot`, `skills-chatbot-runtime` 같은 과거 taxonomy를 다시 만들지 않습니다.
