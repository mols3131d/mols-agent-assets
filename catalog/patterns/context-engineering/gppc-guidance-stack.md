---
description: Goal과 Principles를 본질, Patterns와 Contracts를 실존으로 구분해 안정적인 방향과 적응 가능한 실행 지침을 구조화할 때 참고하는 pattern입니다.
---

# GPPC Guidance Stack

GPPC는 guidance를 **Goal, Principles, Patterns, Contracts**의 네 논리적 계층으로 구조화해 안정적인 방향과 적응 가능한 실행 지침을 구분해 다루는 패턴이다.

GPPC는 **Goal과 Principles를 본질(Essence)**, **Patterns와 Contracts를 실존(Existence)**으로 본다. 본질은 지향점과 판단 기준을 정의하고, 실존은 그것이 실제 환경에서 구현되는 해결 방식과 조건을 나타낸다.

목적과 원칙을 실행 지침과 같은 수준에서 다루면 세부 수정이 방향을 바꾸거나 오래된 실행 방식을 고정하기 쉽다. GPPC는 본질과 실존의 책임을 분리해 이를 막는다.

## Core

| Layer | 영역 | 역할 | 취지 |
| --- | --- | --- | --- |
| **Goal** | Essence | 목적지를 정의한다 | guidance가 향할 방향을 정한다 |
| **Principles** | Essence | 판단 기준을 정의한다 | 선택과 trade-off의 기준을 정한다 |
| **Patterns** | Existence | 재사용 가능한 해결 방식을 정의한다 | 본질을 상황에 맞는 해결 형태로 구체화한다 |
| **Contracts** | Existence | 지켜야 하는 조건과 경계를 정의한다 | 적용 중 충족해야 할 범위를 명확히 한다 |

이 네 layer의 관계는 **우선순위보다 역할과 구체화의 관계**에 가깝다.

```text
Goal       — 무엇을 이루려는가
Principles — 어떤 기준으로 판단하는가
Patterns   — 어떤 방식으로 해결하는가
Contracts  — 무엇을 반드시 지키는가
```

여기서 **계층은 물리적 계층이 아니라 논리적 계층**이다. 문서의 heading depth, section 순서, file·directory 구조를 뜻하지 않으며, 단순한 우선순위나 강제력의 순위도 아니다. 각 layer가 서로 다른 역할과 취지를 맡고, 더 구체적인 layer가 더 추상적인 layer의 의미를 구체화하면서 정합해야 한다는 관계를 나타낸다.

**GP — Goal과 Principles는 본질을 정의한다.** Guidance의 존재 이유와 지향점, 판단 기준을 결정하므로 상대적으로 안정적으로 유지한다.

**PC — Patterns와 Contracts는 실존을 정의한다.** 본질을 실제 상황에서 작동하는 해결 방식과 조건으로 구체화한다. 환경이나 적용 경험에 따라 조정할 수 있지만 Goal과 Principles에 계속 부합해야 한다.

더 구체적인 layer를 바꿀 때는 자신보다 추상적인 layer와의 정합성을 확인한다. 정합되지 않으면 더 추상적인 layer 자체의 변경이 필요한지도 함께 검토한다.

Goal과 Principles가 같고 Patterns와 Contracts만 달라진다면 같은 본질의 다른 실존으로 볼 수 있다. 반대로 Goal이나 Principles의 변화는 guidance 자체의 정체성 변화에 가깝다.

Contract는 적용되는 동안 엄격히 준수될 수 있지만, 그 강제력이 Goal이나 Principles의 역할을 대신하지는 않는다. GPPC의 논리적 계층은 실행 순서나 일반적인 instruction precedence를 의미하지 않는다.

## Composition

GPPC의 네 layer는 **논리적 책임**이지 section이나 file schema가 아니다. Layer, section, file은 1:1로 대응할 필요가 없다.

