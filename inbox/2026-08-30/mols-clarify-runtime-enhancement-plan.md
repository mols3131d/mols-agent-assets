# `mols-clarify-runtime` 고도화 계획

이 계획은 [`mols-clarify-runtime-enhancement-research.md`](mols-clarify-runtime-enhancement-research.md)와 추가 runtime-comprehension 조사를 바탕으로 한다.

## Goal

`mols-clarify-runtime`이 logging 중심으로 조기에 수렴하지 않고, **기존 소스 코드와 테스트 코드의 실제 실행을 먼저 관찰해 runtime behavior를 이해하고, 그래도 반복적인 이해 부채가 남을 때만 가장 작은 지속 evidence를 개선**하도록 고도화한다.

## Active Scope

### In scope

- `src/rulesync/.rulesync/skills/mols-clarify-runtime/`
- 필요하면 새 reference 추가
- Skill description 변경에 따른 generated `route/skills.jsonl` 동기화
- 고도화 판단과 review를 위한 `inbox/2026-08-30/` artifact

### Out of scope

- 제품 코드나 테스트 코드 자체 수정
- 새 test 설계 또는 correctness 판단
- debugger, coverage, tracing, metrics, record/replay framework 도입
- monitoring/telemetry platform 설계
- 특정 언어·framework·vendor schema를 범용 contract로 고정

## Research delta

추가 조사에서 다음을 확인했다.

1. **실행 관찰은 instrumentation과 다르다.** 기존 test, command, result, exception, artifact, state delta, execution history, trace와 coverage는 코드를 수정하지 않고도 runtime behavior를 설명할 수 있다.
2. **Test는 executable scenario가 될 수 있다.** pytest의 fixture와 parametrization처럼 test는 실행 context와 구체적인 input/output case를 이미 제공할 수 있다. Skill은 test를 새로 설계하지 않고 기존 scenario를 좁게 실행해 사용할 수 있다.
3. **Coverage는 path evidence이지 reason evidence가 아니다.** branch coverage는 실제로 실행된 source→destination transition을 보여주지만, 왜 그 branch가 선택됐는지나 behavior correctness를 증명하지 않는다.
4. **Dynamic slicing의 일반화 가능한 교훈은 관련 실행만 좁히는 것이다.** 특정 input의 실제 실행에서 관심 값이나 outcome에 영향을 준 부분을 좁히는 접근은 program comprehension에 유용하지만, Skill이 slicing/debugging 도구 도입을 요구할 필요는 없다.
5. **Why / Why-not 질문이 강하다.** runtime output에서 직접 “왜 발생했나 / 왜 발생하지 않았나”를 묻고 관련 execution evidence만 좁히는 방식은 현재 reconstruction-question 모델과 잘 맞는다.
6. **재현 가능한 최소 실패 input은 강한 evidence다.** property-based testing이 제공하는 minimal failing case나 replayable input이 이미 있다면 복잡한 raw trace보다 먼저 활용할 가치가 있다.
7. **Native execution history는 log와 별개다.** workflow runtime은 state enter/exit, retry, redrive, input/output과 같은 structured history를 소유할 수 있으며, wrapper logging으로 복제할 이유가 없다.
8. **Runtime provenance는 실행 의미의 일부다.** 결과를 실제로 바꾼 input, effective configuration, runtime/code version은 필요할 때만 관찰해야 한다.

## Design decision: Skill은 분리하지 않는다

이번 단계에서는 별도 `mols-understand-runtime` Skill을 만들지 않는다.

이유:

- 현재 `mols-clarify-runtime`의 책임 자체가 runtime understanding debt다.
- 기존 evidence로 질문에 답할 수 있으면 no-op 하는 계약이 이미 있어 observation-only 작업을 수용할 수 있다.
- `understand-runtime`과 `clarify-runtime`을 분리하면 “실행을 이해한 뒤 evidence를 개선”하는 하나의 lifecycle이 두 Skill에 걸리고 routing이 겹친다.
- 별도 Skill이 제공하는 독립된 authority, capability, loading 또는 runtime benefit이 아직 없다.

분리는 향후 실제 사용에서 **관찰만 요청하는 trigger와 persistent evidence 개선 trigger가 지속적으로 충돌하거나 서로 다른 workflow가 필요하다는 evidence**가 생길 때 재검토한다.

## Core model

두 종류의 evidence를 구분한다.

### Observation evidence

현재 실행을 이해하기 위해 잠깐 사용하는 evidence다.

- 기존 test / command / request 실행
- return / result
- exception / failure report
- state before/after와 delta
- output artifact / snapshot / report
- framework-native execution history
- existing trace / coverage / runtime report
- 해당 실행의 relevant input, fixture, parameter, seed, effective config

현재 질문에 답하면 코드 변경 없이 중단할 수 있다.

### Persistent clarification evidence

미래의 사람이나 Agent도 같은 질문을 반복해서 코드까지 추적하지 않고 답해야 할 때 남기는 evidence다.

- result / exception context
- durable artifact / framework metadata
- existing trace/span의 attribute/event/link
- logging
- 필요한 correlation field

