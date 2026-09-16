# Visualization

Tach dependency architecture를 시각화하거나 graph를 해석·설명할 때만 읽는다.

## Choose the Evidence Surface

먼저 무엇을 보여 주려는지 구분한다.

- **Local declared dependency edges** — module의 선언된 dependency 관계를 보려면 local `tach show`를 우선한다. 현재 Tach는 Graphviz DOT 또는 Mermaid output을 지원한다. Exact output semantics나 option이 판단에 중요하면 현재 Tach version의 authoritative source를 확인한다.
- **Observed file dependencies** — 실제 file-level dependency를 machine-readable data나 custom analysis에 쓰려면 `tach map`을 고려한다. Dependency/dependent direction이나 closure view가 필요할 때도 이 surface가 적합한지 먼저 본다.
- **Edge evidence** — 특정 module/file의 dependency나 usage가 왜 존재하는지 추적하려면 `tach report`로 import-level evidence를 확인한다.

이 세 surface를 같은 의미로 취급하지 않는다. Declared edge view와 observed dependency evidence가 다르면 `SKILL.md`의 Core Contract에 따라 mismatch를 판단한다.

## Scope the View

- 질문에 필요한 가장 작은 module/path 범위부터 본다. Repository 전체 graph는 overview 자체가 목적일 때만 우선한다.
- 큰 graph를 억지로 한 화면에 유지하기보다 material한 subgraph로 좁히고, 필요한 경우 상위 overview와 drill-down을 분리한다.
- Human-readable artifact에는 repository와 consumer가 지원하는 native local format을 우선한다. Custom transformation은 native output이나 structured data로 목적을 충족하지 못할 때만 추가한다.
- Remote viewer는 local output의 기본 대체재로 가정하지 않는다. 외부 전송, 현재 지원 상태와 repository policy가 material하면 사용 전에 확인하고, local output과 같은 evidence surface라고 가정하지 않는다.

## Interpret the Graph

- 결과가 **declared dependency view**인지 **observed dependency view**인지 명시한다. 둘을 결합하면 서로 다른 evidence임을 구분 가능한 방식으로 표현한다.
- Dependency arrow의 의미와 방향을 보존한다. Layout을 보기 좋게 바꾸기 위해 dependency direction을 뒤집지 않는다.
- Local `tach show`를 Tach architecture contract 전체의 완전한 시각화로 해석하지 않는다. 현재 local graph는 선언된 module dependency edge를 중심으로 하며 layer, interface, visibility 같은 별도 contract semantics를 모두 표현하지 않는다.
- `tach show` edge의 부재만으로 dependency가 금지되었거나 code에서 사용되지 않는다고 결론내리지 않는다. Layer rules처럼 명시적 `depends_on` 외의 permission이 있을 수 있다.
- Layer, public interface와 visibility는 graph layout이나 edge 존재만으로 추론하지 않는다. 해당 Tach configuration을 authority로 확인하고 필요한 observation과 함께 해석한다.

## Use Visualization as Evidence

- Visualization은 diagnosis, explanation과 review를 위한 inspection evidence다. `SKILL.md`의 Verification을 대체하지 않는다.
- Graph에서 발견한 suspicious edge나 missing relationship은 필요한 경우 `tach report`, code/config inspection 또는 repository-native validation으로 확인한 뒤 architecture 결론을 낸다.
- Derived diagram을 만들면 source surface, scope와 중요한 omission을 보존해 독자가 무엇을 보고 있는지 알 수 있게 한다.

## Boundary

이 reference는 Tach-specific visualization surface 선택과 architecture evidence 해석만 소유한다. Generic diagram design, rendering style, documentation layout과 visualization tooling methodology는 소유하지 않는다.
