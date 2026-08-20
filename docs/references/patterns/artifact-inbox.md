# Artifact Inbox

작업 중 생성되는 report, research, review, handoff, draft 같은 **임시·비정본 artifact**를 canonical surface와 분리해 두는 패턴입니다.

## Layout

```text
inbox/
└─ ...

<scope>/
└─ inbox/
   └─ ...
```

- root `inbox/` — project-wide 또는 명확한 local owner가 없는 artifact
- `**/inbox/*` — 특정 directory, domain, asset 등 가까운 scope에 속한 artifact

소유 범위가 분명하면 가장 가까운 nested inbox를 우선하고, 여러 scope를 가로지르면 root inbox를 사용합니다.

## Pattern

- Inbox는 작업 결과를 안전하게 임시 보관하고 사람·agent 사이에 전달하는 working surface입니다.
- Artifact는 검토·정제 후 필요하면 적절한 canonical owner로 승격합니다.
- 더 이상 가치가 없는 artifact는 삭제할 수 있습니다. 보존 자체가 목적이 아닙니다.
- 구조, 파일명, retention 방식은 project 필요에 맞게 정합니다. 불필요한 index나 hierarchy를 강제하지 않습니다.

## Boundary

- Inbox의 존재만으로 artifact가 canonical documentation, source, plan 또는 project state가 되지 않습니다.
- Inbox를 branch state, task tracker, runtime dependency 또는 영구 archive처럼 사용하지 않습니다.
- Durable knowledge는 inbox에 계속 쌓아두지 말고 실제 owner로 옮깁니다.
- Nested inbox는 상위 inbox와 같은 의미를 가지며, 차이는 **scope와 proximity**뿐입니다.
