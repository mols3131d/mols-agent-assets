---
description: DualVantage의 caller/subagent ownership, independent·parallel delegation, capability, handoff와 invocation budget을 변경·복구할 때 사용합니다.
---

# DualVantage Maintenance

이 문서는 family의 **delegation, handoff, capability와 termination mechanics**를 유지보수할 때 사용한다. 변경 전 [goal.md](goal.md)를 먼저 확인하고, evidence/claim/review-state 의미는 [review-model.md](review-model.md)를 따른다.

## Ownership and roles

| Owner | Owns | Does not own |
| --- | --- | --- |
| caller / outer Skill / workflow / governing instruction | outer Goal/Scope, lifecycle, artifact policy, user-facing response, implementation/mutation, final task completion | specialist 내부 review procedure |
| `mols-review-dualvantage` | bounded brief, two-specialist delegation, candidate adjudication, scope/authority relation, review handoff | outer workflow/loop, artifact/answer format, third full review, scope expansion, implementation/approval/merge |
| `mols-review-dualvantage-verifier` | intended behavior/contract/correctness, reachability, counter-evidence, smallest decisive non-mutating validation | broad hypothesis generation, final authority, caller-facing response |
| `mols-review-dualvantage-challenger` | material assumption, realistic trigger, reachable counterexample, expected defense, falsifier | general correctness checklist, active attack/reproduction, final authority, caller-facing response |

역할 차이는 persona가 아니라 **failure lens와 evidence method**의 차이다. Coverage가 부족해도 Root가 specialist perspective를 대신 수행하지 않고 limitation 또는 blocker signal로 caller에게 돌려준다.

## Brief and independence

두 specialist는 가능한 한 같은 최소 bounded brief를 받는다.

필요한 내용은 target, current state basis, caller-provided Goal/acceptance 중 review에 필요한 부분, in/out scope, authorized contract boundary, governing instruction/contract, known safeguard와 material validation evidence다.

Initial brief에는 sibling finding/speculation/conclusion, caller의 hidden reasoning, 전체 implementation transcript, self-review 결론을 evidence처럼 보이게 하는 서술과 assigned decision에 필요하지 않은 repository-wide context를 넣지 않는다.

## Parallel-first delegation

두 specialist 사이에는 data dependency가 없으므로 **independent concurrent execution이 가능한 runtime에서는 같은 delegation wave에서 둘 다 시작한다.**

- 어느 한쪽 결과를 읽은 뒤 다른 쪽을 호출하는 serial path를 parallel-capable runtime의 기본으로 사용하지 않는다.
- 두 specialist가 terminal result 또는 terminal failure에 도달한 뒤 Root가 adjudication을 시작한다.
- runtime, permission 또는 concurrency limit이 실제 병렬 실행을 제공하지 않을 때만 sequential fallback을 사용한다.
- sequential fallback에서도 먼저 끝난 result를 sibling brief에 추가하지 않는다.
- 실제 제공되지 않은 parallelism이나 isolation을 수행했다고 주장하지 않는다.

## Handoff

Specialist → Root handoff는 Root가 전체 context를 재구성하지 않고 candidate를 확인할 만큼만 전달한다. 보통 target/location과 state basis, decisive observed evidence, 실제 inference, checked counter-evidence 또는 expected defense, validation/falsifier, material impact와 decision-relevant unknown이면 충분하다.

Full repository summary, reasoning transcript와 canonical knowledge를 복제하지 않는다.

Root → caller handoff는 caller-owned format을 따른다. 별도 artifact/report schema를 발명하지 않고 reviewed basis, material finding, scope/authority issue와 useful limitation처럼 다음 owner의 판단에 필요한 의미만 전달한다. Material finding이 없으면 빈자리를 채우기 위한 finding을 만들지 않고, 필요한 review basis와 `clear` 의미만 전달할 수 있다.

## Capability topology

```text
caller / outer orchestrator
           │
           ▼
    DualVantage Root
 read/search + delegation
           │
   ┌───────┴───────┐
   ▼               ▼
Verifier        Challenger
read/search +   read/search
focused check   no execution
   └──── no child delegation ────┘
```

Capability는 responsibility보다 넓지 않게 유지한다.

