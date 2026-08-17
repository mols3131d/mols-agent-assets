---
title: Agent Asset Standard Baseline
description: 외부 생태계와 공개 규격에서 반복적으로 나타나는 Agent customization 자산 개념의 최소 baseline
---

# Agent Asset Standard Baseline

이 문서는 여러 agent/chatbot 생태계에서 **표준 또는 표준에 가까운 형태로 반복되는 공통 개념만** 정리한다.

하나의 범용 Agent Asset 표준이 모든 플랫폼에 존재한다는 뜻은 아니다. 파일명, schema, precedence와 activation semantics는 플랫폼마다 다르다.

## Baseline Concepts

| Concept | Common responsibility |
| --- | --- |
| Instruction / Rule | 일정 scope에서 지속 적용되는 policy와 constraint |
| Skill | 필요할 때 활성화되는 reusable capability와 optional resources |
| Prompt | 특정 invocation의 task intent와 입력 구조 |
| Agent | 독립 role, instructions, tools, authority, handoff/delegation을 가진 runtime actor |

이 네 책임이 여러 생태계에서 반복된다는 의미이며 모든 플랫폼이 같은 이름과 형식을 제공한다는 의미는 아니다.

## Instructions / Rules

지속 지침은 repository-wide, path-specific, agent-specific 같은 scope로 제공될 수 있다.

파일명, nested discovery, glob syntax와 precedence는 harness-specific이므로 범용 Rule file format을 가정하지 않는다.

## Skills

Agent Skills specification에서 Skill은 `SKILL.md`와 optional bundled resources를 가진 reusable capability다.

```text
skill-name/
├─ SKILL.md
├─ scripts/
├─ references/
└─ assets/
```

주요 특성은 metadata 기반 discovery, activation, optional resource loading과 progressive disclosure다. 공식 guidance의 token 권장은 repository-local budget과 구분한다.

## Prompts

Prompt는 현재 invocation 또는 반복 가능한 invocation template의 task intent를 표현한다. persistent policy나 독립 runtime actor를 대신하지 않는다.

## Agents

Agent는 일반적으로 role/instructions, tools, authority/permissions, handoff/delegation과 output responsibility를 결합한 runtime actor다.

단순히 instructions가 길거나 specialization 이름이 필요하다는 이유만으로 Agent가 요구되는 것은 아니다.

## Supporting Resources

`references/`, `scripts/`, `assets/`, docs, evals, tests 등은 독립적인 peer behavioral asset type이라기보다 다른 자산을 지원하는 resource로 본다.

## Not Defined Here

다음은 외부 공통 baseline이 아니라 이 저장소의 repository-local extension이다.

- `CHATBOT.md`와 fallback chain
- directory/glob Rule projection convention
- `load-context-*` naming
- `skills/`, `skills-chatbot/`, `skills-chatbot-runtime/` target profiles
- flat chatbot Skill의 `<4,000 tokens` budget
- Skill package의 dot-prefixed non-runtime surface
- `.docs/baseline/` preservation convention

실제 운용 기준은 [Personal Agent Asset Standard](agent-assets-standard-personal.md)와 유형별 reference가 소유한다.

## Primary Sources

- [Agent Skills Specification](https://agentskills.io/specification)
- [GitHub Copilot: About customizing responses](https://docs.github.com/en/copilot/concepts/prompting/response-customization)
- [GitHub Copilot: Custom instructions support](https://docs.github.com/en/copilot/reference/custom-instructions-support)
- [OpenAI Agents SDK: Agents](https://openai.github.io/openai-agents-python/agents/)
