# Chatbot Asset Surface

Repository 안에 **chatbot-only asset surface**를 두어, 일반 coding agent 자산과 분리해서 관리하기 어려운 chatbot 전용 guidance, work profile, Skill, command, compatibility asset을 모아두는 패턴입니다.

이 패턴은 특정 directory name이나 path를 요구하지 않습니다. `.chatbot/`은 이해하기 쉬운 대표 예시일 뿐이며, repository 구조와 runtime에 맞는 다른 위치나 이름을 사용할 수 있습니다.

## Purpose

Chatbot과 coding agent는 같은 repository를 보더라도 runtime capability와 작업 방식이 크게 다를 수 있습니다.

예를 들어 chatbot은 다음과 같은 차이를 가질 수 있습니다.

- repository 파일을 자동으로 탐색하거나 instruction hierarchy를 적용하지 않을 수 있음
- write, commit, PR, external action 같은 작업 범위를 별도 지시로 제한하거나 활성화해야 할 수 있음
- coding agent의 command, hook, subagent, workspace mechanism을 그대로 사용할 수 없음
- 여러 chatbot vendor에서 공통으로 재사용할 guidance나 routing asset이 필요할 수 있음
- conversational workflow에 맞는 Skill, command, handoff, context-loading instruction이 따로 필요할 수 있음

이런 차이를 기존 agent-native 자산에 억지로 섞기보다 chatbot 전용 surface에 격리하면, 공통 repository 자산은 유지하면서 chatbot runtime의 delta를 별도로 관리할 수 있습니다.

## Core

```text
shared repository behavior
→ existing canonical owners

chatbot-only compatibility / workflow / control delta
→ one chatbot-specific asset surface
```

핵심은 directory 이름이나 위치가 아니라 **chatbot에만 필요한 자산의 ownership과 discovery boundary를 한곳에 모으는 것**입니다.

Chatbot-only surface는 기존 source의 내용을 복제하기보다 chatbot이 추가로 알아야 하거나 다른 방식으로 적용해야 하는 delta를 소유하는 편이 좋습니다.

## Typical Contents

내부 구조는 고정 schema가 아닙니다. 실제 반복되는 책임이 있을 때만 나눕니다.

### Work or Permission Profiles

Chatbot이 어떤 범위까지 작업해도 되는지, 어떤 side effect를 허용할지, 어떤 방식으로 진행할지를 몇 개의 reusable profile로 둘 수 있습니다.

예를 들어 2~4개의 profile만 두고 상황에 따라 하나를 로드할 수 있습니다.

```text
read-only
→ 조사, 분석, 리뷰만

edit
→ bounded file/content mutation 허용

repo-write
→ branch, commit, PR 같은 repository mutation까지 허용
```

예시 layout:

```text
<chatbot-assets>/
└─ profiles/
   ├─ read-only.md
   ├─ edit.md
   └─ repo-write.md
```

이 profile은 **behavioral work boundary**를 표현합니다. 실제 tool permission, sandbox, approval, account authorization을 새로 부여하지는 않습니다. Runtime이 별도 permission system을 제공하면 실제 권한은 그 mechanism이 소유합니다.

### Skills

Chatbot runtime에서만 필요한 lightweight Skill이나 compatibility Skill을 둘 수 있습니다.

```text
<chatbot-assets>/
└─ skills/
   └─ ...
```

예를 들어 coding agent에서는 native discovery가 되지만 chatbot에서는 별도 context-loading Skill이 필요한 경우, chatbot 전용 fallback을 이 surface에서 관리할 수 있습니다.

반대로 여러 runtime에서 동일하게 쓰는 canonical Skill까지 이 surface로 옮길 필요는 없습니다. Chatbot-only delta가 아닌 자산은 원래 authority를 유지하는 편이 좋습니다.

### Commands

자주 반복되는 chatbot 작업을 짧은 command-like entry로 둘 수 있습니다.

```text
<chatbot-assets>/
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
<chatbot-assets>/
├─ shared/
│  ├─ repository-work.md
│  └─ review-policy.md
├─ <vendor-a>/
│  └─ ...
└─ <vendor-b>/
   └─ ...
```

공통 의미는 shared surface가 소유하고, vendor-specific delta가 실제로 있을 때만 vendor별 asset을 추가할 수 있습니다.

Vendor가 요구하는 native project path나 schema가 있다면 실제 vendor-native asset은 그 contract를 따르는 것이 우선입니다. Chatbot-only surface를 vendor-native path의 대체 규격으로 사용하지 않습니다.

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

