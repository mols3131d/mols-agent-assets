---
description: DualVantage의 caller/subagent ownership, independent·parallel delegation, capability, handoff와 invocation budget을 변경·복구할 때 사용합니다.
---

# DualVantage Maintenance

이 문서는 family의 **delegation, context injection, handoff, capability와 termination mechanics**를 유지보수할 때 사용한다. 변경 전 [goal.md](goal.md)를 먼저 확인하고 evidence/claim 의미는 [review-model.md](review-model.md)를 따른다.

## Ownership and roles

| Owner | Owns | Does not own |
| --- | --- | --- |
| outer caller / Skill / workflow / governing instruction | Goal/Scope/Acceptance, lifecycle, review policy, severity/status/disposition, artifact policy, user-facing response, implementation/mutation, final task decision | specialist 내부 exploration과 candidate construction |
| `mols-review-dualvantage` | review context admission/injection, two-specialist delegation, evidence-based candidate adjudication, deduplication, bounded handoff | specialist exploration, outer workflow/loop, review policy, artifact/answer format, third full review, scope expansion, implementation/approval/merge |
| `mols-review-dualvantage-verifier` | independent target/source/test/document exploration, intended behavior/contract/correctness, reachability, counter-evidence, smallest decisive non-mutating validation | Root adjudication, caller review policy, task-level decision/action |
| `mols-review-dualvantage-challenger` | independent target/source/configuration/document exploration, material assumption, realistic trigger, reachable counterexample, expected defense, falsifier | Root adjudication, caller review policy, task-level decision/action |

역할 차이는 persona가 아니라 **failure lens와 evidence method**의 차이다. Coverage가 부족해도 Root가 specialist perspective나 미완료 exploration을 대신 수행하지 않는다.

## Context injection vs. specialist exploration

**Root는 context를 준비한다. Worker는 review를 탐색한다.**

Root가 준비하는 것은 caller-provided basis와 현재 review에 실제 적용되는 Skill, Rule, governing instruction, contract, validation policy와 document다. 이것은 worker의 starting context이지 technical pre-review가 아니다.

Root는 다음을 하지 않는다.

- implementation/source/test를 미리 훑어 defect candidate를 만든다.
- worker 대신 reachable path, counterexample 또는 integration path를 추적한다.
- decisive evidence, counter-evidence 또는 validation target을 미리 선별한다.
- worker가 볼 파일/surface를 불필요하게 고정한다.
- worker가 아직 탐색하지 않은 영역을 adjudication 중 새 review pass처럼 대신 탐색한다.

각 worker는 injected context를 출발점으로 자기 역할에 필요한 target, source, test, configuration, state, related document와 evidence를 직접 찾는다.

## Context admission

Root가 context로 주입하는 항목도 아무 것이나 넣지 않는다.

1. **Applicability** — current target/review basis에 실제 적용되는가?
2. **Authority** — governing authority인가 reference인가?
3. **Scope** — 원래 scope와 precedence를 보존하고 있는가?
4. **Need** — worker가 assigned review를 시작하거나 contract를 해석하는 데 필요한가?
5. **Minimality** — 전체 내용 대신 path/identifier와 적용 범위로 충분한가?

Retrieval되었다는 이유만으로 instruction이 되지 않는다. Reference는 reference로 남기고 governing authority가 확인된 content만 해당 scope에서 instruction/contract로 적용한다.

두 worker에 공통으로 적용되는 context는 같은 shared package로 전달하고, 한 failure lens에만 필요한 governing context는 role-specific addendum으로 분리한다. Sibling finding/speculation/conclusion이나 Root가 미리 만든 defect hypothesis는 넣지 않는다.

### Runtime prompt boundary

Portability 배경, 특정 repository/framework 예시, projection path와 maintainer rationale는 **maintainer docs가 소유한다.** Runtime prompt에는 실제 행동을 바꾸는 operational contract만 둔다.

좋은 runtime rule은 다음처럼 직접적인 행동으로 표현된다.

