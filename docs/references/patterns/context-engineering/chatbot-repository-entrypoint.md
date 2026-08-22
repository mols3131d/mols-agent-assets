---
description: Repository-native context discovery가 부족한 chat runtime에서 stable entrypoint와 runtime bootstrap을 연결할 때 참고하는 reusable compatibility pattern입니다.
---

# Chatbot Repository Entrypoint

Repository-native context discovery가 부족한 runtime에 **stable repository entrypoint와 runtime-side bootstrap을 연결해 first-hop을 복구하는** compatibility pattern입니다.

이 패턴은 chatbot과 agent를 별도 policy taxonomy로 정의하지 않습니다. 적용 여부는 runtime 이름이 아니라 **현재 harness가 필요한 repository guidance와 Agent Asset을 실제로 발견할 수 있는가**로 판단합니다.

## Purpose

Runtime이 applicable repository instructions, Skills, Rules 또는 routing surface를 native하게 발견하지 못하면 repository 안에 자산이 존재해도 첫 context hop이 끊길 수 있습니다.

이때 compatibility layer는 누락된 discovery만 보완하고 기존 owner를 그대로 유지합니다.

```text
runtime guaranteed instruction surface
        ↓
repository entrypoint
        ↓
routing / applicability information
        ↓
task-relevant canonical owner
```

## Core

두 surface의 책임을 분리합니다.

| Surface | Responsibility |
| --- | --- |
| runtime-side bootstrap | runtime이 entrypoint를 native하게 발견하지 못할 때 그 위치와 loading expectation을 알려줌 |
| repository-side entrypoint | repository 안의 기존 guidance, routing과 Agent Asset owner로 연결 |

핵심 원칙은 다음과 같습니다.

- Native discovery가 충분하면 별도 compatibility layer를 만들지 않습니다.
- 부족한 discovery responsibility만 보완합니다. Partial native support는 정상입니다.
- Entrypoint는 기존 policy, Skill body, Rule body 또는 catalog 전체를 복제하지 않고 canonical owner로 route합니다.
- Semantic selection이 필요하면 위치뿐 아니라 description, selector 또는 다른 applicability information도 발견 가능해야 합니다.
- Bootstrap은 repository detail을 복제하지 않고 entrypoint 위치와 loading expectation만 전달하는 얇은 pointer로 유지합니다.
- Entrypoint와 bootstrap은 새로운 authority를 만들지 않습니다.

## Entrypoint Shape

Filename, 위치와 format은 pattern의 본질이 아닙니다.

```text
CHATBOT.md
.chatbot/entry.md
agent-context.json
route/chatbot.json
```

선택 기준은 representation보다 다음에 가깝습니다.

- runtime이 실제로 접근할 수 있는가
- bootstrap에서 안정적으로 가리킬 수 있는가
- 사람이 역할과 authority boundary를 이해하기 쉬운가
- 기존 repository routing이나 instruction surface를 재사용할 수 있는가
- rename이나 이동에 따른 drift 비용이 과하지 않은가

Root `CHATBOT.md`는 가능한 repository convention 중 하나일 뿐 portable standard가 아닙니다. 특정 project가 root 하나만 허용하거나 다른 entrypoint를 사용한다면 해당 local authority를 따릅니다.

## Entrypoint Responsibility

Entrypoint는 **first-hop routing**만 소유하는 편이 좋습니다.

예를 들어 다음을 직접 재작성하지 않고 연결할 수 있습니다.

- repository-wide 또는 path-scoped instruction owner
- task-relevant Skill discovery surface
- Rule selector 또는 scoped context owner
- generated routing/index metadata

작은 repository에서는 짧은 bullet이나 table로 충분할 수 있습니다. 후보가 많거나 routing metadata를 여러 consumer가 재사용할 가치가 있을 때는 [Routing & Index Assets](routing-index-assets.md) pattern을 함께 사용할 수 있습니다.

Directory path나 file list만 보여서는 semantic routing이 불가능한 경우가 있습니다. 그런 경우 candidate를 선택할 최소 applicability information을 함께 노출합니다.

```text
# navigation only
Skills are under src/.../skills/

# routable
mols-rpi — recursive RPI improvement에 사용 — <route>
searcher — current external research에 사용 — <route>
```

Representation은 고정 schema가 아닙니다. 기존 repository mechanism이 같은 역할을 이미 수행한다면 그것을 재사용합니다.

## Bootstrap

Entrypoint가 runtime의 native convention이 아니라면 runtime이 확실히 받는 instruction surface에서 first-hop을 연결할 수 있습니다.

예:

```text
For substantive work in this repository, read <repository entrypoint> first and follow its routing guidance.
```

가능한 bootstrap surface는 runtime에 따라 project instruction, workspace configuration, reusable prompt 또는 다른 guaranteed instruction surface일 수 있습니다.

Runtime-side surface를 현재 권한으로 수정하거나 검증할 수 없다면 repository-side entrypoint만 만들어 놓고 end-to-end compatibility가 완성됐다고 주장하지 않습니다.

## Scope Changes

하나의 stable entrypoint에서 시작하더라도 task scope가 바뀌면 downstream scoped instruction이나 Rule applicability를 다시 계산할 수 있습니다. 이를 위해 nested entrypoint hierarchy를 만들 필요는 없습니다.

추가 entrypoint가 실제로 필요하다면 해당 repository가 **명시적인 discovery·selection·precedence mechanism**을 소유해야 합니다. 단순히 같은 이름의 파일을 여러 directory에 둔 사실만으로 hierarchy나 inheritance를 추정하지 않습니다.

## Considerations

- Compatibility layer는 native harness behavior를 대체하지 않습니다.
- Runtime 이름만으로 누락 capability를 추정하지 말고 실제 discovery behavior를 기준으로 판단합니다.
- Entrypoint가 실제 policy owner가 되면 기존 canonical source와 drift하기 쉽습니다.
- 항상 로드되는 entrypoint가 커질수록 context cost도 커지므로 first-hop에 필요한 정보만 둡니다.
- Generated routing artifact를 사용해도 generated projection을 semantic authority로 승격시키지 않습니다.
- Runtime이 entrypoint가 가리키는 source에 실제로 접근할 수 있는지도 별도로 확인합니다.

## Relationship to Other Patterns

| Pattern | Relationship |
| --- | --- |
| [Routing & Index Assets](routing-index-assets.md) | 후보 selection metadata를 별도 reusable/generated surface로 둘 가치가 있을 때 사용 |
| [Layered Context Instructions](layered-context-instructions.md) | scoped instruction을 어떤 mechanism에 배치할지 다룸 |
| [Progressive Context Routing](progressive-context-routing.md) | 많은 context source 중 필요한 것을 단계적으로 좁혀 로드하는 방식을 다룸 |

## Boundary

이 패턴은 특정 filename, repository 위치, Markdown format, routing schema 또는 chatbot/agent taxonomy를 표준으로 정의하지 않습니다. 특정 runtime의 automatic loading, inheritance, precedence 또는 path discovery도 보장하지 않습니다.

핵심은 세 가지입니다.

1. 실제 runtime에서 누락된 repository discovery가 있는지 먼저 확인합니다.
1. 필요한 경우 stable repository entrypoint와 guaranteed runtime-side bootstrap으로 first-hop만 복구합니다.
1. 기존 guidance와 Agent Asset은 자기 의미의 canonical owner로 남기고 compatibility surface는 그 owner로 route합니다.
