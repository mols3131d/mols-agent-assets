---
title: Personal Agent Asset Standard
description: 외부 baseline을 확장한 repository-local Agent Asset taxonomy와 placement 표준
---

# Personal Agent Asset Standard

이 문서는 [Agent Asset Standard Baseline](agent-assets-standard-baseline.md)을 바탕으로 이 저장소에서 사용하는 **공통 taxonomy와 placement 기준**을 정의합니다.

유형별 projection, authoring, packaging 세부사항은 실제 focused reference가 있을 때 해당 문서가 소유합니다. 이 문서는 이를 다시 정의하지 않습니다.

## Asset Types

이 저장소의 동급 Agent Asset 유형은 네 가지입니다.

| Type | Responsibility | Core question |
| --- | --- | --- |
| Rule | 지속 적용되는 policy와 constraint | 이 scope에서 무엇을 계속 지켜야 하는가? |
| Skill | 재사용 capability와 조건부 context | 지금 어떤 capability/context가 필요한가? |
| Prompt | 현재 invocation의 goal과 일회성 context | 지금 무엇을 원하는가? |
| Agent | 독립 role, authority, tools, delegation | 누가 어떤 권한으로 행동하는가? |

`references/`, `scripts/`, `assets/`, docs, evals, tests 같은 supporting resource는 이 네 유형을 지원하지만 동급 behavioral asset type은 아닙니다.

Chatbot과 coding agent는 이 taxonomy에서 별도 actor type으로 구분하지 않습니다. 특정 runtime이 가진 tool capability보다 **agent harness의 context·asset discovery/loading behavior** 차이를 별도 문제로 다룹니다.

## Placement

새 자산은 다음 질문으로 분류합니다.

1. 여러 task에서 특정 scope에 지속되는 policy인가? → **Rule**
1. 반복 capability 또는 상황에 따라 로드할 context인가? → **Skill**
1. 현재 invocation에서만 필요한 goal이나 constraint인가? → **Prompt**
1. 독립 role, authority, tool, delegation boundary가 필요한가? → **Agent**

재사용 가능하다는 이유만으로 Skill로 만들지 않습니다. 반대로 별도 role이나 지속 policy가 필요하지 않은 reusable capability/context는 Skill이 기본 후보입니다.

특정 **work surface가 활성화된 동안에는 항상 필요하지만 다른 task에는 불필요한 baseline context**는 전역 Rule 대신 scope baseline Skill loader로 둘 수 있습니다. 이 경우 scope 내부의 넓은 activation은 의도된 coverage이며, 세부 activation과 review 규칙은 유형별 Skill reference가 소유합니다.

AgentsMesh가 충실히 표현할 수 있는 Rule, Skill, Agent는 `src/agentsmesh/` native workspace 안의 `src/agentsmesh/.agentsmesh/`를 canonical source로 사용합니다. Repository root `.agentsmesh/`는 distribution source로 사용하지 않습니다. `src/`의 다른 peer는 현재 AgentsMesh contract 밖의 실제 custom/non-standard 요구가 있을 때만 사용하는 exception surface이며 parallel taxonomy가 아닙니다.

### Optional Asset Documentation

개별 자산의 maintainer 문서는 **선택적 supporting resource**입니다. 모든 자산에 문서 directory를 만들지 않습니다.

이 저장소에서 특정 자산의 maintainer-only 문서가 실제로 필요하면 다음 위치를 사용합니다.

```text
docs/<asset-type>/<asset-name>/
```

예: `docs/skills/<skill-name>/`, `docs/agents/<agent-name>/`.

다음 중 하나 이상이 실질적인 유지보수 가치를 만들 때만 생성합니다.

- source만으로 purpose, architecture 또는 중요한 책임 경계를 복구하기 어렵다.
- refactor·단순화 과정에서 intent, invariant, non-goal이 훼손될 위험이 크다.
- durable decision, trade-off 또는 recovery/migration 지식이 필요하다.
- baseline을 별도 보존하면 향후 회귀·복구 비용이 의미 있게 낮아진다.

