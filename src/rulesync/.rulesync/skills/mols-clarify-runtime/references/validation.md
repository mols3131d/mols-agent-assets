# Validation

Runtime clarification은 evidence를 의도적으로 바꿀 수 있지만 **observable behavior와 기존 caller/consumer contract는 보존**해야 한다. 가능하면 변경 전후에 같은 작은 executable scenario를 사용한다.

## Behavior Envelope

대상과 실제 관련된 surface만 확인한다.

| Surface | Preserve / Check |
| --- | --- |
| Return / result | 값, type, ordering, caller-visible semantics |
| Exceptions | type, trigger condition, causal chain; 의도한 context 보강만 허용 |
| State | mutation, persistence, idempotency, commit timing |
| Side effects | file, database, process, network action과 ordering |
| Gates | approval, validation, promotion acceptance/rejection 기준 |
| Artifacts / history | 생성물, lifecycle, retry/redrive와 native metadata semantics |
| Runtime evidence | 선택한 질문에 필요한 event/context/relation만 의도대로 변경됨 |

이해 가능성이 좋아졌다는 이유로 실행 순서, business decision, 실패 조건 또는 retry behavior를 바꾸지 않는다.

## Baseline Observation

Persistent evidence를 수정하기 전에 가능한 경우 [Observation](observation.md)에 따라 현재 behavior와 evidence를 먼저 본다.

Baseline은 최소한 다음을 구분할 수 있어야 한다.

- 어떤 executable scenario를 사용했는가
- relevant input/fixture/parameter/config는 무엇인가
- 실제 result/exception/outcome은 무엇인가
- 질문과 관련된 state delta, artifact, history 또는 path evidence가 무엇인가
- 현재 reconstruction이 정확히 어디서 끊기는가

현재 evidence만으로 질문이 충분히 풀리면 변경하지 않는다.

## Before And After

Persistent clarification을 적용했다면:

1. 변경 전 사용한 동일하거나 의미상 동등한 좁은 executable scenario를 다시 실행한다.
1. return, exception, state와 side effect가 의도치 않게 달라지지 않았는지 확인한다.
1. artifact/history/trace/log 같은 evidence가 선택한 owner에서 기대한 의미로 남는지 확인한다.
1. 변경 후 **남은 selected evidence만 보고** 복원 질문에 답한다.
1. 제거·이동한 evidence가 기존 consumer, audit/security 또는 framework contract를 깨지 않았는지 확인한다.
1. 질문에 필요하지 않은 field, event, relation 또는 duplication이 남아 있으면 제거한다.

기존 safeguard가 충분하면 clarification 검증만을 위해 넓은 test suite나 새로운 test infrastructure를 만들지 않는다.

## Reconstructability Gate

다음 질문에 답할 수 있어야 한다.

> **선택한 evidence만 보고 source code를 다시 추적하지 않아도 target, 실제 action/outcome, 필요한 reason·state delta·causal relation을 오해 없이 복원할 수 있는가?**

질문에 따라 필요한 subset만 본다.

- 어떤 path가 실제로 실행됐거나 실행되지 않았는가?
- 어떤 relevant input/context가 decision에 영향을 줬는가?
- 어떤 action과 outcome이 있었는가?
- 무엇이 바뀌거나 만들어졌는가?
- failure cause가 어느 boundary에서 발생했는가?
- retry/async라면 logical operation과 attempt를 구분할 수 있는가?

정답을 만들기 위해 다시 전체 source와 여러 unrelated log를 조합해야 한다면 clarification이 아직 충분하지 않을 수 있다.

## Validate Evidence Viability

Persistent reconstruction이 특정 evidence availability에 의존하면 필요한 범위에서 확인한다.

- selected success/failure/skip/retry path에서 실제로 생성되는가
- consumer가 필요한 시점에 접근할 수 있는가
- sampling, filtering, truncation, drop 또는 retention limitation이 있는가
- relation이 필요한데 timestamp나 우연한 naming에만 의존하지 않는가
- best-effort telemetry를 반드시 남아야 하는 audit/durable fact처럼 주장하지 않는가

제약을 제거할 필요가 항상 있는 것은 아니다. 다만 limitation이 reconstruction claim을 약화시키면 그 사실을 숨기지 않는다.

## Validate Meaning

로그 문자열이나 formatter 자체보다 의미를 검증한다.

- 필요한 evidence가 owning boundary에서 남는가?
- 중요한 target/action/outcome/reason이 안정적인 field나 native representation으로 구분되는가?
- failure path의 causal context가 보존되는가?
- skip, retry, fallback, why-not 같은 대상 경로를 필요한 경우 구분할 수 있는가?
- state delta와 output effect가 전체 raw dump 없이 충분히 보이는가?
- duplicate/noisy evidence를 줄였어도 복원 질문에 답할 수 있는가?
- 민감하거나 과도한 데이터가 추가되지 않았는가?

정확한 formatting이나 incidental wording을 contract로 고정하지 않는다. 기존 test나 외부 consumer가 이미 log/event/metadata contract를 명시한 경우에는 그 contract를 따른다.

## Coverage And Trace Limits

기존 coverage나 trace를 validation evidence로 사용할 때 그 범위를 넘겨 해석하지 않는다.

- coverage는 실행 여부나 branch transition을 확인할 수 있지만 decision reason이나 correctness를 자동으로 증명하지 않는다.
- trace는 instrumentation과 sampling 범위 안에서 observed path를 보여준다.
- timestamp proximity는 causal relation의 충분한 증거가 아니다.

## Validation Gaps

실행할 수 없으면 static inspection, caller/result 비교, exception chain, artifact/framework metadata 구조와 existing tests를 사용해 가능한 범위만 확인하고 한계를 명시한다.

실행하지 않은 test나 runtime observation을 수행했다고 표현하지 않는다. 검증 중 defect가 발견되면 runtime clarification 범위를 넘어 수정하지 않고 별도 review/debugging 대상으로 분리한다.
