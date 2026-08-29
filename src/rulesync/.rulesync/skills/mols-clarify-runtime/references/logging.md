# Logging

Logging은 runtime clarification의 기본값이 아니다. **[Observation](observation.md)으로 기존 behavior와 native evidence를 먼저 확인하고, 다른 owner로는 사라지는 시간적 사건·decision·boundary outcome이 미래 reconstruction에 필요할 때만 사용한다.**

## Good Log

좋은 log event는 나중에 다음 질문 중 필요한 것에 빠르게 답하게 한다.

- **무슨 사건이 있었는가?**
- **무엇을 대상으로 했는가?**
- **어떤 action과 outcome이 있었는가?**
- **필요하다면 왜 그 결과가 났는가?**
- **어떤 operation·attempt와 연결되는가?**

그 질문에 답하지 않는 log는 추가하지 않는다.

## Event, Not Narration

의미가 생기는 사건을 기록한다.

```text
작업 완료
변경 승격 거부
target 상태 불일치
fallback 선택
```

코드 진행을 중계하지 않는다.

```text
파일 읽기를 시작합니다
다음 단계로 이동합니다
함수에 진입했습니다
```

함수 entry/exit, 모든 branch, loop iteration을 기계적으로 기록하지 않는다.

## Useful Boundaries

다음을 우선 검토한다.

- 외부 process, database, network 또는 framework 작업의 의미 있는 결과
- 중요한 mutation 또는 state transition
- approval, validation, reconciliation 같은 gate 결과와 why-not reason
- retry, fallback, skip 같은 의미 있는 path 선택
- 다른 result, exception, artifact, metadata, history 또는 trace로는 사라지는 결정 근거
- 상위 경계가 처리해야 하는 failure

단순 함수 호출이나 값 계산 자체는 event가 아니다.

## Action, Outcome And Reason

필요하면 다음 의미를 구분한다.

```text
action: promotion
outcome: rejected
reason: accuracy_guard_failed
```

이 조합은 mandatory schema가 아니다. 중요한 점은 event name/message에 동적 값을 섞기보다 **사건 종류와 runtime context의 의미를 안정적으로 분리**하는 것이다.

`reason`은 결과를 이해하는 데 실제로 필요할 때만 남긴다. 모든 condition이나 intermediate value를 설명하지 않는다.

## Message And Structured Context

Message나 event name은 **사건 종류**를 짧고 안정적으로 표현한다. 실행마다 달라지는 값은 runtime이나 project가 지원하는 structured context로 둔다.

```text
message: "promotion rejected"
context:
  target: model-v17
  outcome: rejected
  reason: accuracy_guard_failed
```

Structured logging은 단순히 JSON으로 출력한다는 뜻이 아니다. 반복되는 event와 field가 **안정적인 의미와 type을 가져 사람이 검색하고 Agent가 해석할 수 있는 구조**가 중요하다.

Context는 필요한 것만 고른다.

- stable operation, request, job 또는 artifact identifier
- target: resource, table, asset, partition, artifact
- outcome: status, action, reason, return code
- bounded measurement: count, duration
- 여러 evidence를 연결해야 할 때의 operation/attempt relation

민감도와 크기 기준은 [Evidence](evidence.md#data-safety)를 따른다.

## Native Span Or Event Surface

Runtime이 이미 trace/span/event를 제공한다면 새 log로 같은 사실을 복제하기 전에 그 surface가 질문을 더 자연스럽게 소유하는지 본다.

- start/end가 의미 있는 operation 전체 → existing span/operation evidence
- operation 전체의 성질이나 final attribute → existing result/metadata/span attribute
- 특정 시점의 의미 있는 occurrence → existing event 또는 log event
- 자유로운 진단 설명 → ordinary log가 더 적절할 수 있음

이 구분은 새 tracing framework를 도입하라는 뜻이 아니다. **이미 존재하는 native surface를 재사용할 때의 선택 기준**이다.

사용자가 logging을 구체적으로 요청했다면 [Evidence](evidence.md#explicit-surface-requests)의 surface 제약을 따른다. 기존 span/result가 상세 사실을 소유하더라도 요청을 조용히 다른 surface로 대체하지 않고, 필요한 최소 boundary event나 link만 logging에 projection한다.

## Level And Outcome

| Level | Typical meaning |
| --- | --- |
| `DEBUG` | 정상 실행에서 숨겨도 되는 내부 진단 정보 |
| `INFO` | 정상적인 주요 실행 경계 또는 의미 있는 완료 결과 |
| `WARNING` | 실행은 계속되지만 예상과 다른 상태, fallback, degraded path |
| `ERROR` | 요청한 operation이 실패했거나 필요한 결과를 제공할 수 없음 |
| `CRITICAL` | process/system 수준에서 계속 진행하기 어려운 실패; 드물게 사용 |

Runtime이 다른 level model을 사용하면 그 native semantics를 따른다. 어떤 level을 고르기 전에 event 자체가 필요한지 먼저 판단한다.

Exception이 발생했다는 이유만으로 항상 `ERROR`가 되는 것은 아니다. 예상된 rejection, handled retry, fallback, cancellation 또는 domain outcome이 operation의 정상 계약 안에서 처리됐다면 **최종 operation outcome과 runtime convention**을 기준으로 판단한다.

## Failure Ownership

같은 failure를 여러 layer에서 반복 logging하지 않는다.

- failure를 최종 처리하거나 operator-visible 의미로 바꾸는 boundary를 우선한다.
- 상위 layer가 새로운 의미를 추가할 때만 별도 event를 남긴다.
- traceback이나 상세 failure record는 원인 파악에 필요한 경계에서 한 번 충분히 남기는 것을 목표로 한다.
- existing trace/event가 같은 exception을 이미 충분히 소유하면 log에 동일 stack/context를 다시 복제하지 않는다.

## Noise Budget

로그도 이해 부채를 만든다. 다음 신호가 있으면 줄인다.

- 정상 실행마다 같은 의미의 event가 반복된다.
- 한 사건을 이해하려면 많은 line을 조합해야 한다.
- routine log가 중요한 warning/error를 가린다.
- 기존 result, artifact, metadata, history, trace 또는 exception과 같은 사실을 반복한다.
- dynamic field가 unbounded/high-cardinality인데 reconstruction 가치가 낮다.

새 event를 추가할 때 기존 event를 제거하거나 합칠 수 있는지도 본다. 전체 evidence 비용은 [Evidence](evidence.md#evidence-budget)를 따른다.

## Final Check

- 이 event는 어떤 복원 질문에 답하는가?
- existing observation이나 다른 owning surface로 이미 충분하지 않은가?
- 사건의 owner와 기록 위치가 맞는가?
- message/event type과 최소 context만으로 사건을 식별할 수 있는가?
- action/outcome/reason 중 실제로 필요한 의미가 구분되는가?
- 기존 evidence와 중복되지 않는가?
- 반복 실행에서 noise, cardinality와 데이터 크기가 감당 가능한가?

이 event를 제거해도 복원 질문에 답할 수 있다면 제거한다. 단, 사용자가 logging 자체를 유지하라고 명시했거나 별도 logging contract가 있으면 그 제약을 먼저 따른다.
