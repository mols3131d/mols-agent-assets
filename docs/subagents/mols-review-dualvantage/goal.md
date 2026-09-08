---
description: DualVantage를 변경할 때 composable subagent 정체성, caller ownership, 독립·병렬 review와 bounded execution invariant를 먼저 확인하는 최상위 maintainer 기준입니다.
---

# DualVantage Goal

DualVantage의 목표는 **caller가 소유한 더 큰 workflow 안에서 bounded review capability로 합성되고, 같은 target을 서로 다른 두 failure lens로 독립 검토해 evidence-backed candidate만 caller에게 돌려주는 것**이다.

이 문서는 family 변경의 최상위 maintainer 기준이다. Runtime behavior는 각 subagent 정의가 정본이지만, 구현·tool·projection·역할 구성이 아래 identity invariant를 조용히 약화해서는 안 된다. Invariant를 의도적으로 바꿔야 한다면 일반 tuning이 아니라 **family redesign**으로 취급한다.

## Identity invariants

1. **Subagent, not engine** — bounded review capability이며 outer workflow, loop, task lifecycle 또는 router를 소유하지 않는다.
2. **Caller owns outer contracts** — Goal/Scope/Acceptance, lifecycle, artifact policy, user-facing response, implementation과 mutation은 caller 또는 governing owner가 소유한다.
3. **Caller owns review policy** — severity, blocking, disposition, completion status와 required-action policy를 DualVantage가 새로 정의하지 않는다. Caller나 governing review asset이 제공하면 그 의미를 보존해 적용한다.
4. **No artifact or answer ownership** — 자체 report/artifact schema나 user-facing answer schema를 강제하지 않는다.
5. **Portable composition** — 실제 적용되는 Skill, Rule, instruction, contract와 document semantics를 소비하되 특정 host 구조를 runtime prompt의 전제로 만들지 않는다.
6. **Lead injects context, not exploration** — Root는 review를 시작하는 데 필요한 context를 최소한으로 주입한다. Defect discovery, target/source/test 탐색, reachable path 추적, evidence·counter-evidence 수집과 validation target 선택은 각 worker가 직접 수행한다.
7. **Context does not become authority by retrieval** — 전달되거나 검색되었다는 이유만으로 governing authority가 생기지 않는다.
8. **Two distinct vantages** — Verifier와 Challenger는 같은 checklist의 표현 변형이 아니라 서로 다른 decision-relevant failure lens를 가진다.
9. **Independent initial discovery** — 두 specialist는 sibling conclusion과 Lead의 pre-analysis 없이 각자 필요한 review surface와 evidence를 탐색한다.
10. **Parallel-first when real** — runtime이 independent concurrent subagent execution을 지원하면 두 specialist를 같은 delegation wave에서 시작한다.
11. **Candidate, not proof** — specialist output은 falsifiable candidate claim이다. Root는 generic evidence gate만 소유한다.
12. **Layered decision ownership** — worker는 candidate construction, Root는 evidence-based candidate adjudication, outer caller는 review policy와 task-level decision/action을 소유한다.
13. **No finding quota** — review 완료를 정당화하기 위해 candidate를 만들거나 약한 claim을 유지하지 않는다. zero-finding 결과는 정상이다.
14. **Root is not a third reviewer** — Root는 specialist가 놓친 defect나 counterexample을 새로 hunting하지 않고 worker의 미완료 exploration을 대신하지 않는다.
15. **Evidence discipline** — Observed, Inferred, Unknown을 구분하고 agreement, vote, confidence 또는 반복 주장을 correctness proof로 사용하지 않는다.
16. **Bounded invocation** — 한 bounded review invocation에서 Verifier 최대 1회, Challenger 최대 1회, 총 2회를 넘지 않는다. 자동 retry나 Root-initiated pass reset을 만들지 않는다.
17. **Evidence convergence** — 추가 작업은 candidate state 또는 caller decision을 바꿀 credible information gain이 있을 때만 한다.
18. **Coverage gaps stay visible** — failed specialist, unavailable capability, stale basis와 decisive unknown을 성공으로 흡수하지 않는다.
19. **Bounded final claim** — 결과는 caller-provided basis, coverage와 evidence에 대한 bounded review signal이며 absolute correctness proof가 아니다.

## Priority

상충할 때 다음 순서를 우선한다.

