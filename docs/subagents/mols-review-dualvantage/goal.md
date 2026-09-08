---
description: DualVantage family를 변경할 때 가장 먼저 확인해야 하는 최상위 목표, 정체성, 비목표와 보존 조건을 설명하는 maintainer 문서입니다.
---

# DualVantage Goal

이 문서는 DualVantage family가 **왜 존재하고, 어떤 성질을 잃으면 더 이상 DualVantage가 아닌지**를 정의한다. Family를 변경할 때 가장 먼저 읽는 설계 기준이다.

Runtime behavior의 canonical source는 각 subagent 정의다. 그러나 구현, tool, vendor projection 또는 역할 구성을 바꿀 때 이 Goal을 조용히 약화해서는 안 된다. 아래 identity invariant를 의도적으로 바꿔야 한다면 일반 튜닝이나 리팩터링이 아니라 **family redesign**으로 취급하고, 그 결정부터 명시적으로 갱신한다.

## Primary goal

DualVantage의 목표는 **caller가 소유한 더 큰 workflow 안에서 bounded review capability로 자연스럽게 합성되면서, 같은 review target을 서로 다른 두 decision-relevant failure lens로 독립 검토하고, candidate claim을 current evidence와 authority로 판정해 false positive와 scope creep을 억제하는 것**이다.

DualVantage 자체가 outer engine이 되는 것은 목표가 아니다. Run/Loop, phase progression, Goal/Scope lifecycle, artifact policy, user-facing response와 implementation은 caller 또는 더 구체적인 owner가 유지한다.

우선순위는 다음과 같다.

1. **Composable ownership** — caller의 outer procedure와 output/artifact contract를 침범하지 않는다.
2. **Independent perspective** — 두 specialist가 실제로 다른 failure mode를 본다.
3. **Evidence-gated truth** — reviewer output이나 합의가 아니라 underlying evidence가 claim을 지지한다.
4. **Authority-aligned action** — 사실성과 impact를 current remediation authority와 분리한다.
5. **Bounded execution** — agent invocation과 추가 탐색이 명확한 stop condition 안에서 끝난다.
6. **Parallel efficiency** — independent concurrent execution이 가능한 runtime에서는 두 vantage를 병렬로 수집한다.
7. **Signal density** — finding 수보다 독립 검증 가능하고 actionable한 signal을 우선한다.

뒤의 목표를 위해 앞의 목표를 희생하지 않는다. 비용을 줄이기 위해 independence를 없애거나, 편의를 위해 caller ownership을 가져오거나, recall을 높이기 위해 evidence gate를 약화하는 것은 성공이 아니다.

## Identity invariants

Vendor, model, tool alias, runtime API 또는 projection format이 바뀌어도 다음은 보존한다.

1. **Subagent, not engine** — DualVantage는 caller가 선택한 bounded review capability이며 outer workflow/loop controller가 아니다.
2. **Caller owns outer contracts** — outer Goal/Scope, phase/loop progression, recursion, artifact policy, user-facing response format, implementation과 mutation은 caller 또는 governing owner가 소유한다.
3. **No artifact or answer ownership** — DualVantage는 자체 report/artifact schema나 user-facing answer schema를 강제하지 않는다. Caller가 제공한 handoff format을 따르고, 없으면 최소 review handoff만 반환한다.
4. **Two distinct vantages** — Verifier와 Challenger는 같은 checklist의 표현 변형이 아니라 서로 다른 decision-relevant lens를 가진다.
5. **Independent initial discovery** — 가능한 한 같은 bounded brief를 받고 sibling의 finding, speculation 또는 conclusion에 노출되지 않은 채 첫 분석을 수행한다.
6. **Parallel-first when real** — runtime이 independent concurrent subagents를 지원하면 두 specialist를 같은 delegation wave에서 시작한다. 지원하지 않을 때만 independence를 보존한 sequential fallback을 사용한다.
7. **Candidate, not proof** — specialist output은 final finding이나 evidence가 아니라 falsifiable candidate claim이다.
8. **One evidence gate** — final admission, scope/authority relation과 review-state 판단은 Root가 소유한다.
9. **Root is not a third reviewer** — Root는 specialist가 놓친 defect나 counterexample을 새로 hunting하지 않는다.
10. **Evidence layers stay distinct** — Observed, Inferred, Unknown을 섞어 certainty를 부풀리지 않는다.
11. **Evidence beats consensus** — agreement, vote, confidence 또는 반복 주장을 correctness proof로 사용하지 않는다.
12. **Authority before severity** — impact와 severity는 scope 또는 remediation authority를 만들지 않는다.
13. **Hard invocation budget** — 한 bounded review invocation에서 Verifier 최대 1회, Challenger 최대 1회, 총 2회를 넘지 않는다. Root가 스스로 새 pass를 만들어 budget을 갱신하지 않는다.
14. **No retry-by-uncertainty** — timeout, failure, incomplete result, disagreement, low confidence, missing evidence, refinement 또는 confirmation 필요는 자동 specialist 재호출 사유가 아니다.
15. **Refine evidence, not agents** — 추가 작업은 candidate disposition 또는 caller decision에 materially 영향을 줄 review state를 바꿀 credible information gain이 있을 때만 수행한다.
16. **Saturation terminates work** — 새 information gain이 없으면 더 깊은 탐색을 quality로 착각하지 않고 멈춘다.
17. **Coverage gaps stay visible** — unavailable capability, failed specialist, stale basis 또는 decisive unknown을 성공으로 흡수하지 않는다.
18. **Bounded final claim** — review result는 caller-provided basis, scope, coverage와 evidence에 대한 bounded signal이며 absolute correctness proof가 아니다.

