# Mermaid Diagram 예제

이 디렉터리는 Mermaid 공식 syntax 전체를 복제하는 catalog가 아니라, **`mols-mermaid-diagram`의 local design pattern을 보여주는 예제 모음**이다. 정확한 현재 syntax, type 지원 여부와 minimum version은 [Mermaid 공식 문서](https://mermaid.js.org/)와 실제 target renderer를 기준으로 확인한다.

예제에 없는 Mermaid type도 Skill의 구조적 책임에 해당하고 target이 지원하면 사용할 수 있다. 반대로 예제가 존재해도 target renderer가 지원하지 않으면 그대로 복사하지 않는다.

## 질문별 예제 찾기

| 중심 질문 | 예제 |
| --- | --- |
| 절차·분기·ownership | [Flowchart](flowchart.md), [Swimlanes](swimlanes.md) |
| message order | [Sequence Diagram](sequence-diagram.md), [ZenUML](zenuml.md) |
| lifecycle | [State Diagram](state-diagram.md) |
| domain model·schema | [Class Diagram](class-diagram.md), [ER Diagram](er-diagram.md) |
| architecture·boundary | [Architecture](architecture-diagram.md), [C4](c4-context.md), [Block Diagram](block-diagram.md) |
| chronology·planning·work | [Timeline](timeline.md), [Gantt](gantt.md), [Git Graph](git-graph.md), [Kanban](kanban.md) |
| hierarchy·experience·requirements | [Mindmap](mindmap.md), [TreeView](tree-view.md), [User Journey](user-journey.md), [Requirement Diagram](requirement-diagram.md) |
| specialized relationship·sensemaking | [Packet](packet-diagram.md), [Event Modeling](event-modeling.md), [Venn](venn.md), [Ishikawa](ishikawa.md), [Wardley](wardley.md), [Cynefin](cynefin.md) |

선택한 유형의 문서만 읽고 전체 예제 모음을 한 번에 context에 넣지 않는다.

## 예제의 역할

- **Basic**은 해당 notation의 핵심 구조를 최소 요소로 보여준다.
- **Intermediate**는 실제 판단에 도움이 되는 option, label 또는 presentation 기능을 추가한다.
- **Advanced/Improvement**는 boundary, branching, multiple actors, metadata, annotation, recovery path 또는 fidelity constraint처럼 실제 문제 해결에 필요한 요소를 결합한다.
- Advanced가 단순히 줄 수만 늘어나지 않도록, 무엇을 더 잘 판단하게 하는지 설명한다.
- 예제는 복사 시작점일 뿐이며 실제 문서의 domain, terminology, evidence와 target renderer에 맞게 다시 설계한다.

## Upstream 변화 다루기

- 이 index는 Mermaid의 전체 type 목록, support tier 또는 version matrix를 유지하지 않는다.
- 예제가 version-sensitive, beta, experimental 또는 external integration syntax를 사용하면 복사 전에 공식 문서와 target renderer에서 현재 지원을 확인한다.
- Mermaid에 새 type이 추가됐다는 이유만으로 local example을 자동으로 추가하지 않는다. 반복되는 local design 판단이나 fallback guidance가 있을 때만 예제를 추가한다.
- local example의 syntax가 upstream과 달라졌다면 현재 공식 문서에 맞게 고치거나, local value가 없다면 example을 줄이거나 제거한다.
