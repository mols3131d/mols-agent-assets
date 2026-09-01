# Subagent Review

Agent 또는 Subagent review에만 필요한 축을 다룬다. 공통 review 기준은 `../common/review.md`를 따른다.

- **Need** — separate agent가 실제 specialization, isolation, capability, independence, coordination benefit을 제공하는가?
- **Responsibility** — caller와 sibling agent의 책임과 구분되는가?
- **Delegation** — 호출 조건과 non-use가 구분되는가?
- **Context** — handoff가 충분하지만 irrelevant history나 다른 specialist의 결론으로 오염되지 않았는가?
- **Capabilities** — tool과 permission이 task에 필요한 최소인가?
- **Independence** — independence claim을 runtime과 brief가 실제로 보존할 수 있는가?
- **Result contract** — caller가 hidden assumption 없이 결과를 사용할 수 있는가?
- **Termination** — completion boundary가 명확하고 recursive/circular delegation이 없는가?
- **Failure behavior** — unavailable capability, incomplete context, blocked delegation이 visible한가?
- **Portability** — target-specific field와 runtime semantics를 portable responsibility contract와 섞지 않았는가?
