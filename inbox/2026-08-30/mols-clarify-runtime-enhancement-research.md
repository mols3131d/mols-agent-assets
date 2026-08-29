# `mols-clarify-runtime` 고도화 조사

`mols-clarify-runtime`을 단순한 logging 개선 Skill이 아니라, **사람과 Agent가 실행 후 runtime 동작을 최소한의 신뢰 가능한 evidence로 복원하고 이해할 수 있게 하는 Skill**로 고도화하기 위한 조사 결과를 정리한다.

이 문서는 구현 계획이 아니라 Research artifact다. 현재 Skill의 강점과 공백, 외부 표준·연구에서 반복해서 확인되는 runtime 이해 정보, 흡수 가치가 높은 원칙과 범위 밖에 둘 내용을 구분한다.

## 결론

현재 Skill의 중심 계약은 유지하는 것이 좋다.

> 실행 후 답하기 어려운 가장 중요한 복원 질문 하나를 고르고, 기존 behavior와 contract를 보존하면서 그 질문에 답하는 가장 작은 runtime evidence 변경을 선택한다.

고도화의 핵심은 더 많은 log를 남기는 데 있지 않다. 현재 Skill이 강한 **복원 질문, evidence ownership, 중복·noise 제거, no-op stop condition** 위에 다음 세 축을 보강하는 것이 가장 가치가 크다.

1. **Evidence viability** — 의미상 올바른 evidence owner를 찾는 것과 그 evidence가 실제 failure path와 필요한 기간에 남아 있는지를 구분한다.
2. **Causality and decision** — 단순 execution ID나 timestamp보다 parent/link/trigger, logical operation/attempt, action/outcome/reason처럼 실행 관계와 결정 이유를 복원한다.
3. **Runtime provenance and completeness** — 결과를 materially 바꾼 input/config/version과 evidence의 missing/truncated/sampled 상태를 사실 자체와 구분한다.

사람과 Agent를 위한 evidence를 별도로 만들기보다는 **짧은 human-readable meaning + 안정적인 machine-readable semantics**를 같은 runtime evidence에 결합하는 방향이 가장 좋다.

## 현재 Skill에서 보존해야 할 강점

현재 `mols-clarify-runtime`은 이미 다음 설계가 좋다.

- logging이나 instrumentation 추가를 기본 해법으로 가정하지 않는다.
- 한 번에 **복원 질문 하나**를 해결한다.
- `Missing`, `Duplicate`, `Misowned`, `Noisy`, `Disconnected`로 runtime 이해 부채를 진단한다.
- result, exception, artifact/framework metadata, logging, 기존 trace/span 중 적절한 owner를 고른다.
- 기존 evidence를 재사용·보강·이동·병합·제거하는 것을 새 evidence 추가보다 먼저 고려한다.
- `clarify-code`, debugging/review, testing, monitoring/observability, profiling/performance와 책임을 분리한다.
- 기존 evidence만으로 질문에 답할 수 있으면 아무것도 변경하지 않는다.
- observable behavior와 기존 caller/consumer contract를 보존한다.
- 특정 logging library, telemetry stack, framework schema를 범용 contract로 고정하지 않는다.

따라서 고도화는 observability 교과서나 vendor-specific schema를 Skill에 복제하는 방식이 아니라, 현재 판단 모델에서 실제로 비어 있는 부분만 보강해야 한다.

## Runtime을 이해할 때 필요한 정보

여러 runtime tracing, workflow history, lineage/provenance, logging 표준과 debugging 연구를 비교하면 사람과 Agent가 반복해서 필요로 하는 정보는 다음 질문으로 정리된다.

