---
title: Instruction Design
description: 에이전트 instruction의 적용 조건, 결과·행동, 재량·권한 경계와 검증·중단 조건을 명확하게 설계하는 공통 원칙
---

# Instruction Design

[Agent Asset Design Principles](design-principles.md)에서 instruction을 실제 owner로 선택한 뒤에는, 모델이 **언제 적용되고 무엇을 달성해야 하며 어디까지 재량이 있고 언제 멈춰야 하는지 다시 추론하지 않아도 되게** 설계합니다.

이 문서는 무엇을 instruction으로 둘지 결정하지 않습니다. **선택된 behavior를 instruction으로 어떻게 표현할지**를 소유합니다.

## Contract

중요한 behavior는 필요한 요소만 사용하되 다음 계약을 복원할 수 있어야 합니다.

```text
Condition → Outcome / Action → Boundary → Validation / Stop
```

- **Condition** — 언제 적용되고 언제 적용되지 않는가
- **Outcome / Action** — 어떤 결과가 필요하거나 기본적으로 무엇을 해야 하는가
- **Boundary** — 무엇을 보존·금지하고 어디까지 재량과 권한이 있는가
- **Validation / Stop** — 무엇으로 성공·실패를 확인하고 언제 fallback, handoff 또는 중단하는가

모든 문장을 이 형식으로 기계적으로 바꾸지는 않습니다. 결과만으로 충분한 behavior에는 절차를 강제하지 않고, 순서나 특정 행동이 contract인 behavior에는 필요한 action을 직접 씁니다.

## Core Rules

- Required behavior는 직접 씁니다. 설명, rationale 또는 example만으로 action을 암시하지 않습니다.
- 같은 authored behavior는 authoritative owner에 한 번만 둡니다. Generated representation이나 target projection을 별도 semantic owner로 취급하지 않고, 반복을 reliability의 대체물로 사용하지 않습니다.
- Normative instruction과 explanatory context를 구분합니다. Rationale은 상황에 따른 판단을 materially 개선할 때만 남기고 directive를 다시 설명하지 않습니다.
- 서로 의존하는 condition, outcome/action, boundary와 validation은 가능한 한 가까이 둡니다. 떨어뜨려 놓고 모델이 관계를 복원하게 하지 않습니다.
- Default는 하나를 명확히 두고, 대안은 default를 벗어나는 실제 condition이 있을 때만 노출합니다.
- `must`, `never`, `only` 같은 강한 표현은 true invariant, safety·permission boundary, required contract 또는 순서가 깨지면 실패하는 fragile operation에 사용합니다. Preference나 흔한 경로는 default와 escape condition으로 표현합니다.
- 금지나 negative boundary를 쓸 때 다음 valid action이 명확하지 않으면 허용되는 default, fallback 또는 handoff도 함께 씁니다.
- 권한이나 side effect가 중요한 행동은 **무엇을 계속 수행할 수 있는지와 어디서 승인·handoff·중단이 필요한지**를 함께 씁니다. Instruction 자체가 없는 권한을 만들 수는 없습니다.
- 같은 개념에는 같은 용어를 사용하고, 같은 단어에 서로 다른 책임을 부여하지 않습니다.
- Machine-enforceable contract를 prose로 둘지 판단할 때 [Agent Asset Design Principles](design-principles.md)의 mechanism gate를 따릅니다. 더 직접적인 owner가 있으면 같은 contract를 instruction으로 복제하지 않습니다.

`필요하면 관련 문서를 보고 적절히 처리한다`처럼 condition, owner와 expected action을 모델에게 다시 추론시키는 표현은 피합니다.

## Specificity

Instruction의 구체성은 task 전체가 아니라 **각 behavior의 fragility와 failure cost**에 맞춥니다.

| 상황 | 기본 형태 |
| --- | --- |
| 여러 접근이 유효하고 실패 비용이 낮음 | outcome + constraints/heuristics + success criteria |
| 선호 경로가 있으나 변형 가능 | default procedure + escape condition |
| 순서·선택 오류 비용이 큼 | exact steps + hard boundary + validation gate |

Outcome과 success criteria만으로 충분한 곳에 상세 절차를 강제하지 않습니다. 반대로 exact path가 contract인 곳에서는 모델의 재량이나 일반적인 best practice에 의존하지 않습니다.

## Scope, Authority and Conflict

Instruction은 **의도한 applicability보다 넓지 않은 scope**에 둡니다. 이것은 파일이나 directory를 가장 잘게 나누라는 뜻이 아닙니다. 같은 activation과 owner 아래 항상 함께 적용되는 coherent instruction은 함께 유지할 수 있습니다.

