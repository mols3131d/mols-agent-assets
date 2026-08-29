# Observation

Runtime behavior를 이해하려고 바로 persistent logging이나 instrumentation을 추가하지 않는다. **먼저 기존 실행을 가장 작게 관찰하고, 현재 evidence만으로 선택한 복원 질문에 답할 수 있는지 확인한다.**

## Choose The Smallest Executable Scenario

가능하면 이미 존재하고 재현 가능한 실행을 사용한다.

우선순위는 고정 규칙이 아니라 일반적인 선택 순서다.

1. 질문을 직접 재현하는 기존 test case
1. 관련 command, task, request 또는 entrypoint의 좁은 실행
1. framework가 이미 보존한 execution history나 report
1. 더 넓은 integration 실행

전체 suite나 application을 돌리는 것보다 질문에 필요한 input과 boundary만 실행할 수 있으면 그것을 우선한다.

새 test를 설계하거나 acceptance criteria를 만드는 것은 이 Skill의 책임이 아니다. 기존 test가 없고 별도 재현 설계가 필요하면 testing 또는 debugging 책임으로 넘긴다.

## Existing Tests As Runtime Scenarios

관련 test는 correctness assertion만이 아니라 **구체적인 runtime context를 제공하는 executable scenario**로 읽을 수 있다.

관찰할 수 있는 정보:

- 실제 input과 expected outcome
- fixture가 준비하는 state, dependency와 environment
- parametrized case와 case identifier
- 실제 return, exception 또는 side effect
- failure report에 노출되는 local value와 causal context
- framework가 이미 제공하는 seed, replay input 또는 minimal failing case

모든 fixture와 parameter를 기록하지 않는다. 선택한 behavior를 바꾸거나 설명하는 값만 본다.

Property-based test처럼 runtime이 minimal failing input이나 replayable example을 이미 제공하면 큰 trace보다 그 입력을 먼저 사용해 질문을 좁힐 수 있다. 별도 shrinking 또는 replay framework를 도입하라는 뜻은 아니다.

## Observe Surfaces

질문에 맞는 기존 surface만 선택한다.

| Surface | Useful for |
| --- | --- |
| Return / result | 최종 status, value, action, affected count, caller-visible outcome |
| Exception / failure report | failure type, target, stage, cause와 chained context |
| State before/after | mutation, transition, persisted delta와 unchanged state |
| Output artifact / snapshot / report | 생성물, manifest, diff, checkpoint와 durable result |
| Framework execution history | scheduled/started/completed/failed, state enter/exit, retry/redrive와 native lifecycle |
| Existing trace/span/event | operation path, duration, parent/link와 cross-boundary causal flow |
| Existing coverage/path report | 실제 실행된 line 또는 branch transition과 실행되지 않은 path 후보 |
| Relevant runtime context | fixture, parameter, seed, effective config, code/runtime version 중 behavior에 영향을 준 값 |

`stdout`/`stderr`도 기존 command가 소유하는 bounded evidence라면 사용할 수 있지만, 대용량 raw output을 이해 surface로 복제하지 않는다.

## Reconstruction Frame

관찰을 raw event 나열로 끝내지 않는다. 필요한 경우 다음 frame 중 질문에 필요한 부분만 복원한다.

```text
Input / Context
    ↓
Decision / Path
    ↓
Action
    ↓
Effect / State Delta
    ↓
Outcome
```

특히 중요한 질문:

- **Why did?** 어떤 input/state/decision 때문에 이 outcome이 발생했는가?
- **Why didn't?** 어떤 gate, condition 또는 prior state 때문에 기대한 action/path가 실행되지 않았는가?

모든 intermediate value를 수집하지 않는다. 선택한 outcome이나 decision을 설명하지 못하는 값은 관찰 범위에서 제외한다.

## Path Evidence Is Not Reason Evidence

Coverage, trace와 execution history가 보여주는 범위를 과장하지 않는다.

- coverage는 특정 line·branch가 실행됐는지 좁히는 데 유용하지만 **왜** 그 branch가 선택됐는지나 behavior가 올바른지는 증명하지 않는다.
- trace는 실제 operation 관계를 보여줄 수 있지만 sampling, missing instrumentation 또는 retention 때문에 전체 실행을 항상 보장하지 않는다.
- timestamp 순서는 causal relationship을 대신하지 않는다.
- test pass/fail은 해당 assertion의 결과이며 전체 domain correctness를 자동으로 증명하지 않는다.

질문의 답이 decision reason이나 causal dependency라면 path evidence와 relevant input/state 또는 native causal relation을 함께 본다.

## State Delta

Mutation을 이해할 때 전체 object dump보다 **질문과 관련된 before/after 차이**를 우선한다.

예:

```text
before: status=pending, rows=120
after:  status=approved, rows=118

delta: status pending→approved, rows -2
```

파일, database, cache, object, workflow state와 generated artifact 모두 같은 원칙을 적용한다.

변경되지 않은 중요한 state도 “왜 아무 일도 일어나지 않았는가”를 설명할 때 evidence가 될 수 있다.

## Runtime Context And Provenance

결과를 실제로 바꿀 수 있는 context만 본다.

- input 또는 target
- fixture / parametrized case
- retry attempt 또는 replay input
- effective configuration
- code/service revision
- runtime/dependency version

전체 environment dump나 모든 config를 기본적으로 수집하지 않는다. 선택한 reconstruction question과 관련성이 있어야 한다.

## Temporary Observation

현재 repository나 runtime이 이미 제공하는 diagnostic switch, verbose report, trace viewer, coverage report 또는 disposable local probe가 있고 안전하게 사용할 수 있다면 **현재 조사에만 필요한 transient observation**으로 사용할 수 있다.

- persistent evidence가 필요하다는 결론과 혼동하지 않는다.
- 새 debugger, coverage, tracing 또는 logging framework를 clarification만을 위해 도입하지 않는다.
- source를 일시적으로 바꿨다면 최종 변경에 남길 의도가 없는 probe는 제거하고 working diff와 behavior를 다시 확인한다.
- probe 자체가 behavior, timing 또는 concurrency를 materially 바꿀 가능성이 있으면 신뢰 가능한 observation으로 단정하지 않는다.

## Stop Or Escalate

다음이면 persistent code/evidence 변경 없이 중단할 수 있다.

- 기존 scenario와 evidence만으로 복원 질문에 답할 수 있다.
- 질문이 일회성 조사이고 future consumer가 같은 evidence를 반복해서 필요로 하지 않는다.

다음이면 [Evidence](evidence.md)로 넘어간다.

- 같은 질문 때문에 사람이나 Agent가 반복해서 source를 재추적해야 한다.
- 필요한 사실이 execution 후 사라진다.
- existing evidence가 noisy, duplicated, misowned, disconnected 또는 실제 path에서 unavailable하다.

실행 중 defect가 의심되거나 correctness 판단이 필요해지면 관찰 결과를 evidence로 넘기고 debugging/review 책임으로 route한다. 이 Skill 안에서 defect를 수정하지 않는다.
