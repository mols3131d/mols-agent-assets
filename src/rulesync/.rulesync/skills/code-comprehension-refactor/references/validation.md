# Validation

이 skill의 refactor는 comprehension을 개선하지만 **작동을 바꾸는 작업이 아니다.** 변경 전후의 behavior envelope와 task에 중요한 performance characteristic을 보존한다.

## Preservation Envelope

대상에서 실제로 관찰되거나 의존되는 surface만 확인한다.

| Surface | Check |
| --- | --- |
| API / registration | import path, call shape, framework entrypoint identity |
| Return | value, type, ordering, shape, sentinel 의미 |
| Exceptions | type, trigger condition, causal context |
| State | mutation, persistence, idempotency, lifecycle |
| Side effects | file/database/network write, overwrite/delete, 실행 순서 |
| Validation | acceptance/rejection 기준과 timing |
| Observability | log/event 의미와 failure visibility |
| Performance | hot-path latency, algorithmic complexity, allocation, I/O/query count 등 task에 material한 특성 |

모든 항목을 기계적으로 측정하지 않는다. target과 caller가 실제로 의존하는 surface를 먼저 식별한다.

## Before and After

가능하면 동일한 좁은 validation을 변경 전후에 적용한다.

1. 기존 test, characterization 또는 재현 가능한 입력으로 baseline을 확인한다.
1. comprehension refactor를 적용한다.
1. 같은 validation을 다시 실행한다.
1. output, exception, state, side effect, registration 차이가 없는지 확인한다.
1. type/lint/static check는 보조 evidence로 사용한다.
1. performance-sensitive code라면 repository에 이미 있는 benchmark, profiler evidence 또는 안정적인 비교 방법이 있을 때 before/after를 비교한다.

기존 safeguard가 충분하면 새 test나 benchmark를 만들지 않는다.

## Performance Boundary

이 skill은 performance optimization skill이 아니다.

- readability를 위해 algorithmic complexity를 악화시키지 않는다.
- I/O, query, allocation 또는 hot-loop work를 material하게 늘릴 수 있는 refactor는 동등성 근거 없이 적용하지 않는다.
- 기존 benchmark가 없다는 이유로 microbenchmark를 형식적으로 추가하지 않는다.
- performance 영향이 합리적으로 배제되지 않고 task에 중요하다면 더 안전한 intervention을 선택하거나 scope를 멈춘다.
- 측정하지 않은 performance equivalence를 측정했다고 표현하지 않는다.

정확한 CPU cycle 동등성을 요구하는 것은 아니다. repository와 task에서 의미 있는 성능 특성을 보존하는 것이 계약이다.

## Characterization and Gaps

중요한 behavior에 safeguard가 없고 다른 검증으로 refactor 위험을 줄일 수 없을 때만 작은 characterization test를 고려한다. 현재 observable contract만 고정하고 새 requirement나 implementation detail은 추가하지 않는다.

검증할 수 없으면 가능한 대체 evidence를 사용하고 한계를 명시한다: static/type check, deterministic I/O 비교, import/registration 확인, caller와 test oracle 대조, complexity reasoning.

대체 evidence를 실제 test나 benchmark 실행과 동등하게 표현하지 않는다.
