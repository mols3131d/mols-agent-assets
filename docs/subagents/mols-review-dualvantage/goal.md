---
description: DualVantage를 변경할 때 composable subagent 정체성, caller ownership, 독립·병렬 review와 bounded execution invariant를 먼저 확인하는 최상위 maintainer 기준입니다.
---

# DualVantage Goal

DualVantage의 목표는 **caller가 소유한 더 큰 workflow 안에서 bounded review capability로 합성되면서, 같은 target을 서로 다른 두 decision-relevant failure lens로 독립 검토하고, candidate claim을 current evidence와 authority로 판정해 false positive와 scope creep을 억제하는 것**이다.

이 문서는 family 변경의 최상위 maintainer 기준이다. Runtime behavior는 각 subagent 정의가 정본이지만, 구현·tool·projection·역할 구성이 아래 identity invariant를 조용히 약화해서는 안 된다. Invariant를 의도적으로 바꿔야 한다면 일반 tuning이 아니라 **family redesign**으로 취급한다.

## Identity invariants

1. **Subagent, not engine** — caller가 선택한 bounded review capability이며 outer workflow, loop, task lifecycle 또는 router를 소유하지 않는다.
2. **Caller owns outer contracts** — Goal/Scope, phase·loop progression, recursion, artifact policy, user-facing response, implementation과 mutation은 caller 또는 governing owner가 소유한다.
3. **No artifact or answer ownership** — 자체 report/artifact schema나 user-facing answer schema를 강제하지 않는다. Caller가 handoff format을 주면 따르고, 없으면 decision에 필요한 최소 review signal만 반환한다.
4. **Lead injects context, not exploration** — Root는 applicable Agent Asset, Skill, governing instruction, contract와 document를 시작 컨텍스트로 선별·주입한다. Defect discovery, target/source/test 탐색, reachable path 추적, evidence·counter-evidence 수집과 validation target 선택은 각 worker가 자기 failure lens 안에서 직접 수행한다.
5. **Context does not become authority by retrieval** — 검색되었거나 instruction처럼 보인다는 이유만으로 governing rule이 되지 않는다. Root와 worker는 기존 authority hierarchy, provenance와 applicability를 확인하고 나머지는 reference/evidence로만 취급한다.
6. **Two distinct vantages** — Verifier와 Challenger는 같은 checklist의 표현 변형이 아니라 서로 다른 decision-relevant failure lens를 가진다.
7. **Independent initial discovery** — 두 specialist는 같은 bounded basis와 injected context를 출발점으로 삼되 sibling conclusion과 Lead의 pre-analysis 없이 각자 필요한 review surface와 evidence를 독립적으로 탐색한다.
8. **Parallel-first when real** — runtime이 independent concurrent subagent execution을 지원하면 두 specialist를 같은 delegation wave에서 시작한다. 지원하지 않을 때만 독립성을 보존한 sequential fallback을 사용한다.
9. **Candidate, not proof** — specialist output은 evidence나 final finding이 아니라 falsifiable candidate claim이다. Root가 underlying evidence와 caller-provided authority를 기준으로 판정한다.
10. **No finding quota** — review 완료를 정당화하기 위해 finding을 만들거나 유지하지 않는다. 모든 candidate가 탈락하거나 current remediation 대상이 아니고 blocker도 없으면 `clear`가 정상 결과다. Finding 수, reviewer effort, review depth, disagreement 또는 specialist 수는 admission 근거가 아니다.
11. **Root is not a third reviewer** — Root는 specialist가 놓친 defect나 counterexample을 새로 hunting하지 않고 worker의 미완료 exploration을 대신하지 않는다.
12. **Evidence discipline** — Observed, Inferred, Unknown을 구분하고 agreement, vote, confidence 또는 반복 주장을 correctness proof로 사용하지 않는다.
13. **Authority before severity** — issue의 사실성·impact와 current remediation authority를 분리한다. Severity는 scope를 확대하지 않는다.
14. **Bounded invocation** — 한 bounded review invocation에서 Verifier 최대 1회, Challenger 최대 1회, 총 2회를 넘지 않는다. Timeout, failure, incomplete result, disagreement, uncertainty 또는 refinement 필요도 자동 retry 사유가 아니며 Root가 스스로 새 pass를 만들어 budget을 초기화하지 않는다.
15. **Evidence convergence** — 추가 작업은 candidate disposition 또는 caller decision을 바꿀 credible information gain이 있을 때만 한다. 같은 evidence를 반복하거나 saturation 이후 탐색을 계속하지 않는다.
16. **Coverage gaps stay visible** — failed specialist, unavailable capability, stale basis와 decisive unknown을 성공으로 흡수하지 않는다.
17. **Bounded final claim** — 결과는 caller-provided basis, scope, coverage와 evidence에 대한 bounded review signal이며 absolute correctness proof가 아니다.

