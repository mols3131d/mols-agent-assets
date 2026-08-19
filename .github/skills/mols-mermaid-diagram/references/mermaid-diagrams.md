# Mermaid Diagram Reference

Mermaid diagram은 **수치보다 관계·절차·책임·상태·시간 순서·구조가 핵심**일 때 사용한다. 수치 비교·추세·구성·양적 흐름이 핵심이면 `mols-mermaid-chart`를 사용한다.

## Selection

1. 독자가 답해야 하는 질문을 한 문장으로 정의한다.
1. 중심 구조가 flow, message, lifecycle, chronology, hierarchy, data relationship 또는 boundary 중 무엇인지 식별한다.
1. 그 구조를 가장 직접적으로 표현하는 type을 선택한다.
1. 익숙하다는 이유로 모든 내용을 flowchart로 만들지 않는다.
1. target renderer 지원이 불확실하면 core type 또는 text/table fallback을 사용한다.

## Compatibility

실제 target renderer와 embedded Mermaid version을 source of truth로 사용한다. Example의 minimum version은 feature gate일 뿐 dependency pin 권장이 아니다.

| Level | Types | Policy |
| --- | --- | --- |
| Core | flowchart, sequence, state, class, ER, Gantt, mindmap | portable documentation에서 우선 고려한다 |
| Extended | journey, requirement, gitGraph, timeline, block, packet, kanban | target renderer 지원을 확인한다 |
| New / Beta | swimlanes, architecture, event modeling, Venn, Ishikawa, Wardley, Cynefin, TreeView | 실제 render를 확인하고 fallback을 둔다 |
| Experimental / External | C4, ZenUML, animation, external icon packs | fallback 없이 문서 이해를 의존하지 않는다 |

## Type Catalog

| Type | Declaration | Best For | Avoid When |
| --- | --- | --- | --- |
| Flowchart | `flowchart TD/LR` | 단계, 분기, dependency, pipeline | ownership·message·lifecycle이 핵심일 때 |
| Swimlanes | `swimlane-beta LR` | responsibility와 cross-lane handoff | ownership이 중요하지 않을 때 |
| Sequence | `sequenceDiagram` | 호출·message의 시간 순서 | 정적 구조가 핵심일 때 |
| Class | `classDiagram` | type, member, inheritance, domain model | runtime interaction이 핵심일 때 |
| State | `stateDiagram-v2` | lifecycle, transition, guard | task 순서만 필요할 때 |
| ER | `erDiagram` | entity, key, cardinality, schema | 처리 흐름이 핵심일 때 |
| User Journey | `journey` | actor 경험 단계와 score | 정밀 수치 분석 또는 system call 흐름 |
| Gantt | `gantt` | 일정, 기간, milestone, dependency | 기간 없는 사건 순서 |
| Requirement | `requirementDiagram` | requirement-element traceability | 일반 dependency map |
| Git Graph | `gitGraph` | branch, merge, release strategy | 실제 history의 완전한 재현 |
| C4 | `C4Context` 등 | architecture zoom levels | renderer 지원이 불확실할 때 |
| Mindmap | `mindmap` | taxonomy, scope, concept hierarchy | 정확한 방향·순서·cardinality |
| Timeline | `timeline` | 사건·release·결정의 chronology | duration과 dependency가 중요할 때 |
| ZenUML | `zenuml` | code-like nested interaction | plugin 없는 portable Markdown |
| Block | `block` | author-controlled grid와 nested blocks | automatic layout이 더 적합할 때 |
| Packet | `packet` | network/binary bit fields | 일반 record schema |
| Kanban | `kanban` | workflow stage별 work snapshot | dependency·duration 계획 |
| Architecture | `architecture-beta` | service·group·resource topology | portable renderer가 우선일 때 |
| Event Modeling | `eventmodeling` | UI-command-event-read model timeline | 단순 event sequence |
| Venn | `venn-beta` | set intersections | hierarchy나 정확한 비율 |
| Ishikawa | `ishikawa-beta` | cause hypothesis decomposition | causal proof나 action plan |
| Wardley | `wardley-beta` | value chain, evolution, sourcing | component topology만 필요할 때 |
| Cynefin | `cynefin-beta` | complexity-domain sensemaking | 일반 priority matrix |
| TreeView | `treeView-beta` | directory-like hierarchy | arbitrary relationship graph |

Pie, Quadrant, Sankey, XY, Radar와 Treemap은 `mols-mermaid-chart`에서 다룬다.

## Diagram Rules

- 하나의 diagram에는 하나의 핵심 질문만 담는다.
- node ID는 짧고 안정적으로, label은 사람이 읽기 쉽게 작성한다.
- edge label에는 condition, message, ownership 또는 handoff 의미를 쓴다.
- 의미 없는 node, relationship, subgraph와 style은 추가하지 않는다.
- 색상만으로 의미를 전달하지 않는다.
- table이나 짧은 list가 더 명확하면 diagram을 사용하지 않는다.

## Syntax Safety

- 첫 줄의 declaration과 type별 block 종료를 확인한다.
- 공백, punctuation, braces 또는 Markdown 문자가 있는 label은 quote를 우선한다.
- participant, node, class와 subgraph reference는 사용 전에 선언한다.
- experimental syntax, animation과 icon pack은 renderer 지원을 확인한다.
- setup failure와 syntax failure를 구분한다. 자세한 절차는 [Verification](./mermaid-verification.md)을 따른다.

## Grouping And Splitting

- `subgraph`는 stage, ownership, system boundary 또는 domain 중 하나의 일관된 기준에 사용한다.
- boundary 사이의 handoff는 edge로 드러내고 깊은 중첩은 피한다.
- overview, detail, lifecycle과 ownership이 한 화면에 섞이거나 edge 추적이 어려우면 overview + detail로 분리한다.
- overview와 detail의 용어, 방향, 상태 이름을 일치시킨다.

Styling이 필요하면 [Style Policy](./style-policy.md)를 따른다.

## Output Modes

| Mode | Deliverable | Verification |
| --- | --- | --- |
| Inline Markdown | fenced `mermaid` block | source review + compatibility 확인 |
| Source Artifact | `.mmd` file | source review + renderer validation when available |
| Rendered Artifact | `.mmd` + PNG/SVG/PDF | actual render + visual review |

## Examples

Type별 문법과 패턴은 [Mermaid Diagram Examples](./examples/README.md)에서 필요한 문서만 읽는다.
