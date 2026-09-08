---
description: mols-review-bivantage family의 목적, 본질, 역할 분리, evidence convergence와 유지보수 원칙을 판단할 때 사용합니다.
---

# Mols Review BiVantage

`mols-review-bivantage`는 하나의 reviewer가 가진 reasoning path와 failure mode에 review 품질이 과도하게 의존하지 않도록, **서로 다른 두 vantage를 독립적으로 만든 뒤 별도의 evidence gate에서 하나의 판단으로 수렴시키는 review family**다.

이 문서는 실행 prompt를 복제하지 않는다. 각 subagent의 tool, target, output contract와 runtime semantics는 대응하는 Agent Asset이 소유한다. 여기서는 구현이 바뀌어도 보존해야 할 목적, 본질, 책임 경계와 유지보수 판단을 기록한다.

## 목적

목적은 reviewer 수를 늘리는 것이 아니다.

1. 하나의 reasoning path가 놓치는 문제를 다른 실패 모드의 관점으로 보완한다.
2. discovery bias와 final judgment를 분리한다.
3. specialist가 생성한 claim을 underlying evidence에 다시 대조한다.
4. technically valid한 지적과 current Goal에서 반드시 고쳐야 하는 지적을 분리한다.
5. 추가 탐색이 더 이상 판정을 바꾸지 않는 지점에서 멈춰 signal density와 비용 효율을 지킨다.

즉 핵심은 다음이다.

```text
                         BiVantage
                            │
                 same bounded review brief
                  ┌─────────┴─────────┐
                  ▼                   ▼
             Verifier             Challenger
          evidence-first         challenge-first
          precision bias          recall bias
                  │                   │
                  └─────────┬─────────┘
                            ▼
                     Evidence Gate
          scope / authority / evidence / reachability
        attribution / counter-evidence / materiality
                            │
                            ▼
              clear | changes_required | blocked
```

**independent specialist discovery → evidence-gated adjudication → bounded final assessment**가 family의 기본 shape다.

## 이름의 의미

`BiVantage`에서 `bi`는 단순히 agent가 두 개라는 뜻이 아니다. 같은 target을 판단할 때 결과를 바꿀 수 있는 **두 개의 서로 다른 decision-relevant vantage**를 의미한다.

- Verifier vantage: "관찰 가능한 근거로 입증되는 material defect가 있는가?"
- Challenger vantage: "현재 동작이 의존하는 전제를 현실적인 trigger로 깨면 reachable failure가 생기는가?"
- Evidence gate: "이 candidate를 current Goal의 remediation 또는 blocker로 주장할 근거와 권한이 있는가?"

Root reviewer는 세 번째 vantage가 아니다. 두 vantage에서 나온 candidate를 판정하는 owner다.

## 본질

### 1. Two lenses, one gate

두 specialist가 서로 다른 질문을 가져야 separate execution의 가치가 생긴다. 같은 checklist를 다른 문구로 반복하면 agent 수만 늘고 독립 perspective 이점은 사라진다.

Verifier는 precision을, Challenger는 useful recall을 편향으로 가진다. Final gate는 다시 precision과 authority boundary를 우선한다.

### 2. Candidate claim과 finding을 분리한다

Specialist output은 final evidence가 아니다. Subagent가 자신이 발견한 문제의 최종 admission까지 소유하면 discovery bias, anchoring과 overclaim이 그대로 외부 결과가 된다.

따라서 specialist는 **falsifiable candidate**를 만들고, root reviewer가 underlying evidence와 current state를 확인한다.

`subagent output = candidate claim`, never proof by itself.

### 3. Reviewer consensus보다 evidence를 우선한다

두 specialist가 같은 결론에 도달해도 agreement는 evidence가 아니다. 서로 다른 결론에 도달해도 disagreement 자체가 어느 쪽을 약하게 만들지 않는다.

최종 판정은 다음에 의해 결정된다.

- source 또는 observable state에서 무엇을 직접 확인했는가
- 어떤 governing contract/authority가 적용되는가
- failure path가 실제로 reachable한가
- current target과 causal/acceptance relation이 있는가
- stronger counter-evidence나 safeguard가 있는가
- current Goal에서 실제 수정 가치와 권한이 있는가

