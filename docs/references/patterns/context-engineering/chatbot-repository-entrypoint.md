---
description: Chat runtime이 repository의 context와 Agent Asset을 native하게 발견하지 못할 때 stable entrypoint와 runtime bootstrap을 연결하는 reusable pattern입니다.
---

# Chatbot Repository Entrypoint

Repository 안에 **chatbot이 context loading을 시작할 stable entrypoint 하나를 두고**, runtime 밖의 bootstrap instruction이 그 entrypoint를 명시적으로 읽도록 연결해 chatbot이 agent harness와 비슷하게 repository context를 시작할 수 있게 하는 패턴입니다.

이 entrypoint가 자동으로 발견된다고 가정하지 않습니다. 따라서 이 패턴의 핵심은 특정 filename이나 위치가 아니라 **repository-side entrypoint와 runtime-side bootstrap의 결합**입니다.

## Purpose

Agent harness는 보통 repository instruction, scoped guidance, Skill, Rule, project context 같은 자산을 일정한 방식으로 발견하거나 주입합니다. 일반 chatbot은 이런 discovery contract가 없거나 runtime마다 다를 수 있습니다.

Repository entrypoint는 이런 환경에서 chatbot이 사용할 **첫 context hop**을 제공합니다. Chatbot은 이 entrypoint를 통해 현재 repository에서 무엇을 확인해야 하는지, 어떤 guidance나 routing surface가 있는지, task에 따라 무엇을 더 읽거나 어디로 route해야 하는지를 알 수 있습니다.

이 패턴은 chatbot을 완전한 agent harness로 바꾸는 것이 아니라, **초기 context loading과 routing을 repository 안에서 재현하기 위한 얇은 compatibility layer**를 제공합니다.

## Core

```text
runtime / project instruction
        ↓
"이 repository에서 substantive work를 할 때 <entrypoint>를 먼저 읽는다"
        ↓
repository entrypoint
        ↓
routing guidance / selection signals
        ↓
task-relevant context / next route
```

두 surface의 책임을 분리합니다.

| Surface | Responsibility |
| --- | --- |
| runtime-side bootstrap | entrypoint가 자동 발견된다고 가정하지 않고 위치를 명시적으로 알려줌 |
| repository-side entrypoint | repository 안에서 chatbot이 사용할 context, guidance와 routing으로 연결 |

Bootstrap instruction은 짧고 안정적으로 유지하는 편이 좋습니다. Repository-specific detail은 가능한 한 entrypoint 또는 그 entrypoint가 가리키는 canonical owner에 둡니다.

## Entrypoint Shape

Entrypoint의 filename, 위치와 format은 pattern의 본질이 아닙니다.

예를 들어 다음 모두 가능합니다.

```text
CHATBOT.md
.chatbot/entry.md
config/chatbot.yaml
agent-context.json
route/chatbot.txt
```

Root `CHATBOT.md`는 사람이 찾기 쉽고 repository 전체 entrypoint라는 의도가 명확해 대표적인 형태로 사용할 수 있지만 필수는 아닙니다.

Entrypoint를 선택할 때는 보통 다음이 더 중요합니다.

- bootstrap instruction에서 안정적으로 가리킬 수 있는가
- 사람이 repository를 볼 때 역할을 이해하기 쉬운가
- 다른 자산과 authority가 충돌하지 않는가
- 이동이나 rename이 잦지 않은가
- runtime이 실제로 읽을 수 있는 format과 위치인가

Format도 Markdown일 필요가 없습니다. 사람이 직접 유지하는 instruction/router라면 readable text format이 편리할 수 있고, machine-generated routing metadata라면 JSON이나 다른 structured format이 더 적합할 수 있습니다.

## Entrypoint Responsibility

Entrypoint는 repository의 모든 지침을 복제하기보다 **chatbot이 기존 자산을 어떻게 발견하고 사용할지 연결하는 역할**에 집중할 수 있습니다.

예를 들어 Markdown entrypoint는 routing 정보를 직접 담을 수 있습니다.

```markdown
# Chatbot Entrypoint

Repository-wide guidance는 `AGENTS.md`를 확인한다.

## Skills

| Skill | Use when | Route |
| --- | --- | --- |
| `mols-rpi` | recursive RPI improvement가 필요할 때 | `src/.../mols-rpi/SKILL.md` |
| `searcher` | current external research나 verification이 필요할 때 | `src/.../searcher/SKILL.md` |
```

