# Subagent Review

Subagent 리뷰는 delegation boundary와 handoff 품질을 중심으로 본다. 공통 기준은 `../common/review.md`를 따른다.

## Review axes

- **Need** — separate agent가 실제 specialization, isolation, capability, independence, coordination benefit을 제공하는가?
- **Responsibility** — caller와 sibling agent의 책임과 구분되며 delegation depth가 깊어질수록 더 구체적인 owner가 생기는가?
- **Delegation** — 호출 조건과 non-use가 구분되고 generic fallback이나 relay agent가 되지 않는가?
- **Context** — handoff가 최소 충분한 state를 담고 irrelevant history, transcript, duplicated canonical knowledge를 싣지 않는가?
- **State basis** — revision/runtime state에 의존하는 handoff는 freshness를 확인할 단서가 있는가?
- **Independence** — runtime과 brief가 independence claim을 실제로 보존하는가?
- **Capabilities** — tool과 permission이 task에 필요한 최소이며 finalizing authority가 올바른 owner에 남아 있는가?
- **Result** — caller가 reasoning transcript를 재구성하지 않고 answer, evidence state, unknown, next action을 사용할 수 있는가?
- **Durability** — durable artifact가 continuation cost를 줄이는가, 아니면 stale surface를 하나 더 만드는가?
- **Termination** — completion boundary가 명확하고 recursive/circular delegation이 없는가?
- **Failure visibility** — unavailable capability, incomplete context, blocked delegation이 visible한가?

Subagent 수 자체를 finding으로 만들지 않는다. 각 delegation boundary가 독립적인 책임과 실행 이점을 제공하는지가 핵심이다.