- 적용되는 governing context의 authority/scope를 보존한다.
- 필요한 context만 주입한다.
- worker exploration을 대신하지 않는다.
- caller-owned review policy를 재정의하지 않는다.

“어떤 repository/framework를 가정하지 않는다”는 유지보수 목적은 docs에서 설명하고, runtime에는 그 목적을 달성하는 위 동작 계약만 남긴다.

## Review-policy composition

DualVantage는 자체 review policy engine을 두지 않는다.

Caller나 governing review asset이 admission, materiality, severity, blocking, disposition, completion 또는 required-action policy를 제공하면 Root는 그 의미를 보존해 사용한다. Worker에게 필요한 부분만 review-local context로 전달한다.

Policy가 없으면 DualVantage가 `PASS/FAIL`, `clear/blocked`, severity 또는 disposition vocabulary를 새로 만들지 않는다. Root의 고정 내부 state는 evidence accounting용 `confirmed | rejected | merged | unresolved`뿐이다.

## Brief and independence

두 specialist는 가능한 한 같은 최소 bounded basis를 받는다.

포함할 수 있는 내용은 target, state basis, caller-provided Goal/acceptance 중 review에 필요한 부분, in/out scope, authorized contract boundary, applicable context path/identifier와 authority/reference 구분, review-local criteria, caller가 이미 제공한 safeguard/validation evidence와 material limitation이다.

Initial brief에는 sibling finding/speculation/conclusion, caller의 hidden reasoning, 전체 implementation transcript, self-review 결론, Root의 pre-analysis와 assigned decision에 필요하지 않은 repository-wide context를 넣지 않는다.

## Parallel-first delegation

두 specialist 사이에는 data dependency가 없으므로 **independent concurrent execution이 가능한 runtime에서는 같은 delegation wave에서 둘 다 시작한다.**

- shared context package와 role-specific addendum만 병렬 dispatch 전에 확정한다.
- 어느 한쪽 결과를 읽은 뒤 다른 쪽의 exploration 방향을 바꾸지 않는다.
- 두 worker는 각자 독립적으로 target/evidence discovery를 수행한다.
- 두 specialist가 terminal result 또는 terminal failure에 도달한 뒤 Root가 adjudication을 시작한다.
- runtime, permission 또는 concurrency limit이 실제 병렬 실행을 제공하지 않을 때만 sequential fallback을 사용한다.
- sequential fallback에서도 먼저 끝난 result를 sibling brief/context에 추가하지 않는다.
- 실제 제공되지 않은 parallelism이나 isolation을 수행했다고 주장하지 않는다.

## Handoff

Specialist → Root handoff는 Root가 candidate를 확인할 만큼만 전달한다. 보통 target/location과 state basis, decisive observed evidence, inference, checked counter-evidence 또는 expected defense, validation/falsifier, material impact와 decision-relevant unknown이면 충분하다.

Root → caller handoff는 caller-owned format과 review-policy vocabulary를 따른다. 별도 artifact/report schema나 status taxonomy를 발명하지 않는다. Material candidate가 없으면 빈자리를 채우기 위한 finding을 만들지 않는다.

## Capability topology

```text
outer caller / orchestrator
           │
           ▼
    DualVantage Root
context read/search + delegation
           │
   ┌───────┴───────┐
   ▼               ▼
Verifier        Challenger
own exploration   own exploration
read/search +     read/search
focused check     no execution
   └──── no child delegation ────┘
```

Capability는 responsibility보다 넓지 않게 유지한다.

- Root의 read/search는 context admission과 candidate adjudication에 사용한다. Specialist technical exploration을 선행하는 용도로 넓히지 않는다.
- Root만 specialist delegation capability를 가진다.
- 지원되는 runtime에서는 Root 자체도 primary/user-facing agent가 아니라 internal/programmatic subagent로 제한한다.
- Verifier는 자기 exploration과 smallest decisive non-mutating validation에 필요한 read/search/execution을 가진다.
- Challenger는 자기 exploration에 필요한 read/search를 기본으로 하고 active attack/reproduction을 수행하지 않는다.
- Worker child delegation을 capability 수준에서 차단할 수 있으면 native mechanism을 우선한다.
- Runtime이 independence, parallelism 또는 permission boundary를 제공하지 않으면 제공했다고 주장하지 않는다.