하지만 같은 패턴을 다음처럼 구현해도 됩니다.

```text
repository/chatbot/
config/chatbot/
.agent-assets/chatbot/
tools/chat-runtime/
```

위 이름과 경로도 예시일 뿐입니다. Dot-directory, root placement, 특정 extension, 특정 내부 layout은 이 패턴의 invariant가 아닙니다.

작게 시작한다면 파일 하나만 있어도 됩니다.

```text
<chatbot-assets>/
└─ repo-work.md
```

실제 responsibility가 반복될 때만 directory를 분리하는 편이 단순합니다.

## Surface README

`.chatbot/`처럼 **비표준 repository-local surface**는 이름이나 위치만으로 목적과 사용법을 알기 어려울 수 있습니다. 이런 surface에는 `README.md` 같은 설명 문서를 두어 단순한 file entrypoint를 넘어 **surface 자체의 소개와 local contract를 제공하는 것**이 유용할 수 있습니다.

`README.md`라는 이름이나 Markdown 형식은 필수가 아닙니다. 같은 책임을 맡는 다른 entry document, manifest 또는 catalog를 사용할 수 있습니다.

이 문서는 필요에 따라 다음 중 일부를 소유할 수 있습니다.

- **Introduction** — 이 surface가 왜 존재하고 어떤 문제를 보완하는지
- **Scope** — 무엇을 이곳에 두고 무엇은 기존 canonical owner에 남기는지
- **Contract** — 이 surface에서 지켜야 하는 중요한 invariant나 authority boundary
- **Conventions** — naming, layout, loading, routing 등 repository-local 관행
- **Recommendations** — 유용하지만 강제하지 않는 기본 선택이나 운영 방식
- **Assets** — 어떤 종류의 asset이 있고 각각 어떤 책임을 가지는지
- **Loading** — chatbot이나 repository entrypoint가 이 surface를 어떻게 발견하고 사용하는지
- **Vendor boundary** — shared asset과 vendor-native 또는 vendor-specific asset의 관계

모든 항목을 가져야 하는 고정 schema는 아닙니다. Surface의 규모와 비표준성 때문에 사람이 추측해야 하는 부분만 설명하면 됩니다.

특히 contract, convention, recommendation은 성격을 구분하는 편이 좋습니다.

```text
contract
→ 이 surface의 의미나 안전한 사용을 위해 지켜야 하는 경계

convention
→ 이 repository에서 일관성을 위해 채택한 관행

recommendation
→ 상황에 따라 바꿀 수 있는 권장 기본값
```

예를 들어 `.chatbot/README.md`를 사용한다면 다음 정도로 시작할 수 있습니다.

```markdown
# Chatbot Assets

이 directory는 coding agent와 다른 chatbot-only guidance와 compatibility asset을 보관합니다.

## Scope

공통 repository behavior는 기존 canonical owner에 둡니다. 이곳에는 chatbot에서만 필요한 workflow, compatibility, work-profile delta를 둡니다.

## Contract

Permission-like profile은 실제 tool permission을 부여하지 않습니다. Runtime의 sandbox, approval, account authorization과 vendor-native configuration이 실제 capability를 소유합니다.

이 directory의 존재만으로 자동 loading을 가정하지 않습니다.

## Conventions

- 반복되는 작업 범위는 `profiles/`에 둘 수 있습니다.
- chatbot-only Skill은 `skills/`, 반복 작업 instruction은 `commands/`에 둘 수 있습니다.
- 현재 task에 필요한 asset만 선택적으로 로드합니다.

필요한 종류만 유지하며 이 layout을 모두 만들 필요는 없습니다.

## Recommendations

공통 agent guidance를 복제하기보다 기존 owner로 route하고, chatbot-specific delta만 이곳에서 소유하는 구성을 권장합니다.

## Assets

- `profiles/` — 작업 범위와 side-effect boundary를 표현하는 reusable work profiles
- `skills/` — chatbot에서만 필요한 Skill 또는 compatibility fallback
- `commands/` — 반복되는 chatbot 작업을 위한 reusable command-like instructions
- `shared/` — 여러 chatbot runtime에서 공통으로 사용하는 guidance
```

Surface가 작다면 별도 README 없이도 충분할 수 있습니다. 반대로 비표준 경로의 의미, 권한 경계, 내부 관행 또는 자산 선택 방법을 **repository 외부 지식 없이는 추측해야 하는 상태**라면 설명 문서를 두는 가치가 큽니다.

