# Agent/Subagent Design

Agent/Subagent 설계에서는 **자산 유형과 실행 역할**을 구분한다. 같은 정의가 런타임에 따라 사용자 선택형 최상위 Agent 또는 위임된 Subagent로 실행될 수 있으므로 실제 invocation, context, authority와 책임 경계를 먼저 본다. 공통 설계 원칙은 `../common/design.md`를 따른다.

## Need and responsibility

별도 Agent 정의는 사용자 직접 선택에 따른 독립적인 책임 또는 delegation에 따른 specialization, isolation, capability, independence, coordination benefit이 있을 때만 둔다.

- persona나 phase 이름만 바꾸기 위해 만들지 않는다.
- 하나의 responsibility를 정하고, 최상위 역할이면 사용자·프로젝트와의 경계, 위임 역할이면 caller·sibling agent와의 경계를 정한다.
- Agent가 소유하는 판단과 사용자·프로젝트·caller가 소유하는 판단을 실행 역할별로 분리한다.
- 같은 context와 capability로 항상 함께 수행되고 독립 결과나 reuse가 없으면 별도 agent가 coordination 비용만 늘리는지 본다.

## Invocation and delegation

- 사용자 직접 선택, 자동 선택, 다른 Agent의 위임 중 실제로 허용할 호출 주체와 실행 위치를 구분한다. 메인 전용 Agent도 유효한 별도 실행 단위다.
- 직접 선택 전용이나 위임 금지가 필요하면 런타임의 네이티브 제어를 우선하며, 지원하지 않는 차단을 prompt만으로 강제한다고 주장하지 않는다.
- 언제 호출하고 언제 호출하지 않는지 구분한다.
- generic fallback이 되도록 description을 넓히지 않는다.
- selection signal과 실제 delegated task brief를 구분한다.
- runtime이 제공하지 않는 independence, parallelism, nested delegation을 약속하지 않는다.
- delegation depth가 깊어질수록 responsibility와 context가 더 구체적으로 좁혀져야 한다. 전달만 하는 중간 agent를 만들지 않는다.

## Handoff

위임 시 assigned decision에 필요한 최소 충분한 context만 넘긴다. 최상위 실행은 사용자에게 유효한 결과와 다음 판단을 인계한다.

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
- 위임된 Agent의 destructive, publishing, merge, approval 같은 finalizing authority는 명시적 필요가 없으면 caller에 남긴다. 최상위 Agent도 사용자·프로젝트·런타임의 승인 경계를 넘어서는 권한을 갖지 않는다.
- tool 이름만으로 side effect나 permission semantics를 추정하지 않는다.
- 필요한 capability가 없으면 다른 동작으로 몰래 대체하지 말고 gap을 드러낸다.

## Result and termination

최상위 Agent에서는 사용자, 위임된 Agent에서는 caller가 reasoning을 재구성하지 않고 다음 행동을 결정할 수 있는 결과를 만든다. Answer/decision, 중요한 evidence, unresolved unknown, state basis, next owner 중 필요한 것만 포함한다.

완료 조건을 명확히 하고 open-ended recursion과 circular delegation을 만들지 않는다. Durable handoff artifact는 continuation cost를 실제로 줄일 때만 만든다.
