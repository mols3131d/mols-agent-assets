# Subagent Design

Agent 또는 Subagent 설계에만 필요한 판단을 다룬다. 공통 설계 원칙은 `../common/design.md`를 따른다.

## Existence and responsibility

별도 agent는 delegation이 실제 specialization, isolation, capability, independence 또는 coordination benefit을 만들 때만 둔다.

- persona나 phase 이름만 바꾸기 위해 만들지 않는다.
- 하나의 coherent responsibility와 caller/sibling agent의 경계를 정한다.
- 어떤 판단을 subagent가 소유하고 어떤 판단을 caller가 유지하는지 분리한다.
- 같은 context와 capability로 항상 함께 수행되고 독립 결과나 reuse가 없다면 별도 agent surface가 coordination 비용만 늘리는지 본다.

## Delegation

- 언제 호출해야 하고 언제 호출하지 말아야 하는지 구분한다.
- generic fallback이 되도록 description을 넓히지 않는다.
- coarse selection 정보와 실제 delegated task brief를 구분한다. 선택 신호에 task-specific detail을 모두 넣지 않는다.
- runtime이 제공하지 않는 independence, parallelism, nested delegation을 계약처럼 약속하지 않는다.
- delegation layer가 늘어날수록 responsibility와 context가 더 구체적으로 좁혀져야 한다. 단순 전달만 하는 중간 agent를 만들지 않는다.

## Context handoff

Assigned decision에 필요한 최소 충분한 context를 전달한다.

- target과 relevant revision 또는 observable state
- assigned question 또는 expected outcome
- in-scope / out-of-scope
- applicable authority와 known evidence
- unresolved unknown이나 blocker가 판단에 중요하면 그 상태
- required output contract와 다음 owner

전체 conversation, reasoning transcript, 모든 upstream artifact를 기본으로 전달하지 않는다. Canonical source에 이미 있는 규칙이나 큰 evidence는 복제하지 말고 필요한 identifier나 위치만 제공한다.

Independence가 중요하면 다른 specialist의 결론이나 speculative diagnosis를 brief에 섞지 않는다. Reconciliation이 목적일 때만 다른 의견을 명시적으로 전달한다.

Handoff가 session, worker, machine 또는 asynchronous boundary를 넘는다면 다음 실행이 상태의 freshness를 판단할 수 있도록 필요한 경우 revision이나 state basis를 포함한다. Durable state는 현재 truth보다 높은 authority가 아니며, 재개 시 현재 source와 중요한 state를 다시 확인할 수 있어야 한다.

## Capability and authority

- 필요한 tool과 permission만 부여한다.
- mutation이 필요 없으면 read-only를 우선한다.
- destructive, publishing, merge, approval 같은 finalizing authority는 명시적 필요와 권한이 없으면 caller에 남긴다.
- tool 이름만 보고 side effect나 safety를 추정하지 않고 target runtime의 실제 permission semantics를 따른다.
- required capability가 없으면 다른 동작으로 몰래 대체하기보다 gap을 caller에게 드러낸다.

## Result and termination

Caller가 reasoning을 재구성하지 않고 다음 행동을 결정할 수 있는 결과를 만든다.

필요에 따라 다음을 포함한다.

- answer, decision 또는 candidate findings
- 판단에 중요한 evidence basis
- unresolved unknown, blocked check 또는 coverage gap
- state가 특정 revision이나 runtime condition에 의존하면 그 기준점
- 다음 행동이 caller, 다른 specialist 또는 현재 agent 중 누구에게 속하는지

완료 조건을 명확히 하고 open-ended recursion과 circular delegation을 만들지 않는다. 별도 durable handoff artifact는 continuation cost를 실제로 줄일 때만 만들고, 짧은 delegation 결과로 충분하면 추가 artifact를 만들지 않는다.