README를 단순 file index처럼 세세하게 유지할 필요도 없습니다. 안정적인 목적, 책임, 계약과 관행을 설명하고 세부 behavior는 각 asset이 소유하도록 두면 drift를 줄일 수 있습니다.

## Loading and Routing

이 asset surface도 자동 discovery를 전제하지 않습니다.

Repository entrypoint나 runtime-side bootstrap이 필요한 asset으로 route할 수 있습니다.

```text
runtime bootstrap
→ repository chatbot entrypoint
→ task / requested capability 판단
→ chatbot-specific asset surface의 relevant asset
```

모든 profile과 Skill을 처음부터 로드하기보다 현재 task에 필요한 것만 선택하면 chatbot-only context가 커지는 것을 줄일 수 있습니다.

## Multi-Vendor Use

여러 chatbot vendor가 같은 repository를 사용한다면 이 surface를 **vendor-neutral authored surface**로 사용할 수 있습니다.

- 공통 의미는 한 번만 유지할 수 있습니다.
- vendor-specific capability나 behavior는 필요한 경우 delta로 분리할 수 있습니다.
- vendor가 native asset format이나 native project path를 요구하면 그 representation은 vendor contract를 따릅니다.
- shared chatbot asset과 vendor-native source를 동일한 semantic asset의 이중 canonical authority로 만들지 않는 편이 좋습니다.

## Options

- Directory가 아니라 하나의 file이나 작은 bundle로 시작할 수 있습니다.
- Permission/work profile 없이 Skills나 commands만 둘 수 있습니다.
- 반대로 Skill 없이 profile과 routing guidance만 둘 수도 있습니다.
- 하나의 chatbot만 사용해도 coding agent와의 behavioral delta가 크다면 이 패턴이 유용할 수 있습니다.
- 여러 chatbot vendor를 사용하면 shared core와 vendor delta를 함께 관리하는 capsule로 확장할 수 있습니다.
- Runtime이 이미 충분한 native chatbot asset surface와 discovery mechanism을 제공한다면 그 native mechanism을 사용하는 편이 더 단순할 수 있습니다.

## Considerations

- Chatbot-only asset을 너무 많이 만들면 공통 repository guidance와 중복되고 drift가 생길 수 있습니다.
- `read-only`, `write`, `full-access` 같은 이름은 실제 runtime permission과 혼동될 수 있으므로 해당 profile이 behavioral instruction인지 real permission configuration인지 분명하게 하는 편이 좋습니다.
- 여러 vendor의 차이를 하나의 universal schema로 추상화하려 하면 오히려 vendor-native capability를 잃을 수 있습니다.
- Directory hierarchy 자체보다 어떤 asset이 왜 chatbot-only인지 ownership을 명확하게 유지하는 것이 중요합니다.
- 항상 로드되는 bootstrap이나 entrypoint에 전체 chatbot-only surface 내용을 복사하지 않고 필요한 자산으로 route하는 구성이 context economy에 유리할 수 있습니다.

## Relationship to Repository Entrypoint

이 패턴은 **chatbot-only assets를 하나의 관리 surface로 묶는 것**을 다룹니다.

[Chatbot Repository Entrypoint](chatbot-repository-entrypoint.md)은 chatbot이 repository context에 처음 진입하는 surface를 다룹니다. 두 패턴을 함께 쓰면 다음과 같은 구성이 가능합니다.

```text
runtime-side bootstrap
→ repository chatbot entrypoint
→ chatbot-specific profile / Skill / command
→ existing canonical repository assets
```

Entrypoint와 chatbot-only asset surface는 같은 위치에 있을 수도 있고 완전히 분리되어 있을 수도 있습니다.

## Boundary

이 패턴은 `.chatbot/`이나 다른 특정 directory를 chatbot vendor의 표준 경로로 정의하지 않습니다.

또한 directory placement, filename, extension, internal layout 또는 root placement를 강제하지 않습니다. 실제 location은 repository structure, discoverability, vendor contract와 유지보수 편의에 따라 선택할 수 있습니다.

또한 이 surface에 있는 permission-like asset이 실제 sandbox, tool authorization, account permission 또는 approval gate를 우회하거나 확장한다고 가정하지 않습니다.

핵심은 **coding agent와 다른 chatbot-only delta를 하나의 명확한 asset surface에 모아두고, 필요한 runtime에서 선택적으로 로드·재사용하는 것**입니다.
