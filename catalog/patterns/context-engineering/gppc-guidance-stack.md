---
description: Goal과 Principles의 안정적인 방향을 Patterns와 Contracts의 적응 가능한 실행 지침과 분리해 guidance를 구조화할 때 참고하는 pattern입니다.
---

# GPPC Guidance Stack

GPPC는 guidance를 **Goal, Principles, Patterns, Contracts**의 네 계층으로 나누어, 안정적으로 유지할 방향과 상황에 맞게 조정할 실행 지침을 분리하는 패턴이다.

목적과 원칙을 구체적인 실행 지침과 같은 수준에서 다루면 세부 사항을 수정하다 방향까지 바꾸거나, 반대로 오래된 실행 방식을 지나치게 고정하기 쉽다. GPPC는 이 책임을 계층별로 분리한다.

## Core

| Layer | 책임 | 성격 |
| --- | --- | --- |
| **Goal** | 목적지를 정의한다 | 추상적 · 안정적 · 높은 권위 |
| **Principles** | 판단 기준을 정의한다 | 추상적 · 안정적 · 높은 권위 |
| **Patterns** | 재사용 가능한 해결 방식을 정의한다 | 상대적으로 구체적 · 적응 가능 |
| **Contracts** | 지켜야 하는 조건과 경계를 정의한다 | 명확 · 적응 가능 · 적용 시 준수 |

**Goal과 Principles**는 guidance의 방향과 판단 기준을 소유한다. 쉽게 변경하지 않으며, agent도 명시적인 요청이나 적절한 변경 권한 없이 이를 수정 대상으로 취급하지 않는 편이 좋다.

**Patterns와 Contracts**는 Goal과 Principles를 실제 상황에 적용한다. 적용 경험이나 환경 변화에 따라 수정할 수 있지만, 변경된 내용은 Goal과 Principles에 계속 부합해야 한다.

Contract는 적용되는 동안 엄격하게 준수될 수 있다. 그러나 강제력이 높다는 것이 Goal이나 Principles보다 의미적 권위가 높다는 뜻은 아니다.

이 계층은 실행 순서나 일반적인 instruction precedence를 의미하지 않는다.

## Goal

Goal은 guidance가 **왜 존재하는지, 무엇을 이루려는지, 어디에 도달하려는지**를 정의한다.

대표적으로 다음을 포함할 수 있다.

- **Purpose** — 왜 필요한가
- **Objective** — 무엇을 달성하려는가
- **Target** — 어떤 상태에 도달하려는가

Goal은 방향과 목적지를 정의하며 구체적인 해결 방법이나 실행 조건은 정하지 않는다.

**판별 질문:** 왜 존재하는가, 무엇을 이루는가, 어디에 도달하려는가?

## Principles

Principles는 Goal을 향해 나아갈 때 **어떤 가치와 기준으로 판단하고 선택할지**를 정의한다.

대표적으로 다음을 포함할 수 있다.

- **Philosophy** — 어떤 관점과 사고방식을 따르는가
- **Priority** — 무엇을 우선하는가
- **Trade-off** — 무엇을 위해 무엇을 감수할 수 있는가
- **Preference** — 여러 유효한 선택지 중 무엇을 선호하는가

Principles는 특정한 해결 방법을 고정하지 않는다. 상황이나 선택지가 달라져도 일관된 판단을 내릴 수 있는 기준을 제공한다.

**판별 질문:** 어떤 기준으로 판단하고 선택할 것인가?

## Patterns

Patterns는 반복되는 문제에 적용할 수 있는 **재사용 가능한 해결 방식**을 정의한다.

Approach, structure, practice처럼 여러 상황에서 다시 사용할 수 있는 해결 형태가 여기에 포함될 수 있다.

Patterns는 절대적인 규칙이나 특정 구현을 그대로 반복하는 절차가 아니다. Goal과 Principles를 보존하면서 상황에 맞게 선택하거나 변형할 수 있다.

여기서 Patterns는 GPPC 자체가 아니라, GPPC로 구조화된 guidance 안에서 사용하는 해결 패턴을 의미한다.

**판별 질문:** 반복되는 문제를 어떤 방식으로 해결할 것인가?

## Contracts

Contracts는 guidance를 적용할 때 **명확하게 지켜야 하는 조건과 경계**를 정의한다.

Requirement, invariant, boundary, prohibition처럼 충족 여부나 위반 여부를 비교적 명확하게 판단할 수 있는 내용이 여기에 포함될 수 있다.

Contracts는 선호나 권고와 구분된다. 적용되는 동안에는 준수해야 하지만, 적절한 변경 권한이 있고 Goal과 Principles에 더 잘 부합한다면 수정할 수 있다.

**판별 질문:** 무엇이 반드시 지켜져야 하며, 어디까지 허용되는가?

## Classification

내용을 어느 계층에 둘지 애매하면 그 내용을 변경했을 때 **무엇이 달라지는지** 본다.

| 변경되는 것 | Layer |
| --- | --- |
| 목적, 목표 또는 도달하려는 상태 | **Goal** |
| 판단 기준, 우선순위 또는 trade-off | **Principles** |
| 반복해서 사용하는 해결 방식 | **Patterns** |
| 충족해야 하는 조건 또는 허용 경계 | **Contracts** |

하나의 항목이 여러 책임을 동시에 가진다면 한 계층에 억지로 넣기보다 책임을 분리하는 편이 낫다.

## Boundary

GPPC는 guidance 내부의 역할과 변경 성격을 구조화하는 패턴이다.

다음은 GPPC 자체가 정의하지 않는다.

- system, user, project 사이의 instruction precedence
- 실제 변경 권한이나 승인 절차
- 특정 파일이나 directory 구조
- 특정 agent 또는 runtime의 동작
- 각 계층에 반드시 들어가야 하는 고정 schema

네 계층이 항상 같은 양의 내용을 가질 필요도 없다. 필요한 책임만 필요한 만큼 사용한다.
