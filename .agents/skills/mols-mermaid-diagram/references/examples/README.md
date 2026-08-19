# Mermaid Diagram Examples

Mermaid 공식 syntax의 **비차트 타입 24개를 모두 포함**한다. 각 문서는 기본 예제와 심화 패턴 또는 compatibility guidance를 제공한다. 수치 chart 6개는 `mols-mermaid-chart` skill에 둔다.

| Type | Example | Support | Best for |
| --- | --- | --- | --- |
| Flowchart | [Flowchart](./flowchart.md) | Core | process, branching, dependencies |
| Swimlanes | [Swimlanes](./swimlanes.md) | v11.16+ beta | ownership and handoffs |
| Sequence Diagram | [Sequence Diagram](./sequence-diagram.md) | Core | messages over time |
| Class Diagram | [Class Diagram](./class-diagram.md) | Core | types and relationships |
| State Diagram | [State Diagram](./state-diagram.md) | Core | lifecycle and transitions |
| ER Diagram | [ER Diagram](./er-diagram.md) | Core | schema and cardinality |
| User Journey | [User Journey](./user-journey.md) | Extended | experience steps and actors |
| Gantt | [Gantt](./gantt.md) | Core | duration and dependencies |
| Requirement Diagram | [Requirement Diagram](./requirement-diagram.md) | Extended | requirements traceability |
| Git Graph | [Git Graph](./git-graph.md) | Extended | branch strategy |
| C4 | [C4](./c4-context.md) | Experimental | architecture zoom levels |
| Mindmap | [Mindmap](./mindmap.md) | Core | concept hierarchy |
| Timeline | [Timeline](./timeline.md) | Extended | chronological events |
| ZenUML | [ZenUML](./zenuml.md) | External/experimental; dedicated source fence + fallback | code-like interactions |
| Block Diagram | [Block Diagram](./block-diagram.md) | Extended | manual grid layout |
| Packet | [Packet](./packet-diagram.md) | v11.0+ | bit fields |
| Kanban | [Kanban](./kanban.md) | Extended | workflow status |
| Architecture | [Architecture](./architecture-diagram.md) | v11.1+ beta | service topology |
| Event Modeling | [Event Modeling](./event-modeling.md) | v11.15+ | commands, events, read models |
| Venn | [Venn](./venn.md) | v11.12.3+ beta | set intersections |
| Ishikawa | [Ishikawa](./ishikawa.md) | v11.13+ beta | cause exploration |
| Wardley | [Wardley](./wardley.md) | v11.14+ beta | value chain and evolution |
| Cynefin | [Cynefin](./cynefin.md) | v11.16+ beta | complexity domains |
| TreeView | [TreeView](./tree-view.md) | v11.14+ beta | directory hierarchy |

선택한 type의 문서만 읽고 전체 example catalog를 한 번에 context에 넣지 않는다.

## Difficulty Contract

- **Basic**은 declaration과 핵심 문법을 최소 entity로 보여준다.
- **Intermediate**는 단일 option, label 또는 presentation 기능을 추가한다.
- **Advanced**는 실제 문제를 해결하도록 boundary, branching, multiple series/actors, metadata, annotation, feedback 또는 data-integrity constraint 중 최소 두 가지를 결합한다.
- Advanced가 단순히 줄 수만 늘어나지 않도록, 무엇을 더 잘 판단하게 하는지 설명한다.

## Coverage Policy

- Mermaid 공식 Diagram Syntax navigation에 새 type이 추가되면 index와 example file을 함께 갱신한다.
- 각 type은 최소 **Basic** 예제 1개와 **Advanced/Improvement** 예제 또는 명시적 fallback을 가진다.
- `-beta`, external plugin, experimental type은 target renderer에서 실제 지원을 확인한다. External plugin source는 일반 `mermaid` fence로 감싸지 않고 portable fallback을 함께 둔다.
- 예제는 복사 시작점이며 실제 문서의 domain, terminology, evidence에 맞게 다시 설계한다.

## Version-sensitive Coverage

| Feature | Minimum version | Example |
| --- | ---: | --- |
| Architecture diagram | 11.1.0 | [Architecture](./architecture-diagram.md) |
| Packet bit-count syntax | 11.7.0 | [Packet](./packet-diagram.md) |
| Venn | 11.12.3 | [Venn](./venn.md) |
| Ishikawa | 11.13.0 | [Ishikawa](./ishikawa.md) |
| Wardley and TreeView | 11.14.0 | [Wardley](./wardley.md), [TreeView](./tree-view.md) |
| Event Modeling | 11.15.0 | [Event Modeling](./event-modeling.md) |
| Flowchart datastore shape | 11.15.0 | [Flowchart](./flowchart.md) |
| Class nested namespaces | 11.15.0 | [Class](./class-diagram.md) |
| Sequence custom autonumber | 11.15.0 | [Sequence](./sequence-diagram.md) |
| Swimlanes and Cynefin | 11.16.0 | [Swimlanes](./swimlanes.md), [Cynefin](./cynefin.md) |
| ER nullable attribute type | 11.16.0 | [ER](./er-diagram.md) |

minimum version은 feature gate일 뿐 권장 pin이 아니다. 실제 사용에서는 target 환경이 지원하는 최신 patched release를 우선한다.
