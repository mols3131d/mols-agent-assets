---
description: DualVantage의 역할 경계, handoff, capability topology, 호출 예산과 runtime 변화 시 유지보수 기준을 설명하는 문서입니다.
---

# DualVantage Maintenance

이 문서는 DualVantage의 역할과 실행 경계를 변경·복구할 때 사용하는 maintainer 기준이다. 변경 전 [goal.md](goal.md)를 먼저 확인한다. Evidence/claim/gate semantics는 [review-model.md](review-model.md)가 소유한다.

## Role boundaries

| Role | Owns | Does not own |
| --- | --- | --- |
| `mols-review-dualvantage` | bounded brief, independent delegation, evidence gate, scope/authority, reconciliation, deduplication, final assessment | third full review, 새 defect/counterexample hunting, scope expansion, implementation/approval/merge |
| `mols-review-dualvantage-verifier` | intended behavior/contract/correctness 검증, reachability, counter-evidence, smallest decisive non-mutating validation | broad hypothesis generation, final disposition/authority |
| `mols-review-dualvantage-challenger` | material assumption, realistic trigger, reachable counterexample, expected defense, falsifier | general correctness checklist, active attack/reproduction, final disposition/authority |

역할 차이는 persona가 아니라 **failure lens와 evidence method**의 차이여야 한다. Verifier와 Challenger가 같은 checklist로 수렴하면 separate agent justification을 다시 검토한다.

Coverage가 부족해도 Root가 specialist perspective를 대신 수행하지 않는다. Gap을 limitation 또는 blocker로 드러내는 것이 family contract다.

## Brief and independence

두 specialist는 가능한 한 같은 최소 bounded brief를 받는다.

필요한 내용은 target, current state basis, Goal/acceptance, in/out scope, authorized contract boundary, governing instruction/contract, known safeguard와 material validation evidence다.

다음은 initial brief에서 제외한다.

- sibling reviewer의 finding, speculation 또는 conclusion
- caller의 hidden reasoning이나 전체 implementation transcript
- self-review 결론을 evidence처럼 보이게 하는 서술
- assigned decision에 필요하지 않은 repository-wide context

병렬 실행은 latency optimization이다. Independence가 더 중요하다. 병렬 실행이 없어도 sibling result를 다음 specialist brief에 섞지 않으면 핵심 구조를 보존할 수 있다.

## Handoff

Specialist output은 Root가 전체 context를 다시 재구성하지 않고 candidate를 확인할 수 있을 만큼만 전달한다.

좋은 handoff에는 다음이 있다.

- target/location과 state basis
- decisive observed evidence
- 실제 inference
- checked counter-evidence 또는 expected defense
- validation 또는 falsifier
- material impact
- final 판정을 바꿀 수 있는 unknown

Full repository summary, reasoning transcript와 canonical knowledge 복제는 필요하지 않다.

## Capability topology

Capability는 responsibility보다 넓지 않게 유지한다.

```text
                     DualVantage Root
                 read/search + delegation
                           │
                 ┌─────────┴─────────┐
                 ▼                   ▼
             Verifier            Challenger
          read/search +          read/search
       focused validation       no execution
                 │                   │
                 └── no child delegation ──┘
```

- Root만 specialist delegation capability를 가진다.
- Verifier는 smallest decisive non-mutating validation에 필요한 제한적 execution만 가진다.
- Challenger는 기본적으로 read/search만 사용하고 active attack/reproduction을 수행하지 않는다.
- Worker는 다른 agent를 호출하지 않는다. Runtime이 capability-level 차단을 제공하면 instruction보다 그 mechanism을 우선한다.
- Runtime이 independence, nested delegation 또는 permission boundary를 실제 제공하지 않으면 제공했다고 주장하지 않는다.

Vendor-specific field나 tool alias는 빠르게 변할 수 있다. 의미를 이 문서에 고정하지 말고 target runtime과 source framework의 current authoritative contract를 확인한다.

## Invocation budget

한 review run의 자동 specialist 호출 budget은 **총 2회: Verifier 최대 1회 + Challenger 최대 1회**다.

- 호출을 시도하면 해당 1회를 사용한 것으로 본다.
- timeout, runtime/tool failure, empty/incomplete result에도 자동 retry하지 않는다.
- disagreement, low confidence, missing evidence, refinement, second opinion 또는 confirmation을 위해 재호출하지 않는다.
- 이후 확인은 Root의 read/search와 authoritative evidence로 수행한다.
- decisive evidence/coverage가 부족하면 `unresolved`, limitation 또는 `blocked`로 남긴다.
- caller가 명시적으로 새 review pass를 요청한 경우에만 새 budget을 시작한다. Root가 내부적으로 pass를 재정의해 budget을 초기화하지 않는다.

이 제한은 비용 최적화만을 위한 것이 아니라 independence와 termination을 보장한다.

## Runtime changes

Vendor, model, tool schema 또는 projection이 바뀔 때는 먼저 native mechanism으로 기존 topology를 표현할 수 있는지 본다.

1. Root delegation을 가장 좁게 제한한다.
2. Worker child-delegation을 capability 수준에서 차단할 수 있으면 차단한다.
3. Verifier execution은 non-mutating focused validation에 필요한 범위만 연다.
4. Challenger는 read-only를 기본으로 유지한다.
5. Native capability가 부족하면 instruction으로 보완하되 실제보다 강한 isolation/parallelism/permission을 주장하지 않는다.
6. Vendor delta를 reusable core에 복제하지 않고 target-specific configuration으로 제한한다.

Runtime 차이 때문에 [goal.md](goal.md)의 identity invariant를 지킬 수 없다면 그 제한을 숨기지 말고 degraded capability 또는 redesign 필요로 기록한다.

## Adding or replacing a specialist

새 specialist는 이름이나 coverage 욕심만으로 추가하지 않는다. 다음이 모두 성립할 때만 고려한다.

- 기존 Verifier/Challenger와 다른 decision-relevant failure lens가 있다.
- 별도 context/isolation이 실제 품질 이점을 만든다.
- 독립 activation/loading/reuse 또는 ownership 가치가 있다.
- Root가 직접 수행하면 안 되는 distinct discovery responsibility가 있다.
- coordination, context와 token 비용보다 기대 signal gain이 크다.
- 새 역할 때문에 current roles의 경계가 모호해지지 않는다.

단지 기존 두 역할의 checklist를 나누거나 reviewer 수를 늘리는 변경이면 추가하지 않는다.

## Maintenance checks

변경 후 다음을 확인한다.

- [goal.md](goal.md)의 identity invariant가 모두 유지되는가?
- 두 specialist의 질문과 failure lens가 여전히 명확히 다른가?
- sibling result가 initial brief에 새어 들어가지 않는가?
- Root가 third reviewer로 커지지 않았는가?
- capability가 role responsibility보다 넓어지지 않았는가?
- worker의 child delegation이 가능한 runtime에서 적절히 차단되는가?
- hard invocation budget과 no-auto-retry가 유지되는가?
- handoff가 Root 판단에 충분하면서 reasoning transcript를 복제하지 않는가?
- failure, stale state와 unavailable capability가 성공처럼 숨겨지지 않는가?
- 새 context, agent, rule 또는 abstraction이 실제 independent value를 만드는가?

변경의 이점이 경계 명확화, context/duplication 감소, stronger evidence 또는 더 직접적인 handoff로 설명되지 않으면 추가 복잡성을 만들지 않는다.
