# Agent Asset 소스 (`src/`)

`src/`는 배포 가능한 Agent Asset의 정본 소스 트리입니다.

`src/rulesync/`는 Rulesync로 표현하는 Rule, Skill, Agent를 위한 격리된 native workspace입니다. Rulesync에서는 repository Agent를 canonical `subagents/` feature로 표현합니다.

```text
src/rulesync/
├── rulesync.jsonc
└── .rulesync/
    ├── rules/
    ├── skills/
    └── subagents/
```

이 구조는 Rulesync의 native layout을 그대로 유지하면서도 저장소 루트의 `.rulesync/` 자동 탐색과 분리합니다. 따라서 저장한 배포 자산이 이 저장소 자체의 runtime configuration으로 자동 활성화되지 않습니다.

Read-only native command는 `src/rulesync/`에서 직접 실행합니다. `generate`처럼 파일을 쓰는 검증은 workspace 전체를 임시 디렉터리로 복사한 뒤 실행하며, 생성된 target projection과 Rulesync lock state는 정본 저장소 파일이 아닙니다.

Rulesync가 표현할 수 없는 실제 custom/non-standard format이 필요할 때만 `src/`에 형제 디렉터리를 추가합니다. `skills-chatbot`, `skills-chatbot-runtime` 같은 과거 분류 체계를 다시 만들지 않습니다.
