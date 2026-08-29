# Wardley Map

> Mermaid v11.14.0+의 `wardley-beta` 문법이다. 좌표 순서는 `[visibility, evolution]`이다.

사용자 가치 chain과 component의 evolution, sourcing strategy를 함께 분석할 때 사용한다.

## Basic: Value Chain

```mermaid
wardley-beta
    title Data Product Value Chain

    anchor Analyst [0.95, 0.90]
    component Trusted Dataset [0.82, 0.72]
    component Transformation [0.62, 0.55]
    component Source Data [0.42, 0.80]
    component Compute [0.20, 0.92]

    Analyst -> Trusted Dataset
    Trusted Dataset -> Transformation
    Transformation -> Source Data
    Transformation -> Compute
```

## Advanced: Evolution And Sourcing Strategy

```mermaid
wardley-beta
    title Reliability Platform Strategy

    anchor Operator [0.94, 0.90]
    component Incident Console [0.82, 0.68] (build)
    component Detection Engine [0.68, 0.52] (build)
    component Metadata Catalog [0.55, 0.74] (buy)
    component Compute Platform [0.25, 0.94] (market)
    component Legacy Scheduler [0.48, 0.38] (inertia)

    Operator -> Incident Console
    Incident Console -> Detection Engine
    Detection Engine -> Metadata Catalog
    Detection Engine -> Compute Platform
    Detection Engine -> Legacy Scheduler

    evolve Detection Engine 0.70
    evolve Legacy Scheduler 0.62
    note "Replace bespoke scheduling dependency" [0.42, 0.48]
```

## Rules

- 좌표를 일반 `(x, y)`로 해석하지 않는다. 첫 값은 visibility, 두 번째 값은 evolution이다.
- position은 관찰과 전략 가정을 구분해 근거를 남긴다.
- `evolve`와 build/buy/outsource/market 같은 전략 표시는 실제 판단이나 scenario를 표현할 때만 사용한다.
- custom `size`는 target artifact가 명시적인 canvas를 요구할 때만 지정한다. Portrait viewport에 맞추기 위해 좌표 의미를 왜곡하거나 글자를 과도하게 축소하지 않는다.
- Wardley Map은 본질적으로 2차원 positioning을 사용하므로 semantic fidelity와 좌표 가독성이 portrait preference보다 우선한다.
- dependency만 보여주려는 경우보다 visibility와 evolution positioning 자체가 질문에 중요할 때 사용한다.