Persistent evidence는 의미상 owner뿐 아니라 **생성 여부, failure-path 가용성, sampling/filtering/drop, 보존 기간, 접근 가능성, correlation**까지 확인한다.

## Planned changes

### `SKILL.md`

- description과 Purpose를 “observe before instrument” 중심으로 확장한다.
- 기존 test와 executable scenario를 runtime observation surface로 인정한다.
- Workflow를 `질문 선택 → 기존 실행 관찰 → no-op 판정 → persistent evidence 개선 → 동일 scenario 재관찰` 순서로 재구성한다.
- Progressive Disclosure에 `Observation`과 `Correlation`을 추가한다.
- test design/debugging/tooling boundary는 유지한다.

### `references/observation.md` — 신규

다음을 소유한다.

- smallest executable scenario 선택
- existing test를 scenario로 읽는 법
- result/exception/state delta/artifact/native history/existing trace·coverage 관찰
- input/fixture/parameter/seed/effective config 중 materially relevant한 것만 선택
- `Input → Decision → Effect → Outcome`과 Why/Why-not frame
- coverage·trace가 보여주는 것과 보여주지 못하는 것
- 기존 evidence로 질문이 풀리면 변경 없이 stop

### `references/diagnosis.md`

- “실제 실행을 이해하고 싶다”는 runtime question을 명확히 포함한다.
- Why-not, material input/context, effect/output, logical operation/attempt 질문을 보강한다.
- `Disconnected`에 attempt 혼합과 causal relation 부재를 포함한다.

### `references/evidence.md`

- observation evidence와 persistent evidence를 명시적으로 구분한다.
- persistent evidence 선택 전에 **Evidence viability** gate를 추가한다.
- framework-native history/report를 명시한다.
- metrics를 per-execution reconstruction의 기본 surface에서 제외한다.
- log-only `Noise Budget`보다 넓은 `Evidence Budget`을 추가한다.
- security/audit/compliance evidence는 별도 contract 없이 duplicate/noise라고 제거하지 않는다.

### `references/correlation.md` — 신규

다음을 조건부로 소유한다.

- logical operation vs attempt
- parent-child vs causal link/shared identifier
- retry, async, batch, fan-out/fan-in
- timestamp ≠ causality
- external propagated context는 identity/auth proof가 아님

특정 OpenTelemetry field나 protocol을 contract로 복제하지 않는다.

### `references/logging.md`

- observation 후에도 필요한 경우에만 logging을 선택하도록 연결한다.
- stable event semantics와 `action / outcome / reason`을 강화한다.
- structured logging은 단순 JSON이 아니라 안정적인 event/field 의미라는 점을 명확히 한다.
- handled/expected outcome을 자동으로 ERROR로 올리지 않는다.
- 이미 native span/event surface가 있으면 그것을 우선하되 새 tracing 도입을 요구하지 않는다.

### `references/validation.md`

- 변경 전 baseline observation을 명확히 한다.
- 같은 executable scenario로 변경 후 behavior와 evidence를 다시 관찰한다.
- `코드를 다시 읽지 않고 selected evidence만으로 질문에 답할 수 있는가?`를 semantic gate로 둔다.
- sampling/truncation/retention 등 evidence limitation을 성공으로 숨기지 않는다.

## Acceptance conditions

- logging이 Workflow의 기본 경로가 아니다.
- 기존 test 실행은 test design과 구분되어 runtime observation으로 명확히 허용된다.
- existing evidence로 충분하면 no-op가 더 빨리 발생한다.
- persistent evidence를 추가하기 전에 viability를 검토한다.
- retry/async에서 execution ID 하나로 잘못 단순화하지 않는다.
- coverage, trace, metrics의 역할과 한계를 과장하지 않는다.
- security/audit evidence를 일반 noise 제거 규칙으로 훼손하지 않는다.
- 새 vendor/framework dependency를 요구하지 않는다.
- `clarify-code`, debugging/review, testing, monitoring, profiling 책임과 routing이 선명하다.
- 핵심 Skill은 짧게 유지하고 조건부 detail은 reference로 내린다.

## Validation plan

1. package structure와 links를 직접 검사한다.
2. 기존 description과 변경 description을 routing 관점에서 비교한다.
3. positive / negative / near-miss scenario를 시뮬레이션한다.
4. 다음 adversarial case를 반복 검토한다.
   - 기존 test result만으로 충분한데 log를 추가하려는 경우
   - test가 실패했지만 correctness defect 수정으로 넘어가려는 경우
   - coverage가 branch를 보여준다는 이유로 decision reason까지 안다고 가정하는 경우
   - retry 3회를 하나의 execution ID로 뭉개는 경우
   - sampled trace를 sole durable evidence로 선택하는 경우
   - audit log를 duplicate라고 제거하려는 경우
   - 모든 fixture/config/raw payload를 남기려는 경우
   - monitoring metric에 request ID를 넣어 실행 하나를 추적하려는 경우
5. description 변경 시 generated route가 canonical source와 일치하는지 확인한다.
6. connector 환경에서 실행할 수 없는 repository-native `mise` 검증은 실행했다고 주장하지 않는다.
