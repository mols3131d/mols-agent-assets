# Quadrant Chart

두 축의 positioning과 prioritization이 핵심이면 `quadrantChart`를 사용한다. 축의 의미와 좌표 기준이 불명확하면 사용하지 않는다.

```mermaid
quadrantChart
    title Remediation priorities
    x-axis Low effort --> High effort
    y-axis Low impact --> High impact
    quadrant-1 Strategic
    quadrant-2 Quick wins
    quadrant-3 Defer
    quadrant-4 Reconsider
    "Add freshness check": [0.25, 0.80]
    "Rewrite ingestion": [0.82, 0.72]
    "Tune report wording": [0.18, 0.28]
    "Add unused dashboard": [0.75, 0.20]
```

## Advanced: Decision Portfolio Across All Quadrants

Advanced example은 item 수만 늘리지 않고, 각 quadrant가 실제 action으로 이어지도록 구성한다. 좌표는 impact와 effort score를 0~1로 normalization한 값이며 status나 owner는 좌표에 섞지 않는다.

```mermaid
quadrantChart
    title Reliability investment portfolio
    x-axis Low effort --> High effort
    y-axis Low impact --> High impact
    quadrant-1 Fund and sequence
    quadrant-2 Execute now
    quadrant-3 Park or remove
    quadrant-4 Challenge the scope
    "Contract checks": [0.18, 0.88]
    "Freshness alerts": [0.28, 0.76]
    "Automated reconciliation": [0.46, 0.82]
    "Storage rewrite": [0.88, 0.84]
    "Lineage redesign": [0.74, 0.62]
    "Dashboard polish": [0.24, 0.26]
    "Unused export": [0.14, 0.12]
    "Custom rule engine": [0.82, 0.24]
```

이 예시는 four-quadrant coverage, action-oriented labels와 normalized scoring을 결합한다. 실제 실행 순서와 owner는 별도 table에서 관리한다.

## Improvement: Separate Priority From Status

개선된 Quadrant chart는 effort와 impact처럼 비교 가능한 두 축만 사용한다. 진행 상태, owner, deadline을 좌표에 숨기지 말고 별도 table이나 semantic marker로 제공한다.


## Intermediate: Explicit Coordinate Scale

Quadrant 좌표는 0~1 normalized 값이다. source score를 normalization한 경우 계산식을 문서에 남긴다.

```mermaid
quadrantChart
    title Data quality investments
    x-axis Low confidence --> High confidence
    y-axis Low impact --> High impact
    quadrant-1 Scale now
    quadrant-2 Investigate
    quadrant-3 Defer
    quadrant-4 Maintain
    "Contract tests": [0.88, 0.82]
    "Anomaly model": [0.42, 0.76]
    "Dashboard polish": [0.71, 0.24]
    "Unused export": [0.18, 0.15]
```
