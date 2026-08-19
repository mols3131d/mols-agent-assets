# Mermaid Diagram 예제

Mermaid 공식 syntax의 **비차트 유형 24개를 모두 포함**한다. 각 문서는 기본 예제와 심화 패턴 또는 compatibility guidance를 제공한다. 수치 chart 6개는 `mols-mermaid-chart` Skill에 둔다.

| 유형 | 예제 | 지원 상태 | 적합한 용도 |
| --- | --- | --- | --- |
| Flowchart | [Flowchart](flowchart.md) | Core | 프로세스, 분기, 의존성 |
| Swimlanes | [Swimlanes](swimlanes.md) | v11.16+ beta | 책임과 handoff |
| Sequence Diagram | [Sequence Diagram](sequence-diagram.md) | Core | 시간 순 메시지 |
| Class Diagram | [Class Diagram](class-diagram.md) | Core | 타입과 관계 |
| State Diagram | [State Diagram](state-diagram.md) | Core | 생명주기와 상태 전이 |
| ER Diagram | [ER Diagram](er-diagram.md) | Core | 스키마와 cardinality |
| User Journey | [User Journey](user-journey.md) | Extended | 경험 단계와 actor |
| Gantt | [Gantt](gantt.md) | Core | 기간과 의존성 |
| Requirement Diagram | [Requirement Diagram](requirement-diagram.md) | Extended | 요구사항 추적성 |
| Git Graph | [Git Graph](git-graph.md) | Extended | 브랜치 전략 |
| C4 | [C4](c4-context.md) | Experimental | 아키텍처 zoom level |
| Mindmap | [Mindmap](mindmap.md) | Core | 개념 계층 |
| Timeline | [Timeline](timeline.md) | Extended | 시간 순 사건 |
| ZenUML | [ZenUML](zenuml.md) | External/experimental; 전용 source fence + fallback | 코드형 상호작용 |
| Block Diagram | [Block Diagram](block-diagram.md) | Extended | 수동 grid layout |
| Packet | [Packet](packet-diagram.md) | v11.0+ | bit field |
| Kanban | [Kanban](kanban.md) | Extended | 작업 상태 |
| Architecture | [Architecture](architecture-diagram.md) | v11.1+ beta | 서비스 topology |
| Event Modeling | [Event Modeling](event-modeling.md) | v11.15+ | command, event, read model |
| Venn | [Venn](venn.md) | v11.12.3+ beta | 집합 교차 관계 |
| Ishikawa | [Ishikawa](ishikawa.md) | v11.13+ beta | 원인 탐색 |
| Wardley | [Wardley](wardley.md) | v11.14+ beta | 가치 사슬과 evolution |
| Cynefin | [Cynefin](cynefin.md) | v11.16+ beta | 복잡성 domain |
| TreeView | [TreeView](tree-view.md) | v11.14+ beta | 디렉터리 계층 |

선택한 유형의 문서만 읽고 전체 예제 catalog를 한 번에 context에 넣지 않는다.

## 난이도 기준

- **Basic**은 선언과 핵심 문법을 최소 요소로 보여준다.
- **Intermediate**는 단일 option, label 또는 presentation 기능을 추가한다.
- **Advanced**는 실제 문제를 해결하도록 boundary, branching, multiple series/actors, metadata, annotation, feedback 또는 data-integrity constraint 중 최소 두 가지를 결합한다.
- Advanced가 단순히 줄 수만 늘어나지 않도록, 무엇을 더 잘 판단하게 하는지 설명한다.

## 예제 범위

- Mermaid 공식 Diagram Syntax navigation에 새 유형이 추가되면 index와 example file을 함께 갱신한다.
- 각 유형은 최소 **Basic** 예제 1개와 **Advanced/Improvement** 예제 또는 명시적 fallback을 가진다.
- `-beta`, external plugin, experimental 유형은 target renderer에서 실제 지원을 확인한다. External plugin source는 일반 `mermaid` fence로 감싸지 않고 portable fallback을 함께 둔다.
- 예제는 복사 시작점이며 실제 문서의 domain, terminology, evidence에 맞게 다시 설계한다.

## 버전별 지원 범위

| 기능 | 최소 버전 | 예제 |
| --- | ---: | --- |
| Architecture diagram | 11.1.0 | [Architecture](architecture-diagram.md) |
| Packet bit-count syntax | 11.7.0 | [Packet](packet-diagram.md) |
| Venn | 11.12.3 | [Venn](venn.md) |
| Ishikawa | 11.13.0 | [Ishikawa](ishikawa.md) |
| Wardley and TreeView | 11.14.0 | [Wardley](wardley.md), [TreeView](tree-view.md) |
| Event Modeling | 11.15.0 | [Event Modeling](event-modeling.md) |
| Flowchart datastore shape | 11.15.0 | [Flowchart](flowchart.md) |
| Class nested namespaces | 11.15.0 | [Class](class-diagram.md) |
| Sequence custom autonumber | 11.15.0 | [Sequence](sequence-diagram.md) |
| Swimlanes and Cynefin | 11.16.0 | [Swimlanes](swimlanes.md), [Cynefin](cynefin.md) |
| ER nullable attribute type | 11.16.0 | [ER](er-diagram.md) |

최소 버전은 feature gate일 뿐 권장 pin이 아니다. 실제 사용에서는 대상 환경이 지원하는 최신 patched release를 우선한다.
