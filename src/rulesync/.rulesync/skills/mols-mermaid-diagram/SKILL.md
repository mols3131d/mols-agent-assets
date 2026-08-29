---
name: mols-mermaid-diagram
description: "Use for Mermaid diagrams whose main job is to explain structure or relationships: procedures, branching, handoffs, message order, lifecycle, chronology, dependencies, boundaries, models, requirements, cardinality, or unweighted hierarchy. Also use when the user names a non-quantitative Mermaid diagram type. Do not use when numeric magnitude, trend, proportion, quantified flow, weighted hierarchy, profile, or normalized positioning is the main question; route those to mols-mermaid-chart. Route whole-dashboard design to mols-markdown-dashboard."
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
  - agentsskills
---

# Mermaid Diagram

## Purpose

Mermaid로 **관계·절차·책임·상태·시간·구조를 빠르고 쉽게 읽을 수 있는 diagram-as-code**를 생성하거나 개선한다.

## References

현재 Mermaid syntax, type·feature 지원 여부와 version semantics는 **실제 target renderer와 Mermaid 공식 문서**가 소유한다. 이 Skill의 reference와 example은 type 선택, 의미 보존, portability와 local design pattern을 보조하며 최신 Mermaid 문법 catalog의 정본이 아니다.

- 새 diagram을 만들거나 type·구조를 바꿀 때 [Mermaid Diagram Reference](references/mermaid-diagrams.md)를 읽는다.
- theme, 강조 또는 기존 diagram의 visual language를 다룰 때만 [Style Policy](references/style-policy.md)를 읽는다.
- 문법 예제가 필요하면 [Examples](references/examples/README.md)에서 선택한 type의 문서만 읽는다.
- render, export, syntax error, compatibility 또는 renderer trust boundary를 확인할 때 [Verification](references/mermaid-verification.md)을 읽는다.

## Workflow

1. 독자가 diagram으로 답해야 하는 질문을 한 문장으로 정의한다.
1. 중심 구조에 가장 직접적인 type을 고르고, portability나 최신 기능이 중요하면 target renderer 지원을 확인한다.
1. source가 뒷받침하는 핵심 entity, participant, state, boundary와 relationship만 먼저 작성한다.
1. 새 diagram 또는 구조 재설계는 width:height가 약 3:4인 portrait reading viewport에서 읽는 환경을 기본으로 한다. Vertical scroll은 허용하고, peer group을 하나의 긴 수평 흐름으로 이어 붙이기보다 group 단위로 세로로 쌓되 내부 flow direction은 정보 구조에 맞게 유지한다.
1. 하나의 diagram에는 하나의 핵심 질문만 두고, 복잡하면 overview와 detail로 분리한다.
1. inline Markdown, `.mmd` 또는 rendered artifact 중 필요한 output만 만든다.
1. 필요한 수준까지 검증하고 renderer 제약, fallback 또는 검증하지 못한 부분을 보고한다.

## Semantic Fidelity

- source에 없는 relationship, direction, order, ownership, cardinality, state, dependency 또는 causal claim을 사실처럼 추가하지 않는다.
- layout과 grouping은 readability를 위해 조정할 수 있지만 새로운 domain fact를 암시해서는 안 된다.
- 요청상 추론이 필요하면 diagram의 source fact와 구분되도록 label 또는 주변 설명에서 assumption·inference임을 드러낸다.
- 모호함을 보기 좋은 edge나 state로 메우지 않는다. 생략, 중립적 표현 또는 명시적 불확실성을 우선한다.

## Editing Rules

- 기존 diagram은 요청 범위만 수정하고 direction, grouping, naming, theme과 visual language를 불필요하게 바꾸지 않는다.
- 정보 구조에 맞는 type을 사용하고 익숙하다는 이유로 모든 내용을 flowchart로 만들지 않는다.
- 의미 없는 node, edge, subgraph와 style을 추가하지 않는다.
- 관계를 색상만으로 표현하지 않고 label, shape, position 또는 line style을 함께 사용한다.
- 복잡도를 style로 덮지 말고 diagram을 분리하거나 더 단순한 표현으로 전환한다.
