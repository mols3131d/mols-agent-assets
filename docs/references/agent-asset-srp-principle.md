---
title: Agent Asset SRP Principle
description: 에이전트 자산을 하나의 cohesive responsibility와 변경 이유에 맞게 분리하는 원칙
---

# Agent Asset SRP Principle

에이전트 자산에서 SRP는 **파일 하나에 기능 하나만 두는 것**이 아니라, 한 자산이 하나의 **cohesive responsibility와 주된 변경 이유**를 갖게 하는 것이다.

> 같은 이유로 변하는 것은 함께 두고, 다른 이유로 변하는 것은 분리한다.

## Core Rules

1. **책임을 한 문장으로 설명할 수 있어야 한다.** 자산이 누구를 위해 무엇을 책임지는지 명확해야 한다.
2. **변경의 actor를 본다.** 서로 다른 사용자 intent, 정책 owner, 운영 주체가 독립적으로 변경을 요구한다면 분리 신호다.
3. **하나의 task를 수행하는 단계는 함께 둘 수 있다.** 여러 단계나 도구가 있어도 하나의 outcome을 위해 함께 변하면 하나의 capability다.
4. **독립적인 authority와 success criteria를 분리 신호로 본다.** 권한, 승인 경계, 결과 계약이 따로 진화한다면 책임도 다를 가능성이 높다.
5. **분리는 coordination 비용을 정당화해야 한다.** 자산을 나눈 결과 routing, handoff, context loading이 더 복잡해지면 과분리일 수 있다.
6. **길이는 책임의 증거가 아니다.** 긴 자산은 progressive disclosure가 필요할 수 있지만, 그 자체로 별도 책임을 의미하지 않는다.

## Cohesion Test

자산을 다음 문장으로 표현한다.

> **이 자산은 `[actor 또는 intent]`를 위해 `[하나의 outcome]`을 책임진다.**

그다음 묻는다.

- 포함된 행동들이 같은 outcome을 위해 함께 변하는가?
- 하나의 변경 요구가 자산 대부분에 자연스럽게 영향을 주는가?
- 일부 행동만 전혀 다른 actor나 정책 owner 때문에 자주 바뀌는가?

마지막 질문이 반복해서 `Yes`라면 분리를 검토한다.

## Strong Split Signals

- 서로 다른 사용자 intent에서 독립적으로 활성화된다.
- 서로 다른 정책 owner 또는 authority에 반응한다.
- permission이나 destructive boundary가 본질적으로 다르다.
- 성공 기준과 output contract가 독립적으로 진화한다.
- 독립적인 배포, versioning, evaluation이 필요하다.

## Weak Split Signals

- 문서가 길다.
- heading이 많다.
- workflow가 여러 단계다.
- 여러 tool을 사용한다.
- 구현 방법이 일부 다르다.

이 신호들만으로는 책임이 둘이라는 결론을 내리지 않는다.

## What SRP Is Not

- 파일을 최대한 작게 만드는 원칙이 아니다.
- workflow의 각 단계를 별도 Skill로 만드는 원칙이 아니다.
- 모든 tool마다 Agent나 Skill을 하나씩 만드는 원칙이 아니다.
- 공통 context를 무조건 별도 자산으로 추출하는 원칙이 아니다.
- 관련 행동을 coordination이 필요할 정도로 파편화하는 원칙이 아니다.

## Anti-patterns

- 하나의 Skill이 서로 무관한 사용자 intent를 계속 흡수한다.
- 하나의 Rule이 독립된 정책 owner를 가진 여러 정책을 한 덩어리로 관리한다.
- Agent가 자신의 역할과 무관한 authority와 tool까지 소유한다.
- workflow 단계마다 Skill을 만들어 routing이 실제 작업보다 복잡해진다.
- 책임 경계 대신 파일 길이나 디렉터리 모양을 기준으로 분리한다.

## Review Question

> **이 자산의 변경을 요구하는 주된 actor와 이유를 하나의 cohesive group으로 설명할 수 있는가?**

아니라면 분리를 검토한다. 분리 후 coordination 비용이 더 크다면 실제로는 하나의 책임인지 다시 확인한다.

## Research Basis

- [Robert C. Martin: The Single Responsibility Principle](https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html) — SRP를 한 가지 기능이 아니라 reason to change와 actor 관점에서 설명한다.
- [Agent Skills: Best practices for skill creators](https://agentskills.io/skill-creation/best-practices) — Skill을 너무 좁거나 넓지 않은 coherent unit of work로 설계하도록 권고한다.
- [OpenAI Agents SDK: Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/) — specialist agent와 routing은 책임이 실제로 분리될 때 유용하며 coordination trade-off가 있음을 보여준다.
