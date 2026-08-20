# Inbox

`inbox/`는 사람, chat runtime, coding agent와 automation이 공통으로 사용할 수 있는 **platform-independent non-canonical artifact workspace**입니다.

## Paths

- 작업 중이거나 전달할 artifact → `inbox/YYYY-MM-DD/<artifact>`
- 보존 가치가 있지만 현재 정본이 아닌 artifact → `inbox/archive/YYYY-MM-DD/<artifact>`

날짜 directory는 실제 artifact가 생길 때만 만듭니다. 빈 directory나 placeholder를 유지하지 않습니다.

## Use

`inbox/`에는 report, review, research result, handoff, generated output, 임시 note와 같이 작업 과정에서 생기지만 canonical source나 durable documentation은 아닌 artifact를 둡니다.

다음은 `inbox/`에 두지 않습니다.

- 현재 behavior를 결정하는 policy나 contract
- runtime이 정상 동작하기 위해 필요한 source
- 계속 유지해야 하는 durable decision, invariant 또는 recovery knowledge

이런 지식은 해당 canonical source나 `docs/`의 좁은 owner로 승격합니다.

## Lifecycle

1. 새 non-canonical artifact는 `inbox/YYYY-MM-DD/`에 둡니다.
1. 현재와 미래의 판단을 계속 바꾸는 지식이 되면 canonical source 또는 durable documentation으로 승격하고 inbox copy를 authority로 남기지 않습니다.
1. 현재 정본은 아니지만 artifact 자체를 나중에 참고할 가치가 있으면 `inbox/archive/YYYY-MM-DD/`로 이동합니다.
1. 지속 가치가 없으면 삭제합니다.

`inbox/`와 `archive/`는 자동으로 authority가 되지 않습니다. Canonical source와 충돌하면 canonical source가 우선합니다.

## Archive vs Git History

`inbox/archive/`는 **비정본 artifact 자체를 보존할 가치가 있을 때** 사용합니다. 과거 report, review, handoff처럼 원문을 다시 찾아볼 이유가 있는 경우가 여기에 해당합니다.

Git history와 PR은 **repository가 어떻게 변했는지**를 복원하는 기본 기록입니다. 완료된 migration 과정, 일반 작업 로그, 이전 canonical content처럼 별도 artifact로 보존할 가치가 없는 과거 상태는 archive에 복제하지 않습니다.

Archived artifact는 current policy나 guidance로 자동 로드하지 않고, 최신 상태로 계속 갱신하지도 않습니다. 새로운 current knowledge가 필요하면 canonical source나 새 artifact를 작성합니다.

## Boundary

`inbox`는 directory convention이지 별도 branch, vendor feature 또는 workflow engine이 아닙니다. 일반 repository branch와 review 규칙을 그대로 따르며 특정 IDE, agent, chatbot, Notion 또는 GitHub 기능에 의존하지 않습니다.

별도 index는 요구하지 않습니다. Artifact 형식도 특정 플랫폼 metadata에 종속시키지 않습니다.
