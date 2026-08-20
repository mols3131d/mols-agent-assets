# Routing & Index Assets

필요한 정보를 빠르게 찾고 **관련 context만 효율적으로 주입**하기 위해 내용 자체와 분리된 discovery asset을 두는 패턴입니다.

Agent Skill이나 Rules뿐 아니라 문서, 코드, 설정, 연구자료 등 탐색 가능한 모든 information surface에 적용할 수 있습니다.

## Examples

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

포맷은 고정하지 않습니다. `md`, `jsonl`, `tsv`, `json`, `yaml` 등 목적과 소비 주체에 맞는 형식을 사용합니다.

## Pattern

- `INDEX.*`는 디렉터리의 표면 파일·디렉터리와 필요하면 주요 내부 파일까지 요약합니다.
- `route/` 같은 전담 surface에 여러 위치와 information domain을 연결하는 routing asset을 둘 수 있습니다.
- domain, topic, artifact type 등 탐색 축별로 routing file을 나눌 수 있습니다.
- `ROUTE.md` 같은 entry asset은 필요한 routing/index file로 연결하는 최소 router 역할을 합니다.
- Router/index를 먼저 읽고 필요한 원본만 선택하도록 하여 불필요한 context load를 줄입니다.

## Boundary

- Routing/index asset은 **discovery, selection, navigation, context routing**만 소유하고 실제 내용·정책·동작의 canonical source가 되지 않습니다.
- 원본을 다시 설명하기보다 이름, 위치, 용도, 선택 기준처럼 탐색에 필요한 최소 정보만 둡니다.
- 원본에서 안정적으로 생성할 수 있는 index는 가능하면 generated/derived asset으로 관리합니다.
- stale route가 잘못된 source로 유도하지 않도록 원본 구조 변경과 함께 갱신하거나 검증합니다.