| 복원 질문 | 필요한 정보 |
| --- | --- |
| 무엇이 실행됐는가? | operation, action 또는 event type |
| 어떤 실행인가? | run, execution, trace identity |
| 어디서 실행됐는가? | source, service/process, environment |
| 무엇을 대상으로 했는가? | subject, target, resource |
| 어떤 경로를 거쳤는가? | lifecycle/state, parent/link, sequence |
| 왜 이 경로를 탔는가? | decision, reason, decisive condition |
| 왜 다른 경로를 타지 않았는가? | gate, rejection, skip reason |
| 무엇을 사용했는가? | relevant input, parameter, effective configuration |
| 무엇이 바뀌었는가? | state transition, delta, mutation |
| 무엇을 만들었는가? | result, output, artifact, lineage |
| 성공했는가? | outcome/status |
| 실패했다면 무엇 때문인가? | error type/code, cause, causal chain |
| 재시도였는가? | logical operation과 attempt/retry 관계 |
| 언제·얼마나 걸렸는가? | occurrence time, sequence, duration |
| 어떤 코드·환경에서 실행됐는가? | code/service version, runtime, effective config |
| evidence를 믿어도 되는가? | producer, schema/version, sampled/truncated/missing 여부 |

이 표는 공통 schema가 아니다. 모든 event가 모든 field를 가져야 한다는 뜻도 아니다. **선택한 복원 질문에 필요한 최소 subset을 찾기 위한 사고 모델**이다.

## 질문 중심 evidence가 raw trace보다 중요하다

Whyline 연구는 개발자가 runtime을 이해할 때 반복해서 묻는 질문을 크게 두 종류로 설명한다.

- Why did this happen?
- Why didn't this happen?

즉 runtime clarification에서 단순히 “무엇이 발생했다”를 남기는 것만으로는 부족할 수 있다. 특히 approval, validation, retry, fallback, skip, rejection 같은 중요한 gate에서는 **왜 그 결과가 나왔는가**가 핵심 evidence가 된다.

이 관점에서 매우 강한 최소 semantic 조합은 다음과 같다.

```text
action
outcome
reason
```

예:

```text
action=promotion
target=model-v17
outcome=rejected
reason=accuracy_guard_failed
```

자유 텍스트를 길게 늘리는 것보다 사람이 빠르게 읽고 Agent가 안정적으로 검색·비교할 수 있다.

중요한 보강 후보는 현재 복원 질문에 **“왜 실행되지 않았는가?”**를 더 분명하게 포함하는 것이다. 다만 모든 branch predicate를 기록하지 않고 오해 비용이 큰 gate의 결정 이유에만 적용해야 한다.

## Semantic identity와 occurrence identity를 구분한다

여러 표준에서 반복해서 확인되는 설계는 실행의 종류와 개별 발생을 구분하는 것이다.

- OpenLineage: `Job`과 `Run`
- OpenTelemetry: 안정적인 operation/span name과 개별 trace/span ID
- CloudEvents: event `type`, `id`, `source`, `subject`

따라서 개념적으로 다음이 서로 다른 책임을 가진다.

```text
operation=import_dataset
execution_id=...
event_id=...
target=customers/2026-08-30
```

동적인 ID를 operation/event type 자체에 섞으면 사람이 검색하기 어렵고 Agent도 같은 종류의 실행을 집계·비교하기 어려워진다.

## Execution ID보다 causal relationship이 중요할 수 있다

분산·비동기 runtime에서는 같은 execution ID만으로 사건 관계를 충분히 설명할 수 없다.

다음 세 구조는 같은 ID 집합만 보면 구분되지 않는다.

```text
A -> B -> C
```

```text
A
├─ B
└─ C
```

```text
A -> B
A -> C
B + C -> D
```

OpenTelemetry의 parent/child/link와 messaging span relation, distributed tracing 연구가 공통적으로 보여주는 것은 runtime이 실제로 **causal graph**에 가깝다는 점이다.

따라서 async, message, batch, fan-out/fan-in, cross-process 경계를 가로지르는 복원 질문에서는 단순 correlation ID 외에 다음 관계가 필요할 수 있다.

```text
parent
caused_by
triggered_by
linked_to
```

