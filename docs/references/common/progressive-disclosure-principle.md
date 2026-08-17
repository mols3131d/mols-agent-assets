---
title: Progressive Disclosure Principle
description: 에이전트가 필요한 정보를 필요한 시점에만 로드하도록 context와 resource 경계를 설계하는 원칙
---

# Progressive Disclosure Principle

Progressive disclosure는 **모든 정보를 처음부터 context에 넣지 않고, 현재 판단에 필요한 정보만 단계적으로 노출하는 것**이다.

> 먼저 발견에 필요한 정보, 다음으로 공통 실행 지침, 마지막으로 현재 task에 필요한 세부 지식만 로드한다.

목적은 파일을 많이 만드는 것이 아니라 **관련 없는 context를 줄이면서 필요한 정보를 놓치지 않는 것**이다.

## Loading Model

Agent Skills에서는 다음 세 층으로 이해할 수 있다.

| 단계 | 내용 | 시점 |
| --- | --- | --- |
| Discovery | `name`, `description` 같은 최소 metadata | Skill을 찾을 때 |
| Activation | 선택된 Skill의 core instructions | Skill이 활성화될 때 |
| Execution | reference, script, asset 같은 세부 resource | 실제로 필요할 때 |

각 단계는 다음 단계에 필요한 판단을 가능하게 해야 한다. **뒤에 정보가 존재한다는 사실조차 알 수 없게 숨기면 progressive disclosure가 아니다.**

## Core Rules

1. **Discovery에는 선택에 필요한 정보만 둔다.** capability와 activation trigger를 판단할 수 있어야 한다.
2. **Core instruction에는 모든 실행에 공통으로 필요한 행동만 둔다.** workflow, 중요한 constraint, validation, resource load condition이 여기에 속한다.
3. **세부 지식은 필요할 때 로드한다.** 특정 provider, format, error, domain에만 필요한 설명은 focused reference로 분리한다.
4. **Load condition을 명시한다.** `필요하면 참고한다`가 아니라 어떤 상태에서 어떤 resource를 읽는지 적는다.
5. **중요한 gotcha의 discoverability를 보존한다.** 에이전트가 문제나 trigger 자체를 알아차리기 어렵다면 그 gotcha를 core instruction에 남긴다.
6. **reference chain을 얕게 유지한다.** core에서 필요한 resource를 직접 찾을 수 있게 한다.
7. **분리 비용이 이득보다 크면 분리하지 않는다.** 작은 문서를 만들기 위한 분할 자체가 목적이 아니다.

## What Stays in Core

조건부 정보라고 해서 모두 reference로 내리지 않는다.

Core에 남길 강한 이유:

- 모든 실행에 적용된다.
- safety, permission, destructive boundary처럼 놓치면 비용이 크다.
- 어떤 reference를 읽어야 하는지 결정하는 routing rule이다.
- 에이전트가 trigger 자체를 스스로 알아차리기 어려운 non-obvious gotcha다.
- 실행 후 반드시 확인해야 하는 validation requirement다.

Reference로 내릴 강한 이유:

- 특정 상태나 variant에서만 필요하다.
- trigger가 사용자 요청, tool result, file type처럼 명시적으로 식별 가능하다.
- 상세 설명이 core workflow를 이해하는 데 필요하지 않다.
- 필요 시 다시 읽어도 task 진행이 깨지지 않는다.

## Discoverability Test

세부사항을 reference로 옮기기 전에 묻는다.

> **이 정보를 읽지 않은 에이전트도, 언제 이 reference가 필요한지 알아차릴 수 있는가?**

- `Yes` → reference로 분리할 수 있다.
- `No` → trigger 또는 핵심 gotcha를 core에 남긴다.
- trigger만 알면 된다 → core에는 trigger를, reference에는 상세 절차를 둔다.

이 테스트는 progressive disclosure가 **information hiding**으로 변하는 것을 막는다.

## Routing Pattern

좋은 routing instruction은 **조건과 resource를 함께 지정**한다.

```text
API가 non-200 response를 반환하면 references/api-errors.md를 읽는다.
```

다음과 같은 지침은 피한다.

```text
필요하면 관련 reference를 확인한다.
```

에이전트가 어떤 상황에서 어떤 정보를 찾아야 하는지 다시 추론해야 하기 때문이다.

## Skill Split Boundary

Progressive disclosure와 Skill 분리는 다른 문제다.

하나의 Skill 안에서 reference로 분리하기 좋은 경우:

- 같은 activation intent와 core workflow를 공유한다.
- 차이가 특정 variant의 상세 지식이다.
- 같은 task에서 여러 resource를 조합할 수 있다.

별도 Skill을 검토할 경우:

- activation intent가 독립적이다.
- capability와 success criteria가 독립적으로 진화한다.
- 별도 permission, distribution, evaluation boundary가 필요하다.

단순히 `SKILL.md`가 길다는 이유만으로 별도 Skill을 만들지 않는다. 책임 분리는 [SRP Principle](./agent-asset-srp-principle.md)을 함께 적용한다.

## What Progressive Disclosure Is Not

- 모든 세부사항을 reference로 옮기는 규칙이 아니다.
- root file을 단순한 링크 목록으로 만드는 것이 아니다.
- 깊은 reference chain을 만드는 것이 아니다.
- 모든 variant를 별도 파일로 만드는 것이 아니다.
- 중요한 safety rule이나 gotcha를 숨기는 것이 아니다.

## Review Checklist

- [ ] Discovery 정보만으로 capability와 trigger를 판단할 수 있다.
- [ ] Core에는 공통 workflow와 중요한 constraint가 남아 있다.
- [ ] 각 reference에는 명확한 load condition이 있다.
- [ ] 관련 없는 reference를 eager load하지 않는다.
- [ ] 에이전트가 스스로 trigger를 알아차리기 어려운 중요한 gotcha는 core에 남아 있다.
- [ ] Reference는 가능한 한 core에서 직접 찾을 수 있다.
- [ ] 파일 분리가 routing과 탐색을 더 복잡하게 만들지 않는다.

## Review Question

> **현재 task에 필요 없는 context는 줄이면서, 필요한 정보에 도달할 단서는 충분히 남아 있는가?**

둘 중 하나라도 실패하면 disclosure boundary를 다시 조정한다.

## Research Basis

- [Agent Skills Specification](https://agentskills.io/specification) — Skill metadata, instructions, optional resources와 progressive loading의 기본 구조.
- [Agent Skills: Best practices for skill creators](https://agentskills.io/skill-creation/best-practices) — core와 references의 역할, explicit load conditions, non-obvious gotcha의 discoverability 기준.
- [Anthropic: Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) — Skills의 on-demand context loading과 reusable capability 모델.
- [Anthropic: Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) — context efficiency와 progressive disclosure 설계 원칙.
