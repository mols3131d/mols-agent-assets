---
title: Agent Asset Boundaries
description: Rule, Skill, Prompt, Agent의 책임 경계와 repository-local deployment convention을 정의하는 원칙
---

# Agent Asset Boundaries

에이전트 자산은 파일 형식보다 **scope, lifetime, authority, responsibility**로 구분한다.

> 자산 유형은 무엇을 담았는지가 아니라 언제, 어디서, 어떤 권한으로 모델의 행동과 판단에 영향을 주는가로 구분한다.

플랫폼마다 terminology와 loading semantics가 다르다. 이 문서의 자산 경계, `load-context-*` naming, Skill target profile, Rule projection은 이 저장소의 설계 개념이며 모든 플랫폼의 공식 표준을 의미하지 않는다.

## Core Boundaries

| 자산 | 핵심 책임 | 일반적 lifetime | 핵심 질문 |
| --- | --- | --- | --- |
| Rule | 반복 적용되는 policy와 constraint | 여러 task | 항상 또는 특정 scope에서 무엇을 지켜야 하는가? |
| Skill | 재사용 가능한 capability와 조건부 context | 관련 task마다 | 이 상황에서 어떤 capability나 context를 모델이 로드해야 하는가? |
| Prompt | 현재 invocation의 goal과 일회성 context | 현재 task | 지금 무엇을 원하는가? |
| Agent | 역할, authority, tools, delegation | runtime role | 누가 어떤 권한과 도구로 판단하는가? |

`Reference`는 이 표의 동급 Agent Asset 유형이 아니다. `references/`, `docs/`, `scripts/`, `assets/`, `evals/` 등은 Rule·Skill·Prompt·Agent의 작성, 실행, 검증 또는 이해를 돕는 **supporting resource**로 취급한다.

## Rule

Rule은 **반복되는 행동 경계**를 소유한다.

적합한 내용:

- 여러 task에 지속적으로 적용되는 policy와 convention
- 반드시 지켜야 하는 constraint와 guardrail
- repository, directory, path pattern, file type 같은 scope의 지속 규칙

Rule은 특정 task의 긴 procedure나 일회성 요구를 소유하지 않는다. 특정 상황에서만 필요한 판단 context를 항상 노출해야 한다면 Skill이 더 적합한지 검토한다.

### Repository-local Rule Projection

> [!IMPORTANT]
> 다음 두 Rule projection은 **이 저장소가 여러 coding-agent harness를 다루기 위해 채택한 비표준 repository-local convention**이다. 이를 범용 Agent 표준으로 설명하지 않는다.

#### Directory-scoped `AGENTS.md`

루트를 포함한 각 디렉터리의 `AGENTS.md`를 해당 subtree에 적용되는 Rule projection으로 사용할 수 있다.

- root `AGENTS.md`는 repository-wide 기본 Rule을 둔다.
- nested `AGENTS.md`는 해당 디렉터리와 하위 경로에 필요한 더 좁은 Rule을 둔다.
- concrete target path를 다룰 때는 root부터 target까지의 applicable directory chain을 함께 고려한다.
- nested file 하나만 읽고 ancestor Rule을 잃지 않는다.
- 실제 precedence와 override semantics는 target harness와 repository가 명시한 규칙을 따른다. 이 문서가 새로운 범용 precedence 표준을 만들지 않는다.

#### Glob-scoped Rule

공통 하위 디렉터리, 파일군, 확장자처럼 directory tree 하나로 표현하기 어려운 scope에는 **glob selector가 붙은 Rule projection**을 사용할 수 있다.

예시 scope:

```text
**/*.md
**/*.py
**/tests/**
```

- selector가 현재 target path와 일치할 때만 적용한다.
- 같은 규칙을 여러 디렉터리 `AGENTS.md`에 복제하기보다 공통 path/file-type concern에 사용한다.
- glob의 저장 형식, front matter, selector field와 discovery path는 harness마다 다를 수 있다.
- 특정 harness의 glob 문법이나 파일 형식을 Rule 자체의 표준 schema로 승격하지 않는다.

Directory Rule과 glob Rule은 동시에 적용될 수 있다. 충돌 시 target harness와 repository가 선언한 authority/specificity semantics를 우선하며, 근거 없는 universal precedence를 만들지 않는다.

## Skill

Skill은 **재사용 가능한 coherent capability**를 소유한다.