- Root만 specialist delegation capability를 가진다.
- 지원되는 runtime에서는 Root 자체도 primary/user-facing agent가 아니라 internal/programmatic subagent로 제한한다.
- Verifier만 smallest decisive non-mutating validation에 필요한 제한적 execution을 가진다.
- Challenger는 read/search를 기본으로 하고 active attack/reproduction을 수행하지 않는다.
- Worker child delegation을 capability 수준에서 차단할 수 있으면 instruction보다 native mechanism을 우선한다.
- Runtime이 independence, nested delegation, parallelism 또는 permission boundary를 제공하지 않으면 제공했다고 주장하지 않는다.

Vendor-specific field와 tool alias는 빠르게 변할 수 있으므로 이 문서에 고정하지 않는다. Target runtime과 source framework의 current authoritative contract를 확인하고 reusable core에는 의미만 유지한다.

## Invocation budget

한 bounded review invocation의 자동 specialist 호출 budget은 **총 2회: Verifier 최대 1회 + Challenger 최대 1회**다.

- 호출을 시도하면 해당 1회를 사용한 것으로 본다.
- timeout, runtime/tool failure, empty/incomplete result에도 자동 retry하지 않는다.
- disagreement, low confidence, missing evidence, refinement, second opinion 또는 confirmation을 위해 재호출하지 않는다.
- 이후 확인은 Root의 read/search와 authoritative evidence로 수행한다.
- decisive evidence/coverage가 부족하면 unresolved/limitation/blocker signal로 caller에게 반환한다.
- caller가 명시적으로 새 review pass를 요청한 경우에만 새 budget을 시작한다. Root가 내부적으로 pass를 재정의해 budget을 초기화하지 않는다.

Parallel execution은 invocation 수를 늘리는 허가가 아니다.

## Runtime changes

Vendor, model, tool schema 또는 projection이 바뀔 때는 기존 의미를 가장 직접적인 native mechanism으로 표현한다.

1. Root를 가능한 한 programmatic subagent-only surface로 유지한다.
2. Root delegation을 두 named specialist로 가장 좁게 제한한다.
3. Parallel-capable runtime에서는 두 specialist의 concurrent dispatch를 기본 경로로 유지한다.
4. Worker child delegation을 capability 수준에서 차단할 수 있으면 차단한다.
5. Verifier execution은 focused non-mutating validation에 필요한 범위만 연다.
6. Challenger는 read-only를 기본으로 유지한다.
7. Native capability가 부족하면 instruction으로 보완하되 실제보다 강한 isolation, parallelism 또는 permission을 주장하지 않는다.
8. Vendor delta는 target-specific configuration에 두고 reusable core에 복제하지 않는다.

[goal.md](goal.md)의 identity invariant를 지킬 수 없는 runtime 제한은 숨기지 않고 degraded capability 또는 redesign 필요로 기록한다.

## Specialist evolution

새 specialist를 추가하거나 기존 역할을 대체하려면 다음이 모두 성립해야 한다.

- 기존 두 역할과 다른 decision-relevant failure lens가 있다.
- 별도 context/isolation이 실제 품질 이점을 만든다.
- 독립 activation/loading/reuse 또는 ownership 가치가 있다.
- Root가 직접 수행하면 안 되는 distinct discovery responsibility가 있다.
- coordination/context/token 비용보다 기대 signal gain이 크다.
- 새 역할 때문에 current ownership boundary가 모호해지지 않는다.

기존 checklist를 나누거나 reviewer 수만 늘리는 변경이면 추가하지 않는다.

## Maintenance checks

변경 후 다음을 확인한다.

- [goal.md](goal.md)의 identity invariant가 유지되는가?
- outer workflow/loop, artifact 또는 user-facing response ownership을 가져오지 않았는가?
- caller-provided Goal/Scope를 소비하고 outer task contract를 발명하지 않는가?
- 두 specialist의 failure lens가 여전히 다른가?
- parallel-capable runtime에서 같은 delegation wave로 실행되도록 instruction/capability가 정렬되어 있는가?
- sibling result가 initial brief에 새지 않는가?
- Root가 third reviewer로 커지지 않았는가?
- zero-finding 결과를 비정상으로 취급하거나 review effort를 정당화하려고 약한 candidate를 살려두지 않는가?
- capability가 responsibility보다 넓어지지 않았는가?
- worker child delegation과 hard invocation budget이 유지되는가?
- handoff가 next owner 판단에 충분하면서 reasoning transcript나 format ownership을 복제하지 않는가?
- failure, stale state와 unavailable capability가 성공처럼 숨겨지지 않는가?

경계 명확화, context/duplication 감소, stronger evidence, parallel efficiency 또는 더 직접적인 handoff로 설명되지 않는 복잡성은 추가하지 않는다.
