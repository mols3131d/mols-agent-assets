---
title: Agent Asset KISS Principle
description: 에이전트 자산에서 필요한 행동 신뢰성을 유지하면서 판단과 context 복잡도를 최소화하는 원칙
---

# Agent Asset KISS Principle

에이전트 자산에서 KISS는 **가장 짧게 만드는 것**이 아니라, 원하는 행동을 안정적으로 만들기 위한 **최소 충분 지침(minimum sufficient guidance)**을 찾는 것이다.

> 같은 행동 신뢰성을 유지할 수 있다면 context, 선택지, 분기, 개념을 줄인다.

## Core Rules

1. **행동에 기여하는 내용만 둔다.** 에이전트가 없어도 올바르게 처리하는 설명은 제거 후보로 본다.
2. **기본 경로를 하나 둔다.** 여러 접근이 동등하다면 기본값을 정하고 대안은 필요한 조건에서만 연다.
3. **행동 차이가 있을 때만 분기한다.** 권한, 위험, 도구, 결과, 검증이 실질적으로 달라질 때 분기를 만든다.
4. **작업의 취약성에 맞춰 자유도를 조절한다.** 열린 문제에는 판단 여지를 주고, 오류 비용이 큰 작업에는 정확한 순서와 guardrail을 둔다.
5. **조건부 세부사항은 조건부로 노출한다.** 항상 필요한 핵심과 특정 상황에서만 필요한 지식을 분리한다. 자세한 구조는 [Progressive Disclosure](./progressive-disclosure-principle.md)를 따른다.
6. **구조 자체의 비용을 계산한다.** router, taxonomy, abstraction, 추가 Agent가 줄이는 복잡성보다 새로 만드는 복잡성이 크면 도입하지 않는다.

## Minimum Sufficient Guidance

KISS는 instruction을 무조건 줄이는 원칙이 아니다. 중요한 기준은 **제거 후에도 행동 신뢰성이 유지되는가**다.

- 일반 지식 설명 → 모델이 안정적으로 아는 내용이면 제거한다.
- 선택지 → 실제 기본값이 있으면 하나를 기본으로 정한다.
- 예외 → 빈번하거나 위험한 예외만 핵심 지침에 둔다.
- 안전 절차 → 오류 비용이 크다면 길어져도 명시한다.
- 상세 reference → 현재 task에서 필요할 때만 로드한다.

## Decision Test

요소를 추가하거나 유지하기 전에 묻는다.

> **이 요소를 제거했을 때 실제 task에서 잘못된 행동, 불필요한 탐색, 위험이 의미 있게 증가하는가?**

- `Yes` → 유지한다.
- `No` → 제거한다.
- 특정 조건에서만 `Yes` → 그 조건과 함께 분리한다.
- 불확실 → 실제 실행이나 eval로 확인한다.

## What KISS Is Not

- 최소 글자 수나 파일 수 경쟁이 아니다.
- 중요한 제약을 모델 추론에 떠넘기는 것이 아니다.
- 모든 예외나 분기를 없애는 것이 아니다.
- 큰 자산을 무조건 여러 자산으로 나누는 것이 아니다.
- 복잡한 문제를 단순한 문제인 것처럼 표현하는 것이 아니다.

## Anti-patterns

- 동등한 도구와 접근을 메뉴처럼 나열한다.
- 실제 행동 차이가 없는 workflow variant를 만든다.
- 모든 edge case를 root instruction에 적는다.
- 모델이 이미 아는 일반론을 장황하게 설명한다.
- 작은 문제에 router, framework, multi-agent 구조를 먼저 도입한다.
- 짧게 만들기 위해 validation과 guardrail을 암시적으로 만든다.

## Review Question

> **더 적은 개념과 결정으로 같은 행동 신뢰성과 안전성을 유지할 수 있는가?**

가능하면 단순화한다. 단순화가 신뢰성이나 안전성을 낮추면 유지한다.

## Research Basis

- [Agent Skills: Best practices for skill creators](https://agentskills.io/skill-creation/best-practices) — 모델이 이미 아는 내용 제거, coherent scope, defaults over menus, specificity와 fragility의 정합성.
- [Anthropic: Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) — context 비용과 task별 degree of freedom 조절.
- [OpenAI: A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) — 명확한 action, 필요한 branch, 복잡성의 점진적 증가.
