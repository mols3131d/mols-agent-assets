---
title: Agent Asset Boundaries
description: Rule, Skill, Prompt, Agent, Reference를 scope, lifetime, authority 기준으로 구분하는 자산 경계 원칙
---

# Agent Asset Boundaries

에이전트 자산은 파일 형식보다 **어떤 범위에서, 얼마나 오래, 어떤 권한으로 행동에 영향을 주는가**로 구분하는 편이 안정적이다.

> 자산 유형은 내용의 모양이 아니라 scope, lifetime, authority, responsibility로 구분한다.

이 문서의 `Rule`은 이 저장소에서 사용하는 설계 개념이다. 모든 agent platform이 동일한 이름이나 loading semantics를 표준화한 것은 아니다.

## Core Boundaries

| 자산 | 핵심 책임 | 일반적 lifetime | 핵심 질문 |
| --- | --- | --- | --- |
| Rule | 반복 적용되는 policy와 constraint | 여러 task | 항상 또는 특정 scope에서 무엇을 지켜야 하는가? |
| Skill | 재사용 가능한 task 또는 decision capability | 관련 task마다 | 이 상황에서 어떤 capability나 판단 context가 필요한가? |
| Prompt | 현재 invocation의 goal과 context | 현재 task | 지금 무엇을 원하는가? |
| Agent | 역할, authority, tools, delegation | runtime role | 누가 어떤 권한과 도구로 판단하는가? |
| Reference | 판단을 돕는 knowledge와 source material | 필요할 때 | 정확히 판단하려면 무엇을 알아야 하는가? |

## Rule

Rule은 **반복되는 행동 경계**를 소유한다.

적합한 내용:

- 여러 task에 적용되는 policy와 convention
- 반드시 지켜야 하는 constraint와 guardrail
- 특정 repository, organization, path 같은 scope의 지속 규칙

Rule은 특정 한 task의 긴 procedure나 일회성 요구를 소유하지 않는다.

## Skill

Skill은 **재사용 가능한 coherent capability**를 소유한다.

적합한 내용:

- capability와 activation 조건
- 반복 가능한 procedure 또는 workflow
- 특정 상황에서만 필요한 decision lens와 행동 context
- task-specific tool 사용법과 gotcha
- validation과 성공 기준
- 필요할 때 읽는 bundled reference와 script의 사용 조건

Skill에 고정 workflow가 반드시 필요한 것은 아니다. 명확한 activation condition이 있고, 로드된 context가 실제 판단이나 행동을 의미 있게 바꾸며, 하나의 cohesive responsibility를 가진다면 **context capability**도 Skill이 될 수 있다.

예를 들어 특정 engineering trade-off에서만 KISS/YAGNI/operability 판단 기준을 로드하는 Skill은 유효하다. 반대로 activation과 행동 효과 없이 지식만 모아둔 문서는 Reference가 더 자연스럽다.

Skill은 단순한 지식 저장소도, 무관한 capability들의 namespace도 아니다.

## Prompt

Prompt는 **현재 invocation에서 원하는 결과**를 소유한다.

적합한 내용:

- 현재 목표와 입력
- 현재 task에 필요한 context
- 이번 요청에만 적용되는 제약
- 원하는 output이나 acceptance condition

같은 지침을 여러 invocation에서 반복해서 넣어야 한다면 Rule이나 Skill이 더 자연스러운 owner인지 검토한다.

## Agent

Agent는 **runtime actor의 책임과 행동 surface**를 소유한다.

일반적으로 Agent는 다음의 조합으로 정의된다.

- role과 instructions
- 사용할 수 있는 tools
- authority와 guardrails
- handoff 또는 delegation 관계
- output responsibility

Agent를 나누는 이유는 instruction 길이가 아니라 **역할, authority, specialization, delegation boundary가 실제로 달라질 때**다.

## Reference

Reference는 **행동을 결정하는 데 필요한 지식과 근거**를 제공한다.

두 종류를 구분한다.

- repository-level `docs/references/`: 사람과 자산 작성자가 사용하는 설계 지식. runtime에 자동 적용된다고 가정하지 않는다.
- Skill 내부 `references/`: 해당 Skill이 조건에 따라 읽는 실행 지식. Skill이 load condition을 명시적으로 소유한다.

Reference에 적혀 있다는 사실만으로 runtime policy가 활성화되는 것은 아니다.

## Placement Test

새 내용을 둘 위치가 모호하면 다음 순서로 묻는다.

1. 여러 task에서 지속적으로 지켜야 하는 policy인가? → **Rule**
2. 반복 수행되는 task capability이거나 특정 상황에서 조건부로 필요한 decision context인가? → **Skill**
3. 현재 요청에서만 필요한 goal이나 constraint인가? → **Prompt**
4. 역할, authority, tool, delegation을 정의하는가? → **Agent**
5. 행동 자체보다 판단에 필요한 static knowledge인가? → **Reference**

둘 이상의 답이 강하면 먼저 내용이 여러 책임을 섞고 있는지 확인한다. 하나의 내용이 여러 자산에 나타나야 한다면 [DRY Principle](./agent-asset-dry-principle.md)의 ownership 기준을 적용한다.

## Boundary Changes

내용의 owner는 영구적이지 않다.

- 한 번의 prompt correction이 반복되면 Rule이나 Skill로 승격될 수 있다.
- Skill의 일부가 독립 intent와 authority를 가지면 별도 Skill이나 Agent로 분리될 수 있다.
- runtime에 항상 필요하지 않은 상세 설명은 Reference로 내려갈 수 있다.
- 전역 instruction의 조건부 판단 기준은 명확한 activation boundary가 생기면 context Skill로 내려갈 수 있다.

변경은 파일 크기가 아니라 **scope와 responsibility가 실제로 바뀌었을 때** 수행한다.

## Anti-patterns

- Prompt에 영구 policy를 계속 복사한다.
- Rule 안에 하나의 task를 위한 전체 workflow를 넣는다.
- Skill을 activation이나 행동 효과가 없는 단순 reference collection으로 사용한다.
- 서로 독립적인 context를 하나의 broad Skill에 모아 항상 함께 로드한다.
- Agent를 instruction namespace처럼 늘린다.
- `docs/references/`를 runtime dependency로 가정한다.
- 파일명이나 디렉터리 이름만 보고 자산 유형을 결정한다.
- platform-specific loading behavior를 범용 표준처럼 가정한다.

## Review Question

> **이 내용의 scope, lifetime, authority를 기준으로 가장 자연스러운 canonical owner는 무엇인가?**

한 문장으로 답하기 어렵다면 boundary나 responsibility가 섞였는지 확인한다.

## Research Basis

- [Agent Skills Specification](https://agentskills.io/specification) — Skill의 metadata, instructions, references, scripts와 progressive loading 경계를 정의한다.
- [Anthropic: Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) — prompt를 one-off conversation instruction, Skill을 reusable on-demand capability로 구분한다.
- [OpenAI Agents SDK: Agents](https://openai.github.io/openai-agents-python/agents/) — Agent를 instructions, tools, handoffs, guardrails, output behavior를 가진 runtime building block으로 정의한다.
- [GitHub: About customizing Copilot responses](https://docs.github.com/en/copilot/concepts/prompting/response-customization) — persistent instruction의 scope를 personal, repository, organization 등으로 분리해 적용한다.
