# Evidence

Runtime evidence는 목적이 아니라 **복원 질문에 답하기 위한 surface**다. 먼저 기존 execution을 관찰하고, future execution에서도 같은 질문을 반복해서 답해야 하거나 사용자가 유지되는 evidence surface를 명시적으로 요구할 때만 maintained runtime evidence를 바꾼다.

## Observation And Maintained Evidence

둘을 구분한다.

| Kind | Purpose | Examples |
| --- | --- | --- |
| Observation evidence | 지금 이 execution을 이해한다 | existing test/command output, result, exception, state delta, artifact diff, framework history, existing trace/coverage |
| Maintained runtime evidence | future execution에서도 code를 다시 추적하지 않고 같은 질문에 답할 surface를 유지한다 | result/exception context, artifact/framework metadata, existing trace/span data, log/event, correlation relation |

`maintained`는 각 실행의 record가 영구 저장된다는 뜻이 아니다. **Surface를 future execution에도 유지한다는 뜻**이며, 실제 record가 필요한 기간 동안 살아남는지는 별도의 durability/availability 문제다.

Observation만으로 현재 질문이 풀리고 maintained change가 필요하지 않으면 source/runtime evidence를 추가하지 않는다.

## Choose The Owner

Maintained evidence가 필요하면 가장 자연스러운 기존 owner를 고른다.

| Surface | Prefer when |
| --- | --- |
| Result / return | caller가 완료 결과, 상태, action 또는 bounded summary를 사용해야 한다 |
| Exception context | 실패 대상, 단계, 원인을 caller나 failure handler가 진단해야 한다 |
| Artifact / framework metadata | 실행 결과가 durable record로 남아야 하거나 framework가 그 사실을 소유한다 |
| Framework execution history / report | runtime이 lifecycle, state, attempt 또는 result를 이미 authoritative하게 보존한다 |
| Existing trace / span / event | runtime이 operation path나 causal relation을 이미 제공하고 그 관계가 복원 질문에 필요하다 |
| Logging | 다른 owner로는 사라지는 시간적 사건, decision 또는 boundary outcome을 실행 후 복원해야 한다 |
| Correlation relation / field | 기존 evidence는 충분하지만 operation, attempt 또는 causal relation을 연결할 수 없다 |

Metrics는 aggregate health, rate, distribution과 trend를 위한 surface다. **개별 execution을 복원하려고 request/user/execution identifier를 metric label로 추가하지 않는다.** 질문이 aggregate 상태라면 monitoring/observability 책임으로 route한다.

## Choose The Change

새 evidence 추가만 해법으로 보지 않는다.

| Debt form | Prefer |
| --- | --- |
| Missing | 기존 owner에 필요한 context만 보강한다. |
| Duplicate | owning surface 하나를 남기고 의미 없는 복제를 제거하거나 병합한다. |
| Misowned | contract를 깨지 않는 범위에서 owning boundary로 옮기거나 상위 layer에는 필요한 의미만 projection한다. |
| Noisy | 질문에 답하지 않는 event/field를 제거·병합하고 반복성을 줄인다. |
| Disconnected | 기존 operation/attempt/relation을 재사용하고, 그것으로 부족할 때만 correlation을 보강한다. |

기존 consumer가 의존하는 result, event, field가 명시적 contract라면 clarification만으로 제거하거나 이동하지 않는다.

## Evidence Viability

Semantic owner가 맞아도 실제 reconstruction에 쓸 수 없다면 충분한 evidence가 아니다.

Maintained evidence를 선택하기 전에 필요한 범위에서 확인한다.

- **Generated** — 선택한 success/failure/skip/retry path에서 실제로 만들어지는가?
- **Available** — 필요한 사람이나 Agent가 실행 후 접근할 수 있는가?
- **Complete enough** — sampling, filtering, truncation, buffer limit 또는 dropped event 때문에 질문의 핵심 관계가 사라질 수 있는가?
- **Durable enough** — 필요한 reconstruction window까지 남아 있는가?
- **Correlatable** — 관련 result, artifact, attempt 또는 downstream work와 필요한 수준으로 연결되는가?
- **Trustworthy enough** — 외부에서 주입된 context나 best-effort telemetry를 identity/auth proof 또는 완전한 audit record처럼 오해하고 있지 않은가?

모든 evidence record가 영구적일 필요는 없다. 필요한 사용 시점보다 충분히 오래 남으면 된다. 반대로 sampling되거나 쉽게 drop되는 telemetry를 **반드시 복원되어야 하는 사실의 유일한 owner**로 두지 않는다.

## Selection Rules

1. **누가 이 사실을 알아야 하는가?** caller, maintainer, operator, downstream Agent 중 실제 독자를 정한다.
1. **기존 observation으로 충분한가?** 현재 이해만 필요하고 충분하면 maintained evidence를 추가하지 않는다.
1. **사용자가 maintained surface를 명시했는가?** logging, result context, metadata처럼 future execution에 남을 surface가 명시되었다면 no-op 규칙으로 요청 자체를 무시하지 않는다. 다만 중복·오소유·과도한 방식은 더 작은 설계로 조정한다.
1. **기존 durable/native owner가 있는가?** result, exception, artifact, framework metadata/history가 충분하면 wrapper log를 추가하지 않는다.
1. **operation path나 causal relation이 필요한가?** 이미 존재하는 trace/history/relation을 우선하고 새 tracing 체계를 만들지 않는다.
1. **시간적 사건 자체가 의미 있는가?** 다른 owner로는 사라지는 decision, transition 또는 boundary outcome일 때만 logging/event를 고려한다.
1. **relation이 필요한가?** retry, async, batch 또는 cross-process 관계가 핵심이면 [Correlation](correlation.md)을 따른다.
1. **viability가 충분한가?** 나중에 필요할 evidence라면 actual path, retention, accessibility와 completeness를 확인한다.

