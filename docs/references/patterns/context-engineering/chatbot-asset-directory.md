# Chatbot Asset Surface

Repository 안에 **chatbot-only asset surface**를 두어, coding agent와 다른 chatbot 전용 guidance, work profile, Skill, command, compatibility asset을 함께 관리하는 패턴입니다.

특정 directory name이나 path를 요구하지 않습니다. `.chatbot/`은 이해하기 쉬운 대표 예시일 뿐이며 repository 구조와 runtime에 맞는 다른 위치나 이름을 사용할 수 있습니다.

## Purpose

Chatbot과 coding agent는 같은 repository를 사용해도 capability와 작업 방식이 크게 다를 수 있습니다.

예를 들어 chatbot은 다음과 같은 차이를 가질 수 있습니다.

- repository instruction이나 asset을 자동 discovery하지 않을 수 있음
- write, commit, PR, external action 같은 작업 범위를 별도 guidance로 조정할 필요가 있음
- coding agent의 command, hook, subagent, workspace mechanism을 그대로 사용할 수 없음
- conversational workflow에 맞는 Skill, command, handoff, context-loading instruction이 따로 필요할 수 있음
- 여러 chatbot vendor에서 공통으로 재사용할 guidance가 필요할 수 있음

이런 차이를 공통 agent 자산에 억지로 섞기보다 chatbot-only surface에 모으면 기존 repository 자산을 유지하면서 chatbot runtime의 delta를 별도로 관리할 수 있습니다.

## Core

```text
shared repository behavior
→ existing canonical owners

chatbot-only compatibility / workflow / control delta
→ chatbot-specific asset surface
```

핵심은 directory 이름이나 위치가 아니라 **chatbot에만 필요한 자산의 ownership과 discovery boundary를 한 surface에 모으는 것**입니다.

기존 source의 내용을 복제하기보다 chatbot이 추가로 알아야 하거나 다른 방식으로 적용해야 하는 delta를 소유하는 편이 좋습니다.

## Typical Contents

내부 구조는 고정 schema가 아닙니다. 실제 반복되는 책임이 있을 때만 나눕니다.

### Work or Permission Profiles

Chatbot이 어떤 범위까지 작업해도 되는지, 어떤 side effect를 허용할지, 어떤 방식으로 진행할지를 몇 개의 reusable profile로 둘 수 있습니다.

예를 들어 2~4개 정도의 profile로 시작할 수 있습니다.

```text
read-only
→ 조사, 분석, 리뷰

edit
→ bounded file/content mutation

repo-write
→ branch, commit, PR 같은 repository mutation
```

대표적인 layout:

```text
<chatbot-assets>/
└─ profiles/
   ├─ read-only.md
   ├─ edit.md
   └─ repo-write.md
```

이 profile이 **behavioral work boundary**라면 실제 tool permission, sandbox, approval, account authorization을 새로 부여하지 않습니다. Runtime이 실제 permission mechanism을 제공하면 capability 자체는 그 mechanism이 소유합니다.

반대로 실제 permission configuration 파일을 이 surface에서 관리하는 구성도 가능하며, 그 경우 behavioral guidance와 real permission configuration을 구분하는 편이 좋습니다.

### Skills

Chatbot에서만 필요한 Skill이나 compatibility Skill을 둘 수 있습니다.

```text
<chatbot-assets>/
└─ skills/
   └─ ...
```

예를 들어 coding agent에서는 native discovery가 되지만 chatbot에서는 별도 context-loading Skill이 필요한 경우 chatbot 전용 fallback을 이 surface에서 관리할 수 있습니다.

여러 runtime에서 동일하게 쓰는 canonical Skill까지 이 surface로 옮길 필요는 없습니다. Chatbot-only delta가 아닌 자산은 원래 authority를 유지할 수 있습니다.

### Commands

자주 반복되는 chatbot 작업을 command-like asset으로 둘 수 있습니다.

```text
<chatbot-assets>/
└─ commands/
   ├─ review.md
   ├─ research.md
   └─ release-check.md
```

이 command는 실제 slash-command feature일 수도 있고, entrypoint가 자연어 요청을 해당 instruction asset으로 route하는 repository convention일 수도 있습니다.

Filename이나 invocation syntax보다 **반복되는 chatbot 작업 단위를 재사용할 수 있는가**가 중요합니다.

### Shared Multi-Vendor Assets

여러 chatbot vendor를 함께 사용한다면 vendor-neutral한 공통 guidance를 한 번만 둘 수 있습니다.

```text
<chatbot-assets>/
├─ shared/
│  ├─ repository-work.md
│  └─ review-policy.md
├─ <vendor-a>/
│  └─ ...
└─ <vendor-b>/
   └─ ...
```

공통 의미는 shared surface가 소유하고 vendor-specific delta가 실제로 있을 때만 vendor별 asset을 추가할 수 있습니다.

Vendor가 native project path나 schema를 요구한다면 실제 vendor-native asset은 그 contract를 따르는 것이 우선입니다. Chatbot-only surface를 vendor-native path의 대체 규격으로 만들 필요는 없습니다.

## Typical Forms

대표적인 형태 중 하나는 repository root의 `.chatbot/`입니다.

```text
repository/
└─ .chatbot/
   ├─ profiles/
   ├─ skills/
   ├─ commands/
   └─ shared/
```