구체적인 field 이름이나 tracing framework는 project/runtime가 소유한다. Skill은 **“같은 실행인가?”에서 끝내지 말고 필요하면 “어떤 관계인가?”까지 복원한다**는 판단만 소유하는 것이 적절하다.

## Logical operation과 attempt를 분리한다

Retry, fallback, redrive가 있는 runtime에서는 논리적인 작업 하나와 물리적인 실행 attempt가 다르다.

```text
operation=upload_dataset
  attempt=0 -> timeout
  attempt=1 -> 503
  attempt=2 -> success
```

이 구분이 없으면 다음 질문에 답하기 어렵다.

- 전체 operation은 성공했는가?
- 몇 번 시도했는가?
- 어떤 attempt가 실패했는가?
- retry를 유발한 원인은 무엇인가?

Argo Workflows와 AWS Step Functions 같은 workflow runtime도 execution history에서 attempt/status/error/duration 등을 별도로 표현한다.

따라서 retry가 복원 질문과 관련될 때는 최소한 **operation identity, attempt identity/index, attempt outcome, retry reason**을 구분할 수 있어야 한다.

## State snapshot보다 transition과 delta가 이해하기 쉽다

Runtime 이해에서 “현재 상태가 무엇인가?”만큼 중요한 질문은 **“무엇이 어떻게 바뀌었는가?”**다.

큰 object 전체를 before/after로 dump하기보다 질문에 필요한 변화를 표현하는 편이 낫다.

```text
state_before=pending
state_after=approved
```

또는:

```text
rows_before=120034
rows_after=119992
removed=42
```

Workflow execution history의 state entered/exited, data lineage의 create/drop/overwrite/rename 같은 모델도 변화 자체를 일급 정보로 다룬다.

`mols-clarify-runtime`에서는 state 전체를 기록하라는 규칙이 아니라 **선택한 질문이 mutation/state transition을 묻는다면 snapshot보다 최소 delta를 우선 고려한다**는 heuristic이 유용하다.

## Relevant input과 effective configuration이 중요하다

최신 Agent failure-attribution 연구에서도 output만 있는 partial trace보다 **input과 context를 포함한 full execution trace**가 failure attribution을 크게 개선했다. 일반 runtime에서도 결과를 설명할 때 input과 effective configuration이 빠지면 같은 문제가 생긴다.

다만 raw payload나 전체 config dump는 좋은 해법이 아니다. 결과나 결정에 실제 영향을 준 context만 남긴다.

```text
input_dataset=raw.orders
partition=2026-08-30
records=34192
mode=incremental
code_revision=...
runtime=...
```

특히 재현성과 원인 분석이 필요한 경우 다음 정보가 materially 중요할 수 있다.

- relevant input identity 또는 bounded summary
- effective runtime parameter
- feature/config flag
- code/service revision
- dependency/runtime version
- deployment environment

OpenLineage의 execution parameters/source-code facet과 OpenTelemetry resource metadata가 이런 provenance를 별도 의미로 다루는 이유도 같다.

## Data pipeline에서는 lineage 자체가 runtime evidence다

데이터 작업에서는 단순 input/output 목록만으로 실제 변환 관계를 잘못 추론할 수 있다.

```text
orders_raw -> orders_clean
customers_raw -> customers_clean
```

이 두 관계가 있는데 inputs=`orders_raw, customers_raw`, outputs=`orders_clean, customers_clean`만 남으면 모든 input이 모든 output을 만든 것처럼 해석될 수 있다.

따라서 선택한 복원 질문이 데이터 provenance를 묻는 경우에는 단순 목록보다 **실제 input -> output lineage edge**가 더 정확한 evidence일 수 있다.

이것도 모든 runtime에 lineage를 추가하라는 뜻은 아니다. 기존 framework가 native lineage/artifact를 제공하면 그것을 먼저 재사용하고 wrapper가 상세 관계를 중복하지 않는다.

## Error occurrence와 operation failure를 구분한다

