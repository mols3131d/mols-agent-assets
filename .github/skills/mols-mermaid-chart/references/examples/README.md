# Mermaid Chart Examples

Mermaid 공식 Diagram Syntax의 **수치 chart 타입 6개를 모두 포함**한다. 각 문서는 기본 예제와 심화 문법 또는 data-integrity guidance를 제공한다.

| Type | Example | Declaration | Advanced coverage |
| --- | --- | --- | --- |
| XY Chart | [XY Chart](./xy-chart.md) | `xychart` | bar, line, named series, data labels |
| Pie Chart | [Pie Chart](./pie-chart.md) | `pie` | showData, donut, legend position, highlight |
| Quadrant Chart | [Quadrant Chart](./quadrant-chart.md) | `quadrantChart` | normalized two-axis positioning |
| Sankey | [Sankey](./sankey.md) | `sankey` | multi-stage flow, CSV labels, layout config |
| Radar | [Radar](./radar.md) | `radar-beta` | comparable multidimensional profiles |
| Treemap | [Treemap](./treemap.md) | `treemap-beta` | hierarchy and value formatting |

선택한 type의 문서만 읽고 전체 example catalog를 한 번에 context에 넣지 않는다.

## Difficulty Contract

- **Basic**은 declaration과 핵심 문법을 최소 entity로 보여준다.
- **Intermediate**는 단일 option, label 또는 presentation 기능을 추가한다.
- **Advanced**는 실제 문제를 해결하도록 boundary, branching, multiple series/actors, metadata, annotation, feedback 또는 data-integrity constraint 중 최소 두 가지를 결합한다.
- Advanced가 단순히 줄 수만 늘어나지 않도록, 무엇을 더 잘 판단하게 하는지 설명한다.

## Coverage Policy

- 각 type은 최소 Basic 예제와 Advanced 예제를 가진다.
- example value는 문법 설명용이며 실제 사용 시 source, unit, population, timestamp를 확인한다.
- `-beta` type은 renderer support를 확인하고 table 또는 portable chart fallback을 둔다.

## Version-sensitive Coverage

| Feature | Minimum version | Example |
| --- | ---: | --- |
| Sankey | 10.3.0 | [Sankey](./sankey.md) |
| Radar | 11.6.0 | [Radar](./radar.md) |
| XY data label outside bar | 11.14.0 | [XY Chart](./xy-chart.md) |
| Sankey label and spacing config | 11.15.0 | [Sankey](./sankey.md) |
| XY per-point line label | 11.16.0 | [XY Chart](./xy-chart.md) |
| Pie donut, legend position and highlight | 11.16.0 | [Pie](./pie-chart.md) |

minimum version은 feature gate일 뿐 권장 pin이 아니다. 실제 사용에서는 target 환경이 지원하는 최신 patched release를 우선한다.