하지만 같은 패턴을 다음처럼 구현할 수도 있습니다.

```text
repository/chatbot/
config/chatbot/
.agent-assets/chatbot/
tools/chat-runtime/
```

위 이름과 경로도 예시일 뿐입니다. Dot-directory, root placement, filename, extension, 내부 layout은 이 패턴의 invariant가 아닙니다.

작게 시작한다면 파일 하나나 작은 bundle만 있어도 됩니다.

## Local Guide

`.chatbot/`처럼 repository가 자체적으로 만든 비표준 directory를 사용한다면, 필요에 따라 그 위치에 `README.md` 같은 guide를 추가해 surface의 목적, scope, contract, convention, recommendation과 내부 자산을 설명할 수 있습니다.

이 guide가 entrypoint, index 또는 routing guide를 겸하는 것도 가능합니다. 이 패턴에서는 chatbot asset surface에 어떤 README section을 반드시 두어야 한다고 정의하지 않습니다.

## Loading and Routing

Chatbot-only asset surface도 자동 discovery를 전제하지 않습니다.

Repository entrypoint나 runtime-side bootstrap이 필요한 asset으로 route할 수 있습니다.

```text
runtime bootstrap
→ repository chatbot entrypoint
→ task / requested capability 판단
→ chatbot-specific asset surface의 relevant asset
```

모든 profile, Skill, command를 처음부터 로드하기보다 현재 task에 필요한 것만 선택하면 context를 작게 유지하는 데 도움이 됩니다.

## Multi-Vendor Use

여러 chatbot vendor가 같은 repository를 사용한다면 이 surface를 vendor-neutral authored surface로 사용할 수 있습니다.

- 공통 의미는 한 번만 유지할 수 있습니다.
- vendor-specific capability나 behavior는 필요할 때 delta로 분리할 수 있습니다.
- vendor가 native format이나 project path를 요구하면 그 representation은 vendor contract를 따릅니다.
- shared chatbot asset과 vendor-native source를 같은 semantic asset의 이중 canonical authority로 만들지 않는 편이 좋습니다.

## Options

- Directory가 아니라 하나의 file이나 작은 bundle로 구현할 수 있습니다.
- Work profile 없이 Skills나 commands만 둘 수 있습니다.
- 반대로 Skill 없이 profile과 routing guidance만 둘 수도 있습니다.
- 하나의 chatbot만 사용해도 coding agent와의 behavioral delta가 크다면 유용할 수 있습니다.
- 여러 chatbot vendor를 사용하면 shared core와 vendor delta를 함께 관리하는 surface로 확장할 수 있습니다.
- Runtime이 이미 충분한 native chatbot asset surface와 discovery mechanism을 제공한다면 그 mechanism을 그대로 사용하는 편이 더 단순할 수 있습니다.

## Considerations

- Chatbot-only asset을 너무 많이 만들면 공통 repository guidance와 중복되고 drift가 생길 수 있습니다.
- `read-only`, `write`, `full-access` 같은 이름은 실제 runtime permission과 혼동될 수 있으므로 behavioral instruction과 real permission configuration을 구분하는 편이 좋습니다.
- 여러 vendor의 차이를 하나의 universal schema로 추상화하려 하면 vendor-native capability를 잃을 수 있습니다.
- Directory hierarchy 자체보다 어떤 asset이 왜 chatbot-only인지 ownership을 명확하게 유지하는 것이 중요합니다.
- 항상 로드되는 bootstrap이나 entrypoint에 전체 surface를 복사하기보다 필요한 자산으로 route하는 구성이 context economy에 도움이 될 수 있습니다.

## Relationship to Repository Entrypoint

이 패턴은 **chatbot-only assets를 하나의 관리 surface로 묶는 것**을 다룹니다.

[Chatbot Repository Entrypoint](chatbot-repository-entrypoint.md)은 chatbot이 repository context에 처음 진입하는 stable first hop을 다룹니다.

두 패턴을 함께 쓰면 다음과 같은 구성이 가능합니다.

```text
runtime-side bootstrap
→ repository chatbot entrypoint
→ chatbot-specific profile / Skill / command
→ existing canonical repository assets
```

Entrypoint와 chatbot-only asset surface는 같은 위치에 있을 수도 있고 완전히 분리되어 있을 수도 있습니다. Surface 안의 README나 다른 guide가 repository entrypoint를 겸하는 구성도 가능합니다.

## Related Patterns

| Pattern | Relationship |
| --- | --- |
| [Nonstandard Directory Guide](../documentation/nonstandard-directory-guide.md) | `.chatbot/` 같은 repository-local nonstandard surface에 local guide가 필요할 때 참고합니다. |

## Boundary

이 패턴은 `.chatbot/`이나 다른 특정 directory를 chatbot vendor의 표준 경로로 정의하지 않습니다. Directory placement, filename, extension, internal layout 또는 root placement도 강제하지 않습니다.

또한 permission-like behavioral asset이 실제 sandbox, tool authorization, account permission 또는 approval gate를 우회하거나 확장한다고 가정하지 않습니다.

핵심은 **coding agent와 다른 chatbot-only delta를 하나의 명확한 asset surface에 모아두고 필요한 runtime에서 선택적으로 로드·재사용하는 것**입니다.
