# Validation

이 Skill의 refactor는 comprehension을 개선하지만 **observable behavior와 relevant usage contract를 바꾸는 작업이 아니다.** Validation은 test count가 아니라 무엇을 preserved해야 하고 어떤 evidence가 그 claim을 실제로 지지하는지 확인한다.

Core `SKILL.md`가 common-path preservation gate를 소유한다. 이 reference는 tests/contract가 불완전·충돌하거나 dynamic usage, characterization, material performance 또는 before/after equivalence가 단순하지 않을 때 사용한다.

## Preservation Envelope

대상에서 실제로 관찰되거나 의존되는 surface만 확인한다.

| Surface | Check |
| --- | --- |
| API / usage identity | import/path, call shape, symbol identity, framework entrypoint, registration |
| Return | value, type, ordering, shape, sentinel 의미 |
| Exceptions | type, trigger condition, causal context와 visibility |
| State | mutation, persistence, idempotency, lifecycle |
| Side effects | file/database/network write, overwrite/delete, execution ordering |
| Validation | acceptance/rejection 기준과 timing |
| Dynamic/tooling usage | reflection, config/string lookup, serialization, generated code, schema 또는 naming convention |
| Observability | log/event 의미, ordering과 failure visibility가 실제 consumer contract인지 |
| Performance | hot-path latency, algorithmic complexity, allocation, I/O/query count 등 task에 material한 특성 |

모든 항목을 기계적으로 측정하지 않는다. Candidate transformation이 실제로 건드릴 수 있고 caller/runtime/tooling이 의존할 수 있는 surface를 먼저 식별한다.

## Evidence Is Not Automatically Specification

Preservation evidence의 종류는 서로 다른 claim을 지지한다.

- **Current contract/spec/schema/protocol** — 무엇이 의도적으로 유지돼야 하는지에 대한 authority가 될 수 있다.
- **Caller/usage evidence** — 실제 consumer가 무엇에 의존하는지 보여준다.
- **Tests** — covered behavior가 바뀌었는지 강하게 감지할 수 있지만, untested behavior가 존재하지 않는다는 증명은 아니다.
- **Characterization test** — 현재 observed behavior를 baseline으로 고정한다. 그 behavior가 바람직하거나 normative requirement라는 뜻은 아니다.
- **Static/type analysis** — name/type/binding과 일부 structural invariant를 검증할 수 있지만 dynamic/runtime coupling 전체를 증명하지 않는다.
- **Refactoring tool usage/preview** — known reference와 conflict discovery에 유용하지만 dynamic string/config/reflection usage를 완전하게 증명하지 않을 수 있다.
- **Benchmark/profile/measurement** — 측정한 performance characteristic에 대한 evidence다. 측정하지 않은 성능 전체를 증명하지 않는다.

한 evidence source가 green이라는 이유로 다른 surface까지 자동으로 preserved됐다고 주장하지 않는다.

Evidence가 서로 material하게 충돌하면 편의상 하나를 complete truth로 canonize하지 않는다. Exact preservation claim과 가장 직접적인 current owner/consumer/observable behavior를 기준으로 좁게 재확인하고, unresolved conflict가 안전한 transformation을 막으면 더 작은 change 또는 handoff/no-op을 선택한다.

## Observed Baseline vs Normative Contract

Characterization은 legacy refactor의 좋은 safety net이 될 수 있다. 다만 두 질문을 구분한다.

1. **현재 무엇이 실제로 일어나는가?** — observed baseline
2. **무엇이 durable contract여야 하는가?** — normative/current contract

Refactor scope에서는 observed externally visible behavior를 임의로 고치지 않는다. Odd behavior가 defect로 의심돼도 comprehension refactor에 correctness fix를 섞지 않고 별도 concern으로 보고한다.

반대로 characterization test를 추가했다는 이유만으로 accidental implementation detail이나 suspected bug를 새 durable requirement라고 설명하지 않는다. 현재 behavior를 보존하기 위한 temporary/characterization safeguard와 semantic contract authority를 분리한다.

## Transformation Risk

각 refactoring family에는 서로 다른 preservation risk가 있을 수 있다. Portable Skill에 language-specific precondition을 나열하지 않고 **현재 candidate에 material한 risk만** 확인한다.

대표적인 질문:

- **Rename** — name binding, hierarchy/override, dynamic/config/string/reflection usage가 있는가?
- **Move / Extract / Inline** — execution count, variable/state capture, visibility, binding, registration identity가 달라지는가?
- **Control-flow rewrite** — short-circuiting, exception timing, validation timing, side-effect ordering이 달라지는가?
- **Representation change** — serialized/persisted/wire/schema shape 또는 equality/hash/order semantics가 달라지는가?
- **State/phase simplification** — transition order, reentrancy, lifecycle 또는 failure recovery semantics가 달라지는가?

이 목록은 exhaustive catalog가 아니다. 적용되는 language, framework, repository convention과 tooling이 더 구체적인 precondition을 소유한다.

## Before and After

가능하면 동일한 relevant envelope를 변경 전후에 비교한다.

1. Existing contract, caller/usage context와 필요한 tests/characterization으로 baseline을 확인한다.
1. Candidate transformation의 relevant preservation risk를 확인한다.
1. Comprehension refactor를 적용한다.
1. 같은 observable/usage envelope에 대해 relevant validation을 다시 실행한다.
1. Output, exception, state, side effect, ordering, registration/identity 또는 shape 차이가 없는지 target에 맞게 확인한다.
1. Type/lint/static check와 refactoring-tool preview는 해당 claim에 맞는 보조 evidence로 사용한다.
1. Performance-sensitive code라면 repository에 이미 있는 benchmark, profiler evidence 또는 안정적인 비교 방법이 있을 때 before/after를 비교한다.

기존 safeguard가 충분하면 새 test나 benchmark를 만들지 않는다.

## Hidden and Dynamic Usage

Private/internal symbol도 runtime 또는 tooling contract가 될 수 있다.

다음 signal이 실제로 있으면 usage discovery를 넓힌다.

- plugin/callback/DI registration
- symbol name을 저장하는 config/manifest/string
- reflection/dynamic lookup
- serialization/schema/generated code
- external script/tooling이 path/name/shape를 참조

가능성만으로 모든 rename을 금지하지 않는다. Repository evidence에서 material한 signal이 있는지 먼저 본다.

Native refactoring tool의 dynamic-reference search나 text-occurrence preview를 사용할 수 있다면 확인에 도움을 줄 수 있다. 그러나 heuristic result는 false positive/negative가 있을 수 있으므로 tool success를 complete proof로 보고하지 않는다.

## Performance Boundary

이 Skill은 performance optimization Skill이 아니다.

- readability를 위해 algorithmic complexity를 악화시키지 않는다.
- I/O, query, allocation 또는 hot-loop work를 material하게 늘릴 수 있는 refactor는 동등성 근거 없이 적용하지 않는다.
- 기존 benchmark가 없다는 이유로 microbenchmark를 형식적으로 추가하지 않는다.
- performance 영향이 합리적으로 배제되지 않고 task에 중요하다면 더 안전한 intervention을 선택하거나 scope를 멈춘다.
- 측정하지 않은 performance equivalence를 측정했다고 표현하지 않는다.

정확한 CPU cycle 동등성을 요구하는 것은 아니다. Repository와 task에서 의미 있는 성능 특성을 보존하는 것이 계약이다.

## Characterization and Gaps

중요한 behavior에 safeguard가 없고 다른 evidence로 refactor 위험을 충분히 줄일 수 없을 때만 작은 characterization test를 고려한다.

- 현재 observed behavior를 필요한 범위만 capture한다.
- 그 observation을 자동으로 desired requirement라고 부르지 않는다.
- implementation detail을 불필요하게 고정하지 않는다.
- suspected correctness problem은 별도 concern으로 기록한다.

검증할 수 없으면 가능한 대체 evidence를 사용하고 한계를 명시한다: static/type check, deterministic I/O 비교, import/registration 확인, caller와 current contract 대조, complexity reasoning.

Risk가 낮고 transformation이 좁으면 incomplete evidence를 이유로 형식적인 ceremony를 추가하지 않는다. 반대로 high-risk transformation의 material preservation claim을 지지할 evidence가 부족하면 **더 작은 intervention 또는 no-op**을 선택한다.

대체 evidence를 실제 test, benchmark 또는 exhaustive usage analysis와 동등하게 표현하지 않는다.
