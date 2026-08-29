# `mols-clarify-runtime` 고도화 계획

이 계획은 [`mols-clarify-runtime-enhancement-research.md`](mols-clarify-runtime-enhancement-research.md)와 구현 후 재귀 Review에서 확인한 delta를 반영한 최종 Plan이다.

## Goal

`mols-clarify-runtime`이 logging 중심으로 조기에 수렴하지 않고, **이미 남아 있는 runtime evidence를 먼저 재사용해 실제 behavior를 이해하며, gap이 남을 때만 가장 작은 안전한 기존 scenario를 실행하고, future execution에서도 같은 질문을 복원해야 할 때만 가장 작은 runtime evidence를 개선**하도록 고도화한다.

## Active Scope

### In scope

- `src/rulesync/.rulesync/skills/mols-clarify-runtime/`
- 조건부 detail에 실질적 loading benefit이 있는 reference 추가
- Skill description 변경에 따른 generated `route/skills.jsonl` 동기화
- `inbox/2026-08-30/`의 Research, Plan, Review artifact

### Out of scope

- 제품 코드와 테스트 코드의 domain/correctness 변경
- 새 test 설계 또는 defect 수정
- debugger, coverage, tracing, metrics, record/replay framework 도입
- monitoring/telemetry platform 설계
- 특정 언어·framework·vendor schema의 범용 contract화

## Research decisions

1. **Reuse before re-executing.** 현재 revision과 질문에 적용되는 result, failure report, artifact, native history, trace/coverage가 이미 충분하면 같은 scenario를 단지 관찰 목적으로 다시 실행하지 않는다.
2. **Observe before instrument.** Existing evidence로 부족할 때만 safe existing test, command, request를 사용한다. Observation은 별도 실행 권한을 부여하지 않는다.
3. **Existing test는 executable scenario다.** fixture, parameter, seed, expected result와 failure report는 실제 실행 context를 제공한다. 새 test 설계는 별도 책임이다.
4. **한 실행은 그 scenario만 증명한다.** 특정 input의 observed path를 다른 input이나 일반 behavior로 확대하지 않는다. Mock/stub/fake가 있으면 그 대체 경계 안의 behavior로 해석한다.
5. **Coverage는 path evidence다.** 실행된 line/branch를 좁힐 수 있지만 decision reason이나 correctness를 증명하지 않는다.
6. **Why / Why-not가 핵심 질문이다.** raw trace 전체보다 선택한 outcome에 관련된 execution evidence를 좁히는 편이 이해 비용이 낮다.
7. **Native history와 provenance를 우선한다.** framework가 lifecycle, retry, input/output, effective config와 artifact를 이미 소유하면 wrapper logging으로 복제하지 않는다.
8. **Evidence viability는 semantic ownership과 별도다.** sampling, filtering, truncation, retention, accessibility와 relation 때문에 맞는 surface도 실제 reconstruction에는 부족할 수 있다.
9. **Runtime evidence에는 budget이 있다.** volume, cardinality, payload와 duplication을 함께 본다.
10. **Specific surface request는 제약이다.** 사용자가 logging이나 metadata처럼 구체적인 future surface를 지정하면 더 자연스러운 owner가 있다는 이유로 조용히 다른 surface로 대체하지 않는다.

## Design decision: Skill은 분리하지 않는다

별도 `mols-understand-runtime` Skill은 만들지 않는다.

- `mols-clarify-runtime`의 기존 책임 자체가 runtime understanding debt다.
- observation-only와 future evidence improvement는 `기존 evidence → 필요하면 실행 → 필요성 판정 → 개선 → 재관찰`이라는 한 lifecycle이다.
- 분리하면 `understand-runtime`과 `clarify-runtime`의 trigger가 겹치고 handoff 비용이 생긴다.
- 별도 Skill이 제공하는 독립 authority, capability, loading 또는 runtime benefit이 아직 없다.

관찰 전용 요청과 evidence 개선 요청이 실제 사용에서 반복적으로 다른 workflow와 routing을 요구한다는 근거가 생길 때만 분리를 재검토한다.

## Core model

### Current observation evidence

현재 execution을 이해하는 데 사용하는 evidence다.

- prior result / return / failure report
- state snapshot, artifact, manifest 또는 diff
- framework-native execution history
- existing trace / coverage / runtime report
- 기존 test run의 case, seed, replay input 또는 output
- 필요할 때 안전하게 실행한 existing test / command / request의 결과
- relevant input, fixture, parameter, seed, effective config와 version

이 evidence는 일회성일 수 있다. 현재 질문만 답하면 되는 경우 final source change가 없어도 된다.

### Future runtime evidence

미래 execution에서도 같은 질문을 code retracing 없이 답할 수 있도록 source/runtime surface에 유지하는 clarification이다.

- result / exception context
- artifact / framework metadata 또는 history
- existing trace/span/event의 필요한 semantic
- logging
- 필요한 operation/attempt/correlation relation

각 evidence record가 영구 보존되어야 한다는 뜻은 아니다. 실제 record가 필요한 기간 동안 살아남는지는 별도의 **durability / availability / completeness** 문제로 검증한다.

## Review-driven rules

### Explicit future-evidence request

현재 observation만으로 질문을 이해할 수 있어도 사용자가 logging, metadata, result context처럼 **future execution에 유지할 evidence 개선을 명시적으로 요청했다면** 단순 no-op로 종료하지 않는다.

