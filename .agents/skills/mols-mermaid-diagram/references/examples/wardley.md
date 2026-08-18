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
    size [1100, 700]

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

- 좌표를 일반 `(x, y)`로 해석하지 않는다.
- position은 관찰과 전략 가정을 구분해 근거를 남긴다.
- dependency만 필요하면 architecture/C4가 더 단순하다.
