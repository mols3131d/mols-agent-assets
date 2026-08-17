---
title: Canonical Superset Agent Assets
description: 여러 target harness로 투영되는 Agent Asset의 canonical superset과 projection 관계
---

# Canonical Superset Agent Assets

같은 Agent Asset을 여러 target harness에 배포해야 할 때 하나의 **canonical superset**을 source authority로 두고 target-native asset을 projection으로 만들 수 있다.

Superset은 지원 대상 전체의 의도된 의미를 포괄하는 authoritative source model이다. **모든 target의 최소 공통분모가 아니다.**

```text
canonical superset
├─ shared semantics
├─ target A semantics
└─ target B semantics
        ↓ projection
   target-native assets
```

Superset은 새 Agent Asset 유형이 아니다. Rule, Skill, Prompt, Agent 중 하나의 자산에 적용되는 cross-target ownership model이다.

## Core Model

Canonical superset은 다음을 함께 소유할 수 있다.

- 여러 target이 공유하는 semantic contract와 invariant
- target별 capability 차이 때문에 의도적으로 달라지는 target-scoped semantics
- projection에서 보존해야 할 중요한 behavioral boundary

Target projection은 canonical 의미를 해당 harness가 실행할 수 있는 native form으로 표현한다. format, metadata, placement, package shape와 tool binding 같은 target encoding은 projection에 속한다.

Generated projection은 기본적으로 derived artifact다. target이 표현하지 못하는 의미는 생략·근사·대체 여부를 숨기지 않는다.

Superset은 여러 target이 실제로 필요할 때만 사용한다. 하나의 target만 운용하는 자산에 중간 추상화를 만들 이유는 없다.

## Delivery Route

여러 target을 지원한다고 해서 항상 별도 projection 파일을 만들지는 않는다. 실제 target contract가 허용하는 가장 작은 route를 사용한다.

1. **Direct reuse** — target이 canonical source를 직접 발견하고 필요한 semantics를 소비할 수 있으면 그대로 사용한다.
1. **Canonical fan-out** — canonical superset이 authoritative하고 target-native payload가 따로 필요할 때 projection을 생성한다.
1. **Native bridge** — 이미 하나의 native target asset이 authoritative하면 그 source를 유지하고 필요한 다른 target으로만 bridge한다.

Format이 비슷하다는 이유만으로 direct reuse를 가정하지 않고, 단순 bridge를 위해 별도 canonical layer 채택을 강제하지 않는다.

## By Asset Type

| Asset | Canonical superset owns | Projection adapts |
| --- | --- | --- |
| Rule | policy, constraint, scope semantics | instruction format, placement, selector |
| Skill | capability, activation intent, behavior contract | package shape, discovery metadata, runtime surface |
| Prompt | task intent, inputs, constraints, output contract | invocation format, parameters, target metadata |
| Agent | role, authority, tool/delegation boundary | agent schema, tool binding, handoff representation |

### Rule

Rule superset은 여러 harness에 같은 policy를 배포하면서 target별 scope나 표현 차이까지 한 source authority에서 관리할 때 사용한다. GitHub Copilot과 Google Antigravity 같은 target의 native Rule은 canonical Rule의 projection일 수 있다.

### Skill

Skill superset은 같은 capability와 행동 계약을 서로 다른 runtime profile에 맞게 배포할 때 사용한다. 이 저장소의 `skills/`, `skills-chatbot/`, `skills-chatbot-runtime/` 간 semantic overlap은 이 projection 모델로 설명할 수 있다.

Target에 따라 package surface나 제공 가능한 runtime capability가 다르면 그 차이를 canonical target-scoped semantics로 보존하고 각 projection이 지원 범위에 맞게 표현한다.

### Prompt

Prompt superset은 같은 invocation intent와 input/output contract를 여러 harness의 prompt surface에 맞게 배포할 때 사용한다. target-specific parameter, invocation syntax 또는 지원 기능 차이는 target-scoped semantics나 projection encoding으로 구분한다.

### Agent

Agent superset은 동일한 role과 authority boundary를 여러 harness의 custom-agent 표현으로 배포할 때 사용한다. target별 tool, permission, delegation 차이는 명시적으로 보존하며 사용할 수 없는 기능을 지원되는 것처럼 가장하지 않는다.

## Projection Rules

1. **One authority** — 관리 대상 전체 의미의 source authority는 하나만 둔다.
1. **Full intent** — 공통분모로 축소하지 말고 필요한 target-scoped 차이까지 canonical하게 표현한다.
1. **Semantic fidelity** — projection은 문구 동일성보다 의미와 행동 계약 보존을 우선한다.
1. **Native fit** — target이 요구하는 schema와 idiom에 맞게 표현한다.
1. **Visible loss** — unsupported, omitted, approximated semantics를 숨기지 않는다.
1. **Explicit locality** — canonical 밖에 남기는 target-only 의미는 local extension임을 명확히 한다.
1. **Target validation** — 각 projection은 실제 target contract에 맞게 검증한다.

## DRY Boundary

Canonical source와 target projection에 관련 의미가 함께 존재하는 것은 그 자체로 DRY 위반이 아니다. 서로 다른 runtime surface가 독립 payload를 요구한다면 필요한 semantic overlap이다.

문제는 같은 관리 대상 의미가 여러 파일에서 **독립 authority**로 진화하여 서로 다른 답을 가지게 되는 경우다.

## Boundary

- Superset은 Rule, Skill, Prompt, Agent에 공통 적용 가능한 repository-local authoring/deployment model이다.
- 모든 자산에 superset을 강제하지 않는다.
- 하나의 범용 중간 schema나 transpiler를 요구하지 않는다.
- target-specific capability를 억지로 공통분모로 축소하지 않는다.
- Prompt와 Agent에 별도 target profile 규격이 생기기 전까지 이 문서는 구체적인 vendor schema나 placement를 정의하지 않는다.
- platform/system/user instruction과 target harness의 강제 규격이 이 convention보다 우선한다.