Exception이 존재한다고 operation 전체가 실패한 것은 아니다.

다음은 정상적인 runtime behavior일 수 있다.

- 처리된 retry
- expected rejection
- cancellation
- fallback으로 복구된 attempt
- domain-level negative result

따라서 failure evidence는 exception 발생 자체보다 **operation outcome**을 기준으로 해석해야 한다.

좋은 실패 정보는 보통 다음 중 필요한 일부다.

```text
outcome=failure
error_type=ConnectionTimeout
target=warehouse
cause=connection_deadline_exceeded
```

같은 failure를 여러 layer에서 반복 기록하지 않고 가장 적절한 owner가 한 번 충분한 causal context를 남긴다는 현재 Skill의 원칙은 유지한다.

## Timestamp만으로 causal order를 추론하지 않는다

분산 runtime에서는 wall-clock timestamp가 실제 causal ordering을 완전히 설명하지 못할 수 있다.

ECS는 event timestamp와 별도로 `event.sequence`를 제공하고, OpenTelemetry Logs는 사건 발생 시각과 collector가 관찰한 시각을 구분한다.

복원이 중요할 때 기본적인 신뢰 순서는 다음에 가깝다.

```text
causal relationship
> explicit logical sequence
> timestamp inference
```

즉 parent/link/trigger나 explicit sequence가 이미 있다면 timestamp 정렬만으로 새로운 causal relation을 추론하지 않는다.

## Evidence owner와 evidence viability는 다르다

현재 Skill은 result, exception, artifact/framework metadata, logging, existing trace/span 중 의미상 적절한 owner를 잘 선택한다. 하지만 **semantic ownership과 실제 availability/durability는 별개**다.

예를 들어 trace가 의미상 가장 좋은 surface여도 다음 이유로 복원 시점에는 존재하지 않을 수 있다.

- sampling/drop
- collector queue overflow
- process crash
- filtering
- retention 만료
- payload/attribute truncation
- backend 장애

따라서 중요한 복원 질문에서는 owner를 고른 뒤 다음을 확인할 가치가 있다.

- 필요한 success/failure path에서 실제 생성되는가?
- sampled/filter/drop 가능한 best-effort evidence인가?
- 필요한 기간 동안 남는가?
- 실제 독자가 조회할 수 있는가?
- 필요한 다른 evidence와 연결 가능한가?

복원에 필수적인 사실을 ephemeral/sampled surface 하나에만 의존하면 안 된다. 반대로 Skill이 sampling policy나 collector architecture까지 설계할 필요도 없다. **viability gap을 발견하고 더 durable한 기존 owner를 우선하거나 limitation을 드러내는 것**까지가 적절한 범위다.

## Evidence가 없다는 사실의 의미를 보존한다

사람과 Agent 모두 다음을 혼동하면 안 된다.

```text
false
unknown
not_observed
not_recorded
truncated
sampled
```

예를 들어 output이 `null`인 것과 output이 기록 과정에서 잘린 것은 의미가 다르다. Failure event가 없다는 것과 sampling 때문에 보이지 않는 것도 다르다.

AWS Step Functions는 execution history input/output의 truncation 여부를 별도로 노출하고, 여러 event 표준도 producer/schema/time metadata를 사실과 분리한다.

따라서 복원 질문에 중요한 evidence가 incomplete할 수 있다면 **absence를 정상 결과로 오해하지 않게 completeness/quality를 확인한다**는 원칙이 필요하다.

## Structured evidence는 JSON 여부가 아니라 안정적인 semantics가 중요하다

Machine-readable evidence가 곧 JSON이라는 뜻은 아니다.

사람과 Agent 모두에게 중요한 것은 다음이다.

- 안정적인 event/operation type
- 반복 가능한 field meaning
- 동적 identifier와 event class 분리
- bounded value
- 같은 개념에 같은 field/term 사용

Human-readable message와 machine-readable semantics를 함께 둘 수 있다.