### 4. Scope authority와 impact를 분리한다

High impact issue가 곧 current remediation은 아니다.

문제가 사실이어도 해결하려면 explicit Goal, Scope, Acceptance 또는 authorized contract-change boundary를 넓혀야 한다면 review는 그 확장을 승인하지 않는다. 반대로 작은 defect라도 current acceptance를 직접 깨면 current work에서 닫아야 할 수 있다.

따라서 **authority boundary를 materiality/severity보다 먼저 판정한다.** Severity는 impact를 설명할 뿐 scope authority를 mint하지 않는다.

### 5. Independence가 parallelism보다 중요하다

병렬 실행은 latency optimization이고, independence는 review-quality mechanism이다.

Runtime이 parallel subagent execution을 지원하지 않아도 순차 호출하면서 sibling 결과를 다음 brief에 넣지 않으면 independent perspective를 상당 부분 보존할 수 있다. 반대로 병렬 실행해도 두 agent에게 같은 speculative diagnosis나 implementation reasoning을 주입하면 독립성은 약해진다.

### 6. Single-pass delegation, adaptive evidence refinement

기본값은 각 specialist를 한 번 호출하는 것이다. 동일 specialist를 반복 호출해 토론시키거나 refinement loop를 만드는 것을 기본 전략으로 삼지 않는다.

반복이 필요한 곳은 agent invocation이 아니라 **evidence adjudication**이다. Root reviewer와 Verifier는 판정을 바꿀 credible information gain이 있는 동안에만 context 또는 validation을 한 단계씩 추가한다.

```text
candidate
   │
   ▼
smallest decisive evidence
   │
   ├─ disposition can change with next evidence? ─ yes ─► load/validate narrowly
   │                                                    │
   └─ no / saturated / decisive blocker ◄───────────────┘
   │
   ▼
terminal claim state
```

같은 evidence의 재표현, no-op search, finding 수를 채우기 위한 탐색은 refinement가 아니다.

### 7. Saturation은 실패가 아니라 stop signal이다

추가 탐색이 information gain, uncertainty reduction, verified quality gain 또는 acceptance closure로 이어질 credible path가 없으면 saturation이다.

Saturation에서 더 깊게 읽는 것은 품질이 아니라 churn이 될 수 있다. 다만 한 evidence source가 saturation이라는 이유만으로 아직 보지 않은 distinct material vantage까지 생략하지 않는다.

### 8. Freshness는 evidence 품질의 일부다

좋은 evidence라도 다른 revision, version 또는 stale observable state를 가리키면 current finding의 근거가 아닐 수 있다. Handoff와 candidate는 가능한 범위에서 state basis를 포함하고, root reviewer가 current review basis와 일치하는지 확인한다.

## 역할 경계

### `mols-review-bivantage`

Family의 public/root reviewer이자 evidence gate owner다.

소유하는 책임:

- bounded review brief와 current review basis
- Goal / Scope / Acceptance / authority boundary 파악
- Verifier와 Challenger의 independent delegation
- specialist coverage 확인
- candidate evidence validation과 disconfirmation
- reachability / attribution / materiality 판정
- conflict reconciliation
- scope disposition과 current remediation authority 판정
- duplicate/root-cause consolidation
- `clear | changes_required | blocked` final assessment

소유하지 않는 책임:

- Verifier가 놓친 correctness defect를 새로 hunting하는 것
- Challenger가 놓친 counterexample을 새로 발명하는 것
- 전체 artifact를 third full review하는 것
- review 결과를 근거로 Scope를 스스로 확대하는 것
- implementation, edit, approval 또는 merge를 수행하는 것

Coverage가 부족하면 직접 메우지 않고 coverage gap을 드러낸다.

### `mols-review-bivantage-verifier`

Evidence-first, precision-biased specialist다.

주요 질문:

> current target이 intended behavior, governing contract와 reachable integration path를 실제로 만족하는가?

핵심 책임:

- observed evidence와 inference를 분리한다.
- current state basis를 명확히 한다.
- caller/consumer/dependency를 필요한 범위만 추적한다.
- obvious counter-evidence를 먼저 확인한다.
- 가능하고 안전하면 smallest decisive non-mutating validation을 실행한다.
- material correctness/regression/contract candidate만 반환한다.

