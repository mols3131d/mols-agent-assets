---
title: Agent Asset SRP Principle
description: 에이전트 자산의 책임과 변경 이유를 분리하기 위한 설계 원칙
---

# Agent Asset SRP Principle

에이전트 자산에서 SRP의 목적은 **파일 하나에 기능 하나만 두는 것**이 아니라, 한 자산이 **하나의 명확한 책임과 변경 이유**를 갖게 하는 것이다.

> 함께 변하는 행동은 함께 두고, 다른 이유로 변하는 행동은 분리한다.

## Core Rules

1. **Primary responsibility를 하나로 설명할 수 있어야 한다.** 자산의 존재 이유를 한 문장으로 설명하기 어렵다면 책임이 섞였을 가능성이 높다.
2. **변경 이유가 다르면 분리를 검토한다.** trigger, authority, tool, output contract, validation이 독립적으로 변한다면 별도 자산이 더 자연스러울 수 있다.
3. **같은 workflow의 variant는 성급히 분리하지 않는다.** 공통 trigger와 흐름을 공유하고 일부 세부사항만 다르면 하나의 자산 안에서 처리하는 편이 낫다.
4. **책임 분리는 routing 비용보다 가치가 커야 한다.** 분리로 인해 선택 경로와 dependency가 더 복잡해지면 SRP가 KISS를 해칠 수 있다.
5. **자산 유형의 책임을 섞지 않는다.** 정책, capability, task prompt, agent ownership, human reference는 각각 가장 적절한 자산이 소유한다.

## Split Signals

다음 차이가 지속적으로 나타나면 분리를 검토한다.

- 서로 다른 사용자 intent에서 활성화된다.
- 필요한 tool 또는 permission이 다르다.
- 성공 기준과 output contract가 다르다.
- 하나를 변경해도 다른 하나는 영향을 받지 않는다.
- 독립적인 배포 또는 versioning이 필요하다.

반대로 다음은 분리 이유가 약하다.

- 문서가 길어 보인다.
- heading이 여러 개다.
- 같은 capability 안에 여러 단계가 있다.
- 구현 세부사항이 조금 다르다.

## Responsibility Test

자산을 다음 문장으로 표현한다.

> **이 자산은 `[누구/무엇]`을 위해 `[하나의 책임]`을 소유한다.**

여기에 `그리고`가 반복해서 필요하거나 서로 독립적인 목적이 들어가면 분리를 검토한다.

## What SRP Is Not

- 파일을 최대한 작게 만드는 원칙이 아니다.
- workflow의 각 단계를 별도 Skill로 만드는 원칙이 아니다.
- 공통 context를 무조건 별도 자산으로 추출하는 원칙이 아니다.
- 관련된 행동을 지나치게 미세한 단위로 파편화하는 원칙이 아니다.

## Anti-patterns

- 하나의 Skill이 서로 무관한 여러 intent를 동시에 소유한다.
- 하나의 Rule이 formatting, security, Git workflow 같은 독립 정책을 한데 묶는다.
- Agent가 역할과 무관한 도구와 책임까지 소유한다.
- 작은 workflow 단계마다 별도 Skill을 만들어 router가 본체보다 복잡해진다.
- 책임이 아니라 파일 길이를 기준으로 분리한다.

## Review Question

> **이 자산이 바뀌는 주된 이유는 하나인가?**

아니라면 분리를 검토한다. 그러나 분리 후의 routing과 coordination이 더 복잡하다면 현재 책임들이 실제로 하나의 cohesive capability인지 다시 확인한다.