```text
message="promotion rejected"
action=promotion
target=model-v17
outcome=rejected
reason=accuracy_guard_failed
run_id=...
```

`message`는 사람이 빠르게 읽고, semantic fields는 검색·필터·Agent 분석에 쓰인다. 둘을 별도 logging 체계로 만들 필요는 없다.

## Metrics는 개별 실행 reconstruction surface가 아니다

개별 실행을 설명하려는 Skill이 metrics까지 runtime evidence owner로 취급하면 scope가 넓어질 수 있다.

Metrics는 보통 많은 observation을 aggregate해 health, rate, latency, distribution 같은 질문에 답한다. Request ID나 run ID 같은 high-cardinality identity를 metric에 넣어 개별 실행을 복원하려 하면 비용·cardinality 문제가 커질 수 있다.

따라서 다음 boundary가 유용하다.

> 개별 실행의 path, reason, state, cause를 복원하기 위한 detailed identity를 metric에 넣지 않는다. 질문의 주목적이 aggregate health나 monitoring이면 해당 책임으로 넘긴다.

## Audit/security evidence는 일반 duplicate와 다를 수 있다

현재 Skill은 duplicate/noisy evidence를 적극적으로 줄인다. 일반 runtime diagnostics에는 좋은 원칙이지만 security, audit, compliance evidence에는 별도 contract가 있을 수 있다.

겉보기에 같은 사건도 목적이 다르면 semantic duplicate가 아니다.

```text
application event:
  payment completed

audit trail:
  actor=A
  action=transfer
  object=B
  result=success
```

Audit trail은 retention, integrity, attribution, legal/compliance requirement를 가질 수 있다.

따라서 **security/audit/compliance evidence를 일반 runtime clarification의 duplication/noise 판단만으로 제거·이동·retention 변경하지 않고 해당 owner와 contract를 먼저 확인한다**는 boundary가 필요하다.

## Propagated correlation context는 신뢰 증명이 아니다

Trace context나 baggage처럼 외부 경계를 통과하는 identifier는 correlation에는 유용하지만 actor identity, authentication, authorization 또는 사실의 진위를 보장하지 않는다.

따라서:

> propagated identifier는 evidence 연결용으로 사용하되 security identity 또는 authorization proof로 해석하지 않는다.

정도의 trust boundary는 범용 Skill에 흡수할 가치가 있다.

## Noise Budget을 Evidence Budget으로 확장한다

현재 `logging.md`의 Noise Budget은 좋은 출발점이다. 하지만 volume, cardinality, size, retention, cost 문제는 logs에만 존재하지 않는다. Trace event/link/attribute도 제한·truncation·sampling의 영향을 받는다.

더 일반적인 판단은 다음과 같다.

```text
Evidence budget
= volume
+ cardinality
+ payload size
+ retention
+ queryability
+ operational cost
```

별도의 복잡한 budget framework가 필요한 것은 아니다. 선택한 복원 질문에 기여하지 않는 high-cardinality, repeated, unbounded context를 제거하는 원칙으로 충분하다.

## 좋은 runtime evidence는 사건 그래프를 복원한다

조사한 여러 source의 공통 분모를 하나의 사고 모델로 표현하면 다음과 같다.

```text
Execution
│
├─ Identity
│  ├─ operation
│  ├─ run/execution
│  └─ source/version
│
├─ Context
│  ├─ relevant input
│  ├─ effective parameters
│  └─ target/resource
│
├─ Flow
│  ├─ parent/cause/link
│  ├─ state transition
│  ├─ sequence
│  └─ attempt/retry
│
├─ Decision
│  ├─ action
│  ├─ outcome
│  └─ reason
│
├─ Effect
│  ├─ mutation/delta
│  ├─ output/artifact
│  └─ lineage
│
├─ Failure
│  ├─ error type
│  └─ cause
│
└─ Evidence quality
   ├─ producer/schema
   ├─ observed vs occurred
   └─ missing/truncated/sampled
```

