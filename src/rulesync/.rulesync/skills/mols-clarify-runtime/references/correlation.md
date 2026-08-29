# Correlation

여러 runtime evidence를 연결해야 할 때 단순히 identifier 하나를 추가하지 않는다. **무엇이 같은 logical operation이고, 무엇이 별도 attempt이며, 어떤 관계가 실제 causality를 나타내는지** 먼저 구분한다.

## Logical Operation And Attempt

Retry, fallback, redrive 또는 재실행이 있으면 logical operation과 개별 attempt를 혼합하지 않는다.

예:

```text
operation: upload dataset-A
attempt 1: timeout
attempt 2: unavailable
attempt 3: success
```

필요한 질문에 따라 다음 관계를 구분한다.

- 같은 사용자·caller intent를 나타내는 logical operation
- 그 operation을 수행한 개별 attempt
- retry를 발생시킨 prior outcome 또는 reason
- final outcome을 만든 attempt

모든 runtime에 `operation_id`나 `attempt_id` field를 새로 만들라는 뜻은 아니다. 이미 framework, result, task metadata, trace 또는 execution history가 제공하는 identity를 우선한다.

## Choose The Relationship

관계의 의미가 다르면 같은 correlation mechanism으로 뭉개지 않는다.

| Relation | Meaning |
| --- | --- |
| Parent / child | 하나의 operation 안에서 직접 포함되거나 호출된 하위 work |
| Same logical operation | retry·redrive처럼 같은 intent를 여러 execution attempt가 수행 |
| Trigger / caused-by | 이전 event나 outcome이 다음 work를 시작하게 함 |
| Link / related-to | 직접 parent-child는 아니지만 causal 또는 semantic relation이 있음 |
| Shared execution context | 여러 evidence가 같은 execution boundary에 속함 |

Runtime이 native parent, link, message, workflow 또는 task relation을 제공하면 그 의미를 보존한다. 편의를 위해 모든 관계를 parent-child로 바꾸지 않는다.

## Async, Batch And Fan-Out

비동기 queue, message, batch, fan-out/fan-in에서는 하나의 call stack이나 parent chain이 실제 relation을 충분히 표현하지 못할 수 있다.

다음을 확인한다.

- producer와 consumer가 어떤 work를 공유하는가?
- 하나의 input이 여러 child work를 만들었는가?
- 여러 input/result가 하나의 downstream work로 합쳐졌는가?
- batch 안의 개별 item 실패와 batch 전체 outcome을 구분해야 하는가?
- retry attempt가 원래 message/work identity와 어떻게 연결되는가?

필요한 relation만 남긴다. item마다 고유 identifier를 추가해서 high-cardinality evidence를 만드는 것을 기본값으로 삼지 않는다.

## Timestamp Is Not Causality

두 event의 timestamp가 가깝거나 순서대로 보인다는 이유만으로 causal relation을 단정하지 않는다.

가능하면 다음 순서로 신뢰한다.

1. runtime이 소유하는 explicit parent/link/trigger relation
1. stable logical-operation 또는 attempt relation
1. explicit sequence / execution history ordering
1. timestamp를 보조 evidence로 사용

Clock skew, buffering, async delivery와 observation time 차이 때문에 wall-clock ordering은 실제 causality와 다를 수 있다.

## Correlation Field

새 correlation field는 다음 조건을 모두 만족할 때만 고려한다.

- 선택한 reconstruction question에 evidence 연결이 실제로 필요하다.
- 기존 result, artifact, framework metadata, trace 또는 execution identity로는 관계가 충분하지 않다.
- field의 owner와 lifecycle이 명확하다.
- 값이 bounded하고 consumer가 실제로 접근할 수 있다.
- sensitive identity나 불필요한 high-cardinality payload를 노출하지 않는다.

같은 관계를 여러 identifier로 반복 표현하지 않는다.

## Trust Boundary

외부 request, message 또는 upstream system에서 전달된 correlation context는 **관계 후보**이지 identity, authentication, authorization 또는 integrity의 증명이 아니다.

- 외부에서 들어온 context가 forged, missing, duplicated 또는 replayed될 수 있음을 고려한다.
- secret이나 민감한 business data를 correlation context에 넣지 않는다.
- 보안·권한 판단은 해당 security/auth contract가 소유한다.
- trust boundary에서 context를 무시·재생성·sanitization하는 runtime convention이 있으면 그것을 따른다.

## Stop

Relation을 추가하지 않아도 기존 evidence만으로 selected execution, attempt와 cause를 구분할 수 있으면 아무것도 추가하지 않는다.