Maintainability는 그 자체가 목표가 아니다. 이미 구체적인 future correctness/reliability risk를 만들 때만 material review surface가 된다.

### `mols-review-bivantage-challenger`

Challenge-first, recall-biased specialist다.

주요 질문:

> current behavior가 성립하려면 무엇이 반드시 참이어야 하며, 그 전제를 realistic trigger로 깨면 어떤 reachable failure가 생기는가?

핵심 chain:

```text
Assumption
→ Trigger
→ Reachable path
→ Expected defense
→ Observed gap
→ Impact
→ Falsifier
```

Challenger는 가능성 목록을 만드는 agent가 아니다. Existing defense를 먼저 고려하고, caller가 확인할 falsification target이 있는 hypothesis만 반환한다.

## Evidence model

Family 전체에서 다음 세 층을 구분한다.

- **Observed** — source, configuration, contract, test, output 또는 current state에서 직접 확인한 사실
- **Inferred** — observed evidence에서 도출한 root cause, trigger, reachability, attribution 또는 impact
- **Unknown** — 필요한 runtime, state, contract, permission 또는 context가 없어 확인하지 못한 부분

Unknown을 Observed처럼 표현하지 않는다. Inference를 인용 가능한 source fact처럼 포장하지 않는다.

### Counter-evidence

Candidate admission 전에 가장 가까운 반증을 확인하는 것이 기본이다.

- stronger governing contract
- caller-provided invariant가 실제 source에서 확인되는지
- guard / permission / validation / serialization
- transaction / rollback / retry semantics
- compatibility layer
- unreachable state constraint
- current change가 intentional authorized delta인지

반증 탐색은 "모든 claim에 끝없이 반론하기"가 아니다. Candidate를 가장 싸고 강하게 falsify할 evidence가 있을 때 우선하는 전략이다.

## Claim lifecycle

Root reviewer의 내부 claim state는 다음과 같다.

| State | Meaning |
| --- | --- |
| `confirmed` | evidence, reasoning, reachability와 attribution이 충분함 |
| `rejected` | false, contradicted, unreachable, unsupported 또는 immaterial |
| `merged` | 다른 candidate와 같은 root cause로 통합됨 |
| `unresolved` | gate에 영향을 줄 수 있으나 decisive evidence가 부족함 |

이 state는 specialist의 confidence label이나 reviewer agreement로 정하지 않는다.

## Scope disposition

Confirmed/unresolved item과 current Goal의 관계는 다음처럼 분류한다.

| Disposition | Meaning |
| --- | --- |
| `current_required` | authorized boundary 안에서 해결할 수 있고 current Goal acceptance에 반드시 필요함 |
| `scope_decision` | 해결하려면 Goal/Scope/Acceptance/authorized contract boundary 확대 결정이 필요함 |
| `follow_up` | valid하지만 current Goal completion에 필수적이지 않은 독립 요구사항 |
| `unrelated` | current target과 causal/material relation이 없음 |
| `unknown` | relation 또는 impact를 확정할 evidence가 부족함 |

`current_required`만 직접 `changes_required` 근거가 된다.

`scope_decision`은 그 결정 없이는 current Goal acceptance 판단 자체가 불가능할 때 blocker가 된다. 그렇지 않으면 decision/follow-up으로 분리한다.

`follow_up`과 `unrelated`는 impact가 높아도 current remediation 권한을 만들지 않는다.

`unknown`은 current Goal gate에 decisive할 때만 blocker다. 그렇지 않으면 limitation이다.

## Final assessment

Final output은 정확히 하나의 gate state를 가진다.

1. `blocked` — required coverage, decisive evidence, current review basis 또는 scope authority 부족으로 independent gate를 신뢰성 있게 닫을 수 없음
2. `changes_required` — blocker가 없고 confirmed `current_required` finding이 하나 이상 있음
3. `clear` — 위 둘이 모두 없음

Precedence는 `blocked > changes_required > clear`다.

이 assessment는 absolute correctness proof가 아니다. 명시한 review basis, scope, coverage와 evidence에 대한 bounded independent assessment다.