이 구조는 새로운 universal runtime schema가 아니다. **복원 질문과 현재 evidence를 비교해 무엇이 실제로 빠졌는지 찾는 diagnostic lens**로 쓰는 것이 적절하다.

## 인간과 Agent를 함께 고려한 설계

사람과 Agent는 읽는 방식이 다르지만 필요한 underlying facts는 많이 겹친다.

### 사람이 특히 빨리 이해하는 정보

- 짧고 의미 있는 operation/event 이름
- action, outcome, reason
- before -> after transition
- 핵심 input/output
- causal timeline
- failure cause
- 관련 artifact 또는 상세 evidence로의 연결

### Agent가 특히 안정적으로 사용하는 정보

- 안정적인 typed field와 용어
- event/run/operation identifier
- explicit parent/link/trigger relation
- explicit outcome/reason
- source/target
- bounded input/output
- schema/version
- missing/truncated/sampled 같은 completeness metadata

따라서 둘을 따로 최적화하기보다 **human-readable message와 stable semantic fields를 같은 evidence에서 함께 제공**하는 것이 가장 비용 대비 효과가 좋다.

## 우선순위별 고도화 후보

| 우선순위 | 후보 | 판단 |
| --- | --- | --- |
| P1 | Evidence viability/durability 확인 | 의미상 owner와 실제 복원 가능성을 구분하므로 가치가 큼 |
| P1 | Causality: parent/link/trigger 관계 | async/distributed/batch runtime에서 execution ID만으로 부족함 |
| P1 | Logical operation vs attempt | retry/fallback/redrive 이해에 필수 |
| P1 | Action/outcome/reason과 Why-not | 중요한 decision/gate를 설명하는 최소 semantic으로 강함 |
| P1 | Audit/security evidence 보호 | duplicate/noise 제거가 required audit trail을 훼손하는 위험 차단 |
| P2 | Relevant input/effective config/provenance | failure attribution과 재현성 개선, 단 raw dump는 금지 |
| P2 | State delta와 lineage | mutation/data pipeline 질문에서 매우 유용 |
| P2 | Evidence completeness | absence를 false/success로 오해하는 문제 차단 |
| P2 | Evidence Budget | log 외 trace/event/context의 noise·cost까지 일반화 |
| P2 | Event/span/log owner heuristic | 기존 native telemetry가 있을 때 적절한 surface 선택 개선 |
| P2 | Metrics negative boundary | 개별 reconstruction과 aggregate monitoring의 책임 혼동 차단 |
| P3 | Propagated context trust boundary | correlation과 security identity 혼동 방지 |
| P3 | Timestamp보다 causality/sequence 우선 | distributed runtime에서 잘못된 시간순 추론 방지 |

## 권장 package 변화

현재 4-reference package는 대체로 적절하다.

```text
mols-clarify-runtime/
├─ SKILL.md
└─ references/
   ├─ diagnosis.md
   ├─ evidence.md
   ├─ logging.md
   └─ validation.md
```

이번 조사에서 신규 파일 하나를 추가한다면 `correlation.md`가 가장 타당하다.

```text
mols-clarify-runtime/
├─ SKILL.md
└─ references/
   ├─ diagnosis.md
   ├─ evidence.md
   ├─ correlation.md
   ├─ logging.md
   └─ validation.md
```

`correlation.md`는 다음 조건에서만 읽는다.

- retry/fallback/redrive
- async/message
- batch
- fan-out/fan-in
- cross-process/service
- 여러 evidence surface를 같은 logical execution으로 연결해야 함

소유할 내용은 다음 정도면 충분하다.

- logical operation vs attempt
- parent-child vs causal link
- async/message/batch relationship
- existing stable identifier 우선
- timestamp != causality
- propagated context trust boundary

반대로 `sampling.md`, `metrics.md`, `security.md`, `tracing.md`, framework별 reference를 별도로 만드는 것은 현재 단계에서는 과하다.

