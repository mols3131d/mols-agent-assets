# Chatbot Repository Entrypoint

Repository root의 `CHATBOT.md`를 **chat runtime용 stable entrypoint**로 두고, runtime 밖의 bootstrap instruction이 이 파일을 먼저 읽도록 연결해 chatbot이 agent harness와 비슷하게 repository context를 시작할 수 있게 하는 패턴입니다.

`CHATBOT.md`라는 파일이 존재한다고 해서 일반 chatbot이 자동으로 발견하거나 적용한다는 보장은 없습니다. 따라서 이 패턴의 핵심은 파일 하나가 아니라 **repository-side entrypoint와 runtime-side bootstrap의 결합**입니다.

## Purpose

Agent harness는 보통 repository instruction, scoped guidance, Skill, Rule, project context 같은 자산을 일정한 방식으로 발견하거나 주입합니다. 일반 chatbot은 이런 discovery contract가 없거나 runtime마다 다를 수 있습니다.

Root `CHATBOT.md`는 이런 환경에서 repository가 제공하는 **chatbot용 첫 context hop**으로 사용할 수 있습니다. Chatbot은 이 entrypoint를 통해 현재 repository에서 무엇을 확인해야 하는지, 어떤 guidance나 routing surface가 있는지, task에 따라 무엇을 더 읽어야 하는지를 알 수 있습니다.

이 패턴은 chatbot을 완전한 agent harness로 바꾸는 것이 아니라, **초기 context loading과 routing을 repository 안에서 재현하기 위한 얇은 compatibility layer**를 제공합니다.

## Core

```text
runtime / project instruction
        ↓
"이 repository에서 substantive work를 할 때 root CHATBOT.md를 먼저 읽는다"
        ↓
repository root
└─ CHATBOT.md
   ├─ repository guidance로 route
   ├─ task-relevant asset discovery로 route
   └─ 필요한 local context로 route
```

두 surface의 책임을 분리합니다.

| Surface | Responsibility |
| --- | --- |
| runtime-side bootstrap | `CHATBOT.md`가 자동 발견된다고 가정하지 않고 entrypoint를 명시적으로 로드하게 함 |
| root `CHATBOT.md` | repository 안에서 chatbot이 사용할 context, guidance, routing surface로 연결 |

Bootstrap instruction은 짧고 안정적으로 유지하는 편이 좋습니다. Repository-specific detail은 가능한 한 `CHATBOT.md` 또는 그 파일이 가리키는 canonical owner에 둡니다.

## Root `CHATBOT.md`

Root placement는 repository 전체에 대해 하나의 예측 가능한 chatbot entrypoint를 제공한다는 장점이 있습니다.

`CHATBOT.md`는 repository의 모든 지침을 복제하기보다 **chatbot이 기존 자산을 어떻게 발견하고 사용할지 연결하는 역할**에 집중할 수 있습니다.

예를 들어 다음과 같은 내용을 가질 수 있습니다.

```markdown
# CHATBOT.md

이 repository에서 substantive work를 수행할 때:

- repository-wide guidance는 `AGENTS.md`를 확인한다.
- task-relevant Skills는 canonical Skill index 또는 routing surface에서 선택한다.
- path-scoped guidance가 있으면 현재 작업 범위에 맞는 source를 추가로 확인한다.
- repository-specific development/document policy는 각 canonical entrypoint를 따른다.
```

이 예시는 고정 schema가 아닙니다. Repository가 이미 가진 instruction, routing, index, documentation 구조에 맞게 더 작거나 다른 형태로 구성할 수 있습니다.

특히 `AGENTS.md`, Skill body, Rule, development policy처럼 이미 authority를 가진 내용을 `CHATBOT.md`에 다시 복사하기보다 **그 owner로 route하는 방식**이 drift와 context duplication을 줄이는 데 도움이 됩니다.

## Bootstrap

Root에 `CHATBOT.md`를 두는 것만으로는 충분하지 않을 수 있습니다. 해당 runtime이 이 filename을 native convention으로 지원하지 않으면 chatbot은 파일 존재 자체를 알지 못할 수 있습니다.

따라서 runtime이 확실히 보는 surface에서 짧은 bootstrap을 제공할 수 있습니다.

대표적인 위치는 다음과 같습니다.

- project instructions
- custom or system-level instructions
- repository 작업을 시작할 때 사용하는 reusable prompt
- plugin, workspace 또는 harness configuration
- runtime이 제공하는 다른 guaranteed instruction surface

예:

```text
For substantive work in this repository, read the root CHATBOT.md first and follow its routing guidance.
```

Bootstrap은 repository guidance 자체를 품기보다 **entrypoint 위치와 loading expectation만 알려주는 pointer**에 가깝게 유지할 수 있습니다.

