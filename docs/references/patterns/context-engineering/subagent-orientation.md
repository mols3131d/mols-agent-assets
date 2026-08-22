---
description: Subagent를 엄격한 유형으로 분류하지 않고 responsibility orientation과 execution context라는 두 설계 축으로 판단할 때 사용하는 reusable pattern입니다.
---

# Subagent Orientation

Subagent를 서로 배타적인 유형으로 분류하지 않습니다. 대신 **무엇을 중심으로 책임을 정의하는가**와 **작업 context를 어디에 둘 것인가**를 별도 축으로 봅니다.

| Dimension | One end | Other end |
| --- | --- | --- |
| Responsibility orientation | `Role-oriented` | `Capability-oriented` |
| Execution context | `Shared` | `Isolated` |

두 축은 관련될 수 있지만 동일하지 않습니다. Capability-oriented 작업은 isolated context와 잘 결합되는 경우가 많지만, Role-oriented Subagent도 격리할 수 있고 Capability-oriented Subagent도 shared context에서 실행할 수 있습니다. 각 축은 개념적 방향이며 runtime은 그 사이의 다양한 형태를 구현할 수 있습니다.

## Responsibility Orientation

대부분의 Subagent는 Role과 Capability 요소를 함께 가집니다. 중요한 것은 어느 쪽이 **instruction budget, invocation contract, 책임 경계**를 더 많이 결정하는지입니다.

### Role-oriented

Subagent를 하나의 **책임 있는 역할**로 정의하는 방향입니다.

다음 요소의 비중이 큽니다.

- 목적과 책임
- 권한과 금지된 행동
- in-scope / out-of-scope
- 판단 기준과 invariants
- anti-pattern과 failure boundary
- 다른 역할과의 handoff 또는 escalation

Tool과 Skill은 역할을 수행하기 위한 수단이며 특정 도구 목록 자체가 역할의 정체성이 되지 않습니다.

여러 종류의 작업을 같은 책임 아래 판단하거나 자율적인 판단·조율·최종 책임이 중요한 Subagent에 잘 맞습니다. 예: review lead, release steward, incident coordinator, architecture reviewer.

### Capability-oriented

Subagent를 반복해서 호출할 수 있는 **bounded capability 또는 specialist**로 정의하는 방향입니다.

다음 요소의 비중이 큽니다.

- 단일 작업 또는 서로 강하게 결합된 소수 작업
- 입력과 반환 결과
- 사용할 tool과 자주 필요한 Skill
- 실행 제약과 side-effect boundary
- caller가 결과를 소비하는 handoff contract

핵심은 "누구인가"보다 **무엇을 안정적으로 수행하는가**입니다. caller 입장에서는 고수준 tool이나 specialist처럼 사용할 수 있습니다.

검색, 테스트, 정적 분석, 특정 도메인 검토, 변환, 검증처럼 반복 가능하고 비교적 좁은 작업에 잘 맞습니다. 예: test runner, dependency analyst, security checker, adversarial reviewer, research specialist.

Role과 Capability를 억지로 하나만 고르지 않습니다. Reviewer처럼 bounded capability를 가지면서 read-only 권한과 evidence rule을 함께 가질 수 있고, Role-oriented agent도 특정 Skill과 tool을 자주 사용할 수 있습니다.

## Execution Context

이 축은 작업 중 생기는 context를 parent와 얼마나 공유할지 결정합니다.

`Shared`는 instruction, 탐색 결과, tool output과 중간 판단이 parent context에 계속 남아 이후 작업에도 유용할 때 자연스럽습니다.

`Isolated`는 탐색, 대량의 file/tool output, 중간 판단처럼 **caller가 계속 보유할 필요가 없는 working context를 별도 실행 경계 안에 두고 필요한 결과만 반환**할 때 유용합니다. Context pollution과 signal dilution을 줄이는 것이 주요 목적이 될 수 있습니다.

Capability-oriented 작업은 bounded input/output을 가지기 쉬워 isolation과 특히 잘 결합되지만, isolation 자체가 Capability-oriented의 정의는 아닙니다.

### Handoff as Context Boundary

Isolated execution에서 handoff는 단순한 결과 형식이 아니라 **context boundary의 public contract**가 될 수 있습니다.

필요한 경우 다음을 정의합니다.