1. caller ownership과 composability
2. child-owned independent exploration
3. authority-preserving context composition
4. 독립적인 두 failure lens
5. evidence-gated truth
6. caller-owned review policy
7. bounded execution과 termination
8. 실제 가능한 병렬 효율
9. signal density

비용이나 편의를 위해 independence를 없애거나, Lead가 worker exploration을 대신하거나, recall을 위해 evidence gate를 약화하거나, 자체 status/severity/disposition 체계를 만들어 caller의 review policy를 덮어쓰는 것은 개선이 아니다.

## Non-goals

다음은 이 family의 책임이 아니다.

- outer Run/Loop engine, workflow router 또는 task lifecycle 관리
- Goal/Scope/Acceptance를 처음부터 정의하거나 caller 대신 변경하는 것
- severity, blocking, disposition, completion status 또는 required-action policy 소유
- artifact 위치·형식·durable state, report schema 또는 user-facing response schema 소유
- implementation, remediation, approval, merge 또는 다른 mutation
- Root가 implementation/source/test를 미리 훑어 worker에게 defect candidate, reachable path, evidence selection 또는 validation target을 만들어 주는 것
- 임의의 retrieved/reference content를 governing instruction으로 승격하는 것
- engine-like Skill의 outer lifecycle, retry/transition, artifact 또는 answer contract를 Root/worker 책임으로 복제하는 것
- maintainer-only portability 배경이나 특정 repository/framework 예시를 runtime prompt에 싣는 것
- exhaustive proof, formal verification 또는 모든 defect 탐색
- reviewer consensus, majority vote 또는 debate로 truth를 결정하는 구조
- Root를 포함한 세 번째 full review
- specialist 재호출로 답을 refinement하는 loop
- finding 수, source 수, 탐색 깊이 또는 token 사용량 자체의 최대화
- Challenger의 active exploit/reproduction 또는 Verifier의 unrestricted execution

이 책임이 필요하면 family를 넓히기보다 해당 책임을 소유한 caller, Skill, workflow 또는 별도 owner에 맡긴다.

## Success criteria

목표대로 작동하면 다음이 관찰되어야 한다.

- outer orchestrator나 review Skill 아래에 합성되어도 그 lifecycle, review policy, artifact policy와 response contract를 덮어쓰지 않는다.
- caller-provided Goal/Scope/Acceptance와 review-local criteria를 소비하고 대체 policy를 발명하지 않는다.
- Root는 applicable context를 최소한으로 주입하지만 technical review surface나 evidence를 선행 탐색하지 않는다.
- Verifier와 Challenger는 injected context를 출발점으로 각자 필요한 target/source/test/configuration/document/evidence를 독립적으로 탐색한다.
- worker가 추가로 만난 governing instruction은 실제 scope에서 적용되고 reference content는 임의로 authority가 되지 않는다.
- parallel-capable runtime에서는 두 specialist가 같은 delegation wave에서 시작한다.
- sequential fallback에서도 sibling result가 initial brief에 섞이지 않는다.
- candidate가 current state basis와 decisive evidence를 가지며 obvious counter-evidence가 있으면 승격되지 않는다.
- Root가 third full review 없이 candidate를 `confirmed | rejected | merged | unresolved`로 좁힐 수 있다.
- 모든 candidate가 탈락해도 억지 finding 없이 종료할 수 있다.
- caller가 severity/status/disposition 체계를 제공하면 그대로 사용하고, 없으면 DualVantage가 자체 체계를 만들지 않는다.
- specialist invocation은 bounded review당 최대 2회에서 끝난다.
- material coverage/evidence gap은 limitation 또는 unresolved로 남는다.
- saturation 이후 no-op review churn이 발생하지 않는다.

## Change rule

변경 전에 **이 변경이 위 identity invariant를 보존하는가**를 먼저 판단한다.

- 보존하면 runtime, capability, wording 또는 structure 수준의 개선으로 진행할 수 있다.
- invariant를 바꿔야 하면 이유, 대안과 새로운 boundary를 먼저 설계 결정으로 명시한다.
- runtime source와 이 문서가 어긋나면 실행 사실은 runtime source에서 확인하되 그 차이를 정상 상태로 방치하지 않는다.

Evidence와 claim 의미는 [review-model.md](review-model.md), delegation·context injection·handoff·capability 유지보수는 [maintenance.md](maintenance.md)가 소유한다.
