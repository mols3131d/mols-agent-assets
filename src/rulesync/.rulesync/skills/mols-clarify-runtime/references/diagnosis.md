# Diagnosis

Runtime 문제를 모두 관찰하려 하지 않는다. **실행 후 답하기 어렵고 오해 비용이 큰 복원 질문 하나**를 먼저 고른다.

## Route Before Instrumenting

먼저 runtime understanding이 실제 병목인지 확인한다.

| Main question | Decision |
| --- | --- |
| 기존 code/test가 실제로 어떤 경로와 outcome으로 실행되는지 이해하기 어렵다 | 이 Skill 범위 |
| 실행 후 무엇이 일어났거나 왜 일어나지 않았는지 복원하기 어렵다 | 이 Skill 범위 |
| 코드를 읽어도 의미, 책임 또는 caller contract를 이해하기 어렵다 | 범위 밖: static code comprehension |
| 현재 동작이 올바른지, defect인지 판단해야 한다 | 범위 밖: code review 또는 debugging |
| 어떤 test나 validation으로 동작을 증명할지 설계해야 한다 | 범위 밖: testing responsibility |
| 실행 boundary나 책임 자체를 재설계해야 한다 | 범위 밖: architecture/design |
| 지속적인 상태 감시, alert, SLO 또는 aggregate health가 필요하다 | 범위 밖: monitoring/observability |
| 왜 느리거나 자원을 많이 쓰는지 찾아야 한다 | 범위 밖: profiling/performance |

주된 문제가 runtime understanding이 아니면 clarification 명목으로 logging, metadata, test 또는 telemetry를 추가하지 않는다.

## Reconstruction Question

| Question | Typical signal |
| --- | --- |
| 어떤 경로를 탔는가? | skip, retry, fallback 또는 조건부 실행 결과를 구분하기 어렵다. |
| 왜 그 경로를 탔는가? | 결과는 남지만 선택 근거가 사라진다. |
| 왜 기대한 경로를 타지 않았는가? | gate, rejection, skip 또는 unmet condition을 복원하기 어렵다. |
| 어떤 input/context가 결과에 영향을 줬는가? | 같은 code가 fixture, parameter, config 또는 runtime context에 따라 다르게 동작한다. |
| 어떤 상태가 바뀌었거나 그대로 남았는가? | mutation, commit, reconciliation 또는 no-op 전후를 복원하기 어렵다. |
| 무엇을 만들거나 영향을 줬는가? | output artifact, external action 또는 downstream effect가 code와 연결되지 않는다. |
| 무엇이 실패했는가? | exception은 있으나 대상, 단계 또는 causal context가 부족하다. |
| 어떤 operation·attempt와 연결되는가? | retry, async, batch 또는 분리된 event/result/artifact의 관계가 불명확하다. |

여러 질문이 보여도 가장 위험하거나 반복적으로 코드를 다시 추적하게 만드는 하나를 먼저 해결한다.

필요하면 질문을 다음 frame으로 좁힌다.

```text
Input / Context → Decision / Path → Action → Effect → Outcome
```

모든 단계를 채우는 template가 아니다. 선택한 질문에 필요한 관계만 복원한다.

## Debt Form

복원 질문을 어렵게 만드는 주된 형태를 하나 고른다.

| Form | Signal |
| --- | --- |
| Missing | 필요한 result, reason, failure context 또는 해당 execution path의 evidence가 남지 않는다. |
| Duplicate | 같은 사실이 여러 layer나 surface에서 반복된다. |
| Misowned | 사실을 가장 잘 아는 boundary와 evidence 위치가 다르다. |
| Noisy | routine detail이 많아 중요한 event나 state change를 찾기 어렵다. |
| Disconnected | 필요한 evidence는 있으나 operation, attempt 또는 causal relation을 복원하기 어렵다. |

`Missing`과 `Unavailable`을 기계적으로 별도 taxonomy로 늘리지 않는다. 의미상 evidence가 있어도 sampling, filtering, retention 또는 접근 제한 때문에 실제 reconstruction에 쓸 수 없다면 maintained evidence 선택 단계에서 viability 문제로 다룬다.

## Priority

오해했을 때 영향이 큰 순서로 본다.

1. destructive mutation, overwrite, recovery 같은 위험 작업
1. approval, validation, promotion 같은 gate와 why-not
1. 외부 process, framework, database, network 작업과 실패
1. retry, fallback, async handoff와 중요한 causal relation
1. 중요한 branch, state transition 또는 output effect
1. 일반적인 내부 진행 상황

로그가 적거나 많다는 사실 자체는 관찰 공백의 근거가 아니다.

## Observe Before Changing

질문을 고른 뒤 바로 maintained evidence를 추가하지 않는다. 가능한 경우 [Observation](observation.md)에 따라 가장 작은 기존 executable scenario와 native evidence로 실제 behavior를 먼저 확인한다.

기존 observation만으로 질문에 직접 답할 수 있고 future execution에 유지할 evidence 변경이 명시적으로 필요하지 않으면 수정하지 않는다. 한 execution에서 본 결과를 다른 input이나 environment의 일반 behavior로 확대하지 않는다.

관찰 중 defect나 correctness 의문이 생겨도 이 Skill 안에서 고치지 않고 해당 책임으로 넘긴다.