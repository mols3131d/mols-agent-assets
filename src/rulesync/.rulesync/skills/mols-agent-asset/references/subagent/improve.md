# Subagent Improve

Agent 또는 Subagent 개선에만 필요한 판단을 다룬다. 공통 개선 원칙은 `../common/improve.md`를 따른다.

## Diagnose

우선 다음 문제를 찾는다.

- separate agent가 실제 benefit 없이 존재함
- responsibility가 caller나 sibling과 겹침
- delegation condition이 너무 넓거나 모호함
- 여러 delegation hop이 context를 좁히지 않고 전달만 함
- context handoff가 과도하거나 필요한 authority, state basis, unknown이 빠짐
- full conversation, reasoning transcript, canonical rule을 불필요하게 복제함
- tool/permission이 responsibility보다 넓음
- independence를 주장하지만 runtime 또는 brief가 이를 보존하지 못함
- result contract나 termination condition이 불명확함
- handoff state가 stale한데 현재 truth처럼 사용됨
- failure가 caller에게 보이지 않고 성공처럼 흡수됨

## Improve

- agent 수를 늘리기보다 responsibility와 handoff를 단순화하는 쪽을 우선한다.
- specialization, isolation, capability, independence, coordination benefit이 사라진 delegation layer는 제거하거나 caller에 흡수한다.
- context는 assigned decision에 필요한 최소 충분한 state로 줄이고, canonical knowledge를 복제하지 않는다.
- independence가 목적이면 다른 reviewer의 결론과 speculative diagnosis를 brief에서 제거한다.
- session이나 worker 경계를 넘는 handoff는 목표, current state, important evidence, unknown, next owner와 필요한 state basis만 남기고 실행 로그나 transcript를 축적하지 않는다.
- stale handoff는 현재 source와 revision을 확인해 갱신하거나 폐기한다.
- capability는 responsibility에 맞게 줄이고 unavailable capability와 incomplete evidence는 명시적으로 드러낸다.
- caller가 결과를 다시 해석하느라 전체 context를 재구성해야 한다면 result contract를 더 직접적으로 만든다.
- recursion과 circular handoff는 새 owner나 더 구체적인 responsibility가 생기지 않으면 제거한다.

Durable artifact를 추가하는 것은 개선 그 자체가 아니다. Continuation cost가 충분히 크고 기존 surface로 복구하기 어려울 때만 최소한의 resumption state를 남긴다.
