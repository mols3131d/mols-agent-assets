# Mermaid Diagram Reference

Mermaid diagram은 **관계·절차·책임·상태·시간 순서·구조**를 설명할 때 사용한다.

## Authority

- 실제로 render 가능한 type, syntax와 feature는 **target renderer와 그 renderer가 사용하는 Mermaid version**이 결정한다.
- 현재 Mermaid syntax, configuration과 version별 feature semantics는 [Mermaid 공식 문서](https://mermaid.js.org/)를 기준으로 확인한다.
- 이 reference는 질문에 맞는 type 선택, semantic fidelity, portability, viewport composition, grouping과 splitting의 local policy만 소유한다.
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

## Selection Boundaries

비슷해 보이는 표현 사이에서는 **무엇이 load-bearing information인지**로 선택한다. 아래 항목은 새로운 Mermaid type 이름이 아니라 선택 질문이다.

| Selection boundary | 첫 번째 표현이 적합한 경우 | 두 번째 표현이 적합한 경우 |
| --- | --- | --- |
| Hierarchy (`Mindmap`/`TreeView`) ↔ dependency-oriented `Flowchart` | single-parent, acyclic hierarchy 자체가 핵심 | shared dependency, multi-parent 또는 cycle이 핵심 |
| Logical topology (`Architecture`/`C4`/`Flowchart`) ↔ deployment placement | 무엇이 무엇과 연결되고 어떤 boundary가 있는지가 핵심 | 어디에 배치되고 zone·host·artifact·replica가 무엇인지가 핵심; target이 적절한 deployment 표현을 지원하지 않으면 text/table fallback을 검토 |
| Conceptual `ER` ↔ physical schema detail | entity와 cardinality가 핵심 | SQL type, constraint, index와 column-level contract가 핵심; 필요하면 schema/table 표현을 사용 |
| Process ownership (`Swimlanes`) ↔ ownership hierarchy (`Mindmap`/`TreeView`) | process 안에서 owner와 handoff가 핵심 | 정적인 reporting, coverage 또는 ownership 구조가 핵심 |
| `Kanban` ↔ process flow (`Flowchart`/`Swimlanes`) | 현재 work state의 snapshot이 핵심 | ordered transition, condition 또는 handoff가 핵심 |
| `Journey` ↔ process/chronology (`Flowchart`/`Timeline`) | human experience와 actor involvement가 핵심 | 절차 자체나 chronology가 핵심 |
| `Class` ↔ `ER` | inheritance, realization, composition, operation 같은 typed relation이 핵심 | entity, key와 cardinality가 핵심 |
| `Wardley` ↔ runtime architecture (`Architecture`/`C4`/`Flowchart`) | value chain과 evolution positioning이 핵심 | runtime topology와 dependency가 핵심 |
| `Timeline` ↔ `Gantt` | 사건의 chronology가 핵심 | duration, overlap과 dependency가 핵심 |

Selection boundary가 애매하면 더 많은 syntax를 넣기보다 독자가 답해야 할 질문을 다시 좁힌다.

## Readability Budgets

아래 수치는 **문법 validity limit가 아니라 분리 여부를 다시 검토하는 soft trigger**다. Target viewport, label 길이와 renderer가 더 중요하며 숫자 초과만으로 실패로 판정하지 않는다.

| Structure / type | Review trigger | 우선 검토 |
| --- | --- | --- |
| Flowchart | 한 decision에서 4개 이상 branch | decision 분해, rule table, detail split |
| Sequence | participant 약 5개 초과, message 약 12개 초과, fragment nesting 2단계 이상 | scenario별 split, happy/failure path 분리 |
| State | transition 수가 state 수의 약 2배를 크게 넘음 | lifecycle concern별 분리 |
| Hierarchy (`Mindmap`/`TreeView`) | depth 약 4 초과 또는 sibling breadth 약 5 초과 | subtree detail 분리 |
| Dependency-heavy Flowchart | node 약 9개 또는 edge 약 14개 초과 | subsystem detail, 반복 leaf aggregate |
| Gantt | task 약 12개 초과 | phase overview + sub-plan |
| Kanban | column 약 5개 또는 visible card 약 12개 초과 | backlog aggregate, board 분리 |
| Journey | stage 약 6개 초과 | journey phase 분리 |

표에 없는 type도 관계 추적, label 식별 또는 핵심 질문 유지가 어려워지는 순간 같은 원칙을 적용한다.

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

## Semantic Compression

복잡도를 줄일 때는 domain fact를 무작위로 삭제하지 않고 다음 순서로 검토한다.

1. 의미를 전달하지 않는 decoration과 중복 presentation을 먼저 제거한다.
1. exact duplicate는 **identity, responsibility, ownership, state, provenance, boundary와 relationship 중 독립 의미가 남지 않을 때만** 병합한다.
1. 개별 identity가 핵심이 아닌 반복 leaf group은 의미를 보존하는 aggregate로 축약하고, 무엇을 묶었는지 드러낸다.
1. 핵심 질문에 직접 기여하지 않는 cross-cutting detail은 note, table 또는 detail diagram으로 이동한다.
1. 그래도 관계 추적이 어렵다면 overview와 detail로 분리한다.

Layout상 가까워 보인다는 이유만으로 edge를 삭제하지 않는다. Mermaid position은 renderer-dependent하므로 relationship은 source에서 명시적으로 남겨야 한다.

## Editing Existing Mermaid

기존 source를 구조적으로 재작성할 때 semantic layer와 presentation layer를 분리해 본다.

- semantic layer에는 entity·participant·state, relationship, 실제 의미가 있는 direction/order, guard·fragment, cardinality, boundary와 quantitative label이 포함된다.
- theme, `classDef`, decorative style, declaration order와 layout hint는 domain fact로 자동 해석하지 않는다. 다만 사용자나 local convention이 보존을 요구하면 유지한다.
- source의 `LR`/`TB` 같은 direction을 chronology나 causality로 임의 해석하지 않는다.
- structural simplification이 해석에 영향을 줄 정도라면 결과와 함께 **merged / collapsed / omitted** 항목을 짧게 보고한다. 단순 label edit에는 이런 보고를 요구하지 않는다.
- 구조를 줄인 뒤에도 source에 없던 relationship, order, boundary 또는 state가 새로 생기지 않았는지 다시 확인한다.

## Syntax Safety

공통 규칙을 모든 diagram grammar에 억지로 적용하지 않는다.

- declaration, relationship, block와 escaping은 **선택한 type의 현재 grammar**로 확인한다.
- 해당 grammar가 implicit participant, node 또는 state declaration을 허용하면 별도 선행 선언을 요구하지 않는다. 명시 선언은 alias, order, metadata 또는 readability에 실제 이점이 있을 때 사용한다.
- `end`, braces, indentation 또는 다른 block delimiter는 그 type이 요구하는 범위에서만 닫힘을 확인한다.
- punctuation, Markdown text와 Unicode는 해당 type의 quoting·escaping 규칙을 따른다.
- 다른 diagram type의 arrow, shape, frontmatter 또는 config syntax를 호환된다고 가정하지 않는다.
- 새로운·실험적 syntax가 중요하면 기억에 의존하지 않고 공식 문서와 target renderer에서 확인한다.
- setup failure와 syntax failure를 구분한다. 자세한 절차는 [Verification](mermaid-verification.md)을 따른다.

## Viewport Composition

기본 reading surface는 **width:height가 약 3:4인 portrait viewport**로 가정한다. 이는 diagram 자체의 aspect ratio나 고정 pixel 크기 요구가 아니라 desktop과 mobile에서 폭을 과도하게 쓰지 않기 위한 composition 기준이다.

- 전체 diagram을 한 viewport 안에 축소해 넣을 필요는 없다. Vertical scroll은 정상적인 reading flow로 허용한다.
- 같은 수준의 stage, lane, domain 또는 반복 flow를 하나의 긴 수평 chain으로 이어 붙이기보다 **peer group 단위로 세로로 쌓는 구성을 우선한다.**
- group 내부의 자연스러운 direction은 유지한다. 폭을 줄이기 위해 모든 내부 flow를 `TB`로 평탄화하지 않는다.
- horizontal scroll이나 글자를 읽기 어려운 수준의 downscaling이 필요한 폭은 피한다. Renderer scaling을 composition 문제의 해결책으로 사용하지 않는다.
- viewport preference 때문에 source가 요구하는 specific node-level relationship, direction 또는 order를 group-level 관계로 바꾸지 않는다.
- 선택한 grammar나 layout engine이 원하는 상·하위 direction 조합을 안정적으로 유지하지 못하면 node나 label을 압축하기보다 overview/detail 또는 여러 diagram으로 분리한다.
- sequence participant, chronology, planning surface처럼 정보 구조상 넓은 canvas가 본질적인 경우에는 semantic fidelity와 readability가 portrait preference보다 우선한다.

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