작은 repository라면 table이나 bullet list만으로 충분할 수 있습니다. 후보가 많거나 같은 routing metadata를 여러 consumer가 재사용하거나 자동 생성할 가치가 있을 때는 별도 [Routing & Index Assets](routing-index-assets.md) pattern을 함께 사용할 수 있습니다.

`Route`는 local file path에 한정되지 않습니다. 현재 candidate를 실제로 읽거나 사용할 수 있는 source, catalog, native surface 또는 더 구체적인 router를 가리킬 수 있습니다. Authority와 runtime access가 다를 때의 일반적인 경계는 [Routing & Index Assets](routing-index-assets.md)가 다룹니다.

이 예시는 고정 schema가 아닙니다. Repository가 이미 가진 instruction, routing, index, documentation 구조에 맞게 더 작거나 다른 형태로 구성할 수 있습니다.

특히 `AGENTS.md`, Skill body, Rule, development policy처럼 이미 authority를 가진 내용을 entrypoint에 다시 복사하기보다 **그 owner나 적절한 next surface로 route하는 방식**이 drift와 context duplication을 줄이는 데 도움이 됩니다.

## Routable Discovery

Entrypoint가 asset directory나 source path만 알려주는 것으로는 semantic routing이 성립하지 않을 수 있습니다. 여러 후보 중 task-relevant asset을 선택해야 한다면 **후보의 위치뿐 아니라 선택할 근거**도 발견 가능해야 합니다.

Skill이라면 이름과 route만 나열하기보다 description, trigger, `when to use`처럼 현재 task와의 applicability를 판단할 수 있는 정보를 함께 제공하는 식입니다.

```text
# navigation only
Skills are under src/.../skills/

# routable
mols-rpi — recursive RPI improvement에 사용 — src/.../mols-rpi/SKILL.md
searcher — current external research에 사용 — src/.../searcher/SKILL.md
```

Routing guidance는 entrypoint 안의 prose, bullet, table일 수도 있고 별도 index/router일 수도 있습니다. 중요한 것은 **특정 representation이 아니라 소비자가 후보를 실제로 선택할 수 있는가**입니다.

Repository entrypoint가 chatbot 전용 자산만 다룰 필요도 없습니다. 같은 repository에서 local agent와 chatbot이 공유하는 guidance나 Skill이 있다면 함께 route할 수 있고, consumer마다 applicability가 다를 때만 그 차이를 드러내면 됩니다.

## Bootstrap

Repository에 entrypoint를 두는 것만으로는 충분하지 않을 수 있습니다. 해당 runtime이 그 위치나 filename을 native convention으로 지원하지 않으면 chatbot은 존재 자체를 알지 못할 수 있습니다.

따라서 runtime이 확실히 보는 surface에서 짧은 bootstrap을 제공할 수 있습니다.

대표적인 위치는 다음과 같습니다.

- project instructions
- custom or system-level instructions
- repository 작업을 시작할 때 사용하는 reusable prompt
- plugin, workspace 또는 harness configuration
- runtime이 제공하는 다른 guaranteed instruction surface

예:

```text
For substantive work in this repository, read <repository entrypoint> first and follow its routing guidance.
```

Bootstrap은 repository guidance 자체를 품기보다 **entrypoint 위치와 loading expectation만 알려주는 pointer**에 가깝게 유지할 수 있습니다.

이렇게 하면 runtime마다 bootstrap 방식이 달라도 repository 안의 durable chatbot guidance는 같은 entrypoint를 재사용할 수 있습니다.

## Typical Forms

### Root `CHATBOT.md`

사람이 쉽게 발견할 수 있는 대표적인 형태입니다.

```text
bootstrap
→ root CHATBOT.md
→ routing guidance
→ selected context / next surface
```

`CHATBOT.md` 자체가 작은 router가 될 수 있습니다. 별도 routing/index asset은 규모나 재사용 필요가 있을 때 선택합니다.

### Dedicated Entrypoint Path

Repository root를 덜 어지럽히거나 chatbot 관련 자산을 한곳에 모으고 싶다면 별도 위치를 사용할 수 있습니다.

```text
bootstrap
→ .chatbot/entry.md
→ repository context sources
```

### Generated Entrypoint

Discovery metadata가 자동 생성된다면 structured artifact 자체를 entrypoint로 사용할 수도 있습니다.

```text
bootstrap
→ route/chatbot.json
→ candidate metadata
→ selected context / access surface
```

이 경우 generated artifact를 canonical instruction owner로 오해하지 않도록 source authority를 분리하는 것이 좋습니다.

