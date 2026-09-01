# Subagent Improve

Agent 또는 Subagent 개선에만 필요한 판단을 다룬다. 공통 개선 원칙은 `../common/improve.md`를 따른다.

우선 다음 문제를 찾는다.

- separate agent가 실제 benefit 없이 존재함
- responsibility가 caller나 sibling과 겹침
- delegation condition이 너무 넓거나 모호함
- context handoff가 과도하거나 필요한 authority가 빠짐
- tool/permission이 responsibility보다 넓음
- independence를 주장하지만 runtime 또는 brief가 이를 보존하지 못함
- result contract나 termination condition이 불명확함
- failure가 caller에게 보이지 않고 성공처럼 흡수됨

개선은 agent 수를 늘리기보다 responsibility와 handoff를 단순화하는 쪽을 우선한다. 필요 없는 delegation layer는 제거하고, context는 assigned decision에 필요한 최소로 줄이며, unavailable capability와 incomplete evidence는 명시적으로 드러낸다.