## 파일별 흡수 방향

### `SKILL.md`

현재 workflow는 거의 유지한다. Evidence owner 선택 시 다음 판단만 core에 추가할 가치가 있다.

```text
semantic owner
-> evidence viability
-> 필요한 correlation
-> smallest change
```

Progressive Disclosure에는 retry/async/batch/cross-process correlation이 필요할 때 `correlation.md`를 읽는 조건을 추가한다.

### `diagnosis.md`

새 debt form을 많이 만들지 않는다. `Disconnected`를 다음까지 포함하도록 깊게 만든다.

- 같은 logical operation을 연결할 수 없음
- operation과 attempt가 섞임
- causal relationship가 사라짐

복원 질문에는 중요한 gate에 대한 Why-not을 더 명확히 포함할 수 있다.

### `evidence.md`

가장 큰 고도화 대상이다.

추가 후보:

- Evidence Viability gate
- relevant input/effective config/provenance heuristic
- state delta/lineage 판단
- evidence completeness
- Evidence Budget
- metrics negative boundary
- audit/security evidence boundary

### `correlation.md`

조건부 detail만 소유한다.

- operation/attempt
- parent/link/trigger
- async/message/batch
- timestamp/sequence/cause의 우선순위
- trust boundary

### `logging.md`

현재 Event, Not Narration과 failure ownership은 유지한다.

보강 후보:

- event/message type과 dynamic value 분리
- structured는 JSON 여부가 아니라 stable semantics라는 설명
- expected/handled outcome을 자동 ERROR로 승격하지 않음
- 기존 native operation/span/event가 있을 때 중복 log를 만들지 않음

### `validation.md`

현재의 “변경 후 남은 evidence만 보고 복원 질문에 답할 수 있는가”를 강화한다.

최종 reconstructability gate는 다음에 가깝다.

> 코드를 다시 읽지 않고 선택한 evidence만으로 target, action/outcome, 필요한 reason 또는 causal relation을 ambiguity 없이 복원할 수 있는가?

필수 evidence가 sampled/truncated/ephemeral surface에만 의존한다면 limitation도 함께 확인한다.

## 흡수하지 않을 내용

다음은 조사 가치가 있지만 canonical Skill contract로 복제하지 않는 것이 좋다.

- OpenTelemetry의 구체적인 field/attribute 이름
- `traceparent`, `tracestate`, baggage 세부 규격
- OTLP schema
- Collector queue/WAL/retry 설정
- 구체적인 sampling 알고리즘
- 언어별 logging API
- framework-specific artifact schema
- 특정 observability vendor의 naming convention
- 모든 runtime에 trace ID나 structured event를 강제하는 규칙

이런 빠르게 변하거나 target-specific한 detail은 실제 project/runtime의 authoritative documentation과 native mechanism이 소유해야 한다.

## 다음 단계에서 검증할 시나리오

실제 고도화 전에 다음 adversarial scenario로 현재/개선안의 판단 차이를 확인하면 좋다.

1. **Skip without reason** — `deploy skipped`만 있고 왜 skip됐는지 모름.
2. **Retry collapse** — 최종 success만 보이고 앞선 timeout/503 attempt가 사라짐.
3. **Async fan-out** — 같은 run ID는 있지만 어떤 message가 어떤 downstream 작업을 유발했는지 모름.
4. **Sampled-away critical fact** — 중요한 business action의 유일한 evidence가 sampled trace에만 있음.
5. **Audit false duplicate** — application log와 audit trail이 같은 사건을 담는다는 이유로 하나를 제거하려 함.
6. **Config-dependent result** — code는 같지만 effective flag/version이 달라 결과가 달라짐.
7. **Null vs truncated** — output 없음과 evidence truncation을 구분하지 못함.
8. **Timestamp inversion** — distributed clock 차이 때문에 timestamp 순서와 causal order가 어긋남.
9. **Handled exception** — 내부 retry exception을 operation failure로 잘못 기록함.
10. **Data lineage ambiguity** — 여러 input/output 목록만 있어 실제 source-to-result edge를 잘못 추론함.

