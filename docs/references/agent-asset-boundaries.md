---
title: Agent Asset Boundaries
description: Skill, Rule, Prompt, Agent, Reference의 책임과 소유권 경계를 정의하는 기준
---

# Agent Asset Boundaries

에이전트 자산의 품질은 파일 형식보다 **무엇을 어디에 소유시키는가**에 크게 좌우된다.

> 자산 유형은 내용의 모양이 아니라 책임으로 구분한다.

## Core Boundaries

| 자산 | 주된 책임 | 넣지 말아야 할 것 |
| --- | --- | --- |
| Rule | 여러 작업에서 반복 적용되는 정책과 제약 | 특정 작업의 긴 실행 절차 |
| Skill | 재사용 가능한 capability와 그 workflow | 무관한 intent, 범용 정책의 독립 사본 |
| Prompt | 현재 작업의 목표, 입력, 산출물, 일회성 제약 | 지속적으로 재사용될 capability 정의 |
| Agent | 역할, ownership, authority, tool surface | 세부 domain manual 전체 |
| Reference | 설계 지식, 설명, 근거, 세부사항 | 자동으로 적용된다고 가정하는 runtime 정책 |

## Rule

Rule은 **행동의 경계**를 정의한다.

- 여러 작업에서 반복해서 지켜야 하는 constraint
- 금지 사항과 필수 guardrail
- 프로젝트 또는 환경 수준의 정책

Rule은 작업을 수행하는 전체 workflow가 되어서는 안 된다.

## Skill

Skill은 **특정 종류의 일을 수행하는 재사용 가능한 capability**를 소유한다.

- 언제 활성화되는지
- 어떤 workflow를 수행하는지
- 어떤 resource와 tool이 필요한지
- 무엇으로 성공을 판단하는지

서로 다른 intent와 책임이 계속 추가된다면 Skill 분리를 검토한다.

## Prompt

Prompt는 **현재 invocation에서 원하는 일**을 정의한다.

- 목표
- 제공된 context
- 필요한 결과
- 현재 작업에만 적용되는 제약

반복적으로 같은 prompt 지침이 필요하다면 Rule 또는 Skill이 소유해야 할 지식인지 검토한다.

## Agent

Agent는 **누가 어떤 권한과 도구로 어떤 책임을 소유하는가**를 정의한다.

Agent를 분리하는 강한 이유는 다음과 같다.

- ownership이 다르다.
- tool 또는 permission이 다르다.
- 독립적인 판단과 handoff가 필요하다.

단순히 instruction이 길다는 이유만으로 Agent를 늘리지 않는다.

## Reference

Reference는 **이해와 정확한 판단을 돕는 지식**을 담는다.

Repository-level `docs/references/`는 사람과 자산 작성자가 참고하는 canonical knowledge다. Runtime 자산이 이 경로를 반드시 읽는다고 가정하지 않는다.

Skill 내부의 `references/`는 해당 Skill의 조건부 실행 지식으로 사용할 수 있으며, 이 경우 Skill이 언제 무엇을 읽을지 명시적으로 소유해야 한다.

## Placement Test

내용을 어디에 둘지 모호하면 다음 질문을 순서대로 사용한다.

1. 여러 작업에서 반드시 지켜야 하는 정책인가? → **Rule**
2. 반복 수행되는 하나의 capability인가? → **Skill**
3. 지금 이 작업에서만 필요한 요청인가? → **Prompt**
4. 역할, 권한, 도구의 ownership을 정의하는가? → **Agent**
5. 행동 자체보다 이해와 세부 지식을 제공하는가? → **Reference**

둘 이상의 답이 동시에 강하면 내용이 여러 책임을 섞고 있는지 먼저 확인한다.

## Anti-patterns

- Prompt에 영구 정책을 계속 복사한다.
- Rule 안에 전체 구현 workflow를 넣는다.
- Skill을 단순한 reference 문서 저장소로 사용한다.
- Agent를 instruction namespace처럼 사용한다.
- `docs/references/` 문서를 runtime dependency처럼 취급한다.
- 자산 유형을 파일 확장자나 디렉터리 이름만으로 판단한다.

## Review Question

> **이 내용의 canonical owner는 어떤 자산이며, 그 이유를 책임 관점에서 한 문장으로 설명할 수 있는가?**

설명할 수 없다면 boundary가 불명확한 것이다.