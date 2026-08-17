---
title: Personal Agent Asset Standard
description: 외부 baseline을 확장한 repository-local Agent Asset 운용 표준
---

# Personal Agent Asset Standard

이 문서는 [Agent Asset Standard Baseline](agent-asset-standard-baseline.md)을 바탕으로 이 저장소에서 실제 사용하는 **개인 표준(personal standard)**을 정의한다.

> 이 문서의 `CHATBOT.md`, Rule projection, `load-context-*`, Skill 3-profile, flat 4,000-token budget 등은 의도적인 **비표준 repository-local extension**이다. 외부 표준이나 특정 플랫폼의 공식 규격으로 설명하지 않는다.

## Asset Types

이 저장소의 동급 Agent Asset 유형은 네 가지다.

| 자산 | 책임 | 핵심 질문 |
| --- | --- | --- |
| Rule | 지속 적용되는 policy와 constraint | 이 scope에서 무엇을 계속 지켜야 하는가? |
| Skill | 재사용 capability와 조건부 context | 지금 어떤 capability/context를 로드해야 하는가? |
| Prompt | 현재 invocation의 goal과 일회성 context | 지금 무엇을 원하는가? |
| Agent | 독립 role, authority, tools, delegation | 누가 어떤 권한으로 행동하는가? |

`references/`, `docs/`, `scripts/`, `assets/`, `evals/`, `tests/`는 동급 자산 유형이 아니라 **supporting resources**다.

## Rule

Rule은 여러 task에서 지속 적용되는 policy와 constraint를 소유한다.

- repository/directory/path/file-type scope의 지속 규칙
- 반드시 지켜야 하는 guardrail과 convention
- 한 task의 긴 workflow나 상황별 판단 context는 소유하지 않음

상황에 따라 모델이 선택적으로 로드해야 하는 판단 context라면 Rule보다 Skill을 우선 검토한다.

### Rule Projections

아래는 이 저장소의 비표준 projection이다.

#### Directory — `AGENTS.md`

루트와 하위 디렉터리의 `AGENTS.md`를 directory subtree Rule로 사용한다.

- root `AGENTS.md`: repository-wide 기본 Rule
- nested `AGENTS.md`: 해당 directory와 하위 경로의 더 좁은 Rule
- target path를 다룰 때 root부터 target까지 applicable chain을 고려
- nested file만 읽고 ancestor Rule을 버리지 않음

실제 precedence/override semantics는 repository와 target harness가 명시한 규칙을 따른다.

#### Glob

공통 하위 디렉터리, 파일군, 확장자처럼 directory tree 하나로 표현하기 어려운 scope는 glob selector 기반 Rule로 운용한다.

```text
**/*.md
**/*.py
**/tests/**
```

- 현재 target path와 selector가 일치할 때만 적용
- 여러 `AGENTS.md`에 같은 file-type Rule을 반복하는 대신 사용
- 파일 형식, front matter, selector field, discovery path는 target harness에 맞춤
- 특정 harness의 glob schema를 범용 Rule 표준으로 취급하지 않음

#### Chatbot — `CHATBOT.md`

`CHATBOT.md`는 **텍스트 입출력 중심 chatbot**을 위한 Rule projection이다. 웹 검색이나 서비스 plugin/tool을 사용할 수 있는 일반 chatbot도 포함한다.

Repository instruction fallback은 다음과 같다.

```text
CHATBOT.md
  ↓ 없으면
AGENTS.md
  ↓ 없으면
README.md
```

- applicable `CHATBOT.md`가 있으면 chatbot Rule로 우선
- 없으면 applicable `AGENTS.md`
- 둘 다 없으면 applicable `README.md`를 마지막 fallback instruction source로 사용
- 이 fallback 때문에 README 자체를 일반적인 Rule 형식으로 간주하지 않음
- system/user/platform/tool authority는 이 repository-local chain보다 우선

Directory, glob, chatbot projection은 함께 적용될 수 있다.

## Skill

Skill은 이 저장소에서 **가장 이식성이 높고 모델 판단에 따라 필요한 context를 조건부 주입하기 좋은 기본 재사용 단위**다.

재사용 가능한 내용이 Rule·Prompt·Agent여야 할 명확한 이유가 없다면 Skill을 우선 검토한다.

### Why Skill First

- **Model-directed activation** — metadata/description으로 모델이 관련성을 판단
- **Conditional loading** — 항상 context를 점유하지 않고 필요할 때만 로드
- **Progressive disclosure** — core instructions와 optional resources 분리
- **Portability** — 여러 Skills-compatible harness에 projection하기 쉬움
- **Composition** — 현재 task에 필요한 작은 capability/context를 조합 가능

Skill은 workflow에 한정하지 않는다. decision lens, domain context, tool guidance처럼 활성화되면 모델 판단이 달라지는 coherent context capability도 Skill이 될 수 있다.

### Context-only Skills

주책임이 workflow가 아니라 **상황별 context 주입**이면 `load-context-<topic>` 이름을 쓴다.

예:

- `load-context-coding`
- `load-context-github`
- `load-context-notion`
- `load-context-human-writing`
- `load-context-agent-assets`

`load-context-*`는 context discovery/selection/scoping/loading까지만 소유한다. 실제 구현, 작성, 검증, 리뷰, mutation, 최종 output은 downstream capability가 소유한다.

이 naming은 repository-local convention이다.

### Skill Target Profiles

