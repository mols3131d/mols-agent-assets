# Chatbot Asset Directory

Repository 안에 `.chatbot/` 같은 **chatbot-only asset directory**를 두어, 일반 coding agent 자산과 분리해서 관리하기 어려운 chatbot 전용 guidance, work profile, Skill, command, compatibility asset을 모아두는 패턴입니다.

`.chatbot/`은 대표적인 repository convention이지 chatbot vendor가 공통으로 자동 탐색하는 표준 경로라는 뜻은 아닙니다. 이 directory의 가치는 **chatbot에만 필요한 자산의 ownership과 discovery surface를 한곳에 모으는 것**에 있습니다.

## Purpose

Chatbot과 coding agent는 같은 repository를 보더라도 실제 runtime capability와 작업 방식이 크게 다를 수 있습니다.

예를 들어 chatbot은 다음과 같은 차이를 가질 수 있습니다.

- repository 파일을 자동으로 탐색하거나 instruction hierarchy를 적용하지 않을 수 있음
- write, commit, PR, external action 같은 작업 권한을 별도 지시로 제한하거나 활성화해야 할 수 있음
- coding agent의 command, hook, subagent, workspace mechanism을 그대로 사용할 수 없음
- 여러 chatbot vendor에서 공통으로 재사용할 guidance나 routing asset이 필요할 수 있음
- conversational workflow에 맞는 Skill, command, handoff, context-loading instruction이 따로 필요할 수 있음

이런 차이를 기존 agent-native 자산에 억지로 섞기보다 chatbot 전용 surface에 격리하면, 공통 repository 자산은 유지하면서 chatbot runtime의 delta를 별도로 관리할 수 있습니다.

## Core

```text
repository/
├─ agent / project-native assets
└─ .chatbot/
   └─ chatbot-only assets
```

핵심은 `.chatbot/`이라는 정확한 이름보다 다음 책임 분리입니다.

```text
shared repository behavior
→ 기존 canonical owner

chatbot-only compatibility / workflow / control delta
→ chatbot asset directory
```

Chatbot-only directory는 기존 source의 내용을 복제하기보다 **chatbot이 추가로 알아야 하거나 다른 방식으로 적용해야 하는 delta**를 소유하는 편이 좋습니다.

## Typical Contents

Directory 내부 구조는 고정 schema가 아닙니다. 실제 반복되는 책임이 있을 때만 나눕니다.

대표적으로 다음과 같은 자산을 둘 수 있습니다.

### Work or Permission Profiles

Chatbot이 어떤 범위까지 작업해도 되는지, 어떤 side effect를 허용할지, 어떤 방식으로 진행할지를 몇 개의 reusable profile로 둘 수 있습니다.

```text
.chatbot/
└─ profiles/
   ├─ read-only.md
   ├─ edit.md
   └─ repo-write.md
```

예를 들어 2~4개의 profile만 두고 상황에 따라 하나를 로드하게 할 수 있습니다.

```text
read-only
→ 조사, 분석, 리뷰만

edit
→ bounded file/content mutation 허용

repo-write
→ branch, commit, PR 같은 repository mutation까지 허용
```

이 profile은 **behavioral work boundary**를 표현합니다. 실제 tool permission, sandbox, approval, account authorization을 새로 부여하지는 않습니다. Runtime이 별도 permission system을 제공하면 실제 권한은 그 mechanism이 소유합니다.

### Skills

Chatbot runtime에서만 필요한 lightweight Skill이나 compatibility Skill을 둘 수 있습니다.

```text
.chatbot/
└─ skills/
   └─ ...
```

예를 들어 coding agent에서는 native discovery가 되지만 chatbot에서는 별도 context-loading Skill이 필요한 경우, chatbot 전용 fallback을 이 surface에서 관리할 수 있습니다.

반대로 여러 runtime에서 동일하게 쓰는 canonical Skill까지 무조건 `.chatbot/`으로 옮길 필요는 없습니다. Chatbot-only delta가 아닌 자산은 원래 authority를 유지하는 편이 좋습니다.

### Commands

자주 반복되는 chatbot 작업을 짧은 command-like entry로 둘 수 있습니다.

```text
.chatbot/
└─ commands/
   ├─ review.md
   ├─ research.md
   └─ release-check.md
```

이 command는 실제 slash-command feature일 수도 있고, entrypoint가 자연어 요청을 해당 instruction asset으로 route하는 convention일 수도 있습니다.

따라서 filename이나 invocation syntax보다 **반복되는 chatbot 작업 단위를 안정적으로 재사용할 수 있는가**가 중요합니다.

### Shared Multi-Vendor Assets

여러 chatbot vendor를 함께 사용한다면 vendor-neutral한 공통 guidance를 한 번만 둘 수 있습니다.

```text
.chatbot/
├─ shared/
│  ├─ repository-work.md
│  └─ review-policy.md
├─ openai/
│  └─ ...
└─ google/
   └─ ...
```

공통 의미는 `shared/` 같은 surface가 소유하고, vendor-specific delta가 실제로 있을 때만 vendor별 asset을 추가하는 방식이 가능합니다.

이 구조도 예시일 뿐입니다. Vendor가 요구하는 native project path나 schema가 있다면 실제 vendor-native asset은 그 contract를 따르는 것이 우선입니다. `.chatbot/`을 vendor-native path의 대체 규격으로 사용하지 않습니다.

