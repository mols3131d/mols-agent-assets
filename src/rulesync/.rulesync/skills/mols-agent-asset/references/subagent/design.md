# Subagent Design

Subagent 설계에서는 별도 실행 단위가 필요한지, 어떤 context와 authority를 넘길지 먼저 본다. 공통 설계 원칙은 `../common/design.md`를 따른다.

## Need and responsibility

별도 agent는 delegation이 실제 specialization, isolation, capability, independence, coordination benefit을 만들 때만 둔다.

- persona나 phase 이름만 바꾸기 위해 만들지 않는다.
- 하나의 responsibility와 caller/sibling agent의 경계를 정한다.
- 어떤 판단을 subagent가 소유하고 무엇을 caller가 유지하는지 분리한다.
- 같은 context와 capability로 항상 함께 수행되고 독립 결과나 reuse가 없으면 별도 agent가 coordination 비용만 늘리는지 본다.

## Delegation

- 언제 호출하고 언제 호출하지 않는지 구분한다.
- generic fallback이 되도록 description을 넓히지 않는다.
- selection signal과 실제 delegated task brief를 구분한다.
- runtime이 제공하지 않는 independence, parallelism, nested delegation을 약속하지 않는다.
- delegation depth가 깊어질수록 responsibility와 context가 더 구체적으로 좁혀져야 한다. 전달만 하는 중간 agent를 만들지 않는다.

## Handoff

Assigned decision에 필요한 최소 충분한 context만 넘긴다.

- target과 relevant revision 또는 observable state
- assigned question 또는 expected outcome
- in-scope / out-of-scope
- applicable authority와 known evidence
- 판단에 중요한 unknown 또는 blocker
- required output contract와 next owner

전체 conversation, reasoning transcript, 모든 upstream artifact를 기본으로 넘기지 않는다. Canonical source에 이미 있는 지식은 복제하지 않고 필요한 identifier나 위치만 전달한다.

Independence가 중요하면 다른 specialist의 결론이나 speculative diagnosis를 brief에 섞지 않는다. Handoff가 session, worker, machine boundary를 넘으면 필요한 경우 revision이나 state basis를 포함하고, 재개 시 현재 source와 다시 확인할 수 있게 한다.

## Capabilities

- responsibility에 필요한 tool과 permission만 부여한다.
- mutation이 필요 없으면 read-only를 우선한다.
- destructive, publishing, merge, approval 같은 finalizing authority는 명시적 필요가 없으면 caller에 남긴다.
- tool 이름만으로 side effect나 permission semantics를 추정하지 않는다.
- 필요한 capability가 없으면 다른 동작으로 몰래 대체하지 말고 gap을 드러낸다.

## Result and termination

Caller가 reasoning을 재구성하지 않고 다음 행동을 결정할 수 있는 결과를 만든다. Answer/decision, 중요한 evidence, unresolved unknown, state basis, next owner 중 필요한 것만 포함한다.

완료 조건을 명확히 하고 open-ended recursion과 circular delegation을 만들지 않는다. Durable handoff artifact는 continuation cost를 실제로 줄일 때만 만든다.