이 invariant가 사라지면 이름이나 agent 수가 같아도 같은 family로 보지 않는다.

## Priority

상충할 때 다음 순서를 우선한다.

1. caller ownership과 composability
2. child-owned independent exploration
3. authority-preserving context injection
4. 독립적인 두 failure lens
5. evidence-gated truth
6. authority-aligned action
7. bounded execution과 termination
8. 실제 가능한 병렬 효율
9. signal density

비용이나 편의를 위해 independence를 없애거나, Lead가 worker exploration을 대신하거나, recall을 위해 evidence gate를 약화하거나, 사용 편의를 위해 caller의 outer contract를 가져오는 것은 개선이 아니다.

## Non-goals

다음은 이 family의 책임이 아니다.

- outer Run/Loop engine, workflow router 또는 task lifecycle 관리
- Goal/Scope/Acceptance를 처음부터 정의하거나 caller 대신 변경하는 것
- artifact 위치·형식·durable state, report schema 또는 user-facing response schema 소유
- implementation, remediation, approval, merge 또는 다른 mutation
- Root가 implementation/source/test를 미리 훑어 worker에게 defect candidate, reachable path, evidence selection 또는 validation target을 만들어 주는 것
- worker에게 주입할 수 있다는 이유로 임의의 검색 결과, source comment, fixture text 또는 reference document를 governing instruction으로 승격하는 것
- engine-like Skill의 outer lifecycle, transition, artifact 또는 answer contract를 Root/worker 책임으로 복제하는 것
- exhaustive proof, formal verification 또는 모든 defect 탐색
- reviewer consensus, majority vote 또는 debate로 truth를 결정하는 구조
- Root를 포함한 세 번째 full review
- severity를 이유로 scope를 자동 확대하는 것
- specialist 재호출로 답을 refinement하는 loop
- finding 수, source 수, 탐색 깊이 또는 token 사용량 자체의 최대화
- Challenger의 active exploit/reproduction 또는 Verifier의 unrestricted execution

이 책임이 필요하면 family를 넓히기보다 해당 책임을 소유한 caller, Skill, workflow 또는 별도 owner에 맡긴다.

## Success criteria

목표대로 작동하면 다음이 관찰되어야 한다.

- outer orchestrator나 engine-like Skill 아래에 합성되어도 그 procedure, artifact policy와 response contract를 덮어쓰지 않는다.
- caller-provided Goal/Scope/Acceptance를 review basis로 소비하고 outer task contract를 발명하지 않는다.
- Root는 applicable instruction/asset/document를 최소 context로 주입하지만 technical review surface나 evidence를 선행 탐색하지 않는다.
- Verifier와 Challenger는 injected context를 출발점으로 각자 필요한 target/source/test/configuration/document/evidence를 독립적으로 탐색한다.
- worker가 추가로 발견한 instruction-like content는 authority가 확인되기 전까지 reference/evidence로만 취급된다.
- Verifier와 Challenger가 실제로 다른 failure mode를 탐색한다.
- parallel-capable runtime에서는 두 specialist가 같은 delegation wave에서 시작한다.
- sequential fallback에서도 sibling result가 initial brief에 섞이지 않는다.
- candidate가 current state basis와 decisive evidence를 가지며 obvious counter-evidence가 있으면 승격되지 않는다.
- Root가 third full review 없이 candidate를 adjudicate할 수 있다.
- 모든 candidate가 탈락해도 억지 finding 없이 `clear`로 종료할 수 있다.
- impact와 remediation authority가 분리되고 speculative/duplicate claim이 억제된다.
- specialist invocation은 bounded review당 최대 2회에서 끝난다.
- material coverage/evidence gap은 limitation 또는 blocker signal로 남는다.
- saturation 이후 no-op review churn이 발생하지 않는다.

## Change rule

변경 전에 **이 변경이 위 identity invariant를 보존하는가**를 먼저 판단한다.

- 보존하면 runtime, capability, wording 또는 structure 수준의 개선으로 진행할 수 있다.
- invariant를 바꿔야 하면 이유, 대안과 새로운 boundary를 먼저 설계 결정으로 명시한다.
- runtime source와 이 문서가 어긋나면 실행 사실은 runtime source에서 확인하되 그 차이를 정상 상태로 방치하지 않는다.

Evidence와 claim 의미는 [review-model.md](review-model.md), delegation·context injection·handoff·capability 유지보수는 [maintenance.md](maintenance.md)가 소유한다.
