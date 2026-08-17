---
title: Prompt Canonical Superset
description: 여러 invocation surface에 투영할 repository-local canonical Prompt authoring spec
---

# Prompt Canonical Superset

Prompt Superset은 reusable invocation의 goal, arguments, context와 output contract를 target-independent하게 보존한다.

## Schema

```yaml
---
name: <kebab-case>
description: <string>

targets: [<target>]

arguments:
  <argument-name>:
    required: <boolean>
    default: <value>
    description: <string>

copilot:
  agent: <agent-name-or-mode>
  model: <model>
  tools: [<tool>]

antigravity:
  trigger: </command>
  turbo: <boolean>
---

<prompt body>
```

## Fields

| Field | Requirement | Contract |
| --- | --- | --- |
| `name` | Required | Reusable Prompt identity. `kebab-case`. |
| `description` | Required | Prompt 목적과 사용 시점을 설명한다. |
| `targets` | Optional | 명시하면 지원 target을 제한한다. |
| `arguments` | Optional | Prompt가 받는 canonical inputs와 defaults. |
| `<target>` | Optional | 해당 invocation surface에서만 필요한 agent/model/tool/trigger metadata. |
| body | Required | goal, workflow, constraints와 output contract. |

## Arguments

각 argument는 의미가 필요할 때만 정의한다.

```yaml
arguments:
  pr:
    required: false
    default: current-branch
    description: Pull request number or identifier
```

Target-native placeholder 문법은 canonical spec에 넣지 않는다. Projection에서 해당 target syntax로 변환한다.

## Target Extensions

```yaml
copilot:
  agent: agent

antigravity:
  trigger: /review
  turbo: false
```

이 정보는 Prompt의 공통 task contract가 아니라 target-native invocation behavior다. 따라서 공통 field로 일반화하지 않고 namespaced extension으로 보존한다.

## Body Contract

Body는 필요에 따라 다음을 정의한다.

- goal / intent
- argument interpretation
- task-local constraints
- workflow
- completion criteria
- output semantics

지속 policy는 Rule, 재사용 capability 자체는 Skill, 독립 role/authority는 Agent로 분리한다.

## Minimal Example

```yaml
---
name: review-pr
description: Review a pull request and report evidence-backed findings.
arguments:
  pr:
    required: false
    default: current-branch
    description: Pull request number
---

Review the requested pull request.
Prioritize correctness and regression findings.
```

## Projection Requirements

- `name`, arguments와 body의 task semantics를 보존한다.
- Target-native filename, slash-command name, placeholder syntax는 projection 단계에서 결정한다.
- Agent/model/tool selector가 target에서 지원되지 않고 Prompt 성공에 필수라면 incompatible projection으로 처리한다.

## References

- [GitHub Copilot prompt files](https://docs.github.com/en/copilot/tutorials/customization-library/prompt-files/your-first-prompt-file)
- [Google Antigravity IDE](https://codelabs.developers.google.com/getting-started-agy-ide)