이렇게 하면 runtime마다 bootstrap 방식이 달라도 repository 안의 durable chatbot guidance는 같은 `CHATBOT.md`를 재사용할 수 있습니다.

## Nested `CHATBOT.md`

Subdirectory 안에도 `CHATBOT.md`를 둘 수는 있습니다.

```text
repository/
├─ CHATBOT.md
├─ backend/
│  └─ CHATBOT.md
└─ data/
   └─ CHATBOT.md
```

다만 root `CHATBOT.md`와 달리 nested form은 **명시적인 discovery 또는 routing mechanism이 있을 때** 가치가 더 분명합니다.

일반 chatbot이 다음을 자동으로 수행한다고 가정하기 어렵기 때문입니다.

- 현재 path에 해당하는 가장 가까운 `CHATBOT.md` 탐색
- root와 nested instruction의 inheritance
- 여러 `CHATBOT.md` 사이의 precedence 결정
- 작업 scope가 바뀔 때 새로운 nested entrypoint 재탐색

따라서 기본적으로는 root 하나로 시작하고, subtree가 독립적인 context boundary를 가지며 root entrypoint나 별도 loader가 그 nested file을 안정적으로 찾아줄 수 있을 때 확장하는 편이 단순합니다.

Nested `CHATBOT.md` 대신 기존 harness가 이미 지원하는 nested instruction, glob Rule, scoped Skill 같은 mechanism을 사용하고 root `CHATBOT.md`가 그 surface로 route하는 방식도 가능합니다.

## Typical Forms

### Root Router

가장 작은 형태입니다.

```text
bootstrap
→ root CHATBOT.md
→ AGENTS.md / Skills / Rules / docs
```

`CHATBOT.md`는 거의 routing만 소유합니다.

### Chatbot Delta

기존 agent harness용 자산은 그대로 두고 chatbot에만 필요한 compatibility delta를 root `CHATBOT.md`에 둡니다.

```text
CHATBOT.md
├─ chatbot-specific loading guidance
├─ unsupported discovery fallback
└─ canonical agent assets로 route
```

### Explicit Nested Routing

Subtree별 chatbot guidance가 실제로 필요하면 root entrypoint에서 조건을 명시해 nested source로 연결할 수 있습니다.

```text
root CHATBOT.md
├─ repository default
├─ backend work → backend/CHATBOT.md
└─ data work    → data/CHATBOT.md
```

이 경우 nested file의 존재보다 **어떤 조건에서 읽는지가 명확한 것**이 더 중요합니다.

## Considerations

- `CHATBOT.md`는 portable standard가 아니라 repository convention일 수 있으므로 자동 discovery를 주장하지 않습니다.
- Runtime이 native repository instruction discovery를 충분히 제공한다면 별도 `CHATBOT.md`가 불필요할 수 있습니다.
- Root entrypoint가 너무 많은 실제 지침을 직접 소유하면 기존 canonical assets와 중복되고 항상 로드되는 context도 커질 수 있습니다.
- Bootstrap instruction과 `CHATBOT.md`가 같은 내용을 반복하지 않도록 responsibility를 나누는 편이 유지보수하기 쉽습니다.
- Nested files를 늘리면 locality는 좋아질 수 있지만 discovery, precedence, stale duplication 비용도 커질 수 있습니다.
- Chatbot runtime의 file/tool access가 제한적이면 entrypoint가 가리키는 자산을 실제로 읽을 수 있는지도 별도로 고려해야 합니다.

## Relationship to Other Patterns

이 패턴은 **chatbot이 repository context에 진입하는 bootstrap과 entrypoint**를 다룹니다.

그 이후 어떤 scope mechanism에 지침을 배치할지는 [Layered Context Instructions](layered-context-instructions.md), 많은 context source 중 필요한 것을 단계적으로 좁혀 로드하는 방식은 [Progressive Context Routing](progressive-context-routing.md)과 함께 사용할 수 있습니다.

`CHATBOT.md`는 이 pattern들의 기능을 다시 구현할 필요 없이, 해당 repository가 사용하는 mechanism으로 chatbot을 연결하는 첫 hop으로 동작할 수 있습니다.

## Boundary

이 패턴은 `CHATBOT.md`라는 이름을 모든 chatbot runtime이 지원하는 표준으로 정의하지 않습니다. 또한 특정 runtime의 automatic loading, inheritance, precedence 또는 path discovery behavior를 보장하지 않습니다.

핵심은 다음 두 가지입니다.

1. Repository root에 chatbot이 사용할 수 있는 stable entrypoint를 둡니다.
1. 그 entrypoint가 자동으로 보일 것이라 가정하지 않고, 실제 runtime이 확실히 받는 instruction surface에서 명시적으로 연결합니다.

Nested `CHATBOT.md`는 가능한 extension이지 이 패턴의 필수 구성은 아닙니다.
