# Subagent Design

Agent 또는 Subagent 설계에만 필요한 판단을 다룬다. 공통 설계 원칙은 `../common/design.md`를 따른다.

## Existence and responsibility

별도 agent는 delegation이 실제 specialization, isolation, capability, independence, coordination benefit을 만들 때만 둔다.

- persona나 phase 이름만 바꾸기 위해 만들지 않는다.
- 하나의 coherent responsibility와 caller/sibling agent의 경계를 정한다.
- 어떤 판단을 subagent가 소유하고 어떤 판단을 caller가 유지하는지 분리한다.

## Delegation

- 언제 호출해야 하고 언제 호출하지 말아야 하는지 구분한다.
- generic fallback이 되도록 description을 넓히지 않는다.
- runtime이 제공하지 않는 independence, parallelism, nested delegation을 계약처럼 약속하지 않는다.

## Context

assigned decision에 필요한 최소 context를 전달한다.

- target과 relevant revision/state
- assigned question 또는 outcome
- in-scope / out-of-scope
- applicable authority와 known evidence
- required output contract

전체 conversation이나 다른 specialist의 결론을 기본으로 전달하지 않는다. Independence가 중요하면 다른 reviewer의 diagnosis를 brief에 섞지 않는다.

## Capability and termination

- 필요한 tool과 permission만 부여한다.
- mutation이 필요 없으면 read-only를 우선한다.
- destructive, publishing, merge, approval 같은 finalizing authority는 명시적 필요와 권한이 없으면 caller에 남긴다.
- caller가 재구성 없이 사용할 수 있는 result contract와 명확한 completion condition을 둔다.
- open-ended recursion과 circular delegation을 만들지 않는다.
