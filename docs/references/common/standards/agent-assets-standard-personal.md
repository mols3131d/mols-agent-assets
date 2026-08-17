---
title: Personal Agent Asset Standard
description: 외부 baseline을 확장한 repository-local Agent Asset taxonomy와 placement 표준
---

# Personal Agent Asset Standard

이 문서는 [Agent Asset Standard Baseline](agent-assets-standard-baseline.md)을 바탕으로 이 저장소에서 사용하는 **공통 taxonomy와 placement 기준**을 정의한다.

유형별 projection과 packaging 세부사항은 각 유형 reference가 소유한다. 이 문서는 이를 다시 정의하지 않는다.

## Asset Types

이 저장소의 동급 Agent Asset 유형은 네 가지다.

| Type | Responsibility | Core question |
| --- | --- | --- |
| Rule | 지속 적용되는 policy와 constraint | 이 scope에서 무엇을 계속 지켜야 하는가? |
| Skill | 재사용 capability와 조건부 context | 지금 어떤 capability/context가 필요한가? |
| Prompt | 현재 invocation의 goal과 일회성 context | 지금 무엇을 원하는가? |
| Agent | 독립 role, authority, tools, delegation | 누가 어떤 권한으로 행동하는가? |

`references/`, `scripts/`, `assets/`, docs, evals, tests 같은 supporting resource는 이 네 유형을 지원하지만 동급 behavioral asset type은 아니다.

## Placement

새 자산은 다음 질문으로 분류한다.

1. 여러 task에서 특정 scope에 지속되는 policy인가? → **Rule**
1. 반복 capability 또는 상황에 따라 로드할 context인가? → **Skill**
1. 현재 invocation에서만 필요한 goal이나 constraint인가? → **Prompt**
1. 독립 role, authority, tool, delegation boundary가 필요한가? → **Agent**

재사용 가능하다는 이유만으로 Skill로 만들지 않는다. 반대로 별도 role이나 지속 policy가 필요하지 않은 reusable capability/context는 Skill이 기본 후보다.

## Type-Specific Standards

공통 taxonomy와 유형별 deployment convention을 분리한다.

- Rule projection과 chatbot fallback → [Rule Projections](../../rules/agent-assets-rules-projections.md)
- Skill target profile과 package surface → [Skill Target Profiles](../../skills/agent-assets-skills-target-profiles.md)

Prompt와 Agent에 repository-local 규격이 실제로 생기기 전에는 별도 표준 문서를 만들지 않는다.

## Local Extensions

다음은 외부 범용 표준이 아니라 이 저장소의 의도적인 확장이다.

- `CHATBOT.md`와 repository-local fallback
- directory/glob Rule projection convention
- `skills/`, `skills-chatbot/`, `skills-chatbot-runtime/` target profiles
- flat chatbot Skill의 `<4,000 tokens` budget
- Skill package의 dot-prefixed non-runtime surface
- `.docs/baseline/` preservation convention
- `load-context-*` naming convention

세부 의미와 적용 조건은 해당 유형 reference가 소유한다.

## Authority

외부 specification은 baseline의 근거이고, 이 저장소의 실제 운용에서는 이 Personal Standard와 유형별 reference가 repository-local authority다.

단, platform/system/user instruction과 target harness의 강제 규격이 repository-local convention보다 우선한다.

## Review Test

새 규칙이나 구조를 추가하기 전에 확인한다.

- 공통 taxonomy인가, 특정 자산 유형의 세부 규격인가?
- 이미 다른 문서가 같은 의미를 authoritative하게 소유하는가?
- 현재 요구가 있는가, 미래 확장을 예상한 것인가?
- 별도 자산이나 abstraction이 실제 판단 복잡도를 줄이는가?

유형별 세부사항이면 `common/`에 넣지 않는다.
