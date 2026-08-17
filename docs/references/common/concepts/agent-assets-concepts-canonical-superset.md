---
title: Canonical Superset Agent Assets
description: 여러 target harness로 투영되는 Agent Asset의 canonical superset과 projection 관계
---

# Canonical Superset Agent Assets

같은 Agent Asset 의미를 여러 target harness에 배포해야 할 때 하나의 **canonical superset**을 source authority로 두고 target-native asset을 projection으로 만들 수 있다.

```text
canonical superset
├─ target A projection
├─ target B projection
└─ target C projection
```

Superset은 새 Agent Asset 유형이 아니다. Rule, Skill, Prompt, Agent 중 하나의 자산이 여러 target 표현을 포괄하는 **authoritative source model**이다.

## Core Model

- canonical superset이 공통 semantic contract와 invariant를 소유한다.
- target projection은 harness가 요구하는 format, metadata, placement와 표현 차이를 소유한다.
- generated projection은 기본적으로 derived artifact다.
- target-only behavior는 extension으로 분리한다.
- target이 표현하지 못하는 의미는 숨기지 않는다.
- 이미 native target asset이 authoritative하면 이를 유지한 채 다른 target으로 bridge할 수 있다.

Superset은 여러 target이 실제로 필요할 때만 사용한다. 하나의 target만 운용하는 자산에 중간 추상화를 만들 이유는 없다.

## By Asset Type

| Asset | Canonical superset owns | Projection adapts |
| --- | --- | --- |
| Rule | policy, constraint, scope semantics | instruction format, placement, selector |
| Skill | capability, activation intent, behavior contract | package shape, discovery metadata, runtime surface |
| Prompt | task intent, inputs, constraints, output contract | invocation format, parameters, target metadata |
| Agent | role, authority, tool/delegation boundary | agent schema, tool binding, handoff representation |

### Rule

Rule superset은 여러 harness에 동일한 policy 의미를 배포할 때 사용한다. GitHub Copilot과 Google Antigravity 같은 target의 native Rule은 canonical policy의 projection일 수 있다.

### Skill

Skill superset은 같은 capability를 서로 다른 runtime profile에 맞게 배포할 때 사용한다. 이 저장소의 `skills/`, `skills-chatbot/`, `skills-chatbot-runtime/` 간 semantic overlap은 이 projection 모델로 설명할 수 있다.

### Prompt

Prompt superset은 같은 invocation intent와 input/output contract를 여러 harness의 prompt surface에 맞게 배포해야 할 때 사용한다. target-specific parameter나 invocation syntax는 projection에서 다룬다.

### Agent

Agent superset은 동일한 role과 authority boundary를 여러 harness의 custom-agent 표현으로 배포해야 할 때 사용한다. 사용할 수 없는 tool이나 delegation semantics를 지원되는 것처럼 가장하지 않는다.

## Projection Rules

1. **One authority** — 공통 의미의 source authority는 하나만 둔다.
1. **Semantic fidelity** — projection은 문구 동일성보다 의미와 행동 계약 보존을 우선한다.
1. **Native fit** — target이 요구하는 schema와 idiom에 맞게 표현한다.
1. **Visible loss** — unsupported, omitted, approximated semantics를 숨기지 않는다.
1. **Explicit extension** — target-only behavior는 공통 의미와 구분한다.
1. **Target validation** — 각 projection은 실제 target contract에 맞게 검증한다.

## DRY Boundary

Canonical source와 target projection에 관련 의미가 함께 존재하는 것은 그 자체로 DRY 위반이 아니다. 서로 다른 runtime surface가 독립 payload를 요구한다면 필요한 semantic overlap이다.

문제는 같은 공통 의미가 여러 파일에서 **독립 authority**로 진화하여 서로 다른 답을 가지게 되는 경우다.

## Boundary

- Superset은 Rule, Skill, Prompt, Agent에 공통 적용 가능한 repository-local authoring/deployment model이다.
- 모든 자산에 superset을 강제하지 않는다.
- 하나의 범용 중간 schema나 transpiler를 요구하지 않는다.
- target-specific capability를 억지로 공통분모로 축소하지 않는다.
- platform/system/user instruction과 target harness의 강제 규격이 이 convention보다 우선한다.
