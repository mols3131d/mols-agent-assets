---
title: SRP
description: 에이전트 자산을 하나의 cohesive responsibility와 주된 변경 이유에 맞게 나누는 원칙
---

# SRP

에이전트 자산에서 SRP는 파일 하나에 기능 하나를 두는 것이 아니라 **한 자산이 하나의 cohesive responsibility와 주된 변경 이유를 갖게 하는 것**이다.

> 같은 이유로 함께 변하는 것은 함께 두고, 다른 이유로 독립적으로 변하는 것은 분리한다.

## Rules

- 자산의 책임을 한 문장으로 설명할 수 있어야 한다.
- 서로 다른 user intent, policy owner, authority가 독립적으로 변경을 요구하면 분리를 검토한다.
- 여러 단계와 도구가 하나의 outcome을 위해 함께 변하면 하나의 capability일 수 있다.
- permission, success criteria, output contract가 독립적으로 진화하면 강한 split signal이다.
- 분리로 생기는 routing, handoff, context loading 비용도 함께 계산한다.
- 길이, heading 수, tool 수만으로 책임이 둘이라고 판단하지 않는다.

## Cohesion Test

다음 문장을 채운다.

> 이 자산은 `[actor 또는 intent]`를 위해 `[하나의 outcome]`을 책임진다.

그 설명에 억지로 `그리고`가 반복되거나, 일부 행동만 다른 actor/authority 때문에 독립적으로 바뀐다면 분리를 검토한다.

## Strong Split Signals

- 독립적인 activation intent
- 다른 policy owner 또는 authority
- 다른 permission/destructive boundary
- 독립적인 output contract 또는 evaluation
- 독립 배포나 versioning 필요

## Boundary

파일이 길지만 책임은 하나라면 먼저 [Progressive Disclosure](agent-assets-principles-progressive-disclosure.md)를 검토한다.

중복 제거를 위해 책임이 다른 자산을 합치지 않는다. knowledge ownership은 [DRY](agent-assets-principles-dry.md)가 다룬다.

## Sources

- [Robert C. Martin: The Single Responsibility Principle](https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html)
- [Agent Skills: Best practices for skill creators](https://agentskills.io/skill-creation/best-practices)
- [OpenAI Agents SDK: Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/)
