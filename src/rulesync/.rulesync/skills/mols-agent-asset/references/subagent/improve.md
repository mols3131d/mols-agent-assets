# Subagent Improve

Subagent 개선은 agent 수를 늘리기보다 responsibility와 handoff를 더 직접적으로 만드는 데 집중한다. 공통 개선 원칙은 `../common/improve.md`를 따른다.

## Signals

- separate agent가 실제 benefit 없이 존재한다.
- responsibility가 caller나 sibling과 겹친다.
- delegation condition이 너무 넓거나 모호하다.
- 여러 delegation hop이 context를 좁히지 않고 전달만 한다.
- handoff가 과도하거나 필요한 authority, state basis, unknown이 빠져 있다.
- full conversation, reasoning transcript, canonical knowledge를 불필요하게 복제한다.
- tool/permission이 responsibility보다 넓다.
- independence를 주장하지만 runtime이나 brief가 이를 보존하지 못한다.
- result contract나 termination condition이 불명확하다.
- stale handoff를 current truth처럼 사용한다.
- failure가 caller에게 보이지 않고 성공처럼 흡수된다.

## Improve

- specialization, isolation, capability, independence, coordination benefit이 없는 delegation layer는 제거하거나 caller에 흡수한다.
- context는 assigned decision에 필요한 최소 충분한 state로 줄이고 canonical knowledge를 복제하지 않는다.
- independence가 목적이면 다른 reviewer의 결론과 speculative diagnosis를 brief에서 제거한다.
- session/worker boundary를 넘는 handoff는 목표, current state, 중요한 evidence, unknown, next owner와 필요한 state basis만 남긴다.
- stale handoff는 현재 source와 revision을 확인해 갱신하거나 폐기한다.
- capability는 responsibility에 맞게 줄이고 unavailable capability와 incomplete evidence를 드러낸다.
- caller가 결과를 쓰기 위해 전체 context를 재구성해야 한다면 result contract를 더 직접적으로 만든다.
- 새 owner나 더 구체적인 responsibility가 생기지 않는 recursion과 circular handoff는 제거한다.

Durable artifact 자체를 개선으로 간주하지 않는다. Continuation cost가 충분히 크고 기존 surface로 복구하기 어려울 때만 최소 resumption state를 남긴다.
