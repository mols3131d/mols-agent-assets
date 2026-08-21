# Chatbot Repository Entrypoint

Repository 안에 **chatbot이 context loading을 시작할 stable entrypoint 하나를 두고**, runtime 밖의 bootstrap instruction이 그 entrypoint를 명시적으로 읽도록 연결해 chatbot이 agent harness와 비슷하게 repository context를 시작할 수 있게 하는 패턴입니다.

이 entrypoint가 자동으로 발견된다고 가정하지 않습니다. 따라서 이 패턴의 핵심은 특정 filename이나 위치가 아니라 **repository-side entrypoint와 runtime-side bootstrap의 결합**입니다.

## Purpose

Agent harness는 보통 repository instruction, scoped guidance, Skill, Rule, project context 같은 자산을 일정한 방식으로 발견하거나 주입합니다. 일반 chatbot은 이런 discovery contract가 없거나 runtime마다 다를 수 있습니다.

Repository entrypoint는 이런 환경에서 chatbot이 사용할 **첫 context hop**을 제공합니다. Chatbot은 이 entrypoint를 통해 현재 repository에서 무엇을 확인해야 하는지, 어떤 guidance나 routing surface가 있는지, task에 따라 무엇을 더 읽어야 하는지를 알 수 있습니다.

이 패턴은 chatbot을 완전한 agent harness로 바꾸는 것이 아니라, **초기 context loading과 routing을 repository 안에서 재현하기 위한 얇은 compatibility layer**를 제공합니다.

## Core

```text
runtime / project instruction
        ↓
"이 repository에서 substantive work를 할 때 <entrypoint>를 먼저 읽는다"
        ↓
repository entrypoint
        ↓
repository guidance / routing / task-relevant context
```

두 surface의 책임을 분리합니다.

| Surface | Responsibility |
| --- | --- |
| runtime-side bootstrap | entrypoint가 자동 발견된다고 가정하지 않고 위치를 명시적으로 알려줌 |
| repository-side entrypoint | repository 안에서 chatbot이 사용할 context, guidance, routing surface로 연결 |

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

Format도 Markdown일 필요가 없습니다. 다만 사람이 직접 유지하는 instruction/router라면 readable text format이 편리할 수 있고, machine-generated routing metadata라면 JSON이나 다른 structured format이 더 적합할 수 있습니다.

## Entrypoint Responsibility

Entrypoint는 repository의 모든 지침을 복제하기보다 **chatbot이 기존 자산을 어떻게 발견하고 사용할지 연결하는 역할**에 집중할 수 있습니다.

예를 들어 Markdown entrypoint라면 다음처럼 구성할 수 있습니다.

```markdown
# Chatbot Entrypoint

이 repository에서 substantive work를 수행할 때:

- repository-wide guidance는 `AGENTS.md`를 확인한다.
- task-relevant Skills는 canonical Skill index 또는 routing surface에서 선택한다.
- path-scoped guidance가 있으면 현재 작업 범위에 맞는 source를 추가로 확인한다.
- repository-specific development/document policy는 각 canonical entrypoint를 따른다.
```

이 예시는 고정 schema가 아닙니다. Repository가 이미 가진 instruction, routing, index, documentation 구조에 맞게 더 작거나 다른 형태로 구성할 수 있습니다.

특히 `AGENTS.md`, Skill body, Rule, development policy처럼 이미 authority를 가진 내용을 entrypoint에 다시 복사하기보다 **그 owner로 route하는 방식**이 drift와 context duplication을 줄이는 데 도움이 됩니다.

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
→ AGENTS.md / Skills / Rules / docs
```

`CHATBOT.md`는 거의 routing만 소유할 수 있습니다.

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
→ selected canonical sources
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
- Entrypoint가 너무 많은 실제 지침을 직접 소유하면 기존 canonical assets와 중복되고 항상 로드되는 context도 커질 수 있습니다.
- Bootstrap instruction과 repository entrypoint가 같은 내용을 반복하지 않도록 responsibility를 나누는 편이 유지보수하기 쉽습니다.
- Entrypoint를 여러 개로 늘리면 locality는 좋아질 수 있지만 discovery, precedence와 stale duplication 비용도 커질 수 있습니다.
- Chatbot runtime의 file/tool access가 제한적이면 entrypoint가 가리키는 자산을 실제로 읽을 수 있는지도 별도로 고려해야 합니다.

## Relationship to Other Patterns

이 패턴은 **chatbot이 repository context에 진입하는 bootstrap과 first entrypoint**를 다룹니다.

그 이후 어떤 scope mechanism에 지침을 배치할지는 [Layered Context Instructions](layered-context-instructions.md), 많은 context source 중 필요한 것을 단계적으로 좁혀 로드하는 방식은 [Progressive Context Routing](progressive-context-routing.md)과 함께 사용할 수 있습니다.

Repository entrypoint는 이 pattern들의 기능을 다시 구현할 필요 없이, 해당 repository가 사용하는 mechanism으로 chatbot을 연결하는 첫 hop으로 동작할 수 있습니다.

## Boundary

이 패턴은 `CHATBOT.md`, repository root, Markdown 또는 다른 특정 representation을 표준으로 정의하지 않습니다. 또한 특정 runtime의 automatic loading, inheritance, precedence 또는 path discovery behavior를 보장하지 않습니다.

핵심은 다음 두 가지입니다.

1. Repository 안에 chatbot이 context loading을 시작할 **하나의 stable entrypoint**를 둡니다.
1. 그 entrypoint가 자동으로 보일 것이라 가정하지 않고, 실제 runtime이 확실히 받는 instruction surface에서 명시적으로 연결합니다.

추가 entrypoint는 가능한 extension이지 이 패턴의 필수 구성은 아닙니다.
