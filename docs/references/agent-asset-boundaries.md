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

### Context-only Skill Naming

주책임이 workflow 실행이나 artifact 생성이 아니라 **특정 상황에 필요한 판단 기준·제약·지식을 context로 주입하는 것**이면 `load-context-<topic>` 이름을 사용한다.

- `load-context-`는 packaging 방식이 아니라 capability responsibility를 나타낸다.
- flat, runtime, workspace profile 모두 같은 naming을 사용할 수 있다.
- context-only Skill은 context discovery, selection, scoping, loading과 적용 경계까지만 소유한다.
- context를 사용한 실제 구현, 작성, 검증, 리뷰, transformation, mutation과 최종 output은 downstream capability가 소유한다.
- context를 활용하더라도 실제 workflow 수행, transformation, validation, artifact 생성이 주책임이면 이 prefix를 붙이지 않는다.
- context-only 여부가 불분명하면 이름보다 먼저 responsibility를 다시 분리한다.

예:

- `load-context-pragmatic-engineering` — engineering trade-off 판단 context
- `load-context-tech-doc-fidelity` — technical document 보존 context
- `load-context-github` — GitHub 작업 전에 필요한 repository/task context

## Skill Target Profiles

`skills/`, `skills-chatbot/`, `skills-chatbot-runtime/`은 capability의 우열이나 정규화 계층이 아니라 **서로 다른 harness/platform capability에 맞춘 배포 profile**이다.

| Profile | 최적화 대상 |
| --- | --- |
| `skills/` | workspace/filesystem/shell/repository authority를 사용할 수 있는 agent runtime |
| `skills-chatbot/` | 단일 Markdown skill 파일로 완결되며 4,000 tokens 미만인 flat chatbot harness |
| `skills-chatbot-runtime/` | 여러 bundled files 또는 runtime 기능과 progressive loading을 활용하는 hosted chatbot runtime |

같은 capability가 둘 또는 세 profile에 함께 존재할 수 있다. 이 중복은 각 target에서 가장 효율적인 형태를 선택하기 위한 **의도적인 projection**일 수 있으며, 내용이 겹친다는 이유만으로 DRY 위반이나 제거 대상으로 보지 않는다.

### Flat vs Runtime Packaging Boundary

chatbot profile을 고를 때 `skills-chatbot/`을 가장 단순한 packaging으로 보고 다음 두 조건을 모두 만족할 때만 flat variant를 둔다.

1. capability가 `<skill-name>.skill.md` **한 파일**로 완결된다.
1. 배포되는 단일 skill 파일이 **4,000 tokens 미만**이다.

다음 중 하나라도 해당하면 `skills-chatbot-runtime/`을 사용한다.

- 단일 skill 파일이 **4,000 tokens 이상**이라 상세 context를 여러 Markdown 파일로 분리해야 한다.
- references, assets, schemas, scripts, images 등 Markdown 한 파일 밖의 bundled resource가 필요하다.
- host가 제공하는 tools, scripts, progressive loading 또는 기타 runtime 기능을 활용해야 한다.

이 경계는 capability의 중요도나 품질 차이가 아니라 **packaging과 harness capability 차이**다. runtime variant의 `SKILL.md`는 activation boundary와 공통 계약을 유지하고, 상세 context는 필요할 때만 bundled resource에서 로드하는 편을 우선한다.

flat sibling을 유지할 가치가 있다면 핵심 behavior를 보존하면서 4,000 tokens 미만의 self-contained variant로 최적화할 수 있다. 품질을 유지한 채 이 budget을 만족할 수 없다면 flat variant를 억지로 만들지 않는다.

### Cross-profile Optimization

- 각 profile은 자신의 harness가 실제로 제공하는 기능을 최대한 활용한다.
- workspace variant는 workspace authority와 repository tooling을 활용할 수 있다.
- flat variant는 외부 bundle 없이 self-contained하게 동작해야 한다.
- runtime variant는 references, assets, scripts, tools, progressive loading으로 초기 context와 실행 비용을 최적화할 수 있다.
- sibling variants는 핵심 intent와 중요한 behavioral invariant를 공유할 수 있지만 구조, 세부 절차, context 전략은 달라도 된다.
- 한 profile의 최적화를 다른 profile에 억지로 맞추지 않는다.
- 공통 코드를 추출한다는 이유로 target의 독립 배포나 harness-native 최적화를 훼손하지 않는다.

