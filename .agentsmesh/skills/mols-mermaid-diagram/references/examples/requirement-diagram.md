# Requirement Diagram

requirement와 설계 element 사이의 **traceability**가 핵심이면 `requirementDiagram`을 사용한다.

> Bundled Mermaid version에 따라 `direction`과 styling 지원 범위가 다를 수 있다. 아래 예제는 optional direction을 생략하고, 다중 단어와 특수 문자가 포함된 user-defined value를 인용해 호환성을 높인다.

## Basic: Requirement Satisfaction

```mermaid
requirementDiagram
    requirement freshness_req {
        id: "FR-01"
        text: "Published data is less than 24 hours old"
        risk: high
        verifymethod: test
    }

    element freshness_check {
        type: "automated check"
        docRef: "tests/freshness"
    }

    freshness_check - satisfies -> freshness_req
```

## Advanced: Derivation, Refinement And Verification

```mermaid
requirementDiagram
    performanceRequirement latency_req {
        id: "PERF-01"
        text: "Validation finishes within 10 minutes"
        risk: medium
        verifymethod: demonstration
    }

    functionalRequirement batch_req {
        id: "FUNC-02"
        text: "Process records in bounded batches"
        risk: low
        verifymethod: test
    }

    designConstraint memory_limit {
        id: "DC-03"
        text: "Peak memory stays below the worker limit"
        risk: high
        verifymethod: analysis
    }

    element batch_runner {
        type: "service"
        docRef: "src/batch_runner"
    }

    element load_test {
        type: "test suite"
        docRef: "tests/load"
    }

    latency_req - derives -> batch_req
    batch_req - refines -> memory_limit
    batch_runner - satisfies -> batch_req
    load_test - verifies -> latency_req
    load_test - verifies -> memory_limit
```

## Optional Direction

Target renderer의 Mermaid version이 requirement direction을 지원할 때 declaration 다음에 추가한다.

```text
requirementDiagram
    direction LR
```

## Rules

- requirement ID와 text는 원문을 보존한다.
- user-defined value에 공백, 기호 또는 Mermaid keyword가 포함되면 큰따옴표로 감싼다.
- `contains`, `copies`, `derives`, `satisfies`, `verifies`, `refines`, `traces`를 의미에 맞게 구분한다.
- 일반 dependency만 필요하면 flowchart가 더 단순하다.