## Typical Shape

작게 시작한다면 다음 정도로 충분할 수 있습니다.

```text
.chatbot/
├─ profiles/
│  ├─ read-only.md
│  ├─ edit.md
│  └─ repo-write.md
├─ skills/
├─ commands/
└─ shared/
```

Directory가 존재한다고 해서 모든 하위 종류를 만들 필요는 없습니다.

```text
.chatbot/
└─ repo-work.md
```

처럼 파일 하나로 시작해도 되고, 실제 responsibility가 반복될 때만 분리할 수 있습니다.

## Loading and Routing

`.chatbot/`도 자동 discovery를 전제하지 않습니다.

Repository entrypoint나 runtime-side bootstrap이 필요한 asset으로 route할 수 있습니다.

```text
runtime bootstrap
→ repository chatbot entrypoint
→ task / requested capability 판단
→ .chatbot/<relevant asset>
```

예를 들어 entrypoint가 다음과 같은 의미를 가질 수 있습니다.

```text
repository를 읽기만 하는 작업
→ .chatbot/profiles/read-only.md

파일 수정이 필요한 작업
→ .chatbot/profiles/edit.md

PR까지 수행하는 작업
→ .chatbot/profiles/repo-write.md
```

모든 profile과 Skill을 처음부터 로드하기보다 현재 task에 필요한 것만 선택하면 chatbot-only context가 커지는 것을 줄일 수 있습니다.

## Multi-Vendor Use

여러 chatbot vendor가 같은 repository를 사용한다면 `.chatbot/`을 **vendor-neutral authored surface**로 사용할 수 있습니다.

```text
                 ┌→ Chatbot A bootstrap
.chatbot/shared ─┼→ Chatbot B bootstrap
                 └→ Chatbot C bootstrap
```

다만 모든 vendor가 같은 capability나 instruction semantics를 가진다고 가정하지 않습니다.

- 공통 의미는 한 번만 유지할 수 있습니다.
- vendor-specific capability나 behavior는 필요한 경우 delta로 분리할 수 있습니다.
- vendor가 native asset format이나 native project path를 요구하면 그 representation은 vendor contract를 따릅니다.
- `.chatbot/`의 shared asset을 vendor-native source와 이중 canonical authority로 만들지 않는 편이 좋습니다.

## Options

- `.chatbot/` 대신 `chatbot/`, `config/chatbot/`, `.agents/chatbot/` 같은 다른 repository-local directory를 사용할 수 있습니다.
- Permission/work profile 없이 Skills나 commands만 둘 수 있습니다.
- 반대로 Skill 없이 profile과 routing guidance만 둘 수도 있습니다.
- 하나의 chatbot만 사용해도 coding agent와의 behavioral delta가 크다면 이 패턴이 유용할 수 있습니다.
- 여러 chatbot vendor를 사용하면 shared core와 vendor delta를 함께 관리하는 capsule로 확장할 수 있습니다.
- Runtime이 이미 충분한 native chatbot asset directory와 discovery mechanism을 제공한다면 그 native mechanism을 사용하는 편이 더 단순할 수 있습니다.

## Considerations

- Chatbot-only asset을 너무 많이 만들면 공통 repository guidance와 중복되고 drift가 생길 수 있습니다.
- `read-only`, `write`, `full-access` 같은 이름은 실제 runtime permission과 혼동될 수 있으므로 해당 profile이 behavioral instruction인지 real permission configuration인지 분명하게 하는 편이 좋습니다.
- 여러 vendor의 차이를 하나의 universal schema로 추상화하려 하면 오히려 vendor-native capability를 잃을 수 있습니다.
- Directory hierarchy 자체보다 어떤 asset이 왜 chatbot-only인지 ownership을 명확하게 유지하는 것이 중요합니다.
- 항상 로드되는 bootstrap이나 entrypoint에 전체 `.chatbot/` 내용을 복사하지 않고 필요한 자산으로 route하는 구성이 context economy에 유리할 수 있습니다.

## Relationship to Repository Entrypoint

이 패턴은 **chatbot-only assets를 어디에 모아 관리할지**를 다룹니다.

[Chatbot Repository Entrypoint](chatbot-repository-entrypoint.md)은 chatbot이 repository context에 처음 진입하는 surface를 다룹니다. 두 패턴을 함께 쓰면 다음과 같은 구성이 가능합니다.

```text
runtime-side bootstrap
→ repository chatbot entrypoint
→ .chatbot/의 task-relevant profile / Skill / command
→ existing canonical repository assets
```

Entrypoint가 반드시 `.chatbot/` 안에 있을 필요도 없고, `.chatbot/` directory가 반드시 별도 entrypoint를 가질 필요도 없습니다.

## Boundary

이 패턴은 `.chatbot/`을 chatbot vendor의 표준 directory로 정의하지 않습니다.

또한 이 directory에 있는 permission-like asset이 실제 sandbox, tool authorization, account permission 또는 approval gate를 우회하거나 확장한다고 가정하지 않습니다.

핵심은 **coding agent와 다른 chatbot-only delta를 하나의 명확한 repository asset surface에 모아두고, 필요한 runtime에서 선택적으로 로드·재사용하는 것**입니다.