## 유지보수 원칙

### 역할 차이를 보존한다

Verifier와 Challenger가 같은 checklist로 수렴하면 separate agent justification을 다시 검토한다. 역할 차이는 persona가 아니라 failure lens와 evidence method의 차이여야 한다.

### Root를 third reviewer로 키우지 않는다

Root quality는 더 많은 defect hunting이 아니라 더 강한 admission gate에서 나온다. Root가 새 bug를 찾기 시작하면 specialist coverage gap이 숨겨지고 review 비용도 세 배 구조로 커진다.

### Handoff는 최소 충분해야 한다

Specialist output만으로 root가 candidate를 독립 검증할 수 있어야 하지만 full repository summary나 reasoning transcript까지 전달할 필요는 없다.

좋은 handoff에는 target/location, state basis, decisive observed evidence, inference, counter-evidence, validation/falsifier와 material unknown이 있다.

### Tool은 responsibility에 맞춘다

Verifier는 smallest decisive validation을 위해 execution capability가 필요할 수 있다. Challenger는 기본적으로 read/search만으로 challenge하고 active attack을 수행하지 않는다. Root는 read/search/delegation만 필요하다.

### Signal density를 최적화한다

Finding 수, agent 수, source 수, token 수는 quality metric이 아니다.

좋은 결과는 다음 특징을 가진다.

- distinct root cause만 남는다.
- final finding이 underlying evidence에서 독립 검증 가능하다.
- speculative candidate가 gate에서 제거된다.
- actionable current finding과 scope/follow-up이 섞이지 않는다.
- 중요한 unknown과 coverage gap이 성공처럼 흡수되지 않는다.
- 추가 evidence가 더 이상 판정을 바꾸지 않을 때 멈춘다.

### 새 specialist는 쉽게 추가하지 않는다

세 번째 specialist는 다음을 모두 만족할 때만 고려한다.

- Verifier/Challenger와 다른 decision-relevant failure lens가 있다.
- 별도 context isolation이 실제 결과 품질을 높인다.
- 자주 independent activation 또는 reuse할 이유가 있다.
- coordination/token cost보다 material benefit이 크다.

단순한 domain label, phase 이름 또는 persona 다양화만으로 specialist를 추가하지 않는다.

## 성공 기준

BiVantage가 잘 작동한다는 것은 많은 finding을 생성한다는 뜻이 아니다.

- Verifier와 Challenger가 실제로 다른 failure mode를 탐색한다.
- 두 specialist의 initial analysis가 independent하다.
- candidate가 observable evidence와 state basis를 가진다.
- Challenger hypothesis가 trigger/path/defense/falsifier를 가진다.
- Verifier validation이 smallest decisive check에 집중한다.
- Root가 third full review를 하지 않고도 candidate를 adjudicate할 수 있다.
- scope authority와 issue impact가 섞이지 않는다.
- false positive와 duplicate가 final output에서 억제된다.
- final gate가 `clear | changes_required | blocked`로 명확하다.
- saturation에서 멈추고 no-op review churn을 만들지 않는다.

## 변경할 때 보존할 것

Vendor, model, tool alias, runtime API와 projection format은 바뀔 수 있다. 다음 조건은 구현이 바뀌어도 family의 본질로 보존한다.

1. 서로 다른 두 decision-relevant review vantage를 유지한다.
2. 두 vantage의 initial discovery를 가능한 한 독립적으로 유지한다.
3. specialist output을 candidate claim으로 취급한다.
4. final judgment는 별도의 evidence gate가 소유한다.
5. evidence gate는 third full review가 아니라 validation, authority와 admission을 소유한다.
6. observed / inferred / unknown을 구분한다.
7. scope authority를 severity보다 먼저 판정한다.
8. reviewer agreement를 correctness proof로 사용하지 않는다.
9. additional work는 credible information gain이 있을 때만 수행하고 saturation에서 멈춘다.
10. material coverage/evidence gap을 성공으로 흡수하지 않는다.
11. false-positive suppression과 actionable signal을 finding 수보다 우선한다.

이 조건이 사라지면 파일명이나 agent 수가 유지되어도 더 이상 BiVantage라고 보기 어렵다.