## Multiple Entrypoints

Directory나 domain별로 추가 entrypoint를 둘 수도 있지만, **파일이 여러 개 있다는 사실만으로 automatic hierarchy가 생기지는 않습니다**.

예:

```text
repository/
├─ CHATBOT.md
├─ backend/
│  └─ CHATBOT.md
└─ data/
   └─ CHATBOT.md
```

이런 구성이 유용하려면 어떤 mechanism이 다음을 결정하는지 명확해야 합니다.

- 어느 entrypoint를 언제 읽는가
- 여러 entrypoint가 적용될 때 어떤 관계를 가지는가
- 작업 scope가 바뀌면 새로운 entrypoint를 다시 탐색하는가

따라서 기본적으로는 **하나의 stable entrypoint에서 시작**하고, 실제로 독립적인 context boundary나 loading 이점이 있을 때만 추가 entrypoint를 고려하는 편이 단순합니다.

여러 entrypoint가 필요하더라도 반드시 같은 filename이나 format을 사용할 필요는 없습니다. 중요한 것은 routing과 ownership이 명확한가입니다.

## Considerations

- Entrypoint는 portable standard가 아니라 repository convention일 수 있으므로 automatic discovery를 주장하지 않습니다.
- Runtime이 native repository instruction discovery를 충분히 제공한다면 별도 entrypoint가 불필요할 수 있습니다.
- Semantic selection이 필요한 asset에 directory path나 file list만 제공하면 discovery는 가능해도 실제 routing은 불가능할 수 있습니다.
- 작은 routing 문제를 해결하기 위해 별도 index, generator나 schema를 만들 필요는 없습니다. Entrypoint 안의 짧은 table이나 bullet이 충분하면 그것을 사용합니다.
- Chatbot과 local agent가 같은 context를 공유한다면 routing 정보를 불필요하게 consumer별로 복제하지 않습니다.
- Entrypoint가 너무 많은 실제 지침을 직접 소유하면 기존 canonical assets와 중복되고 항상 로드되는 context도 커질 수 있습니다.
- Bootstrap instruction과 repository entrypoint가 같은 내용을 반복하지 않도록 responsibility를 나누는 편이 유지보수하기 쉽습니다.
- Entrypoint를 여러 개로 늘리면 locality는 좋아질 수 있지만 discovery, precedence와 stale duplication 비용도 커질 수 있습니다.
- Chatbot runtime의 file/tool access가 제한적이면 entrypoint가 가리키는 route를 실제로 따라갈 수 있는지도 별도로 고려해야 합니다.

## Relationship to Other Patterns

이 패턴은 **chatbot이 repository context에 진입하는 bootstrap과 first entrypoint**를 다룹니다.

| Pattern | Relationship |
| --- | --- |
| [Routing & Index Assets](routing-index-assets.md) | Routing 정보를 별도 reusable/generated surface로 분리할 가치가 있을 때 사용할 수 있습니다. Entrypoint 자체의 table이나 bullet도 유효한 대안입니다. |
| [Layered Context Instructions](layered-context-instructions.md) | 어떤 scope mechanism에 instruction을 배치할지 다룹니다. |
| [Progressive Context Routing](progressive-context-routing.md) | 많은 context source 중 필요한 것을 단계적으로 좁혀 로드하는 방식을 다룹니다. |

Repository entrypoint는 이 pattern들의 기능을 다시 구현할 필요 없이, 해당 repository가 사용하는 mechanism으로 chatbot을 연결하는 first hop으로 동작할 수 있습니다.

## Boundary

이 패턴은 `CHATBOT.md`, repository root, Markdown, table, 별도 routing index 또는 다른 특정 representation을 표준으로 정의하지 않습니다. 또한 특정 runtime의 automatic loading, inheritance, precedence 또는 path discovery behavior를 보장하지 않습니다.

핵심은 다음과 같습니다.

1. Repository 안에 chatbot이 context loading을 시작할 **하나의 stable entrypoint**를 둡니다.
1. 그 entrypoint가 자동으로 보일 것이라 가정하지 않고, 실제 runtime이 확실히 받는 instruction surface에서 명시적으로 연결합니다.
1. Semantic selection이 필요한 context는 위치만 알려주지 않고 **실제로 선택할 수 있는 applicability information**을 제공합니다.

추가 entrypoint나 별도 routing/index asset은 가능한 extension이지 이 패턴의 필수 구성은 아닙니다.
