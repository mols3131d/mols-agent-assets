# Agent Asset 소스 (`src/`)

`src/`는 배포 가능한 Agent Asset의 canonical source tree입니다.

`src/agentsmesh/`는 AgentsMesh로 표현하는 Rule, Skill, Agent를 소유합니다.

```text
src/agentsmesh/
├── agentsmesh.yaml
├── agents/
├── rules/
└── skills/
```

경로를 `.agentsmesh/`가 아니라 `agentsmesh/`로 두는 것은 의도적입니다. 이 저장소는 자산 라이브러리이므로, 보관한 자산이 IDE나 harness의 conventional dot-directory discovery 때문에 이 저장소 자체의 runtime configuration으로 활성화되면 안 됩니다.

AgentsMesh native tooling이 필요하면 이 tree를 temporary workspace에 stage하여 `rules/`, `skills/`, `agents/`를 `.agentsmesh/{rules,skills,agents}`로 만들고 `agentsmesh.yaml`을 workspace root에 둡니다. 생성된 target projection은 temporary artifact이며 canonical repository file이 아닙니다.

AgentsMesh가 표현할 수 없는 실제 custom/non-standard format이 필요할 때만 `src/`에 peer directory를 추가합니다. `skills-chatbot`, `skills-chatbot-runtime` 같은 과거 taxonomy를 다시 만들지 않습니다.