따라서 최적화 단위는 단순한 `capability`가 아니라 **`capability × target profile`**이다. 통합이나 제거는 target과 loading/authority contract까지 실질적으로 같을 때만 검토한다.

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
1. 반복 수행되는 task capability이거나 특정 상황에서 조건부로 필요한 decision context인가? → **Skill**
1. 현재 요청에서만 필요한 goal이나 constraint인가? → **Prompt**
1. 역할, authority, tool, delegation을 정의하는가? → **Agent**
1. 행동 자체보다 판단에 필요한 static knowledge인가? → **Reference**

Skill로 판단했다면 responsibility와 target profile을 별도로 고른다.

1. 주책임이 context 주입인가? → `load-context-<topic>` naming
1. workspace/filesystem/shell/repository authority가 핵심인가? → `skills/` variant 검토
1. chatbot variant가 단일 Markdown 파일 + 4,000 tokens 미만으로 완결되는가? → `skills-chatbot/`
1. 4,000 tokens 이상이거나 bundle/runtime capability가 필요한가? → `skills-chatbot-runtime/`

둘 이상의 답이 강하면 먼저 내용이 여러 책임을 섞고 있는지 확인한다. 하나의 capability가 여러 target에 필요하다면 sibling variant를 허용한다.

## Boundary Changes

내용의 owner는 영구적이지 않다.

- 한 번의 prompt correction이 반복되면 Rule이나 Skill로 승격될 수 있다.
- Skill의 일부가 독립 intent와 authority를 가지면 별도 Skill이나 Agent로 분리될 수 있다.
- runtime에 항상 필요하지 않은 상세 설명은 Reference로 내려갈 수 있다.
- 전역 instruction의 조건부 판단 기준은 명확한 activation boundary가 생기면 context Skill로 내려갈 수 있다.
- flat skill이 4,000-token budget을 넘거나 bundled resource가 필요해지면 runtime variant로 승격할 수 있다.

변경은 파일 크기만이 아니라 **scope, responsibility, packaging contract가 실제로 바뀌었을 때** 수행한다.

## Anti-patterns

- Prompt에 영구 policy를 계속 복사한다.
- Rule 안에 하나의 task를 위한 전체 workflow를 넣는다.
- Skill을 activation이나 행동 효과가 없는 단순 reference collection으로 사용한다.
- 서로 독립적인 context를 하나의 broad Skill에 모아 항상 함께 로드한다.
- context-only Skill이 downstream workflow나 output까지 소유한다.
- context-only Skill인데 responsibility가 드러나지 않는 broad name을 유지한다.
- workflow Skill에 `load-context-`를 붙여 responsibility를 오해하게 만든다.
- target profile이 다른 sibling Skill을 단순한 내용 중복이라는 이유로 제거한다.
- 한 platform의 제약을 다른 profile에 강제로 전파한다.
- 4,000 tokens를 넘는 flat skill을 계속 비대하게 유지하면서 runtime bundling을 피한다.
- bundled resource가 필요한 capability를 flat file에 억지로 인라인한다.
- Agent를 instruction namespace처럼 늘린다.
- `docs/references/`를 runtime dependency로 가정한다.
- 파일명이나 디렉터리 이름만 보고 자산 유형을 결정한다.
- platform-specific loading behavior를 범용 표준처럼 가정한다.

## Review Question

> **이 capability의 실제 responsibility와 현재 harness에서 가장 효율적인 target profile·packaging은 무엇인가?**

한 문장으로 답하기 어렵다면 boundary나 responsibility가 섞였는지 확인한다.

## Research Basis

- [Agent Skills Specification](https://agentskills.io/specification) — Skill의 metadata, instructions, references, scripts와 progressive loading 경계를 정의한다.
- [Anthropic: Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) — prompt를 one-off conversation instruction, Skill을 reusable on-demand capability로 구분한다.
- [OpenAI Agents SDK: Agents](https://openai.github.io/openai-agents-python/agents/) — Agent를 instructions, tools, handoffs, guardrails, output behavior를 가진 runtime building block으로 정의한다.
- [GitHub: About customizing Copilot responses](https://docs.github.com/en/copilot/concepts/prompting/response-customization) — persistent instruction의 scope를 personal, repository, organization 등으로 분리해 적용한다.
