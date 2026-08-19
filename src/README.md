# 배포 소스 (`src/`)

`src/`는 배포 가능한 configuration asset의 source tree입니다.

Rulesync가 표현할 수 있는 자산은 `src/rulesync/`의 격리된 native workspace에 둡니다.

```text
src/rulesync/
├── rulesync.jsonc
└── .rulesync/
    ├── rules/
    ├── skills/
    └── subagents/
```

Directory와 file shape는 current Rulesync를 따릅니다. Repository-local taxonomy나 변환 layer를 추가하지 않습니다.

이 workspace를 repository root와 분리하는 이유는 이 저장소가 보관한 distribution source를 자기 runtime configuration으로 자동 활성화하지 않기 위해서입니다.

Read-only Rulesync command는 `src/rulesync/`에서 직접 실행합니다. Generation처럼 파일을 쓰는 검증은 workspace 전체를 temporary directory로 복사한 뒤 수행하며 generated target projection과 Rulesync lock state는 source가 아닙니다.

Rulesync가 표현하지 못하는 semantics가 실제로 필요할 때만 `src/rulesync/`의 peer custom source를 추가합니다. 과거 chatbot/agent 또는 flat/runtime 분류를 filesystem taxonomy로 다시 만들지 않습니다.