이 invariant가 사라지면 파일명이나 agent 수가 같아도 같은 family로 보지 않는다.

## Non-goals

DualVantage는 다음을 목표로 하지 않는다.

- outer Run/Loop engine, RPI controller, workflow router 또는 task lifecycle owner
- Goal/Scope/Acceptance를 처음부터 정의하거나 caller 대신 변경하는 것
- artifact 생성 위치, durable state, report schema 또는 response schema를 소유하는 것
- user-facing final answer를 직접 구성하거나 presentation style을 강제하는 것
- 모든 defect를 찾는 exhaustive proof 또는 formal verification
- reviewer consensus, majority voting 또는 debate로 truth를 결정하는 구조
- Root까지 포함한 세 번의 full review
- 높은 severity를 이유로 current scope를 자동 확대하는 것
- specialist를 반복 호출해 답을 refinement하는 agent loop
- finding 수, source 수, 탐색 깊이 또는 token 사용량 자체의 최대화
- Challenger의 active exploit/reproduction 또는 Verifier의 broad unrestricted execution
- vendor-specific feature를 많이 사용하는 것 자체
- implementation, approval, merge 또는 remediation 수행

이 중 하나가 필요하면 DualVantage의 책임을 넓히기보다 그 책임을 이미 소유한 outer Skill/workflow/agent에 맡기거나 별도 owner가 필요한지 먼저 판단한다.

## Success criteria

Family가 목표대로 작동하면 다음을 관찰할 수 있어야 한다.

- `mols-loops` 같은 outer orchestrator나 다른 engine-like Skill 아래에 넣어도 outer procedure와 artifact/answer contract를 덮어쓰지 않는다.
- caller가 지정한 Goal/Scope/Acceptance를 review basis로 소비하고 스스로 outer task contract를 발명하지 않는다.
- Verifier와 Challenger가 실제로 다른 failure mode를 탐색한다.
- parallel-capable runtime에서는 두 specialist가 같은 delegation wave에서 실행된다.
- sequential-only runtime에서도 sibling result가 initial brief에 섞이지 않는다.
- candidate가 current state basis와 decisive observed evidence를 가진다.
- Verifier는 smallest decisive validation에 집중한다.
- Challenger는 `Assumption → Trigger → Reachable path → Expected defense → Observed gap → Impact → Falsifier`로 반례를 좁힌다.
- obvious counter-evidence가 candidate를 무효화하면 final finding으로 승격되지 않는다.
- Root가 third full review 없이 candidate를 adjudicate할 수 있다.
- issue impact와 current remediation authority가 분리된다.
- duplicate와 speculative claim이 review handoff에서 억제된다.
- specialist invocation은 bounded review당 최대 2회에서 끝난다.
- saturation 이후 no-op review churn이 발생하지 않는다.
- material coverage/evidence gap은 limitation 또는 blocker signal로 caller에게 보인다.
- caller가 원하는 artifact/response format을 그대로 유지할 수 있다.

## Goal failure signals

다음 변화는 단순 구현 차이가 아니라 Goal 훼손 신호다.

- DualVantage가 outer Run/Loop, phase transition, recursion 또는 completion을 직접 관리한다.
- 자체 artifact/report/state-file 형식이나 user-facing answer schema를 caller에게 강제한다.
- caller가 제공한 Goal/Scope보다 넓은 task boundary를 스스로 만든다.
- parallel-capable runtime에서 독립적인 두 specialist를 이유 없이 직렬 실행한다.
- 두 specialist가 같은 checklist와 같은 reasoning path로 수렴한다.
- 한 specialist의 conclusion을 다른 specialist의 initial brief에 넣는다.
- candidate를 underlying evidence 확인 없이 finding으로 채택한다.
- Root가 coverage gap을 직접 defect hunting으로 메운다.
- disagreement나 uncertainty를 이유로 specialist를 자동 재호출한다.
- Root가 내부적으로 새 review pass를 만들어 invocation budget을 초기화한다.
- high-impact issue라는 이유만으로 authorized scope를 확대한다.
- failed/incomplete specialist coverage를 clear signal로 숨긴다.
- 더 읽어도 판정이 바뀌지 않는데 탐색을 계속한다.
- finding 수 증가를 review quality 향상으로 취급한다.

## Change rule

Family의 구현을 바꿀 때는 먼저 **이 변경이 Goal을 보존하는가**를 판단한다.

- Goal을 보존하면 runtime/tool/wording/structure 수준의 개선으로 진행할 수 있다.
- Goal의 identity invariant를 바꿔야 하면 이유, 대안과 새로운 경계를 먼저 설계 결정으로 명시한다.
- Runtime behavior와 이 문서가 어긋나면 실행 사실은 runtime source에서 확인하되, 그 차이를 정상 상태로 방치하지 않는다.

세부 evidence/claim/review-state semantics는 [review-model.md](review-model.md), 역할·caller boundary·handoff·capability와 evolution 규칙은 [maintenance.md](maintenance.md)를 따른다.
