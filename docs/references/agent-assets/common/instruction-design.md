---
title: Instruction Design
description: 에이전트 instruction이 언제 적용되고 무엇을 하며 어디까지 판단·행동할 수 있는지, 무엇으로 검증하고 언제 멈출지를 설계하는 공통 원칙
---

# Instruction Design

Instruction은 모델이 행동 계약을 다시 추론하지 않게 써야 합니다. [Agent Asset Design Principles](design-principles.md)에 따라 instruction이 적절한 owner로 선택됐다면, **언제 적용하고 무엇을 해야 하며 어디까지 판단할 수 있고 언제 멈춰야 하는지** 명확하게 표현합니다.

무엇을 instruction으로 둘지는 [Agent Asset Design Principles](design-principles.md)가 결정합니다. 이 문서는 **선택된 행동을 instruction으로 어떻게 표현할지**만 다룹니다.

## Behavior Contract

모든 instruction에 아래 요소를 전부 적을 필요는 없습니다. 다만 중요한 행동은 필요한 요소만으로도 다음 계약이 분명해야 합니다.

```text
Condition → Outcome / Action → Boundary → Validation / Stop
```

- **Condition** — 언제 적용되고 언제 적용되지 않는가
- **Outcome / Action** — 어떤 결과가 필요하거나 기본적으로 무엇을 해야 하는가
- **Boundary** — 무엇을 보존·금지하고 어디까지 재량과 권한이 있는가
- **Validation / Stop** — 무엇으로 성공·실패를 확인하고 언제 fallback, handoff 또는 중단하는가

모든 문장을 이 형식으로 기계적으로 바꾸지는 않습니다. 결과만으로 충분한 행동에는 절차를 강제하지 않고, 순서나 특정 행동이 contract인 경우에만 필요한 action을 직접 씁니다.

## Writing Rules

- 필수 행동은 직접 씁니다. 설명, rationale 또는 example만으로 action을 암시하지 않습니다.
- 같은 행동은 authoritative owner 한 곳에서만 정의합니다. Generated representation과 target projection은 파생 표현이지 별도 semantic owner가 아닙니다. 같은 내용을 반복해서 적는다고 신뢰성이 높아지는 것도 아닙니다.
- 규범적 instruction과 설명용 context를 구분합니다. Rationale은 상황에 따른 판단을 실질적으로 개선할 때만 남기고 지시를 다시 설명하지 않습니다.
- 서로 의존하는 condition, outcome/action, boundary와 validation은 가능한 한 가까이 둡니다. 떨어뜨려 놓고 모델이 관계를 다시 추론하게 하지 않습니다.
- 기본 경로는 하나를 명확히 두고, 대안은 기본 경로를 벗어나는 실제 condition이 있을 때만 노출합니다.
- `must`, `never`, `only` 같은 강한 표현은 true invariant, 안전·권한 경계, 필수 contract 또는 순서가 깨지면 실패하는 작업에 사용합니다. 선호나 흔한 경로는 default와 escape condition으로 표현합니다.
- 금지나 negative boundary를 쓸 때 다음 행동이 분명하지 않으면 허용되는 default, fallback 또는 handoff도 함께 씁니다.
- Instruction은 없는 권한을 만들어내지 못합니다. 권한이나 side effect가 중요한 행동은 **무엇을 계속 수행할 수 있는지와 어디서 승인·handoff·중단이 필요한지**를 함께 씁니다.
- 같은 개념에는 같은 용어를 사용하고, 같은 단어에 서로 다른 책임을 부여하지 않습니다.
- 기계적으로 강제할 수 있는 contract를 prose로 다시 쓰지 않습니다. [Agent Asset Design Principles](design-principles.md)의 mechanism gate를 따르고, 더 직접적인 owner가 있으면 그곳에 맡깁니다.

`필요하면 관련 문서를 보고 적절히 처리한다`처럼 condition, owner와 기대 행동을 모델에게 다시 추론시키는 표현은 피합니다.

## Specificity

Instruction의 구체성은 작업 전체가 아니라 **각 행동의 취약성과 실패 비용**에 맞춥니다.

| 상황 | 기본 형태 |
| --- | --- |
| 여러 접근이 유효하고 실패 비용이 낮음 | outcome + constraints/heuristics + success criteria |
| 선호 경로가 있으나 변형 가능 | default procedure + escape condition |
| 순서·선택 오류 비용이 큼 | exact steps + hard boundary + validation gate |

Outcome과 success criteria만으로 충분한 곳에 상세 절차를 강제하지 않습니다. 반대로 exact path가 contract인 곳에서는 모델의 재량이나 일반적인 best practice에 의존하지 않습니다.

## Scope, Authority and Conflict