모든 runtime evidence를 하나의 공통 schema로 표준화하려 하지 않는다. 선택한 질문에 필요하지 않은 field는 추가하지 않는다.

상위 계층은 새로운 의미를 추가할 때만 하위 계층의 evidence를 projection한다. 단순 복제는 제거한다.

## Common Decisions

| Situation | Preferred decision |
| --- | --- |
| existing test/result만으로 현재 behavior를 충분히 이해할 수 있고 maintained change 요구가 없다 | 코드 변경 없이 stop한다. |
| 사용자가 future logging을 요구했지만 result/history가 이미 같은 사실을 더 잘 소유한다 | 요청 목적을 보존하면서 중복 log 대신 owning surface 보강 또는 가장 작은 boundary event를 선택한다. |
| result가 필요한 상태 전이와 최종 action을 이미 충분히 노출한다 | 추가 log 없이 result를 owner로 유지한다. |
| 같은 failure를 하위·중간·상위 layer가 모두 기록한다 | failure를 소유하거나 처리하는 boundary를 남기고 반복 evidence를 제거한다. |
| framework가 durable execution history, artifact 또는 metadata에 사실을 이미 남긴다 | 그 native evidence를 우선하고 wrapper에는 별도 의미가 있을 때만 projection한다. |
| existing trace가 causal flow를 충분히 제공한다 | 새 log/correlation을 추가하기 전에 trace를 재사용한다. |
| trace가 sampled될 수 있는데 반드시 남아야 하는 destructive action 사실이다 | trace를 sole owner로 두지 않고 durable owner가 있는지 다시 고른다. |
| 외부 command/tool이 상세 output을 이미 소유한다 | wrapper는 operation, target, outcome, return code 같은 bounded boundary context만 남기고 상세 output을 복제하지 않는다. |

이 예시는 해법을 고정하지 않는다. 실제 reconstruction question, 사용자 요청과 기존 consumer contract가 우선한다.

## Runtime Meaning

필요할 때 다음 semantic 중 최소 subset만 남긴다.

- **operation / action** — 무엇을 했는가
- **target / subject** — 무엇을 대상으로 했는가
- **outcome** — 어떤 결과가 났는가
- **reason** — 왜 그 결과·decision이 났는가
- **state delta / effect** — 무엇이 바뀌거나 그대로 남았는가
- **relevant input/context** — 결과를 materially 바꾼 input, parameter, fixture, effective config
- **operation / attempt relation** — retry나 async work가 어떻게 연결되는가
- **artifact / downstream effect** — 무엇이 만들어지거나 영향을 받았는가

`action + outcome + reason`은 강한 일반 frame이지만 mandatory schema가 아니다. caller result나 framework-native representation이 이미 같은 의미를 더 자연스럽게 소유하면 그것을 사용한다.

## Evidence Budget

Evidence도 이해·저장·검색 비용을 만든다. log만이 아니라 모든 surface에서 질문에 필요하지 않은 비용을 줄인다.

검토할 신호:

- routine event/attribute가 반복되어 중요한 state change를 가린다.
- high-cardinality identifier나 unbounded value가 지속적으로 쌓인다.
- 전체 payload, object, stdout/stderr 또는 artifact를 불필요하게 복제한다.
- 같은 context를 log, span, result, metadata 여러 곳에 반복한다.
- retention/query cost가 reconstruction 가치에 비해 과도하다.
- field/event/link 제한 때문에 정작 중요한 evidence가 truncate/drop될 가능성이 커진다.

필요한 semantic을 유지하면서 volume, cardinality, payload size와 duplication을 최소화한다.

## Audit, Security And Compliance Boundary

보안 event, audit trail, compliance record와 legally required evidence는 일반 runtime clarification과 목적·retention·integrity·access contract가 다를 수 있다.

- 겉보기에는 같은 사건을 기록해도 별도 audit/security 목적이 있으면 단순 duplicate로 제거하지 않는다.
- retention, immutability, access control 또는 forensic requirement를 이 Skill이 재정의하지 않는다.
- primary requirement가 audit/security evidence라면 해당 책임과 authoritative policy를 따른다.
- 일반 runtime evidence에 credential, token, secret, 민감한 payload를 추가하지 않는다.

## Data Safety

남기지 않는다.

- credential, token, secret
- 불필요한 raw row, 전체 request/model dump 또는 payload
- 무제한 subprocess stdout/stderr
- 쉽게 변하는 대형 object representation
- correlation을 명목으로 넣는 불필요한 개인·사용자 식별 정보

가능하면 identifier, count, bounded summary, delta 또는 path처럼 작은 표현을 사용한다.

## Contract Boundary

Runtime evidence는 현재 실행을 설명한다. requirement, domain policy 또는 business contract를 새로 정의하지 않는다.
