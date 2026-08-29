# Mermaid Diagram 예제

이 디렉터리는 Mermaid 공식 syntax 전체를 복제하는 catalog가 아니라, **`mols-mermaid-diagram`의 local design pattern을 보여주는 예제 모음**이다. 정확한 현재 syntax와 type·feature 지원 여부는 [Mermaid 공식 문서](https://mermaid.js.org/)와 실제 target renderer를 기준으로 확인한다.

예제에 없는 Mermaid type도 Skill의 구조적 책임에 해당하고 target이 지원하면 사용할 수 있다. 반대로 예제가 존재해도 target renderer가 지원하지 않으면 그대로 복사하지 않는다.

## 질문별 예제 찾기

| 중심 질문 | 예제 |
| --- | --- |
| 절차·분기·ownership | [Flowchart](flowchart.md), [Swimlanes](swimlanes.md) |
| message order | [Sequence Diagram](sequence-diagram.md), [ZenUML](zenuml.md) |
| lifecycle | [State Diagram](state-diagram.md) |
| domain model·schema | [Class Diagram](class-diagram.md), [ER Diagram](er-diagram.md) |
| architecture·boundary | [Architecture](architecture-diagram.md), [C4](c4-diagrams.md), [Block Diagram](block-diagram.md) |
| chronology·planning·work | [Timeline](timeline.md), [Gantt](gantt.md), [Git Graph](git-graph.md), [Kanban](kanban.md) |
| hierarchy·experience·requirements | [Mindmap](mindmap.md), [TreeView](tree-view.md), [User Journey](user-journey.md), [Requirement Diagram](requirement-diagram.md) |
| specialized relationship·sensemaking | [Packet](packet-diagram.md), [Event Modeling](event-modeling.md), [Venn](venn.md), [Ishikawa](ishikawa.md), [Wardley](wardley.md), [Cynefin](cynefin.md) |

선택한 유형의 문서만 읽고 전체 예제 모음을 한 번에 context에 넣지 않는다.

## 예제의 역할

각 문서는 해당 notation에서 **모델이 틀리기 쉬운 local judgment와 최소 예제**를 중심으로 구성한다. `Basic`, `Intermediate`, `Advanced` 같은 단계형 heading은 필요할 때만 사용하며 모든 파일에 같은 구조를 강제하지 않는다.

- 최소 예제는 해당 notation의 핵심 구조와 semantic contract를 가장 적은 요소로 보여준다.
- 확장 예제는 option 수를 늘리는 대신 boundary, branching, multiple actors, metadata, annotation, recovery path 또는 fidelity constraint처럼 **새로운 판단이 필요한 경우**에만 추가한다.
- type-specific review section은 syntax validity와 별도로 확인해야 하는 semantic trap이나 renderer-sensitive acceptance를 정리한다.
- split, overview/detail 또는 zoom 예제는 정보를 생략하거나 재배치할 수 있지만 **원본에 없던 relationship, direction, order, participant, state, transition 또는 다른 domain fact를 추가하지 않는다.**
- 예제는 복사 시작점일 뿐이며 실제 문서의 domain, terminology, evidence와 target renderer에 맞게 다시 설계한다.

## Upstream 변화 다루기

- 이 index는 Mermaid의 전체 type 목록, support tier 또는 version matrix를 유지하지 않는다.
- 예제가 version-sensitive, beta, experimental 또는 external integration syntax를 사용하면 복사 전에 공식 문서와 target renderer에서 현재 지원을 확인한다.
- Mermaid에 새 type이 추가됐다는 이유만으로 local example을 자동으로 추가하지 않는다. 반복되는 local design 판단이나 fallback guidance가 있을 때만 예제를 추가한다.
- local example의 syntax가 upstream과 달라졌다면 현재 공식 문서에 맞게 고치거나, local value가 없다면 example을 줄이거나 제거한다.