## 조사에서 확인한 핵심 문장

`mols-clarify-runtime`이 추구할 runtime evidence를 한 문장으로 정리하면 다음과 같다.

> **어떤 실행이, 어떤 context에서, 무엇을 대상으로, 어떤 인과·결정 경로를 거쳐, 무엇을 바꾸거나 만들었고, 왜 그런 outcome이 되었는지를 최소한의 신뢰 가능한 evidence로 복원할 수 있게 한다.**

이 정의는 현재 Skill의 responsibility를 observability platform 설계로 넓히지 않으면서도 사람과 Agent가 실제 runtime을 이해하는 데 필요한 정보를 더 정확히 포함한다.

## Sources

### 현재 repository와 원본 Skill

- `src/rulesync/.rulesync/skills/mols-clarify-runtime/`
- `src/rulesync/.rulesync/skills/clarify-code/`
- `docs/references/agent-assets/common/design-principles.md`
- `docs/references/agent-assets/common/instruction-design.md`
- `docs/references/agent-assets/skills/skill-authoring-conventions.md`
- https://github.com/mols3131d/hmda-data-reliability/tree/main/.rulesync/skills/prj-clarify-runtime

### Runtime evidence, tracing, events

- OpenTelemetry Trace API: https://opentelemetry.io/docs/specs/otel/trace/api/
- OpenTelemetry Trace SDK / sampling: https://opentelemetry.io/docs/specs/otel/trace/sdk/
- OpenTelemetry Logs data model: https://opentelemetry.io/docs/specs/otel/logs/data-model/
- OpenTelemetry semantic conventions — events: https://opentelemetry.io/docs/specs/semconv/general/events/
- OpenTelemetry semantic conventions — recording errors: https://opentelemetry.io/docs/specs/semconv/general/recording-errors/
- OpenTelemetry semantic conventions — messaging spans: https://opentelemetry.io/docs/specs/semconv/messaging/messaging-spans/
- OpenTelemetry Collector resiliency: https://opentelemetry.io/docs/collector/resiliency/
- W3C Trace Context: https://www.w3.org/TR/trace-context/
- CloudEvents specification: https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md
- Elastic Common Schema — Event fields: https://www.elastic.co/docs/reference/ecs/ecs-event

### Workflow history, provenance, lineage

- OpenLineage object model: https://openlineage.io/docs/spec/object-model/
- OpenLineage execution parameters facet: https://openlineage.io/docs/spec/facets/run-facets/execution_parameters/
- OpenLineage job lineage facet: https://openlineage.io/docs/next/spec/facets/job-facets/lineage/
- AWS Step Functions execution history: https://docs.aws.amazon.com/step-functions/latest/apireference/API_HistoryEvent.html
- AWS Step Functions `get-execution-history`: https://docs.aws.amazon.com/cli/latest/reference/stepfunctions/get-execution-history.html
- Argo Workflows variables and retry context: https://argo-workflows.readthedocs.io/en/latest/variable-flow/variables/

### Human debugging and Agent trace research

- Whyline: https://doi.org/10.1145/1368088.1368130
- Pivot Tracing overview: https://www.usenix.org/publications/login/spring2016/mace
- TraceElephant — execution traces for multi-agent failure attribution: https://aclanthology.org/2026.acl-long.912/
- ACL Findings — context pruning/backward tracing for agent diagnosis: https://aclanthology.org/2026.findings-acl.98/
- Log2 — cost-aware logging: https://www.microsoft.com/en-us/research/publication/log2-cost-aware-logging-mechanism-performance-diagnosis-2/
- OWASP Logging Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html

일부 최신 LLM log-analysis 자료는 preprint 단계이므로 구현 contract의 authority가 아니라 방향성 evidence로만 사용한다.