Vendor-specific field와 tool alias는 빠르게 변할 수 있으므로 maintainer source에서 authoritative contract와 맞는지 확인하고 runtime prose에는 복제하지 않는다.

## Invocation budget

한 bounded review invocation의 자동 specialist 호출 budget은 **총 2회: Verifier 최대 1회 + Challenger 최대 1회**다.

- 호출을 시도하면 해당 1회를 사용한 것으로 본다.
- timeout, runtime/tool failure, empty/incomplete result에도 자동 retry하지 않는다.
- disagreement, low confidence, missing evidence, refinement, second opinion 또는 confirmation을 위해 재호출하지 않는다.
- 이후 Root 확인은 candidate adjudication에 필요한 evidence 대조 범위로 제한한다.
- worker가 하지 못한 discovery를 Root가 새 specialist pass처럼 대신 수행하지 않는다.
- decisive evidence/coverage가 부족하면 `unresolved` 또는 limitation으로 caller에게 반환한다.
- caller가 명시적으로 새 review pass를 요청한 경우에만 새 budget을 시작한다. Root가 내부적으로 pass를 재정의해 budget을 초기화하지 않는다.

Parallel execution은 invocation 수를 늘리는 허가가 아니다.

## Runtime changes

Vendor, model, tool schema 또는 projection이 바뀔 때는 기존 의미를 가장 직접적인 native mechanism으로 표현한다.

1. Root를 가능한 한 programmatic subagent-only surface로 유지한다.
2. Root에는 context admission과 adjudication에 필요한 최소 read/search만 유지한다.
3. Worker에는 자기 review exploration에 필요한 read/search capability를 충분히 유지한다.
4. Root delegation을 두 named specialist로 가장 좁게 제한한다.
5. Parallel-capable runtime에서는 두 specialist의 concurrent dispatch를 기본 경로로 유지한다.
6. Worker child delegation을 capability 수준에서 차단할 수 있으면 차단한다.
7. Verifier execution은 focused non-mutating validation에 필요한 범위만 연다.
8. Challenger는 read-only를 기본으로 유지한다.
9. Native capability가 부족하면 instruction으로 보완하되 실제보다 강한 isolation, parallelism 또는 permission을 주장하지 않는다.
10. Runtime prompt에는 operational contract만 남기고 target/framework-specific rationale는 maintainer docs에 둔다.

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
- outer workflow/loop, review policy, artifact 또는 user-facing response ownership을 가져오지 않았는가?
- Root가 context injection만 준비하고 specialist exploration을 대신하지 않는가?
- Verifier/Challenger가 injected context에 갇히지 않고 자기 역할에 필요한 evidence를 직접 탐색하는가?
- retrieval된 content를 검증 없이 governing instruction으로 승격하지 않는가?
- caller-provided severity/status/disposition 체계를 자체 taxonomy로 바꾸지 않는가?
- maintainer-only portability/rationale가 runtime prompt에 유입되지 않았는가?
- 두 specialist의 failure lens가 여전히 다른가?
- parallel-capable runtime에서 같은 delegation wave로 실행되도록 instruction/capability가 정렬되어 있는가?
- sibling result가 initial brief/context package에 새지 않는가?
- Root가 third reviewer로 커지거나 worker의 미완료 exploration을 대신하지 않는가?
- zero-finding 결과를 비정상으로 취급하거나 review effort를 정당화하려고 약한 candidate를 살려두지 않는가?
- capability가 responsibility보다 넓어지지 않았는가?
- worker child delegation과 hard invocation budget이 유지되는가?
- failure, stale state와 unavailable capability가 성공처럼 숨겨지지 않는가?

경계 명확화, context/duplication 감소, stronger evidence, independent exploration, parallel efficiency 또는 더 직접적인 handoff로 설명되지 않는 복잡성은 추가하지 않는다.