특정 surface를 직접 지정했다면 그 surface를 제약으로 보존한다. 다른 owner의 상세 내용을 그대로 중복하지 말고 요청한 surface에는 가장 작은 boundary meaning 또는 link만 projection한다.

### Observation scope

한 test/run에서 관찰한 behavior를 모든 input, environment 또는 concurrency 조건의 일반 behavior로 주장하지 않는다. Mock/stub/fake를 사용하면 그 대체 경계 안에서 관찰된 behavior로 한정한다.

더 넓은 결론이 필요하지만 existing scenario가 없으면 test를 임의로 만들지 않고 uncertainty 또는 별도 testing/debugging 필요를 드러낸다.

### Execution safety

Observation은 현재 permission과 safety boundary를 넓히지 않는다.

- destructive, irreversible, production-affecting 또는 비용을 발생시키는 action을 이해 목적으로 임의 실행하지 않는다.
- existing read-only history/result/artifact로 충분하면 재실행하지 않는다.
- safe execution이 없으면 static/existing evidence로 가능한 범위만 설명하고 limitation을 남긴다.

### Temporary probe

기존 diagnostic switch, report 또는 viewer를 먼저 사용한다. Source edit를 transient probe로 쓰는 것은 기본값이 아니며 다음을 모두 만족할 때만 제한적으로 허용한다.

- 현재 작업이 source edit를 허용한다.
- existing surface로 질문을 좁힐 수 없다.
- domain behavior, caller-visible output와 external state를 바꾸지 않는다.
- timing/concurrency 영향 위험이 낮다.
- final acceptance 전에 제거하고 behavior와 diff를 다시 확인할 수 있다.

## Planned package

```text
mols-clarify-runtime/
├── SKILL.md
└── references/
    ├── diagnosis.md
    ├── observation.md
    ├── evidence.md
    ├── correlation.md
    ├── logging.md
    └── validation.md
```

`observation.md`는 existing evidence와 필요할 때의 actual execution을 이용한 current behavior 관찰을, `correlation.md`는 retry/async/batch처럼 조건부로 필요한 relation 판단을 소유한다. 나머지 reference와 의미 ownership을 중복하지 않는다.

## File changes

- `SKILL.md` — reuse/observe before instrument, safe execution, current observation과 future evidence 구분, no-op 조건, routing boundary.
- `diagnosis.md` — Why-not, input/context, effect, operation/attempt까지 reconstruction question 확대.
- `observation.md` — existing records reuse, smallest safe executable scenario, tests as scenarios, result/exception/state/artifact/history/trace/coverage 관찰과 limits.
- `evidence.md` — future owner 선택, explicit surface constraint, viability, metrics negative boundary, Evidence Budget, audit/security boundary.
- `correlation.md` — logical operation vs attempt, causal relation, async/batch, timestamp 한계, trust boundary.
- `logging.md` — observation 이후 선택, stable event semantics, action/outcome/reason, handled outcome level, native span/event 재사용.
- `validation.md` — baseline/re-observation, behavior envelope, reconstructability와 evidence viability gate.

## Acceptance conditions

- logging이 Workflow의 기본 경로가 아니다.
- existing evidence가 충분하면 불필요하게 재실행하지 않는다.
- observation 목적으로 기존 permission/safety boundary를 넓히지 않는다.
- existing test 실행과 test design 책임이 명확히 분리된다.
- 한 실행의 observed behavior를 일반화하지 않는다.
- current observation과 future execution에 유지할 evidence를 구분한다.
- 명시적인 future-evidence/surface 요청을 no-op 규칙이 무시하지 않는다.
- future evidence 선택 전에 viability를 검토한다.
- retry/async에서 execution ID 하나로 잘못 단순화하지 않는다.
- coverage, trace, metrics의 역할과 한계를 과장하지 않는다.
- audit/security evidence를 일반 noise 제거 규칙으로 훼손하지 않는다.
- 새 vendor/framework dependency를 요구하지 않는다.
- `clarify-code`, debugging/review, testing, monitoring, profiling 책임과 routing이 선명하다.
- 핵심 Skill은 짧고 조건부 detail은 reference에 남는다.

## Validation plan

반복 Review에서 최소한 다음 case를 challenge한다.

1. existing result/history만으로 현재 질문이 풀리는 observation-only 요청
2. 현재 이해는 되지만 사용자가 future logging을 명시적으로 요청한 경우
3. failing test를 보고 defect 수정으로 scope creep하는 경우
4. 하나의 passing test를 전체 input space의 behavior로 일반화하는 경우
5. mock/stub/fake 기반 test를 production dependency behavior로 일반화하는 경우
6. coverage가 branch를 보여준다는 이유로 decision reason까지 안다고 가정하는 경우
7. retry 3회를 하나의 undifferentiated execution으로 뭉개는 경우
8. sampled trace를 반드시 남아야 하는 destructive-action fact의 sole owner로 선택하는 경우
9. audit/security log를 duplicate라고 제거하는 경우
10. 모든 fixture/config/raw payload를 context로 남기는 경우
11. metric에 per-request identifier를 넣어 한 execution을 복원하려는 경우
12. production-affecting command를 observation 목적으로 실행하려는 경우
13. source temporary probe가 caller-visible output 또는 concurrency behavior를 바꿀 수 있는데 사실로 단정하는 경우
14. no new evidence가 필요한데 새로운 tracing/coverage framework를 도입하려는 경우

Repository-native `mise` 검증은 connector 환경에서 실행할 수 없으면 `not run`으로 남기며, GitHub PR Gate와 직접 source/route inspection을 별도로 확인한다.
