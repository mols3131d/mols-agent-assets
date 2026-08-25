# Ishikawa Diagram

`ishikawa-beta`는 version-sensitive Mermaid syntax다. 정확한 현재 지원 범위와 declaration은 공식 Mermaid 문서와 target renderer에서 확인한다.

문제 결과와 잠재 원인을 category별로 탐색할 때 사용한다.

## Basic: Cause Categories

```mermaid
ishikawa-beta
    Late data publication
    Process
        Manual approval delay
        Missing retry policy
    Data
        Source arrived late
        Schema changed
    Platform
        Worker unavailable
        Queue saturated
```

## Advanced: Nested Cause Decomposition

```mermaid
ishikawa-beta
    Incorrect dashboard metric
    Source
        Duplicate records
        Missing records
    Transformation
        Join logic
            Wrong grain
            Non-unique key
        Aggregation
            Incorrect date boundary
            Nulls treated as zero
    Validation
        No reconciliation
        Threshold too broad
    Communication
        Metric definition changed
        Dashboard not refreshed
```

## Rules

- 원인과 해결책을 같은 branch에 섞지 않는다.
- 관찰된 evidence와 가설을 구분한다.
- causal proof가 아니라 investigation map임을 명확히 한다.
