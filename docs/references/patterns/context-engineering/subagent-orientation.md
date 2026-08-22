---
description: Subagent를 엄격한 유형으로 분류하지 않고 Role-oriented와 Capability-oriented 사이의 설계 방향으로 판단할 때 사용하는 reusable pattern입니다.
---

# Subagent Orientation

Subagent를 서로 배타적인 유형으로 분류하지 않습니다. 대신 **무엇을 중심으로 정의하는가**에 따라 `Role-oriented`와 `Capability-oriented` 사이의 orientation으로 봅니다.

```text
Role-oriented  <──────────── mixed ────────────>  Capability-oriented
```

대부분의 Subagent는 두 요소를 모두 가질 수 있습니다. 중요한 것은 어느 쪽이 그 Subagent의 **instruction budget, invocation contract, 책임 경계**를 더 많이 결정하는지입니다.

## Role-oriented

Subagent를 하나의 **책임 있는 역할**로 정의하는 방향입니다.

다음 요소의 비중이 큽니다.

- 목적과 책임
- 권한과 금지된 행동
- in-scope / out-of-scope
- 판단 기준과 invariants
- anti-pattern과 failure boundary
- 다른 역할과의 handoff 또는 escalation

Tool과 Skill은 역할을 수행하기 위한 수단입니다. 특정 도구 목록 자체가 역할의 정체성이 되지 않습니다.

이 orientation은 여러 종류의 작업을 같은 책임 아래 판단해야 하거나, 자율적인 판단·조율·최종 책임이 중요한 Subagent에 잘 맞습니다.

예: review lead, release steward, incident coordinator, architecture reviewer.

## Capability-oriented

Subagent를 반복해서 호출할 수 있는 **bounded capability 또는 specialist**로 정의하는 방향입니다.

이 orientation을 Skill 같은 다른 reusable asset 대신 선택하는 가장 중요한 이유 중 하나는 **context isolation**입니다. 탐색, tool output, 중간 판단, 대량의 파일 내용처럼 caller에게 계속 남을 필요가 없는 작업 context를 별도 실행 경계 안에 두고, 필요한 결과만 handoff하여 parent context의 오염과 signal dilution을 줄일 수 있습니다.

다음 요소의 비중이 큽니다.

- 수행할 단일 작업 또는 서로 강하게 결합된 소수 작업
- 입력과 반환 결과
- 사용할 tool과 자주 필요한 Skill
- 실행 제약과 side-effect boundary
- caller가 결과를 어떻게 소비할지에 대한 handoff contract
- 내부 작업 context 중 무엇을 local로 남기고 무엇만 parent에 반환할지

필요하면 역할 설명도 포함하지만, 핵심은 "누구인가"보다 **무엇을 격리된 경계 안에서 안정적으로 수행하고 무엇을 반환하는가**입니다. 잘 설계된 경우 caller 입장에서는 고수준 tool이나 specialist처럼 사용할 수 있습니다.

이 orientation은 검색, 테스트, 정적 분석, 특정 도메인 검토, 변환, 검증처럼 반복 가능하고 비교적 좁으면서 중간 context가 많이 생기는 작업에 특히 잘 맞습니다.

예: test runner, dependency analyst, security checker, adversarial reviewer, research specialist.

### Handoff as Context Boundary

Capability-oriented Subagent의 handoff는 단순한 결과 형식이 아니라 **context boundary의 public contract**가 될 수 있습니다.

필요한 경우 다음을 정의합니다.

- caller가 전달해야 하는 최소 input과 scope
- Subagent 내부에 남겨도 되는 intermediate context
- 반드시 반환할 result, evidence, uncertainty와 blocker
- caller가 후속 판단에 필요하지 않은 세부사항을 반환하지 않는 기준
- 수행한 side effect와 검증 상태

전체 transcript나 탐색 과정을 그대로 반환하면 isolation의 이점을 잃습니다. 반대로 결과를 지나치게 축약해 evidence나 uncertainty를 잃어도 안 됩니다. Handoff는 parent가 다음 결정을 내리는 데 필요한 최소 충분 context를 전달합니다.

### Skill and Isolated Capability

Skill과 Capability-oriented Subagent의 차이를 tool 보유 여부로 판단하지 않습니다. 둘 다 procedure, domain knowledge, tool usage를 정의할 수 있습니다.