- caller가 전달할 최소 input과 scope
- 내부에 남겨도 되는 intermediate context
- 반드시 반환할 result, evidence, uncertainty와 blocker
- 수행한 side effect와 verification state
- caller의 다음 판단에 불필요한 세부사항을 반환하지 않는 기준

전체 transcript나 탐색 과정을 그대로 반환하면 isolation의 이점을 잃습니다. 반대로 evidence와 uncertainty까지 제거하면 caller가 결과를 신뢰하거나 이어서 판단하기 어렵습니다. Handoff는 **다음 결정을 위한 최소 충분 context**를 전달합니다.

## Skills and Execution Boundary

Skill과 Subagent는 서로 배타적인 대안이 아닙니다.

- **Skill**은 reusable capability, procedure, knowledge와 resource를 패키징하는 자산입니다.
- **Subagent**는 delegated execution, context, tool/permission 또는 specialist boundary를 표현할 수 있습니다.
- Subagent는 하나 이상의 Skill을 사용할 수 있습니다.
- Runtime이 지원하면 Skill 자체도 shared context가 아니라 isolated context에서 실행할 수 있습니다.

따라서 핵심 질문은 "Skill인가 Subagent인가"보다 **이 capability를 어디에서 실행하고 어떤 context만 경계를 넘어가게 할 것인가**에 가깝습니다.

대표 선택지는 다음과 같습니다.

1. Parent context에 작업 과정이 남아야 하면 Skill이나 capability를 shared context에서 실행합니다.
1. Isolation만 필요하고 runtime이 forked/isolated Skill을 지원하면 더 작은 native mechanism을 우선할 수 있습니다.
1. 별도 context와 함께 tool, permission, specialist identity 또는 명시적인 handoff contract가 유용하면 Capability-oriented Subagent가 자연스럽습니다.

예를 들어 GitHub Copilot for VS Code는 현재 experimental `context: fork`로 Skill을 dedicated subagent context에서 실행하고 final result만 parent에 반환할 수 있습니다. 이는 이 pattern의 구현 예시일 뿐이며 현재 semantics는 [Agent Skills in VS Code](https://code.visualstudio.com/docs/agent-customization/agent-skills)가 소유합니다.

[Agent Skills](https://agentskills.io/) 자체는 open format이므로 Subagent 형식이 Skill보다 더 portable하다고 가정하지 않습니다. Vendor-neutral하게 재사용할 수 있는 것은 **isolated delegated execution + bounded handoff라는 설계 아이디어**이며, 실제 Subagent schema, context inheritance, invocation과 permission semantics는 runtime마다 다를 수 있습니다.

## Design Heuristic

Subagent를 설계할 때 다음 질문을 독립적으로 봅니다.

1. 품질을 더 크게 좌우하는 것은 **올바른 판단 경계와 책임**인가, **특정 작업을 안정적으로 수행하는 capability**인가?
1. Intermediate context를 parent에 남기는 것이 유익한가, 아니면 **격리하고 최소 충분 결과만 handoff하는 것이 더 유익한가?**
1. Isolation이 필요하다면 현재 runtime의 더 작은 native mechanism으로 충분한가, 아니면 별도 Subagent boundary가 실질적인 이점을 주는가?

첫 질문은 Responsibility orientation을, 두 번째와 세 번째는 Execution context와 구현 선택을 돕습니다. 어느 답도 filename, directory 또는 framework metadata만으로 고정하지 않습니다.

## Considerations

다음을 피합니다.

- Role과 Capability를 공식 taxonomy처럼 강제하는 것
- 역할의 책임을 tool 목록으로 대신 설명하는 것
- specialist에게 필요 이상의 최종 결정권이나 넓은 자율권을 주는 것
- isolation 목적 없이 Skill이나 단순 procedure로 충분한 작업을 Subagent로 포장하는 것
- 격리한 intermediate context를 handoff에서 다시 전부 parent에 주입하는 것
- 특정 vendor의 context-forking 기능을 pattern의 본질로 만드는 것

## Boundary

이 pattern은 Subagent의 **responsibility orientation과 execution context를 판단하는 설계 관점**을 설명합니다. 공식 Subagent taxonomy, runtime lifecycle, delegation protocol, vendor-specific frontmatter, tool permission model 또는 orchestration framework를 정의하지 않습니다.

구체적인 source/target representation과 runtime semantics는 사용 중인 framework와 runtime의 authoritative contract를 따릅니다.
