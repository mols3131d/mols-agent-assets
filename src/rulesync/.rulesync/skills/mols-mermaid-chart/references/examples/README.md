# Mermaid Chart 예제

Mermaid 공식 Diagram Syntax의 **수치 chart 유형 6개를 모두 포함**한다. 각 문서는 기본 예제와 심화 문법 또는 데이터 무결성 지침을 제공한다.

| 유형 | 예제 | 선언 | 심화 범위 |
| --- | --- | --- | --- |
| XY Chart | [XY Chart](xy-chart.md) | `xychart` | bar, line, 이름 있는 series, data label |
| Pie Chart | [Pie Chart](pie-chart.md) | `pie` | showData, donut, 범례 위치, highlight |
| Quadrant Chart | [Quadrant Chart](quadrant-chart.md) | `quadrantChart` | 정규화된 2축 위치 지정 |
| Sankey | [Sankey](sankey.md) | `sankey` | 다단계 흐름, CSV label, layout 설정 |
| Radar | [Radar](radar.md) | `radar-beta` | 비교 가능한 다차원 profile |
| Treemap | [Treemap](treemap.md) | `treemap-beta` | 계층 구조와 값 formatting |

선택한 유형의 문서만 읽고 전체 예제 catalog를 한 번에 context에 넣지 않는다.

## 난이도 기준

- **Basic**은 선언과 핵심 문법을 최소 요소로 보여준다.
- **Intermediate**는 단일 option, label 또는 presentation 기능을 추가한다.
- **Advanced**는 실제 문제를 해결하도록 boundary, branching, multiple series/actors, metadata, annotation, feedback 또는 data-integrity constraint 중 최소 두 가지를 결합한다.
- Advanced가 단순히 줄 수만 늘어나지 않도록, 무엇을 더 잘 판단하게 하는지 설명한다.

## 예제 범위

- 각 유형은 최소 Basic 예제와 Advanced 예제를 가진다.
- 예제 값은 문법 설명용이며 실제 사용 시 source, unit, population, timestamp를 확인한다.
- `-beta` 유형은 renderer support를 확인하고 table 또는 portable chart fallback을 둔다.

## 버전별 지원 범위

| 기능 | 최소 버전 | 예제 |
| --- | ---: | --- |
| Sankey | 10.3.0 | [Sankey](sankey.md) |
| Radar | 11.6.0 | [Radar](radar.md) |
| XY data label outside bar | 11.14.0 | [XY Chart](xy-chart.md) |
| Sankey label and spacing config | 11.15.0 | [Sankey](sankey.md) |
| XY per-point line label | 11.16.0 | [XY Chart](xy-chart.md) |
| Pie donut, legend position and highlight | 11.16.0 | [Pie](pie-chart.md) |

최소 버전은 feature gate일 뿐 권장 pin이 아니다. 실제 사용에서는 대상 환경이 지원하는 최신 patched release를 우선한다.
