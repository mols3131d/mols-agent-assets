---
title: Personal Agent Asset Standard
description: 외부 baseline을 확장한 repository-local Agent Asset taxonomy와 placement 표준
---

# Personal Agent Asset Standard

이 문서는 [Agent Asset Standard Baseline](agent-assets-standard-baseline.md)을
바탕으로 이 저장소에서 사용하는 **공통 taxonomy와 placement 기준**을 정의한다.

유형별 projection, authoring, packaging 세부사항은 각 유형 reference가 소유한다.
이 문서는 이를 다시 정의하지 않는다.

## Asset Types

이 저장소의 동급 Agent Asset 유형은 네 가지다.

| Type | Responsibility | Core question |
| --- | --- | --- |
| Rule | 지속 적용되는 policy와 constraint | 이 scope에서 무엇을 계속 지켜야 하는가? |
| Skill | 재사용 capability와 조건부 context | 지금 어떤 capability/context가 필요한가? |
| Prompt | 현재 invocation의 goal과 일회성 context | 지금 무엇을 원하는가? |
| Agent | 독립 role, authority, tools, delegation | 누가 어떤 권한으로 행동하는가? |

`references/`, `scripts/`, `assets/`, docs, evals, tests 같은 supporting resource는
이 네 유형을 지원하지만 동급 behavioral asset type은 아니다.

## Placement

새 자산은 다음 질문으로 분류한다.

1. 여러 task에서 특정 scope에 지속되는 policy인가? → **Rule**
1. 반복 capability 또는 상황에 따라 로드할 context인가? → **Skill**
1. 현재 invocation에서만 필요한 goal이나 constraint인가? → **Prompt**
1. 독립 role, authority, tool, delegation boundary가 필요한가? → **Agent**

재사용 가능하다는 이유만으로 Skill로 만들지 않는다. 반대로 별도 role이나 지속
policy가 필요하지 않은 reusable capability/context는 Skill이 기본 후보다.

특정 **work surface가 활성화된 동안에는 항상 필요하지만 다른 task에는 불필요한 baseline context**는 전역 Rule 대신 scope baseline Skill loader로 둘 수 있다. 이 경우 scope 내부의 넓은 activation은 의도된 coverage이며, 세부 activation과 review 규칙은 유형별 Skill reference가 소유한다.

## Type-Specific Standards

공통 taxonomy와 유형별 repository-local extension을 분리한다.

여러 target harness에 같은 자산 의미를 투영할 때의 공통 authority 모델은
[Canonical Superset Agent Assets](../concepts/agent-assets-concepts-canonical-superset.md)가
소유한다. 유형별 문서는 해당 자산의 projection surface와 target contract만 정의한다.

- Rule projection과 chatbot fallback →
  [Rule Projections](../../rules/agent-assets-rules-projections.md)
- Skill-specific Personal Standard →
  [Personal Skill Standard](../../skills/agent-assets-skills-standard-personal.md)

Skill의 Tier 1 open standard와 Tier 2 vendor/harness 공식 원문 registry는
[Agent Skills Specification](../../skills/agent-skills-io/agent-skills-io-specification.md)이
소유한다. 이 공통 Personal Standard에서 외부 Skill 규격을 다시 정의하지 않는다.

Skill target profile과 package surface의 상세 규격은 Personal Skill Standard가
연결하는 focused reference가 소유한다.

Prompt와 Agent에 repository-local 규격이 실제로 생기기 전에는 별도 표준 문서를
만들지 않는다.

## Local Extensions

다음은 외부 범용 표준이 아니라 이 저장소의 의도적인 확장이다.

- 공통 filesystem naming convention →
  [Agent Asset Naming Convention](agent-assets-naming-convention.md)
- cross-harness canonical superset과 target projection authority model
- `CHATBOT.md`와 repository-local fallback
- directory/glob Rule projection convention
- Skill-specific authoring/deployment convention

Skill 확장의 상세 목록과 경계는
[Personal Skill Standard](../../skills/agent-assets-skills-standard-personal.md)가
소유한다. 공통 표준에서는 이를 다시 나열하지 않는다.

## Authority

외부 specification은 baseline의 근거이고, 이 저장소의 실제 운용에서는 이
Personal Standard와 유형별 Personal Standard/reference가 repository-local
authority다.

단, platform/system/user instruction과 target harness의 강제 규격이
repository-local convention보다 우선한다.

## Review Test

새 규칙이나 구조를 추가하기 전에 확인한다.

- 공통 taxonomy인가, 특정 자산 유형의 세부 규격인가?
- 이미 다른 문서가 같은 의미를 authoritative하게 소유하는가?
- 현재 요구가 있는가, 미래 확장을 예상한 것인가?
- 별도 자산이나 abstraction이 실제 판단 복잡도를 줄이는가?

유형별 세부사항이면 `common/`에 넣지 않는다.
