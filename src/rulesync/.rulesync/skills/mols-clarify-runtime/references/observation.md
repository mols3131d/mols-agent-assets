# Observation

Runtime behavior를 이해하려고 바로 maintained logging이나 instrumentation을 추가하지 않는다. **이미 남아 있는 runtime evidence를 먼저 사용하고, 그래도 질문이 풀리지 않을 때만 가장 작은 안전한 기존 scenario를 실행한다.**

## Reuse Before Re-Executing

먼저 현재 질문과 revision에 실제로 적용되는 existing evidence가 있는지 본다.

- prior result / return 또는 failure report
- state snapshot, artifact, manifest 또는 diff
- framework-native execution history / report
- existing trace/span/event 또는 coverage/path report
- 기존 test run이 남긴 case, seed, replay input 또는 output

이 evidence가 현재 code/config와 무관하거나 stale한데 behavior가 바뀌었을 가능성이 있으면 현재 실행의 증거처럼 사용하지 않는다. 반대로 이미 질문에 충분한 evidence가 있으면 단지 “직접 실행해 보기 위해” 같은 scenario를 다시 돌리지 않는다.

## Choose The Smallest Executable Scenario

실제 execution이 여전히 필요하면 이미 존재하고 재현 가능하며 **현재 권한과 environment에서 안전하게 실행할 수 있는 scenario**를 사용한다.

일반적인 선택 순서:

1. 질문을 직접 재현하는 기존 isolated test case
1. 안전하게 실행 가능한 관련 command, task, request 또는 entrypoint
1. 더 넓은 integration 실행

전체 suite나 application을 돌리는 것보다 질문에 필요한 input과 boundary만 실행할 수 있으면 그것을 우선한다. 반대로 더 작은 command라도 destructive mutation, 외부 호출, 비용 발생 또는 production 영향이 있으면 “작다”는 이유로 실행하지 않는다.

Observation은 실행 권한을 새로 만들지 않는다. 안전하거나 허가된 실행이 없으면 existing history/result/artifact 같은 read-only evidence를 사용하고 limitation을 남긴다.

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

## Observation Scope

**한 execution은 그 scenario에서 관찰된 behavior만 보여준다.**

- 특정 test/input에서 본 path를 모든 input의 일반 path로 확대하지 않는다.
- fixture가 mock, stub, fake, in-memory adapter 또는 synthetic dependency를 사용하면 **그 대체 경계 안에서 실제로 관찰된 behavior**로 해석한다. 실제 external service, production adapter 또는 live environment가 같은 behavior라고 단정하지 않는다.
- 한 environment에서 본 outcome을 다른 runtime, version 또는 concurrency 조건에도 같다고 단정하지 않는다.
- nondeterministic behavior라면 한 run의 순서나 timing을 stable contract처럼 해석하지 않는다.
- 더 넓은 결론에 여러 case가 필요하지만 existing scenario가 없으면 새 test를 임의로 만들지 않고 uncertainty와 별도 testing/debugging 필요를 드러낸다.

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

기존 diagnostic switch, verbose report, trace viewer, coverage report처럼 **runtime이 이미 제공하는 transient observation surface를 먼저 사용한다.**

Source edit를 disposable probe로 쓰는 것은 기본값이 아니다. 필요한 경우에도 다음 조건을 모두 만족해야 한다.

- 현재 task와 workspace가 source edit를 허용한다.
- 기존 surface만으로 질문을 좁힐 수 없다.
- probe가 domain behavior, caller-visible output 또는 external state를 바꾸지 않는다.
- timing/concurrency 영향 위험이 낮다.
- final acceptance 전에 제거하고 working diff와 behavior를 다시 확인할 수 있다.

새 debugger, coverage, tracing 또는 logging framework를 clarification만을 위해 도입하지 않는다. Probe 때문에 execution이 달라질 수 있으면 관찰 결과를 stable fact로 단정하지 않는다.

## Stop Or Escalate

다음이면 maintained code/evidence 변경 없이 중단할 수 있다.

- 기존 scenario와 evidence만으로 복원 질문에 답할 수 있다.
- 질문이 현재 조사에 한정되고 future consumer가 같은 evidence를 반복해서 필요로 하지 않는다.
- 사용자가 future execution에 유지할 evidence surface를 별도로 요구하지 않았다.

다음이면 [Evidence](evidence.md)로 넘어간다.

- 같은 질문 때문에 사람이나 Agent가 반복해서 source를 재추적해야 한다.
- 필요한 사실이 execution 후 사라지고 future reconstruction에도 필요하다.
- existing evidence가 noisy, duplicated, misowned, disconnected 또는 실제 path에서 unavailable하다.
- 사용자가 logging, metadata, result context처럼 유지되는 evidence surface의 개선을 명시적으로 요구했다.

실행 중 defect가 의심되거나 correctness 판단이 필요해지면 관찰 결과를 evidence로 넘기고 debugging/review 책임으로 route한다. 이 Skill 안에서 defect를 수정하지 않는다.