> [!IMPORTANT]
> `skills/`, `skills-chatbot/`, `skills-chatbot-runtime/`의 3분류는 **Agent Skills 표준이 아니라 이 저장소의 비표준 target profile taxonomy**다.

| Profile | 최적화 대상 |
| --- | --- |
| `skills/` | workspace/filesystem/shell/repository authority가 있는 agent runtime |
| `skills-chatbot/` | 단일 Markdown만 받는 flat chatbot harness |
| `skills-chatbot-runtime/` | bundle/tools/connectors/progressive loading을 활용하는 hosted chatbot runtime |

같은 capability가 둘 또는 세 profile에 동시에 존재할 수 있다. target별 harness capability가 다르면 semantic overlap은 의도적인 projection이며 DRY 위반으로 보지 않는다.

최적화 단위는 **`capability × target profile`**이다.

#### Flat vs Runtime

`skills-chatbot/`은 다음을 모두 만족할 때 사용한다.

1. `<skill-name>.skill.md` 한 파일로 완결
2. 배포 파일이 **4,000 tokens 미만**
3. runtime-required bundle이나 host-only capability가 필요하지 않음

다음 중 하나라도 해당하면 `skills-chatbot-runtime/`을 사용한다.

- 4,000 tokens 이상이라 Markdown을 분리해야 함
- references/assets/scripts/images 등 runtime-required bundle 필요
- tools/connectors/scripts/progressive loading이 capability의 중요한 부분

공식 Agent Skills의 `<5,000 tokens` 권장과 달리 `<4,000`은 이 저장소의 더 엄격한 **로컬 flat budget**이다.

Maintainer-only docs/evals/tests/validator는 배포 payload와 분리할 수 있다면 runtime placement를 강제하지 않는다. 작은 textual schema는 명확성을 해치지 않으면 fenced code로 flat Skill에 포함할 수 있다.

## Prompt

Prompt는 현재 invocation의 goal과 일회성 context를 소유한다.

반복해서 같은 capability나 policy를 Prompt에 복사해야 한다면 Skill이나 Rule로 승격할지 검토한다.

## Agent

Agent는 독립 runtime actor의 책임을 소유한다.

- role/instructions
- tools
- authority/permissions/guardrails
- handoff/delegation
- output responsibility

instruction이 길거나 이름을 붙이고 싶다는 이유만으로 Agent를 만들지 않는다. 별도 role/authority가 필요하지 않은 reusable capability/context는 Skill을 우선한다.

## Supporting Resources

Supporting resource는 다른 자산이 필요할 때 읽거나 실행하는 재료다.

- `references/`: 상세 knowledge/context
- `scripts/`: deterministic helper
- `assets/`: template/image/data resource
- `docs/`: human/maintainer documentation
- `evals/`, `tests/`: behavior/package validation

Resource 자체가 model-directed activation을 소유하지 않는다. 특정 knowledge를 상황에 따라 자동으로 활성화해야 한다면 Skill이 activation boundary를 소유하고 resource를 조건부로 로드한다.

## Placement

새 자산은 다음 순서로 판단한다.

1. 특정 scope에서 여러 task 동안 지속되는 policy인가? → **Rule**
2. 반복 capability 또는 상황별로 모델이 로드해야 하는 context인가? → **Skill**
3. 현재 invocation에서만 필요한 goal/constraint인가? → **Prompt**
4. 독립 role/authority/tool/delegation boundary가 필요한가? → **Agent**

재사용 가능한 내용이고 1·3·4의 명확한 이유가 없다면 **Skill을 우선 후보**로 한다.

### Rule placement

- directory subtree → root/nested `AGENTS.md`
- 여러 위치의 공통 directory/file type/extension → glob Rule
- text I/O chatbot → `CHATBOT.md`, 없으면 `AGENTS.md`, 그마저 없으면 `README.md`

### Skill placement

- context-only → `load-context-<topic>` naming 검토
- workspace authority가 capability 핵심 → `skills/`
- single Markdown + `<4,000 tokens` + runtime dependency 없음 → `skills-chatbot/`
- 그 외 bundle/runtime capability 필요 → `skills-chatbot-runtime/`

## Anti-patterns

- 조건부 context를 global Rule/Agent instruction에 항상 로드
- Prompt에 reusable capability 반복 복사
- Rule 안에 한 task의 전체 workflow 작성
- 같은 glob concern을 여러 `AGENTS.md`에 반복
- `CHATBOT.md` fallback이나 Skill 3-profile을 외부 표준처럼 설명
- supporting resource를 동급 Agent Asset으로 분류
- workflow Skill에 `load-context-` naming 사용
- target profile이 다른 sibling Skill을 내용 중복만으로 제거
- 4,000-token flat budget을 외부 표준으로 설명
- 한 harness의 semantics를 다른 target에 강제

## Review Questions

> 이 내용은 지속 Rule인가, 조건부 Skill인가?

> Rule이라면 directory, glob, chatbot 중 어떤 projection이 실제 scope를 가장 정확히 표현하는가?

> Skill이라면 현재 harness에서 어떤 target profile이 가장 효율적인가?

## Baseline

외부 표준과 생태계 공통 개념의 근거는 [Agent Asset Standard Baseline](agent-asset-standard-baseline.md)이 소유한다. 이 문서는 그 baseline을 반복 설명하지 않고 **이 저장소의 확장과 운용 결정만** 소유한다.
