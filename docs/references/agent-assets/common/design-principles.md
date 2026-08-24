---
title: Agent Asset Design Principles
description: 에이전트 자산을 추가, 분리, 중복 제거, 단순화할 때 적용하는 공통 판단 순서
---

# Agent Asset Design Principles

목표는 규칙을 늘리는 것이 아니라 **행동 신뢰성과 authority를 보존하면서 불필요한 local context와 설계 복잡성을 만들지 않는 것**입니다.

## 판단 순서

1. **Standard First / Local Delta Only** — 적용 가능한 표준, source framework, target/runtime contract 또는 확립된 project authority가 이미 행동을 결정하면 local source에 다시 소유하지 않습니다. Local source는 deviation, extension, ambiguity resolution만 소유합니다.
1. **YAGNI** — 현재 요구, 관찰된 failure, accepted policy 또는 보존해야 할 credible invariant가 없는 구조·호환성·metadata·instruction을 만들지 않습니다. 가상의 미래 요구나 막연한 model failure는 충분한 근거가 아닙니다.
1. **SRP** — activation, authority, permission, lifecycle, validation 또는 변경 이유가 실질적으로 다르면 책임 분리를 검토합니다. 파일 크기나 문서 길이만으로 나누지 않습니다.
1. **DRY** — 같은 semantic concern의 authoritative owner를 둘 이상 만들지 않습니다. 서로 다른 concern은 서로 다른 authority를 가질 수 있으며, 필요한 재사용은 복제가 아니라 link, reference 또는 composition으로 연결합니다.
1. **KISS** — 필요한 책임, 정보, 경계와 검증을 이해·변경·운영하기 쉬운 형태로 유지하고 현재 목적에 기여하지 않는 accidental complexity만 제거합니다. 파일·단계·option·구조 요소 수나 문서 길이를 단순함의 목표나 척도로 삼지 않습니다.
1. **Progressive Disclosure** — discovery → core → conditional detail 순으로 필요한 context만 노출합니다. 항상 또는 자주 로드되는 내용일수록 실제 failure를 막거나 invariant를 보존하거나 중요한 ambiguity를 줄이는 정보에 집중합니다.

앞 단계에서 제거할 수 있는 문제를 뒤 단계의 abstraction이나 더 많은 instruction으로 해결하지 않습니다.

## Local Delta

Local Agent Asset content를 추가하기 전에 다음 중 하나인지 확인합니다.

- **Deviation** — upstream/default와 의도적으로 다르게 행동해야 합니다.
- **Extension** — upstream에 없는 repository-specific behavior나 boundary가 필요합니다.
- **Ambiguity resolution** — upstream만으로 이 repository에서 필요한 결정을 안정적으로 복원할 수 없습니다.

셋 중 어느 것도 아니면 작성하지 않는 것이 기본입니다. Upstream detail이 판단에 필요하면 authoritative source를 링크하거나 작업 시점에 확인하고, fast-changing semantics를 local prose로 복제하지 않습니다.

Local Delta가 필요해도 prose instruction이 항상 올바른 mechanism은 아닙니다. 해당 concern을 더 직접적으로 소유·검증하는 established native 또는 deterministic mechanism이 있고, 그것을 사용해도 competing authority나 필요한 portability가 생기지 않으면 그 owner를 우선합니다. 특정 target의 편의만으로 별도 canonical source를 만들지 않습니다. Semantic judgment와 예외 판단처럼 모델이 해석해야 하는 behavior는 readable instruction에 남깁니다.

## Context Test

Context는 무료가 아닙니다. 특히 자동 또는 빈번하게 로드되는 내용은 다른 task context와 모델의 attention을 함께 소비합니다.

각 내용을 유지할 때 다음 중 무엇을 제공하는지 설명할 수 있어야 합니다.

- 없으면 반복적으로 틀릴 가능성이 높은 non-obvious local knowledge 또는 behavior
- 반드시 보존해야 하는 invariant, boundary 또는 required default
- 현재 판단을 materially 바꾸는 evidence, ambiguity resolution 또는 load condition

그 역할이 없다면 삭제하거나 authoritative source로 연결하거나 필요할 때만 로드되는 surface로 내리는 것을 우선합니다. 반대로 짧게 만들기 위해 critical gotcha나 required boundary를 숨기지 않습니다.

## Guardrails

- Standard First를 이유로 실제 target/version 차이나 중요한 local exception을 숨기지 않습니다.
- YAGNI를 이유로 이미 존재하는 비가역적 위험이나 required guard를 방치하지 않습니다.
- SRP를 이유로 항상 함께 변하고 함께 로드되어야 하는 coherent responsibility를 의미 없이 잘게 나누지 않습니다.
- DRY 때문에 runtime 독립성을 깨거나 hidden dependency를 만들지 않습니다.
- KISS를 이유로 서로 다른 책임을 합치거나 필요한 구조, validation, safety guard 또는 중요한 boundary를 제거하지 않습니다.
- Progressive Disclosure로 detail을 분리해도 load condition과 critical gotcha는 발견 가능한 owner에 남깁니다.
- Deterministic mechanism을 선호한다는 이유로 사람이 이해해야 하는 durable rationale이나 모델이 판단해야 하는 semantic boundary를 opaque automation에 숨기지 않습니다.
- Source만으로 복구하기 어려운 durable rationale과 invariant는 보존하고, 작업 로그와 재생성 가능한 상태는 Git history에 맡깁니다.

## Human Comprehension

AI가 자산을 빠르게 만들수록 maintainer가 **무엇이 authoritative하고 왜 존재하는지 이해하는 속도**가 병목이 될 수 있습니다. 이를 더 많은 설명으로 해결하지 않습니다. 불필요한 owner, 책임 경계와 탐색 경로를 만들지 않고, 필요한 owner·boundary·rationale은 빠르게 찾을 수 있게 유지합니다.

## Review

- 이것이 local deviation, extension 또는 ambiguity resolution인가?
- 실제 요구, observed failure, accepted policy 또는 credible invariant가 있는가?
- 더 직접적인 mechanism이 있는데 prose로 다시 구현하거나 competing authority를 만들고 있지 않은가?
- 하나의 concern을 여러 owner가 소유하거나 서로 다른 concern이 한 owner에 섞였는가?
- 정책 변경 시 concern별 authoritative location이 명확한가?
- 필요한 책임과 경계를 유지하면서 이해·변경·검증 비용을 낮출 수 있는 accidental complexity가 있는가?
- 자주 로드되는 각 context가 실제 행동이나 판단을 materially 개선하는가?
- detail을 아직 읽지 않은 agent도 언제 추가 context가 필요한지 알 수 있는가?

## Boundary

- 선택된 behavior를 instruction으로 표현하는 방법 → [Instruction Design](instruction-design.md)
- Skill-specific package, discovery와 body convention → [Skill Authoring Conventions](../skills/skill-authoring-conventions.md)
- 반복되는 문제에 대한 reusable solution shape → [Patterns](../../patterns/README.md)
- source framework와 target/runtime의 구체적인 representation·precedence·loading semantics → 해당 authoritative contract

## Sources

- [Agent Skills — Best practices for skill creators](https://agentskills.io/skill-creation/best-practices)
- [OpenAI — Model guidance](https://developers.openai.com/api/docs/guides/latest-model)