- Goal과 Principles는 하나의 section에서 함께 다룰 수 있다.
- Patterns와 Contracts도 하나의 section에서 함께 다룰 수 있다.
- Principles와 Patterns는 본질과 실존의 경계를 지우는 방식으로 하나의 구분되지 않은 section에 합치지 않는다.
- 네 layer를 하나의 file에 모두 정의할 필요는 없다. 필요에 따라 여러 file로 나눌 수 있으며, 하나의 file이 일부 layer만 다뤄도 된다.
- GPPC는 네 layer 이름 외의 section을 금지하지 않는다. Rationale, Context, Examples, Notes처럼 이해와 적용을 보조하는 section이나 domain에 필요한 별도 section을 둘 수 있다.
- 보조 section은 새로운 GPPC layer를 뜻하지 않는다. 그 안에 guidance가 있다면 해당 내용은 Goal, Principles, Patterns, Contracts 중 적절한 역할과 정합되어야 한다.

문서 구조를 합치거나 나누거나 보조 section을 추가하더라도 각 내용의 논리적 책임과 본질·실존의 경계, layer 사이의 정합성은 유지한다.

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

Principles는 특정 해결 방법을 고정하지 않는다. 상황이나 선택지가 달라도 일관된 판단 기준을 제공한다.

**판별 질문:** 어떤 기준으로 판단하고 선택할 것인가?

## Patterns

Patterns는 반복되는 문제에 적용할 수 있는 **재사용 가능한 해결 방식**을 정의한다.

Approach, structure, practice처럼 여러 상황에서 재사용할 수 있는 해결 형태가 포함될 수 있다.

Patterns는 절대 규칙이나 특정 구현을 그대로 반복하는 절차가 아니다. Goal과 Principles를 보존하면서 상황에 맞게 선택하거나 변형할 수 있다.

여기서 Patterns는 GPPC 자체가 아니라, GPPC로 구조화된 guidance 안의 해결 패턴을 의미한다.

**판별 질문:** 반복되는 문제를 어떤 방식으로 해결할 것인가?

## Contracts

Contracts는 guidance를 적용할 때 **명확하게 지켜야 하는 조건과 경계**를 정의한다.

Requirement, invariant, boundary, prohibition처럼 충족·위반 여부를 비교적 명확히 판단할 수 있는 내용이 포함될 수 있다.

Contracts는 선호나 권고와 구분된다. 적용 중에는 준수해야 하지만 영구불변의 원칙은 아니며, Goal과 Principles에 더 잘 부합하도록 조건이나 경계를 다시 설계할 수 있다.

**판별 질문:** 무엇이 반드시 지켜져야 하며, 어디까지 허용되는가?

## Classification

내용을 어느 layer에 둘지 애매하면 이를 변경했을 때 **무엇이 달라지는지** 본다.

| 변경되는 것 | Layer |
| --- | --- |
| 목적, 목표 또는 도달하려는 상태 | **Goal** |
| 판단 기준, 우선순위 또는 trade-off | **Principles** |
| 반복해서 사용하는 해결 방식 | **Patterns** |
| 충족해야 하는 조건 또는 허용 경계 | **Contracts** |

하나의 항목이 여러 책임을 가지면 한 layer에 억지로 넣기보다 책임을 분리하는 편이 낫다.

## Example

예를 들어 반복 작업의 실패를 줄이기 위한 guidance라면 다음처럼 해석할 수 있다.

- **Goal** — 반복 작업의 실패율을 낮춘다.
- **Principles** — 단순성, 가시성, 복구 가능성을 우선한다.
- **Patterns** — 작업을 작은 단계로 나누고 각 단계에서 상태를 확인한다.
- **Contracts** — 필수 상태 확인을 통과하지 않으면 다음 단계로 진행하지 않는다.

이 예시는 네 layer의 역할 차이를 보여주기 위한 것이며, GPPC가 요구하는 고정 내용은 아니다.

## Boundary

GPPC는 guidance 내부의 역할과 변경 성격을 구조화하는 패턴이다.

Essence와 Existence는 GPPC 구조를 설명하기 위해 빌린 표현이다. 특정 실존주의 철학의 명제나 존재론을 GPPC 규칙으로 채택한다는 뜻은 아니다.

다음은 GPPC 자체가 정의하지 않는다.

- system, user, project 사이의 instruction precedence
- 실제 변경 권한이나 승인 절차
- 특정 파일이나 directory 구조
- 특정 agent 또는 runtime의 동작
- 각 layer에 반드시 들어가야 하는 고정 schema

네 layer의 분량이 같을 필요는 없다. 필요한 책임만 필요한 만큼 사용한다.
