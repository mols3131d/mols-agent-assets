---
title: Progressive Disclosure
description: 필요한 context만 필요한 시점에 로드하도록 discovery, core instruction, resource 경계를 설계하는 원칙
---

# Progressive Disclosure

Progressive disclosure는 **모든 정보를 처음부터 context에 넣지 않고 현재 판단에 필요한 정보만 단계적으로 노출하는 것**이다.

## Loading Model

| Layer | Contains | Loaded when |
| --- | --- | --- |
| Discovery | capability와 activation trigger | 자산을 찾을 때 |
| Core | 공통 workflow, critical constraint, routing | 활성화될 때 |
| Detail | variant/domain/error별 reference와 resource | 조건이 충족될 때 |

각 layer는 다음 layer가 필요한지 판단할 단서를 남겨야 한다.

## Rules

- discovery에는 선택에 필요한 정보만 둔다.
- core에는 모든 실행에 공통인 행동과 중요한 guardrail을 둔다.
- 특정 variant에만 필요한 상세 지식은 focused resource로 분리한다.
- `필요하면 읽는다` 대신 **condition → resource**를 직접 연결한다.
- trigger 자체를 알아차리기 어려운 중요한 gotcha는 core에 남긴다.
- core에서 resource로 직접 도달하게 하고 reference chain을 얕게 유지한다.
- 분리로 탐색과 routing이 더 복잡해지면 분리하지 않는다.

## Discoverability Test

> 이 내용을 아직 읽지 않은 agent도 언제 이 resource가 필요한지 알아차릴 수 있는가?

- `Yes` → detail로 분리할 수 있다.
- `No` → trigger 또는 핵심 gotcha를 core에 남긴다.

좋은 routing:

```text
API가 non-200 response를 반환하면 references/api-errors.md를 읽는다.
```

피할 routing:

```text
필요하면 관련 reference를 확인한다.
```

## Boundary

별도 Skill/Agent로 나눌지는 progressive disclosure가 아니라 [SRP](srp.md)가 결정한다. activation intent와 responsibility가 같다면 먼저 같은 자산 안의 resource 분리를 검토한다.

## Sources

- [Agent Skills Specification](https://agentskills.io/specification)
- [Agent Skills: Best practices for skill creators](https://agentskills.io/skill-creation/best-practices)
- [Anthropic: Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