단순하고 self-explanatory한 자산, 임시 작업 로그, 쉽게 재생성되는 상태에는 만들지 않습니다. Runtime-required 지식은 canonical/deployable 자산 surface가 소유합니다. `docs/references/<asset-type>/`은 유형 전체가 공유하는 reference이며, `docs/<asset-type>/<asset-name>/`은 특정 자산 하나의 maintainer 지식입니다.

빈 reference나 미래용 placeholder를 authority로 만들지 않습니다. 실제 책임과 내용이 생길 때만 focused reference를 추가합니다.

## Type-Specific Standards

공통 taxonomy와 유형별 repository-local extension을 분리합니다.

현재 실제 focused authority는 다음과 같습니다.

- Rule projection → [Rule Projections](../../rules/agent-assets-rules-projections.md)
- Skill-specific Personal Standard → [Personal Skill Standard](../../skills/agent-assets-skills-standard-personal.md)
- Skill package / target boundary → [Skill Package and Target Boundaries](../../skills/agent-assets-skills-target-profiles.md)

Prompt와 Agent에는 현재 별도의 repository-local type-wide reference가 없습니다. 공통 taxonomy, 실제 canonical asset contract, 적용 가능한 target/vendor contract를 사용하고 독립적인 durable responsibility가 생길 때만 focused reference를 추가합니다.

Skill의 Tier 1 open standard와 Tier 2 vendor/harness 공식 원문 registry는 [Agent Skills Specification](../../skills/agent-skills-io/agent-skills-io-specification.md)이 소유합니다. 이 공통 Personal Standard에서 외부 Skill 규격을 다시 정의하지 않습니다.

## Local Extensions

다음은 외부 범용 표준이 아니라 이 저장소의 의도적인 확장입니다.

- 공통 filesystem naming convention → [Agent Asset Naming Convention](agent-assets-naming-convention.md)
- `src/agentsmesh/` native workspace 안의 canonical source와 active target projection 경계
- root `CHATBOT.md` chat-runtime harness compatibility convention → [CHATBOT Runtime Compatibility Layer](chatbot-repository-bootstrap.md)
- directory/glob Rule projection convention
- 필요할 때만 사용하는 `docs/<asset-type>/<asset-name>/` maintainer documentation convention
- Skill-specific authoring/deployment convention

`CHATBOT.md`는 Rule, Skill, Prompt, Agent와 동급의 Agent Asset type이 아닙니다. repository-aware chat runtime에서 누락되는 agent harness의 context·asset discovery/loading을 보정하는 **개인 compatibility convention**입니다. 별도 project policy surface로 사용하지 않으며 세부 contract는 전용 reference가 소유합니다.

Skill 확장의 상세 목록과 경계는 [Personal Skill Standard](../../skills/agent-assets-skills-standard-personal.md)가 소유합니다. 공통 표준에서는 이를 다시 나열하지 않습니다.

## Authority

외부 specification은 baseline의 근거이고, 이 저장소의 실제 운용에서는 이 Personal Standard와 실제 유형별 Personal Standard/reference가 repository-local authority입니다.

단, platform/system/user instruction과 target harness의 강제 규격이 repository-local convention보다 우선합니다.

## Review Test

새 규칙이나 구조를 추가하기 전에 확인합니다.

- 공통 taxonomy인가, 특정 자산 유형의 세부 규격인가?
- 이미 다른 문서가 같은 의미를 authoritative하게 소유하는가?
- 실제 내용과 책임이 있는가, 미래 확장을 위한 placeholder인가?
- 현재 요구가 있는가, 미래 확장을 예상한 것인가?
- 별도 자산이나 abstraction이 실제 판단 복잡도를 줄이는가?
- 자산별 maintainer 문서가 실제 훼손·복구 위험을 줄이는가, 아니면 문서 구조만 늘리는가?

유형별 세부사항이면 `common/`에 넣지 않습니다.
