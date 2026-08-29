# Mermaid Chart Reference

Mermaid chart는 **수치가 있는 비교·추세·구성·이동량·계층 규모·profile·positioning**을 보여줄 때 사용한다.

## Selection

1. 독자가 답해야 하는 수치 질문을 한 문장으로 정의한다.
1. 핵심이 비교, 추세, 구성, 흐름, 계층, profile 또는 positioning 중 무엇인지 식별한다.
1. source, 단위, 기준 시점, 모집단, 순서와 누락값을 확인한다.
1. 가장 직접적인 type을 선택하고 target renderer의 지원 여부를 확인한다.
1. 지원이 불확실하거나 chart가 설명보다 복잡하면 table 또는 다른 chart 도구로 전환한다.

## Compatibility

실제 target renderer와 embedded Mermaid version을 source of truth로 사용한다. Example의 minimum version은 feature gate일 뿐 dependency pin 권장이 아니다.

| Level | Types | Policy |
| --- | --- | --- |
| Core | `pie`, `xychart` | 우선 고려하되 target renderer를 확인한다 |
| Version-sensitive | `quadrantChart`, `sankey` | 실제 render를 확인한다 |
| New / Beta | `radar-beta`, `treemap-beta` | fallback 없이 문서 이해를 의존하지 않는다 |

## Type Catalog

| Question | Type | Declaration | Avoid When |
| --- | --- | --- | --- |
| Category별 값을 비교하는가? | XY bar | `xychart` | category가 너무 많거나 label이 매우 길 때 |
| 시간 또는 순서에 따른 변화를 보는가? | XY line | `xychart` | 순서가 없는 category 비교 |
| 하나의 전체가 어떻게 구성되는가? | Pie | `pie` | 정확한 순위, 많은 slice, 시간 변화 |
| Source에서 target으로 얼마가 이동하는가? | Sankey | `sankey` | 값이 없거나 topology가 핵심일 때 |
| 계층별 크기와 구성은 어떠한가? | Treemap | `treemap-beta` | 음수 값, 깊은 계층, 정확한 순위 |
| 동일 dimension의 profile을 비교하는가? | Radar | `radar-beta` | dimension이 많거나 scale 방향이 다를 때 |
| 두 축에서 항목의 위치를 비교하는가? | Quadrant | `quadrantChart` | 축 정의나 좌표 근거가 불명확할 때 |

- Category가 많거나 정확한 비교가 중요하면 pie보다 bar를 우선한다.
- Ordered progression에는 line을 사용하고 순서 없는 category를 선으로 연결하지 않는다.
- 양적 이동이 아니라 연결 구조가 핵심이면 Sankey 대신 diagram을 사용한다.
- Histogram, box plot, scatter, density plot, multi-axis 또는 dense interactive chart는 전문 도구를 사용한다.

## Data Integrity

- 값, sign, 단위, category 순서, 기준 시점과 결측 상태를 보존한다.
- Pie는 같은 모집단과 기준 시점의 하나의 전체를 구성해야 한다.
- Sankey의 source, target, value와 의도한 보존 관계를 확인한다.
- Radar dimension은 같은 방향과 비교 가능한 scale을 사용한다.
- Quadrant 좌표는 근거 있는 normalized value만 사용한다.
- source에 없는 0, 평균, 목표값 또는 category를 추가하지 않는다.
- trend나 correlation을 causation으로 해석하지 않는다.

## Design

- title은 측정 대상과 질문을, axis는 quantity와 unit을 드러낸다.
- 서로 다른 단위나 scale을 하나의 chart에 억지로 겹치지 않는다.
- y-axis를 잘라 차이를 강조하면 그 사실을 명시한다.
- 색상만으로 series나 상태를 구분하지 않고 label 또는 legend를 함께 사용한다.
- category, series 또는 hierarchy가 과밀하면 chart를 나누거나 table로 전환한다.
- 하나의 chart에는 하나의 핵심 수치 질문만 둔다.

Styling이 필요하면 [Style Policy](style-policy.md)를 따른다.

## Output Modes

| Mode | Deliverable | Verification |
| --- | --- | --- |
| Inline Markdown | fenced `mermaid` block, 필요 시 source table | data·source review + compatibility 확인 |
| Source Artifact | `.mmd` file + source metadata | data·source review + renderer validation when available |
| Rendered Artifact | `.mmd` + PNG/SVG/PDF | actual render + visual and scale review |

## Examples

Type별 문법과 패턴은 [Mermaid Chart Examples](examples/README.md)에서 필요한 문서만 읽는다. Example value는 문법 설명용이며 실제 source로 취급하지 않는다.