Scope와 authority는 서로 다른 문제입니다. Instruction의 위치나 문구가 권한을 새로 만들지는 않습니다.

- Governing standard, source framework, runtime 또는 project authority가 scope·precedence·permission을 정의하면 그 contract를 따릅니다.
- General precedence가 보장되지 않으면 충돌하는 instruction을 제거하거나 scope를 분리합니다.
- 충돌을 제거할 권한이 없고 behavior가 materially 달라질 수 있으면 임의로 하나를 승자로 만들지 않습니다. Conflict를 드러내고 필요한 handoff 또는 stop을 명시합니다.
- Source와 projection의 authority는 [작성 원본과 권한](../../../development/source-authority.md)을 따릅니다.

## Context, Rationale and Examples

항상 로드되는 instruction에는 현재 판단과 행동을 바꾸는 정보만 남깁니다. 조건부 detail은 [Agent Asset Design Principles](design-principles.md)의 Progressive Disclosure를 따르고, 필요한 시점을 가장 가까운 decision point에서 찾을 수 있게 합니다.

Rationale과 example은 숨은 rule을 만드는 수단이 아닙니다.

- Rationale은 directive의 이유를 알면 예외 상황에서 더 올바르게 판단할 수 있을 때 사용합니다.
- Example은 prose만으로 output shape나 behavior가 쉽게 오해되거나, representative edge case가 ambiguity를 줄이거나, 실제 failure·eval에서 특정 패턴의 보정이 필요하다고 확인됐을 때 사용합니다.
- Example은 normative rule을 대신하지 않습니다. 여러 example이 필요하면 실제 variation을 대표하도록 구성하고, 한 예시의 우연한 표현을 일반 규칙처럼 만들지 않습니다.
- Template은 format 자체가 contract일 때 사용합니다. Runtime이 structured output이나 schema를 더 직접적으로 보장하면 prose template보다 그 mechanism을 우선합니다.

## Validation and Stop

Validation은 **관찰 가능한 결과**로 씁니다. `적절히 확인한다`, `문제가 없으면 진행한다`처럼 성공 조건을 다시 해석하게 두지 않습니다.

- 성공과 실패를 구분하는 evidence 또는 observable state를 명시합니다.
- Missing evidence, failed validation과 blocked authority가 서로 다른 다음 행동을 요구하면 구분합니다.
- 필요한 경우에만 retry, fallback, 판단 유보, ask, handoff 또는 stop 중 다음 행동을 정의합니다.
- Retry 횟수나 세부 절차는 실제 operation이 bounded retry를 요구할 때만 고정합니다.
- Validation 없이 오류가 보이지 않았다는 이유만으로 성공을 선언하지 않습니다.

Repository의 deterministic verification, behavioral evaluation과 evidence level은 `docs/development/`가 소유합니다.

## Review

각 instruction에서 다음을 복원할 수 있어야 합니다.

- [Agent Asset Design Principles](design-principles.md)의 Local Delta와 mechanism gate를 통과하는가?
- 언제 적용되고 언제 적용되지 않는가?
- 필요한 outcome 또는 default action은 무엇인가?
- 어디까지 재량이며 무엇이 true invariant 또는 permission boundary인가?
- exception이나 negative boundary가 다음 valid action을 명확하게 바꾸는가?
- success, failure와 stop을 무엇으로 확인하는가?
- 같은 behavior가 다른 authoritative instruction에 반복되거나 충돌하지 않는가?
- example이나 rationale이 명시되지 않은 rule을 만들고 있지 않은가?

행동이나 판단을 materially 바꾸지 않는 설명은 제거 후보입니다.

## Boundary

이 문서는 behavioral instruction의 **표현과 제어 원칙**을 소유합니다. 어떤 behavior가 local asset에 존재해야 하는지, 어떤 asset이나 mechanism이 owner인지에 대한 판단은 [Agent Asset Design Principles](design-principles.md)가 소유합니다.

Vendor-specific instruction path, inheritance, precedence, frontmatter와 loading semantics는 현재 source framework와 target/runtime의 authoritative contract를 따릅니다. Repository의 test/eval workflow와 evidence level은 `docs/development/`가 소유합니다.

## Sources

- [Agent Skills — Best practices for skill creators](https://agentskills.io/skill-creation/best-practices)
- [Anthropic — Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [GitHub — Adding repository custom instructions for GitHub Copilot](https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot)
- [OpenAI — Model guidance](https://developers.openai.com/api/docs/guides/latest-model)
