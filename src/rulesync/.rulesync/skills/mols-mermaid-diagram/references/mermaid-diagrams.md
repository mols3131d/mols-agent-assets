# Mermaid Diagram Reference

Mermaid diagram은 **수치보다 관계·절차·책임·상태·시간 순서·구조가 핵심**일 때 사용한다. 수치 비교·추세·구성·양적 흐름이 핵심이면 `mols-mermaid-chart`를 사용한다.

## Authority

- 실제로 render 가능한 type, syntax와 feature는 **target renderer와 그 renderer가 사용하는 Mermaid version**이 결정한다.
- 현재 Mermaid syntax, configuration과 version별 feature semantics는 [Mermaid 공식 문서](https://mermaid.js.org/)를 기준으로 확인한다.
- 이 reference는 질문에 맞는 type 선택, semantic fidelity, portability, grouping과 splitting의 local policy만 소유한다.
- [Examples](examples/README.md)는 local pattern을 보여주는 출발점이며 완전한 syntax catalog나 version registry가 아니다.

공식 문서가 지원한다고 해도 target renderer가 더 오래된 Mermaid를 embed하면 그 기능을 사용할 수 없다. 반대로 local example에 없는 type이나 syntax도 target과 공식 문서가 지원하면 사용할 수 있다.

## Selection

1. 독자가 답해야 하는 질문을 한 문장으로 정의한다.
1. 중심 구조가 flow, ownership, message order, lifecycle, chronology, hierarchy, model, boundary 또는 specialized relationship 중 무엇인지 식별한다.
1. source가 실제로 말하는 relationship, direction, order와 boundary를 먼저 확정한다.
1. 그 구조를 가장 직접적으로 표현하는 type을 선택한다.
1. 사용자가 특정 type을 지정했어도 질문과 맞지 않거나 target이 지원하지 않으면 의미를 보존하는 더 적절한 type 또는 text/table fallback을 사용한다.
1. table이나 짧은 list가 더 명확하면 diagram을 사용하지 않는다.

## Type Families

아래 표는 선택 관점을 보여주는 대표 예시다. Mermaid type 전체 목록이나 지원 상태를 소유하지 않는다.

| 중심 구조 | 대표 type | 선택 기준 |
| --- | --- | --- |
| 절차·분기·dependency | Flowchart | 단계와 decision path가 핵심 |
| ownership·handoff | Swimlanes 또는 Flowchart | 책임 주체를 lane으로 분리할 가치가 있을 때 |
| message order | Sequence, ZenUML | 호출·message의 시간 순서가 핵심 |
| lifecycle | State | state와 transition이 핵심 |
| domain·schema | Class, ER | type 관계 또는 entity cardinality가 핵심 |
| architecture·boundary | Architecture, C4, Flowchart | system boundary와 dependency를 설명할 때 |
| chronology·planning | Timeline, Gantt, Git Graph | 사건 순서, 기간 또는 branch history가 핵심 |
| hierarchy | Mindmap, TreeView | 방향·수치보다 계층 구조가 핵심 |
| experience·work | Journey, Requirement, Kanban | 경험 단계, traceability 또는 work state가 핵심 |
| specialized relationship | Block, Packet, Venn, Ishikawa, Wardley, Cynefin, Event Modeling 등 | 해당 notation 자체가 질문을 더 직접적으로 설명할 때 |

특정 type의 현재 declaration과 상세 문법이 필요하면 local table을 확장하기보다 공식 문서와 target renderer를 확인한다.

## Compatibility

- portable documentation에서는 target이 확실히 지원하는 단순한 type과 syntax를 우선한다.
- beta, experimental, external integration 또는 최근 추가된 syntax는 실제 target renderer에서 확인한다.
- package의 설치 version, 공식 문서 version과 embedding product의 renderer version을 같은 것으로 가정하지 않는다.
- 지원 여부를 확인할 수 없고 portability가 중요하면 같은 의미를 표현하는 더 널리 지원되는 Mermaid type이나 text/table fallback을 사용한다.
- fallback은 시각적 모양보다 **relationship, order, boundary와 핵심 질문의 의미**를 보존해야 한다.

## Semantic Fidelity

Diagram의 edge, 위치와 notation은 사실 주장처럼 읽힐 수 있다.

- relationship와 dependency의 존재·방향을 source보다 강하게 만들지 않는다.
- chronology나 sequence가 확인되지 않았다면 source의 나열 순서를 실행 순서로 바꾸지 않는다.
- ER cardinality, state transition, ownership과 requirement relationship은 근거가 있을 때만 구체화한다.
- Ishikawa 같은 cause-oriented notation에서도 가설을 causal proof로 표현하지 않는다.
- readability를 위한 layout, ordering과 grouping은 허용하되 새로운 domain semantics를 만들지 않는다.
- 필요한 추론은 source fact와 구별되게 표시한다.

## Syntax Safety

공통 규칙을 모든 diagram grammar에 억지로 적용하지 않는다.

- declaration, relationship, block와 escaping은 **선택한 type의 현재 grammar**로 확인한다.
- 해당 grammar가 implicit participant, node 또는 state declaration을 허용하면 별도 선행 선언을 요구하지 않는다. 명시 선언은 alias, order, metadata 또는 readability에 실제 이점이 있을 때 사용한다.
- `end`, braces, indentation 또는 다른 block delimiter는 그 type이 요구하는 범위에서만 닫힘을 확인한다.
- punctuation, Markdown text와 Unicode는 해당 type의 quoting·escaping 규칙을 따른다.
- 다른 diagram type의 arrow, shape, frontmatter 또는 config syntax를 호환된다고 가정하지 않는다.
- 새로운·실험적 syntax가 중요하면 기억에 의존하지 않고 공식 문서와 target renderer에서 확인한다.
- setup failure와 syntax failure를 구분한다. 자세한 절차는 [Verification](mermaid-verification.md)을 따른다.

## Grouping And Splitting

- `subgraph` 또는 type-specific grouping은 stage, ownership, system boundary 또는 domain처럼 하나의 일관된 기준에 사용한다.
- boundary 사이의 handoff는 relationship으로 드러내고 깊은 중첩은 피한다.
- overview, detail, lifecycle과 ownership이 한 화면에 섞이거나 relationship 추적이 어려우면 overview + detail로 분리한다.
- overview와 detail의 용어, 방향, 상태 이름을 일치시킨다.
- grouping syntax 자체의 지원 여부는 선택한 type과 renderer에서 확인한다.

Styling이 필요하면 [Style Policy](style-policy.md)를 따른다.

## Output Modes

| Mode | Deliverable | Verification |
| --- | --- | --- |
| Inline Markdown | fenced `mermaid` block | source review + target compatibility 확인 |
| Source Artifact | `.mmd` file | source review + renderer validation when available |
| Rendered Artifact | `.mmd` + PNG/SVG/PDF | actual render + visual review |

## Examples

Local design pattern은 [Mermaid Diagram Examples](examples/README.md)에서 필요한 문서만 읽는다. 정확한 최신 syntax와 feature availability는 공식 Mermaid 문서와 target renderer를 다시 확인한다.
