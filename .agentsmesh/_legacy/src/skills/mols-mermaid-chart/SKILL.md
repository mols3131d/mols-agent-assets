---
name: mols-mermaid-chart
description: "Use for Mermaid bar, line, XY, pie, Sankey, treemap, radar, or quadrant requests when the reader must compare numeric categories, inspect an ordered or time-based trend, explain part-to-whole composition, trace quantified flow, compare weighted hierarchy, evaluate same-scale profiles, or position items on normalized axes. Preserve source values, units, order, population, and time basis. Do not use for procedures, handoffs, states, architecture, schema, unweighted hierarchy, or event order; route those to mols-mermaid-diagram. Route whole-dashboard design to mols-markdown-dashboard."
---

# Mermaid Chart

## Purpose

Mermaid로 **수치 구조를 빠르고 쉽게 읽을 수 있는 chart-as-code**를 생성하거나 개선한다.

Category 비교, 시간 추세, 구성비, 양적 이동, 계층 규모, multidimensional profile과 two-axis positioning에 사용한다. Histogram, box plot, scatter처럼 Mermaid가 직접 지원하지 않는 chart는 table이나 전문 chart 도구로 보낸다.

## Activation

다음 조건 중 하나가 핵심이면 이 Skill을 사용한다.

- category 간 **값의 크기나 순위**를 비교한다.
- 시간 또는 정렬된 순서에 따른 **수치 변화**를 본다.
- 하나의 전체에 대한 **구성비**를 설명한다.
- source에서 target으로 이동하는 **양**을 추적한다.
- hierarchy의 구조가 아니라 **노드별 규모**를 비교한다.
- 같은 scale의 dimension으로 여러 대상을 비교하거나 두 normalized axis에 배치한다.

다음은 다른 Skill로 보낸다.

| 중심 질문 | Route |
| --- | --- |
| 사건이 어떤 순서로 일어나는가? | `mols-mermaid-diagram` |
| metric이 시간에 따라 어떻게 변하는가? | `mols-mermaid-chart` |
| 연결 구조나 ownership은 무엇인가? | `mols-mermaid-diagram` |
| 각 연결을 통해 얼마가 이동하는가? | `mols-mermaid-chart` |
| dashboard 전체를 어떻게 구성하는가? | `mols-markdown-dashboard` |
| histogram, scatter, box plot, multi-axis가 필요한가? | 전문 chart 도구 |

## Reference Routing

- 새 chart를 만들거나 type·구조를 바꿀 때 [Mermaid Chart Reference](references/mermaid-charts.md)를 읽는다.
- theme, palette, 강조 또는 기존 chart의 visual language를 다룰 때만 [Style Policy](references/style-policy.md)를 읽는다.
- 문법이 필요하면 [Examples](references/examples/README.md)에서 선택한 type의 문서만 읽는다.
- render, export, syntax error 또는 compatibility 확인이 필요할 때 [Verification](references/mermaid-chart-verification.md)을 읽는다.
- 수치보다 관계·절차·상태·component 구조가 핵심이면 `mols-mermaid-diagram`을 사용한다.

## Workflow

1. 독자가 chart로 답해야 하는 **수치 질문**을 한 문장으로 정의한다.
1. source, 단위, 기준 시점, 모집단, 순서와 누락값을 확인한다.
1. 질문에 가장 직접적인 chart type과 target renderer 지원 여부를 확인한다.
1. 값·sign·scale·order를 보존하고 축, label, series를 최소한으로 설계한다.
1. 정확한 값이 중요하면 source table을 함께 제공한다.
1. inline Markdown, `.mmd` 또는 rendered artifact 중 필요한 output만 만든다.
1. 필요한 수준까지 검증하고 data caveat와 renderer 제약을 보고한다.

## Editing Rules

- 기존 chart는 요청 범위만 수정하고 theme, series order, label convention과 visual language를 불필요하게 바꾸지 않는다.
- 원문에 없는 값·순위·추세·상관관계를 만들지 않는다.
- 하나의 chart에는 하나의 핵심 수치 질문만 둔다.
- 같은 정보를 chart와 table로 반복하지 않는다. 정확한 값 보존이 필요할 때만 table을 병기한다.
- 복잡도를 style로 덮지 말고 chart를 분리하거나 더 단순한 표현으로 전환한다.
