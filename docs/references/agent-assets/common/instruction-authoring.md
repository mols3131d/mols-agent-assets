---
title: Instruction Authoring
description: 모델이 최소 해석으로 trigger, action, 자유도와 validation을 복원하도록 behavioral instruction을 작성하는 원칙
---

# Instruction Authoring

[Design Principles](design-principles.md)를 통과해 instruction이 실제 owner로 선택된 뒤에는, 모델이 **언제 무엇을 해야 하고 어디까지 재량이 있으며 언제 멈춰야 하는지 불필요하게 추론하지 않게** 씁니다.

## Contract

필요한 요소만 사용하되, 중요한 behavior는 다음 계약을 복원할 수 있어야 합니다.

```text
Condition → Action → Boundary → Validation / Stop
```

- **Condition** — 언제 적용되는가
- **Action** — 기본적으로 무엇을 하는가
- **Boundary** — 무엇을 보존·금지하고 어디까지 재량이 있는가
- **Validation / Stop** — 무엇으로 완료·실패를 확인하고, 계속할 수 없을 때 무엇을 하는가

모든 문장을 이 형식으로 기계적으로 바꾸지는 않습니다. 핵심은 behavior의 적용 조건과 결과를 독자가 다시 추론하지 않아도 되는 것입니다.

## Rules

- Required behavior는 직접 씁니다. 설명이나 예시만으로 action을 암시하지 않습니다.
- 같은 behavior는 owning scope에 한 번만 둡니다. 반복해서 강조하는 것을 authority나 reliability의 대체물로 사용하지 않습니다.
- Normative instruction과 explanatory context를 구분합니다. Rationale은 상황에 따른 올바른 판단을 materially 개선할 때 남기고, directive를 장황하게 반복하지 않습니다.
- Trigger, action, boundary와 validation은 가능한 한 가까이 둡니다.
- Default를 하나 두고 대안은 default를 벗어나는 실제 condition이 있을 때만 노출합니다.
- `must`, `never`, `only` 같은 강한 표현은 true invariant, safety/permission boundary, required contract 또는 순서가 깨지면 실패하는 fragile operation에 사용합니다. Preference나 흔한 경로는 default와 escape condition으로 표현합니다.
- 같은 개념에는 같은 용어를 사용하고, 같은 단어에 서로 다른 책임을 부여하지 않습니다.
- Runtime이 더 직접적인 schema, permission, selector, structured output 또는 deterministic validation을 제공하면 [Design Principles](design-principles.md)의 mechanism 선택을 따릅니다. Prose로 그 contract를 이중 구현하지 않습니다.
- Validation은 관찰 가능한 결과로 씁니다. Missing evidence, failed validation, blocked authority가 중요한 경우 retry, fallback, abstain, ask, handoff 또는 stop 중 필요한 behavior를 명시합니다.

`필요하면 관련 문서를 보고 적절히 처리한다`처럼 condition, owner와 expected action을 모델에게 다시 추론시키는 표현은 피합니다.

## Scope and Conflict

Instruction은 가능한 한 **실제로 적용되는 가장 좁은 scope**에 둡니다. 넓은 scope에서 예외를 계속 추가하는 것보다, 명확한 owner와 activation boundary를 두는 편이 안정적입니다.

여러 instruction source가 함께 적용될 수 있다고 해서 local 문서가 임의의 precedence를 만들지는 않습니다.

- Governing standard, source framework, runtime 또는 project authority가 precedence를 정의하면 그 contract를 따릅니다.
- General precedence가 보장되지 않으면 충돌하는 instruction을 제거하거나 scope를 분리합니다.
- 충돌을 제거할 권한이 없고 behavior가 달라질 수 있으면 임의로 하나를 승자로 만들지 말고 conflict를 드러냅니다.

## Control

Instruction의 구체성은 task 전체가 아니라 **각 behavior의 fragility와 failure cost**에 맞춥니다.

| 상황 | 기본 형태 |
| --- | --- |
| 여러 접근이 유효하고 실패 비용이 낮음 | outcome + heuristics + success criteria |
| 선호 경로가 있으나 변형 가능 | default procedure + escape condition |
| 순서·선택 오류 비용이 큼 | exact steps + hard boundary + validation gate |

Outcome만으로 충분한 곳에 상세 절차를 강제하지 않고, exact path가 contract인 곳에서 모델의 재량에 의존하지 않습니다.

## Examples and Templates

Example은 숨은 규칙이 아니라 **이미 명시된 contract를 더 정확히 전달하기 위한 evidence**입니다.

다음 경우에만 추가하는 것을 우선합니다.

- prose만으로 output shape나 behavior가 쉽게 오해될 때
- representative edge case가 중요한 ambiguity를 제거할 때
- 실제 failure나 eval에서 특정 패턴의 보정이 필요하다고 확인됐을 때

Example은 normative rule을 대신하지 않으며, 한 예시의 우연한 표현을 일반 규칙처럼 따라야 하는 상황을 만들지 않습니다. 여러 example이 필요하면 실제 variation을 대표하도록 구성합니다.

Template은 format 자체가 contract일 때 사용합니다. Runtime이 structured output이나 schema를 더 직접적으로 보장하면 prose template보다 그 mechanism을 우선합니다.

## Review

각 instruction에서 다음을 복원할 수 있어야 합니다.

- [Design Principles](design-principles.md)의 Local Delta와 mechanism gate를 통과하는가?
- 언제 적용되고 언제 적용되지 않는가?
- default action은 무엇인가?
- 어디까지 재량이고 무엇이 true invariant인가?
- exception이나 fallback이 실제 behavior를 어떻게 바꾸는가?
- success, failure 또는 stop을 무엇으로 확인하는가?
- 같은 behavior가 다른 instruction에 반복되거나 충돌하지 않는가?
- example이나 rationale이 숨은 rule을 만들고 있지 않은가?

행동이나 판단을 materially 바꾸지 않는 설명은 제거 후보입니다. Conditional detail은 [Design Principles](design-principles.md)의 Progressive Disclosure를 따릅니다.

## Boundary

이 문서는 behavioral instruction의 **표현 원칙**을 소유합니다. 어떤 behavior가 local asset에 존재해야 하는지, 어떤 asset/mechanism이 owner인지에 대한 판단은 [Design Principles](design-principles.md)가 소유합니다.

Vendor-specific instruction path, inheritance, precedence, frontmatter와 loading semantics는 현재 target/runtime의 authoritative contract를 따릅니다. Repository의 test/eval workflow와 evidence level은 `docs/development/`가 소유합니다.

## Sources

- [Agent Skills — Best practices for skill creators](https://agentskills.io/skill-creation/best-practices)
- [Anthropic — Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [GitHub — Adding custom instructions for GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions)
- [OpenAI — Model guidance](https://developers.openai.com/api/docs/guides/latest-model)
