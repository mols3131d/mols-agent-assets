---
title: KISS
description: 에이전트 자산에서 같은 행동 신뢰성을 유지하는 최소 충분 복잡성을 찾는 원칙
---

# KISS

에이전트 자산에서 KISS는 가장 짧게 만드는 것이 아니라 **같은 행동 신뢰성과 안전성을 만드는 최소 충분 복잡성**을 찾는 것이다.

> 제거해도 결과가 나빠지지 않는 context, 선택지, 분기와 구조는 제거한다.

## Rules

- 행동을 바꾸지 않는 일반론은 제거 후보로 본다.
- 여러 접근이 동등하면 default 하나를 정하고 escape condition만 둔다.
- 실제 행동, authority, 위험, output이 달라질 때만 branch를 만든다.
- router, taxonomy, abstraction, Agent 같은 구조는 줄이는 복잡성이 만드는 복잡성보다 클 때만 도입한다.
- safety, permission, validation처럼 실패 비용을 낮추는 지침은 길다는 이유로 제거하지 않는다.

## Minimum Sufficient Test

> 이 요소를 제거했을 때 실제 task의 오류, 불필요한 탐색, 위험이 의미 있게 증가하는가?

- `Yes` → 유지한다.
- `No` → 제거한다.
- 특정 조건에서만 `Yes` → 조건부 context로 분리한다.
- 모르면 실제 task나 eval로 확인한다.

## Boundary

KISS는 다음 질문을 소유하지 않는다.

- 아직 필요하지 않은가? → [YAGNI](yagni.md)
- 책임을 분리해야 하는가? → [SRP](srp.md)
- 중복 지식의 owner는 누구인가? → [DRY](dry.md)
- 언제 세부 context를 로드하는가? → [Progressive Disclosure](progressive-disclosure.md)

## Anti-Patterns

- 동등한 도구와 접근을 메뉴처럼 나열한다.
- 작은 문제에 framework나 multi-agent 구조부터 만든다.
- 중요한 guardrail을 “모델이 알아서 할 것”이라고 생략한다.
- 행동 차이가 없는 workflow variant를 유지한다.

## Sources

- [Agent Skills: Best practices for skill creators](https://agentskills.io/skill-creation/best-practices)
- [Anthropic: Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [OpenAI: A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)
