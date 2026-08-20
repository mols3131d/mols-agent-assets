# Routing & Index Assets

탐색·선택·라우팅을 빠르게 하기 위해 **내용 자체와 분리된 discovery asset**을 두는 패턴입니다.

## Examples

```text
<dir>/
├─ INDEX.tsv
└─ ...

route/
├─ ROUTE.md
├─ skills.jsonl
├─ docs.md
└─ topic-*.tsv
```

포맷은 고정하지 않습니다. `md`, `jsonl`, `tsv`, `json`, `yaml` 등 목적에 맞는 형식을 사용합니다.

## Pattern

- `INDEX.*`는 디렉터리의 표면 파일·디렉터리와 필요하면 주요 내부 파일까지 요약합니다.
- `route/` 같은 전담 surface에 여러 위치를 연결하는 routing asset을 둘 수 있습니다.
- domain, topic, asset type 등 탐색 축별로 routing file을 나눌 수 있습니다.
- `ROUTE.md` 같은 entry asset은 필요한 routing/index file로 연결하는 최소 router 역할을 합니다.

## Boundary

- Routing/index asset은 **discovery와 navigation만 소유**하고 실제 내용·정책·runtime behavior의 canonical source가 되지 않습니다.
- 원본을 다시 설명하기보다 이름, 위치, 용도, 선택 기준처럼 탐색에 필요한 최소 정보만 둡니다.
- 원본에서 안정적으로 생성할 수 있는 index는 가능하면 generated/derived asset으로 관리합니다.
- stale route가 잘못된 source로 유도하지 않도록 원본 구조 변경과 함께 갱신하거나 검증합니다.