| Concern | Skill에 더 자연스러움 | Capability-oriented Subagent에 더 자연스러움 |
| --- | --- | --- |
| Parent가 instruction과 working context를 계속 활용해야 함 | Yes | Sometimes |
| Intermediate context가 parent에 남아도 됨 | Yes | Not required |
| 대량 탐색·tool output을 별도 context에 격리해야 함 | Runtime에 isolation 기능이 있으면 가능 | Core design reason |
| 결과만 compact handoff로 소비하면 됨 | Possible | Strong fit |
| 별도 tool/permission/specialist boundary가 유용함 | Runtime-dependent | Strong fit |

일부 runtime은 Skill 자체에 별도 context 실행 기능을 제공할 수 있습니다. 예를 들어 GitHub Copilot for VS Code는 experimental `context: fork`를 통해 Skill을 dedicated subagent context에서 실행하고 최종 결과만 parent에 반환할 수 있습니다. 이런 기능이 대상 runtime에서 충분하다면 isolation만을 위해 별도 Subagent를 만들 필요가 없습니다.

반대로 같은 capability의 isolation과 handoff contract를 여러 vendor/runtime에서 비교적 일관되게 표현하고 싶거나, capability 자체에 별도 tool·permission·specialist identity가 필요한 경우에는 Capability-oriented Subagent가 더 vendor-neutral한 설계 surface가 될 수 있습니다. 다만 vendor-neutral은 모든 runtime이 동일한 Subagent semantics를 지원한다는 뜻은 아닙니다. 실제 projection과 invocation은 각 runtime contract를 따릅니다.

GitHub Copilot의 현재 forked Skill semantics는 [Agent Skills in VS Code](https://code.visualstudio.com/docs/agent-customization/agent-skills)를 확인합니다.

## Mixed Orientation

두 orientation은 결합할 수 있습니다.

예를 들어 reviewer는 제한된 검토 capability를 가지면서도 read-only 권한, scope boundary, evidence rule 같은 역할 계약을 함께 가질 수 있습니다. 반대로 lead agent도 특정 Skill과 tool을 자주 사용하도록 정의할 수 있습니다.

혼합 자체는 문제가 아닙니다. 다만 다음을 피합니다.

- capability가 넓어질 때마다 별도 역할 정체성을 덧붙이는 것
- 역할의 책임을 tool 목록으로 대신 설명하는 것
- specialist에게 불필요한 최종 결정권이나 넓은 자율권을 주는 것
- role-oriented agent에 모든 가능한 procedure와 tool 사용법을 넣어 instruction을 비대하게 만드는 것
- isolation 목적 없이 Skill로 충분한 작은 procedure를 Subagent로 포장하는 것
- 격리한 intermediate context를 handoff에서 다시 전부 parent에 주입하는 것

## Design Heuristic

Subagent를 설계할 때 먼저 다음 두 질문을 봅니다.

> 이 Subagent의 품질을 가장 크게 좌우하는 것은 **올바른 판단 경계와 책임**인가, 아니면 **특정 작업을 안정적으로 수행하는 capability**인가?

> 이 작업의 intermediate context를 parent에 남기는 것이 유익한가, 아니면 **격리하고 최소 충분 결과만 handoff하는 것이 더 유익한가?**

첫 질문의 전자가 크면 Role 쪽에, 후자가 크면 Capability 쪽에 더 많은 instruction budget을 사용합니다. 두 번째 질문에서 isolation의 가치가 크면 Capability-oriented Subagent의 필요성이 강해집니다. 다만 target runtime이 이미 적절한 forked/isolated Skill을 제공하면 더 작은 mechanism을 우선할 수 있습니다.

orientation은 이름, directory, framework metadata로 고정하지 않습니다. 실제 responsibility, context boundary와 runtime contract가 우선합니다.

## Boundary

이 pattern은 Subagent의 설계 emphasis와 context-isolation 선택을 설명합니다. Subagent의 공식 taxonomy, runtime lifecycle, delegation protocol, vendor-specific frontmatter, tool permission model 또는 orchestration framework를 정의하지 않습니다.

구체적인 source/target representation과 runtime semantics는 사용 중인 framework와 runtime의 authoritative contract를 따릅니다.
