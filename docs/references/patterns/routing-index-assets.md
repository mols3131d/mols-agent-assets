# Routing & Index Assets

필요한 정보를 빠르게 찾고 **관련 context만 효율적으로 주입**하기 위해 내용 자체와 분리된 discovery / routing asset을 두는 패턴입니다.

Agent Skill이나 Rules뿐 아니라 문서, 코드, 설정, 연구자료 등 탐색 가능한 모든 information surface에 적용할 수 있습니다.

## Purpose

전체 source를 처음부터 읽지 않고도 어떤 정보가 어디에 있고 무엇을 읽어야 하는지 판단할 수 있게 하여 탐색 비용과 불필요한 context load를 줄입니다.

## Core

- Index asset은 정보의 위치와 종류를 빠르게 파악하게 합니다.
- Routing asset은 task, domain, topic 등 기준에 따라 다음에 읽을 source를 선택하도록 돕습니다.
- Routing/index layer는 underlying source를 대신하지 않고 **discovery, selection, navigation, context routing**에 집중합니다.
- 포맷이나 directory 구조보다 탐색 효율과 소비 주체에 맞는 표현을 우선합니다.

## Typical Options

```text
<dir>/
├─ INDEX.tsv
└─ ...

route/
├─ ROUTE.md
├─ docs.jsonl
├─ code.tsv
└─ topic-*.md
```

대표적인 선택지는 다음과 같습니다.

- `INDEX.*` — directory의 표면 file/directory를 정리하고 필요하면 주요 내부 파일도 포함
- `route/` — 여러 위치나 information domain을 연결하는 routing 전담 surface
- domain/topic/content type별 routing file
- `ROUTE.md` — 다른 routing/index asset으로 연결하는 최소 entry router
- `md`, `jsonl`, `tsv`, `json`, `yaml` 등 목적에 맞는 포맷

이 예시는 조합하거나 단순화할 수 있으며 특정 형식을 요구하지 않습니다.

## Automation

가능하면 routing/index 정보를 수동으로 중복 작성하기보다 이미 존재하는 metadata를 활용한 자동화를 권장합니다.

- Markdown frontmatter
- manifest
- directory metadata
- file metadata
- 기타 구조화된 source

안정적으로 추출 가능한 정보는 script나 generator로 `INDEX.*`와 routing asset을 생성·갱신할 수 있습니다. 사람이 직접 관리하는 정보는 자동으로 복원하기 어려운 routing intent나 선택 기준 같은 필요한 delta로 제한할 수 있습니다.

## Extensions

규모가 커지면 하나의 index에서 domain/topic별 router, 계층형 route, generated index 등으로 확장할 수 있습니다. 반대로 작은 repository에서는 단일 `INDEX.*`나 `ROUTE.md`만으로 충분할 수 있습니다.

## Considerations

- Routing asset이 stale하면 잘못된 source를 선택하게 할 수 있으므로 구조 변경과 함께 갱신하거나 검증하는 방법을 고려합니다.
- 사람이 읽는 탐색과 agent가 소비하는 context routing은 같은 source를 공유하거나 서로 다른 projection을 사용할 수 있습니다.
- 자동화 비용이 수동 관리보다 크면 단순한 수동 index가 더 적합할 수 있습니다.

## Boundary

Routing/index asset은 underlying 문서·코드·정책·동작의 canonical owner가 되지 않습니다. 다만 **routing 자체에 필요한 위치, 분류, 선택 기준, routing intent**는 이 layer가 소유할 수 있습니다.

이 패턴은 특정 schema, generator, 파일명 또는 routing algorithm을 강제하지 않습니다.