이 저장소에서는 Skill을 에이전트 자산 중 **가장 이식성이 높고, 모델의 판단에 따라 필요한 context를 조건부로 주입하기 좋은 기본 재사용 단위**로 우선 고려한다. Skills-compatible harness라면 discovery metadata만 먼저 노출하고, 모델이 관련성을 판단했을 때 instructions를 활성화하며, 필요하면 bundled resources를 추가로 로드할 수 있기 때문이다.

따라서 Skill은 workflow package에 한정하지 않는다. 다음을 모두 유효한 Skill responsibility로 본다.

- 반복 가능한 procedure 또는 workflow
- 특정 상황에서만 필요한 decision lens와 behavioral context
- domain-specific knowledge와 판단 기준
- task-specific tool 사용법과 gotcha
- validation과 성공 기준
- 조건부 resource loading의 routing

Skill에 고정 workflow가 반드시 필요한 것은 아니다. 명확한 activation condition이 있고, 로드된 context가 실제 판단이나 행동을 의미 있게 바꾸며, 하나의 cohesive responsibility를 가진다면 **context capability 자체가 Skill**이 될 수 있다.

### Why Skill First

재사용 가능한 지침이나 context의 위치가 애매하면 다음 이유로 Skill을 먼저 검토한다.

- **Conditional loading** — 관련 task에서만 instructions를 context에 넣을 수 있다.
- **Model-directed activation** — description을 보고 모델이 필요성을 판단할 수 있다.
- **Progressive disclosure** — core instructions와 optional resources를 분리할 수 있다.
- **Portability** — role이나 repository에 강하게 묶이지 않은 capability는 여러 Skills-compatible harness로 projection하기 쉽다.
- **Composition** — 여러 작은 Skill을 현재 task에 필요한 조합으로 활성화할 수 있다.

다만 모든 것을 Skill로 만들지는 않는다.

- 항상 또는 특정 scope에서 지속 적용되어야 하는 policy → Rule
- 현재 invocation에서만 필요한 goal/constraint → Prompt
- 별도 role, authority, tool/delegation boundary → Agent

Skill은 단순한 지식 저장소도, 무관한 capability들의 namespace도 아니다. 언제 활성화해야 하는지 설명하기 어렵거나 활성화 후 모델 행동이 달라지지 않는다면 Skill로 만들 이유가 약하다.

### Context-only Skill Naming

주책임이 workflow 실행이나 artifact 생성이 아니라 **특정 상황에 필요한 판단 기준·제약·지식을 context로 주입하는 것**이면 이 저장소에서는 `load-context-<topic>` 이름을 사용한다.

이 naming은 **Agent Skills 표준의 일부가 아니라 repository-local convention**이다.

- `load-context-`는 packaging 방식이 아니라 capability responsibility를 나타낸다.
- flat, runtime, workspace profile 모두 같은 naming을 사용할 수 있다.
- context-only Skill은 context discovery, selection, scoping, loading과 적용 경계까지만 소유한다.
- context를 사용한 실제 구현, 작성, 검증, 리뷰, transformation, mutation과 최종 output은 downstream capability가 소유한다.
- 실제 workflow 수행, transformation, validation, artifact 생성이 주책임이면 이 prefix를 붙이지 않는다.

예:

- `load-context-coding` — code health와 engineering decision context
- `load-context-github` — concrete GitHub 작업 전에 필요한 live repository/task context
- `load-context-notion` — concrete Notion 작업 전에 필요한 live workspace/object context
- `load-context-human-writing` — 사람이 읽는 글의 audience, structure, readability context
- `load-context-agent-assets` — agent-facing asset의 activation, authority, context-cost context
- `load-context-tech-doc-fidelity` — technical document 보존 context

## Skill Target Profiles

> [!IMPORTANT]
> `skills/`, `skills-chatbot/`, `skills-chatbot-runtime/`의 3분류는 **Agent Skills 표준이 아니다.** 서로 다른 harness/platform에서 같은 capability를 최대한 효율적으로 배포하기 위해 이 저장소가 만든 **비표준 repository-local target profile taxonomy**다.

공식 Agent Skills format은 기본적으로 `SKILL.md`와 optional `scripts/`, `references/`, `assets/` 같은 resource 구조를 정의한다. 이 저장소의 세 directory 이름, flat `.skill.md` projection, 4,000-token budget, profile 선택 규칙은 그 위에 추가한 로컬 배포 전략이다.

| Repository-local profile | 최적화 대상 |
| --- | --- |
| `skills/` | workspace/filesystem/shell/repository authority를 사용할 수 있는 agent runtime |
| `skills-chatbot/` | 단일 Markdown 파일만 받을 수 있는 flat chatbot harness |
| `skills-chatbot-runtime/` | bundle, tools/connectors와 progressive loading을 활용하는 hosted chatbot runtime |