Instruction은 **의도한 범위보다 넓게 적용되지 않도록 둡니다.** 이것은 파일이나 directory를 가장 잘게 나누라는 뜻이 아닙니다. 같은 activation과 owner 아래 항상 함께 적용되는 instruction은 함께 유지할 수 있습니다.

적용 범위와 authority는 별개입니다. Instruction의 위치나 문구가 권한을 새로 만들지는 않습니다.

- 적용되는 standard, source framework, runtime 또는 project authority가 scope·precedence·permission을 정의하면 그 contract를 따릅니다.
- 일반적인 precedence가 보장되지 않으면 충돌하는 instruction을 제거하거나 scope를 분리합니다.
- 충돌을 제거할 권한이 없고 행동이 실질적으로 달라질 수 있으면 임의로 하나를 승자로 만들지 않습니다. 충돌을 드러내고 필요한 handoff 또는 중단을 명시합니다.
- Source와 projection의 authority는 [작성 원본과 권한](../../../development/source-authority.md)을 따릅니다.

## Context, Rationale and Examples

항상 로드되는 instruction에는 현재 판단과 행동을 바꾸는 정보만 남깁니다. 조건부 세부 내용은 [Agent Asset Design Principles](design-principles.md)의 Progressive Disclosure를 따라 분리하고, 언제 읽어야 하는지 가장 가까운 판단 지점에서 알 수 있게 합니다.

Rationale과 example은 숨은 rule을 만드는 수단이 아닙니다.

- Rationale은 지시의 이유를 알면 예외 상황에서 더 올바르게 판단할 수 있을 때 사용합니다.
- Example은 서술만으로 output 형태나 행동이 오해되기 쉽거나, 대표적인 edge case가 모호성을 줄이거나, 실제 failure·eval에서 특정 패턴의 보정이 필요하다고 확인됐을 때 사용합니다.
- Example은 normative rule을 대신하지 않습니다. 여러 example이 필요하면 실제 variation을 대표하도록 구성하고, 한 예시의 우연한 표현을 일반 규칙처럼 만들지 않습니다.
- Template은 format 자체가 contract일 때 사용합니다. Runtime이 structured output이나 schema를 더 직접적으로 보장하면 prose template보다 그 mechanism을 우선합니다.

## Validation and Stop

Validation은 **관찰 가능한 결과나 상태**로 씁니다. `적절히 확인한다`, `문제가 없으면 진행한다`처럼 성공 조건을 다시 해석하게 두지 않습니다.

- 성공과 실패를 가르는 근거나 상태를 명시합니다.
- 근거가 부족한 경우, validation이 실패한 경우, 권한이 없는 경우에 다음 행동이 다르면 구분해 적습니다.
- 필요한 경우에만 retry, fallback, 판단 유보, ask, handoff 또는 중단 중 다음 행동을 정의합니다.
- Retry 횟수나 세부 절차는 실제 작업에 횟수 제한이 필요할 때만 고정합니다.
- Validation 없이 오류가 보이지 않았다는 이유만으로 성공을 선언하지 않습니다.

Repository의 deterministic verification, behavioral evaluation과 evidence level은 `docs/development/`가 소유합니다.

## Review Checklist

각 instruction에서 다음을 복원할 수 있어야 합니다.

- [Agent Asset Design Principles](design-principles.md)의 Local Delta와 mechanism gate를 통과하는가?
- 언제 적용되고 언제 적용되지 않는가?
- 필요한 outcome 또는 default action은 무엇인가?
- 어디까지 재량이며 무엇이 true invariant 또는 permission boundary인가?
- 예외나 negative boundary를 만났을 때 다음에 허용되는 행동이 분명한가?
- success, failure와 stop을 무엇으로 확인하는가?
- 같은 행동이 다른 authoritative instruction에 반복되거나 충돌하지 않는가?
- example이나 rationale이 명시되지 않은 rule을 만들고 있지 않은가?

행동이나 판단을 실질적으로 바꾸지 않는 설명은 제거 후보입니다.

## Boundary

이 문서는 behavioral instruction의 **표현 방식과 제어 원칙**만 소유합니다. 어떤 행동이 local asset에 있어야 하는지, 어떤 asset이나 mechanism이 owner인지에 대한 판단은 [Agent Asset Design Principles](design-principles.md)가 소유합니다.

Vendor-specific instruction path, inheritance, precedence, frontmatter와 loading semantics는 현재 source framework와 target/runtime의 authoritative contract를 따릅니다. Repository의 test/eval workflow와 evidence level은 `docs/development/`가 소유합니다.

## Sources

- [Agent Skills — Best practices for skill creators](https://agentskills.io/skill-creation/best-practices)
- [Anthropic — Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [GitHub — Adding repository custom instructions for GitHub Copilot](https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot)
- [OpenAI — Model guidance](https://developers.openai.com/api/docs/guides/latest-model)
