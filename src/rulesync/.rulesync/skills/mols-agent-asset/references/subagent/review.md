# Agent/Subagent Review

Agent/Subagent 리뷰는 직접 선택형 최상위 실행과 하위 위임을 구분하고, 실제 실행 역할에 맞는 책임·호출·권한·인계 경계를 중심으로 본다. 공통 기준은 `../common/review.md`를 따른다.

## Review axes

- **Need** — 직접 선택형 Agent로 독립적인 책임이 있는가, 또는 위임 실행이 specialization, isolation, capability, independence, coordination benefit을 제공하는가?
- **Responsibility** — 최상위라면 사용자·프로젝트와, 위임이라면 caller·sibling agent와 책임이 분리되며 delegation depth가 깊어질수록 더 구체적인 owner가 생기는가?
- **Invocation** — 사용자 선택·모델 위임·자동 호출의 허용 범위와 non-use가 구분되는가? 제한의 네이티브 강제 여부가 명확하며 generic fallback이나 relay agent가 되지 않는가?
- **Context** — handoff가 최소 충분한 state를 담고 irrelevant history, transcript, duplicated canonical knowledge를 싣지 않는가?
- **State basis** — revision/runtime state에 의존하는 handoff는 freshness를 확인할 단서가 있는가?
- **Independence** — runtime과 brief가 independence claim을 실제로 보존하는가?
- **Capabilities** — tool과 permission이 task에 필요한 최소이며 finalizing authority가 올바른 owner에 남아 있는가?
- **Result** — 최상위 실행의 사용자 또는 위임 실행의 caller가 reasoning transcript를 재구성하지 않고 answer, evidence state, unknown, next action을 사용할 수 있는가?
- **Durability** — durable artifact가 continuation cost를 줄이는가, 아니면 stale surface를 하나 더 만드는가?
- **Termination** — completion boundary가 명확하고 recursive/circular delegation이 없는가?
- **Failure visibility** — unavailable capability, incomplete context, blocked delegation이 visible한가?

Agent 수나 실행 계층만으로 finding을 만들지 않는다. 직접 선택형은 독립 책임, 위임형은 delegation boundary의 실질적 이점을 기준으로 판단한다.