이 분류는 capability의 우열이나 정규화 계층이 아니다. 같은 capability가 둘 또는 세 profile에 함께 존재할 수 있으며, cross-profile semantic overlap은 target별 최적화를 위한 의도적인 projection일 수 있다.

### Flat vs Runtime Packaging Boundary

`skills-chatbot/`은 배포 capability가 다음 조건을 모두 만족할 때 사용한다.

1. capability가 `<skill-name>.skill.md` **한 파일**로 완결된다.
1. 배포되는 단일 skill 파일이 **4,000 tokens 미만**이다.
1. 실행에 runtime-required bundle이나 host-only runtime capability가 필요하지 않다.

다음 중 하나라도 해당하면 `skills-chatbot-runtime/`을 사용한다.

- 단일 skill 파일이 **4,000 tokens 이상**이라 상세 context를 여러 Markdown 파일로 분리해야 한다.
- 실행에 references, assets, scripts, images 등 Markdown 한 파일 밖의 bundled resource가 필요하다.
- tools, connectors, scripts, progressive loading 또는 기타 host runtime 기능이 capability의 중요한 부분이다.

공식 Agent Skills 문서의 `<5,000 tokens` 권장은 activated `SKILL.md`에 대한 일반 권장치다. 이 저장소의 `<4,000 tokens` flat budget은 **더 엄격한 로컬 정책이며 표준 요구사항이 아니다.**

Maintainer-only `docs/`, `evals/`, `tests/`, 개발용 validator는 배포 Skill과 분리할 수 있다면 그 존재만으로 runtime placement를 강제하지 않는다. 작은 textual schema나 설정 예시는 명확성과 유지보수성을 해치지 않으면 fenced code로 flat file에 포함할 수 있다.

### Cross-profile Optimization

- 각 profile은 자신의 harness가 실제로 제공하는 기능을 최대한 활용한다.
- workspace variant는 workspace authority와 repository tooling을 활용할 수 있다.
- flat variant는 외부 bundle 없이 self-contained하게 동작해야 한다.
- runtime variant는 references, assets, scripts, tools, connectors, progressive loading으로 초기 context와 실행 비용을 최적화할 수 있다.
- sibling variants는 핵심 intent와 중요한 behavioral invariant를 공유할 수 있지만 구조, 세부 절차, context 전략은 달라도 된다.
- 한 profile의 최적화를 다른 profile에 억지로 맞추지 않는다.
- cross-profile 중복을 일반적인 DRY 위반으로 취급하지 않는다.

따라서 최적화 단위는 단순한 `capability`가 아니라 **`capability × target profile`**이다.

## Prompt

Prompt는 **현재 invocation에서 원하는 결과**를 소유한다.

적합한 내용:

- 현재 목표와 입력
- 현재 task에 필요한 일회성 context
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

Agent를 나누는 이유는 instruction 길이가 아니라 **역할, authority, specialization, delegation boundary가 실제로 달라질 때**다. 역할 분리가 필요하지 않은 reusable capability나 conditional context는 Agent보다 Skill을 우선 검토한다.

## Supporting Resources

Supporting resource는 독립적인 Agent Asset 유형이 아니다. 다른 자산이 필요할 때 참조하거나 실행하는 재료다.

- `references/`: Skill 또는 문서가 조건부로 읽는 상세 지식
- `scripts/`: deterministic helper와 executable support
- `assets/`: template, image, output resource
- `docs/`: 사람과 maintainer를 위한 설명·설계 지식
- `evals/` / `tests/`: behavior와 package를 검증하는 개발 자산

Resource가 존재한다는 사실만으로 모델 행동이 활성화되는 것은 아니다. 특정 지식을 모델이 상황에 따라 스스로 발견·활성화해야 한다면 그 **activation boundary는 Skill이 소유**하고, 상세 지식만 resource로 내려놓는다.

## Placement Test

새 내용을 둘 위치가 모호하면 다음 순서로 묻는다.

1. 여러 task에서 지속적으로 지켜야 하는 policy인가? → **Rule**
1. 반복 가능한 capability이거나 모델이 상황에 따라 조건부로 로드해야 하는 context인가? → **Skill**
1. 현재 요청에서만 필요한 goal이나 constraint인가? → **Prompt**
1. 별도 역할, authority, tool, delegation boundary가 필요한가? → **Agent**

재사용 가능한 내용이고 1·3·4의 명확한 이유가 없다면 **Skill을 우선 후보로 검토한다.**

