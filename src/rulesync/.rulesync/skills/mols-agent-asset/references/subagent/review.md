# Subagent Review

Agent 또는 Subagent review에만 필요한 축을 다룬다. 공통 review 기준은 `../common/review.md`를 따른다.

- **Need** — separate agent가 실제 specialization, isolation, capability, independence 또는 coordination benefit을 제공하는가?
- **Responsibility** — caller와 sibling agent의 책임과 구분되고 delegation depth가 깊어질수록 더 구체적인 owner가 생기는가?
- **Delegation** — 호출 조건과 non-use가 구분되는가? generic fallback이나 의미 없는 relay agent가 되지 않는가?
- **Context** — handoff가 최소 충분한 state를 포함하면서 irrelevant history, transcript, duplicated canonical knowledge를 싣지 않는가?
- **State basis** — handoff가 revision/runtime state에 의존하면 freshness를 확인할 단서가 있는가? 오래된 handoff를 current truth로 취급하지 않는가?
- **Independence** — independence claim을 runtime과 brief가 실제로 보존할 수 있는가? 다른 specialist의 결론이 불필요하게 contamination되지 않았는가?
- **Capabilities** — tool과 permission이 task에 필요한 최소인가? finalizing authority가 적절한 owner에 남아 있는가?
- **Result contract** — caller가 reasoning transcript를 재구성하지 않고 answer, evidence state, unknown, next action을 사용할 수 있는가?
- **Durability** — durable artifact가 실제 continuation cost를 줄이는가, 아니면 기존 source와 중복되는 stale surface를 하나 더 만드는가?
- **Termination** — completion boundary가 명확하고 recursive/circular delegation이 없는가?
- **Failure behavior** — unavailable capability, incomplete context, blocked delegation이 visible한가?
- **Portability** — target-specific field와 runtime semantics를 portable responsibility contract와 섞지 않았는가?

Subagent 수가 많다는 사실 자체를 finding으로 만들지 않는다. 각 delegation boundary가 독립적인 책임과 실행 이점을 제공하는지가 핵심이다.
