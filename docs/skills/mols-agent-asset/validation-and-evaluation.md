---
description: Agent Asset의 결정론적·의미론적 Validation과 Routing·Behavior Evaluation의 책임 경계를 판단할 때 사용합니다.
---

# Validation and Evaluation

Validation은 **정해진 계약을 충족하거나 의도한 계약이 올바르게 표현되어 있는지** 확인한다. Evaluation은 **그렇게 표현된 계약이 실제로 얼마나 잘 작동하는지** 평가한다.

짧게 말하면 **Validation은 계약을 보고, Eval은 계약의 실제 성능을 본다.**

## Validation

Validation은 두 종류로 나눈다.

| 유형 | 핵심 질문 | 대표 대상 |
| --- | --- | --- |
| Deterministic Validation | 기계적으로 판정 가능한 규격과 계약을 준수하는가? | schema, frontmatter, 필수 파일과 경로, reference 존재 여부, 허용 값, generated drift, parser·validator 결과 |
| Semantic Validation | 의도한 설계와 행동 계약이 instruction과 구조에 제대로 표현되어 있는가? | responsibility, owner, activation boundary, scope, authority, delegation, handoff, core/delta, safety boundary |

Deterministic Validation은 같은 입력에 대해 안정적으로 같은 판정을 낼 수 있는 성질을 다룬다. 가능한 경우 source framework, schema, parser, generator, test처럼 이미 존재하는 결정론적 mechanism을 사용한다.

Semantic Validation은 단순히 문장이 존재하는지만 보지 않는다. 적혀 있는 내용과 구조가 의도한 설계와 계약을 실제로 표현하는지 의미적으로 판단한다. 다만 이 단계에서 그 설계가 runtime에서 높은 성공률로 작동한다고 주장하지 않는다.

## Evaluation

Evaluation은 실제 선택과 실제 행동이라는 두 종류로 나눈다.

| 유형 | 핵심 질문 | 대표 대상 |
| --- | --- | --- |
| Routing Eval | 필요한 자산이나 실행 단위를 올바르게 선택하고 호출하는가? | Skill selection, Rule routing, tool selection, subagent delegation, positive·negative·near-miss 구분 |
| Behavior Eval | 선택된 뒤 의도한 행동과 결과를 얼마나 잘 수행하는가? | action, output, tool use, handoff, guardrail behavior, correctness, quality, safety, efficiency |

Routing Eval은 **무엇을 선택하고 호출했는지**를 평가한다. Behavior Eval은 **선택된 뒤 무엇을 했고 어떤 결과를 냈는지**를 평가한다.

## Evaluation methods

다음은 별도 최상위 Eval 유형이 아니라 Routing Eval 또는 Behavior Eval에 적용하는 방법, 조건, 비교 기준이다.

- positive, negative, near-miss, failure case
- adversarial challenge
- baseline과 regression 비교
- stability와 repeated trials
- variant 비교
- simulation, runtime output, trace 같은 evidence source

Orchestration도 별도 최상위 유형으로 만들지 않는다. 어떤 agent, tool, Skill을 선택·위임했는지는 Routing Eval로 보고, 호출 이후 협력·handoff·결과 품질은 Behavior Eval로 본다.

## Boundary

Validation을 통과했다는 사실만으로 실제 성능이 좋다고 주장하지 않는다. 올바른 schema와 좋은 설계 표현은 Eval 성공을 보장하지 않는다.

반대로 Eval 결과가 좋더라도 명시된 규격이나 설계 계약이 잘못되었거나 누락되어 있다면 Validation 문제는 남는다. 우연히 잘 작동한 결과를 올바른 계약의 대체물로 취급하지 않는다.

판단이 모호하면 다음 순서로 구분한다.

1. 기계적으로 규격 준수를 판정할 수 있는가? → Deterministic Validation
2. 적혀 있는 instruction과 구조가 의도한 설계를 표현하는지 판단하는가? → Semantic Validation
3. 실제 선택·호출이 얼마나 잘 되는지 측정하는가? → Routing Eval
4. 선택 이후 행동과 결과가 얼마나 잘 나오는지 측정하는가? → Behavior Eval