Skill로 판단했다면 responsibility와 repository-local target profile을 별도로 고른다.

1. 주책임이 context 주입인가? → `load-context-<topic>` naming 검토
1. workspace/filesystem/shell/repository authority가 핵심인가? → `skills/` variant 검토
1. chatbot variant가 단일 Markdown 파일 + 4,000 tokens 미만이고 runtime 기능이 본질이 아닌가? → `skills-chatbot/`
1. 4,000 tokens 이상이거나 runtime-required bundle/tool/connector capability가 필요한가? → `skills-chatbot-runtime/`

Rule로 판단했다면 scope projection을 고른다.

1. 한 directory subtree에 지속 적용되는가? → root/nested `AGENTS.md` projection 검토
1. 여러 위치의 공통 하위 디렉터리, 파일군, 확장자에 적용되는가? → glob-scoped Rule projection 검토

둘은 필요하면 함께 사용할 수 있다.

## Boundary Changes

내용의 owner는 영구적이지 않다.

- 반복되는 prompt correction은 Rule이나 Skill로 승격될 수 있다.
- 항상 로드된 Rule의 조건부 판단 기준은 activation boundary가 생기면 Skill로 내려갈 수 있다.
- Skill의 일부가 독립 role/authority를 가지면 Agent로 분리될 수 있다.
- runtime에 항상 필요하지 않은 상세 설명은 Skill resource로 내려갈 수 있다.
- flat Skill이 4,000-token budget을 넘거나 runtime-required resource가 필요해지면 runtime variant로 승격할 수 있다.

변경은 파일 크기만이 아니라 **scope, responsibility, loading contract가 실제로 바뀌었을 때** 수행한다.

## Anti-patterns

- 조건부로 필요한 context를 global Rule이나 Agent instruction에 항상 로드한다.
- Prompt에 반복 가능한 capability를 계속 복사한다.
- Rule 안에 하나의 task를 위한 전체 workflow를 넣는다.
- 동일한 path/file-type Rule을 여러 directory file에 불필요하게 복제한다.
- directory/glob Rule projection을 범용 agent standard처럼 설명한다.
- Skill을 activation이나 행동 효과가 없는 단순 resource collection으로 사용한다.
- 서로 독립적인 context를 하나의 broad Skill에 모아 항상 함께 로드한다.
- context-only Skill이 downstream workflow나 output까지 소유한다.
- workflow Skill에 `load-context-`를 붙여 responsibility를 오해하게 만든다.
- repository-local 3-profile taxonomy를 Agent Skills 공식 표준처럼 설명한다.
- `<4,000 tokens` flat budget을 외부 표준 요구사항처럼 설명한다.
- target profile이 다른 sibling Skill을 단순한 내용 중복이라는 이유로 제거한다.
- 한 platform의 제약을 다른 profile에 강제로 전파한다.
- runtime-required resource나 tool capability를 flat file에 억지로 인라인한다.
- Maintainer-only docs/evals/tests의 존재만으로 runtime placement를 강제한다.
- Agent를 instruction namespace처럼 늘린다.
- supporting resource를 독립적인 Agent Asset 유형처럼 분류한다.
- platform-specific loading behavior를 범용 표준처럼 가정한다.

## Review Questions

> **이 내용은 항상/특정 scope에서 Rule로 적용되어야 하는가, 아니면 Skill로 조건부 로드하는 편이 더 효율적인가?**

> **Rule이라면 directory scope와 glob scope 중 어느 projection이 실제 적용 범위를 가장 정확하게 표현하는가?**

> **Skill이라면 현재 harness에서 가장 효율적인 repository-local target profile과 packaging은 무엇인가?**

## Research Basis

- [Agent Skills Specification](https://agentskills.io/specification) — `SKILL.md`, optional resources와 progressive disclosure 구조를 정의한다.
- [Agent Skills Overview](https://agentskills.io/home) — Skills를 specialized knowledge와 workflow를 portable하게 묶고 on-demand로 로드하는 reusable capability로 설명한다.
- [Adding Skills Support](https://agentskills.io/client-implementation/adding-skills-support) — discovery → activation → resources의 progressive loading과 model-directed activation을 설명한다.
- [OpenAI Agents SDK: Agents](https://openai.github.io/openai-agents-python/agents/) — Agent의 role/instructions/tools/handoffs/guardrails와 runtime context boundary를 비교 기준으로 사용한다.
- [GitHub: Customizing Copilot responses](https://docs.github.com/en/copilot/concepts/prompting/response-customization) — persistent instruction의 repository/path scope 차이를 비교 기준으로 사용한다.
