# Routing & Index Assets

필요한 정보를 빠르게 찾고 **관련 context만 효율적으로 주입**하기 위해 내용 자체와 분리된 discovery / routing asset을 두는 패턴입니다.

Agent Skill이나 Rules뿐 아니라 문서, 코드, 설정, 연구자료 등 탐색 가능한 모든 information surface에 적용할 수 있습니다.

## Purpose

전체 source를 처음부터 읽지 않고도 어떤 정보가 어디에 있고 무엇을 읽어야 하는지 판단할 수 있게 하여 탐색 비용과 불필요한 context load를 줄입니다.

## Core

- Index asset은 정보의 위치와 종류를 빠르게 파악하게 합니다.
- Routing asset은 task, domain, topic 등 기준에 따라 다음에 읽을 source를 선택하도록 돕습니다.
- Routing/index layer는 underlying source를 대신하지 않고 **discovery, selection, navigation, context routing**에 집중합니다.
- 포맷, filename, directory 이름이나 배치보다 탐색 효율과 소비 주체에 맞는 표현을 우선합니다.

## Naming and Layout

Directory와 filename은 pattern의 고정 schema가 아닙니다. 아래 이름은 **권장 또는 예시**이며 repository 구조, consumer, runtime 또는 이미 존재하는 convention에 맞게 바꿀 수 있습니다.

| Form | Status | Typical use |
| --- | --- | --- |
| `route/` | recommendation | 별도 convention이 없을 때 shared 또는 repository-wide routing surface |
| `INDEX.*` | recommendation | 가까운 directory의 내용을 빠르게 훑기 위한 index |
| `ROUTE.md` | example | 사람이 읽기 쉬운 최소 entry router |
| `.agents/route/` | example | agent에만 필요한 routing을 별도 scope로 둘 때 |
| `.chatbot/route/` | example | chatbot에만 필요한 routing을 별도 scope로 둘 때 |

이 status는 이름 선택을 돕기 위한 설명이지 compliance level이 아닙니다. Framework, vendor 또는 repository가 더 적합한 native convention을 제공하면 그 이름과 위치를 사용할 수 있습니다.

작은 범위에서는 가까운 directory에 index 하나만 둘 수 있습니다.

```text
<dir>/
├─ INDEX.tsv
└─ ...
```

Repository 수준에서는 routing 전담 surface를 둘 수 있습니다.

```text
route/
├─ ROUTE.md
├─ docs.jsonl
├─ code.tsv
└─ topic-*.md
```

소비 주체별 routing이 실제로 다르면 scope를 드러내는 directory를 사용할 수도 있습니다.

```text
repository/
├─ route/             # shared or repository-wide routing
├─ .agents/
│  └─ route/          # agent-oriented routing
└─ .chatbot/
   └─ route/          # chatbot-oriented routing
```

`.agents/route/`와 `.chatbot/route/`는 vendor 표준이나 자동 discovery path를 의미하지 않습니다. 같은 패턴을 `routing/`, `index/`, vendor-native surface 또는 다른 project-local 이름으로 구현할 수 있습니다.

File format도 목적에 맞게 선택합니다. `md`, `jsonl`, `tsv`, `json`, `yaml` 등 사람이 읽는 navigation과 machine-readable discovery에 적합한 표현을 사용할 수 있습니다.

## Automation

가능하면 routing/index 정보를 수동으로 중복 작성하기보다 이미 존재하는 metadata를 활용한 자동화를 권장합니다.

- Markdown frontmatter
- manifest
- directory metadata
- file metadata
- 기타 구조화된 source

안정적으로 추출 가능한 정보는 script나 generator로 index와 routing asset을 생성·갱신할 수 있습니다. 사람이 직접 관리하는 정보는 자동으로 복원하기 어려운 routing intent나 선택 기준 같은 필요한 delta로 제한할 수 있습니다.

## Extensions

규모가 커지면 하나의 index에서 domain/topic별 router, 계층형 route, generated index 등으로 확장할 수 있습니다. 반대로 작은 repository에서는 단일 index나 router만으로 충분할 수 있습니다.

Shared routing과 consumer-specific routing을 함께 둘 때는 실제 선택 기준이 다른 경우에만 분리하는 편이 좋습니다. 같은 source와 같은 routing intent를 여러 directory에 반복하지 않습니다.

## Considerations

- Routing asset이 stale하면 잘못된 source를 선택하게 할 수 있으므로 구조 변경과 함께 갱신하거나 검증하는 방법을 고려합니다.
- 사람이 읽는 탐색과 agent가 소비하는 context routing은 같은 source를 공유하거나 서로 다른 projection을 사용할 수 있습니다.
- 자동화 비용이 수동 관리보다 크면 단순한 수동 index가 더 적합할 수 있습니다.
- Directory나 filename이 널리 쓰이는 형태라는 이유만으로 runtime이 자동 discovery한다고 가정하지 않습니다.

## Related Patterns

| Pattern | Relationship |
| --- | --- |
| [Nonstandard Directory Guide](nonstandard-directory-guide.md) | `route/` 같은 repository-local routing surface에 local guide가 필요할 때 참고합니다. |

## Boundary

Routing/index asset은 underlying 문서·코드·정책·동작의 canonical owner가 되지 않습니다. 다만 **routing 자체에 필요한 위치, 분류, 선택 기준, routing intent**는 이 layer가 소유할 수 있습니다.

이 패턴은 특정 schema, generator, directory, filename, format 또는 routing algorithm을 강제하지 않습니다. 예시 이름은 discovery intent를 설명하기 위한 representative form이며 실제 적용은 framework, runtime과 repository convention에 맞게 조정합니다.
