---
description: Subagent를 엄격한 유형으로 분류하지 않고 Role-oriented와 Capability-oriented 사이의 설계 방향으로 판단할 때 사용하는 reusable pattern입니다.
---

# Subagent Orientation

Subagent를 서로 배타적인 유형으로 분류하지 않습니다. 대신 **무엇을 중심으로 정의하는가**에 따라 `Role-oriented`와 `Capability-oriented` 사이의 orientation으로 봅니다.

```text
Role-oriented  <──────────── mixed ────────────>  Capability-oriented
```

대부분의 Subagent는 두 요소를 모두 가질 수 있습니다. 중요한 것은 어느 쪽이 그 Subagent의 **instruction budget, invocation contract, 책임 경계**를 더 많이 결정하는지입니다.

## Role-oriented

Subagent를 하나의 **책임 있는 역할**로 정의하는 방향입니다.

다음 요소의 비중이 큽니다.

- 목적과 책임
- 권한과 금지된 행동
- in-scope / out-of-scope
- 판단 기준과 invariants
- anti-pattern과 failure boundary
- 다른 역할과의 handoff 또는 escalation

Tool과 Skill은 역할을 수행하기 위한 수단입니다. 특정 도구 목록 자체가 역할의 정체성이 되지 않습니다.

이 orientation은 여러 종류의 작업을 같은 책임 아래 판단해야 하거나, 자율적인 판단·조율·최종 책임이 중요한 Subagent에 잘 맞습니다.

예: review lead, release steward, incident coordinator, architecture reviewer.

## Capability-oriented

Subagent를 반복해서 호출할 수 있는 **bounded capability 또는 specialist**로 정의하는 방향입니다.

다음 요소의 비중이 큽니다.

- 수행할 단일 작업 또는 서로 강하게 결합된 소수 작업
- 입력과 반환 결과
- 사용할 tool과 자주 필요한 Skill
- 실행 제약과 side-effect boundary
- caller가 결과를 어떻게 소비할지에 대한 handoff contract

필요하면 역할 설명도 포함하지만, 핵심은 "누구인가"보다 **무엇을 안정적으로 수행하는가**입니다. 잘 설계된 경우 caller 입장에서는 고수준 tool이나 specialist처럼 사용할 수 있습니다.

이 orientation은 검색, 테스트, 정적 분석, 특정 도메인 검토, 변환, 검증처럼 반복 가능하고 비교적 좁은 작업에 잘 맞습니다.

예: test runner, dependency analyst, security checker, adversarial reviewer, research specialist.

## Mixed Orientation

두 orientation은 결합할 수 있습니다.

예를 들어 reviewer는 제한된 검토 capability를 가지면서도 read-only 권한, scope boundary, evidence rule 같은 역할 계약을 함께 가질 수 있습니다. 반대로 lead agent도 특정 Skill과 tool을 자주 사용하도록 정의할 수 있습니다.

혼합 자체는 문제가 아닙니다. 다만 다음을 피합니다.

- capability가 넓어질 때마다 별도 역할 정체성을 덧붙이는 것
- 역할의 책임을 tool 목록으로 대신 설명하는 것
- specialist에게 불필요한 최종 결정권이나 넓은 자율권을 주는 것
- role-oriented agent에 모든 가능한 procedure와 tool 사용법을 넣어 instruction을 비대하게 만드는 것

## Design Heuristic

Subagent를 설계할 때 먼저 다음 질문을 합니다.

> 이 Subagent의 품질을 가장 크게 좌우하는 것은 **올바른 판단 경계와 책임**인가, 아니면 **특정 작업을 안정적으로 수행하는 capability**인가?

전자가 크면 Role 쪽에, 후자가 크면 Capability 쪽에 더 많은 instruction budget을 사용합니다.

orientation은 이름, directory, framework metadata로 고정하지 않습니다. 실제 responsibility와 runtime contract가 우선합니다.

## Boundary

이 pattern은 Subagent의 설계 emphasis를 설명합니다. Subagent의 공식 taxonomy, runtime lifecycle, delegation protocol, vendor-specific frontmatter, tool permission model 또는 orchestration framework를 정의하지 않습니다.

구체적인 source/target representation과 runtime semantics는 사용 중인 framework와 runtime의 authoritative contract를 따릅니다.
