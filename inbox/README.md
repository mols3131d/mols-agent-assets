# Inbox

`inbox/`는 조사·계획·검토·인계 등의 **working / non-canonical artifact**를 보관하는 repository-local workspace입니다. 사람, chat runtime, coding agent와 automation이 같은 구조를 사용하며 특정 도구에 의존하지 않습니다.

## Paths

작업을 나중에 다시 찾기 쉬운 **하나의 기준**으로 artifact를 묶습니다.

| 기준 | 경로 | 선택할 때 |
| --- | --- | --- |
| Date (기본값) | `inbox/YYYY-MM-DD/<artifact>` | 독립적인 조사나 일회성 작업 등 별도 작업 식별자가 없을 때 |
| Branch | `inbox/branch-<slug>/<artifact>` | 브랜치가 작업의 주된 단위이고 Issue·PR보다 자연스러울 때 |
| Issue | `inbox/github-issue-<number>[-<topic>]/<artifact>` | Issue 자체의 조사·계획·추적을 위한 작업일 때 |
| Pull Request | `inbox/github-pr-<number>[-<topic>]/<artifact>` | 특정 PR의 구현·검증·리뷰를 위한 작업일 때 |

- 날짜는 artifact 묶음을 처음 만든 날짜를 사용합니다. `<slug>`와 `<topic>`은 짧고 구분 가능한 이름을 사용하며, 번호만으로 충분하면 `<topic>`은 생략합니다.
- 이미 적절한 디렉터리가 있다면 재사용합니다. 작업이 Branch에서 PR로 발전해도 자동으로 옮기거나 동일한 artifact를 복제하지 않습니다. 소속을 알아보기 어려울 때만 경로를 정리합니다.
- 디렉터리는 실제 artifact가 생길 때만 만듭니다. 빈 디렉터리, placeholder, 고정된 파일 세트나 인덱스를 요구하지 않습니다.

## Artifacts

파일명은 주제나 역할을 알아볼 수 있게 짓습니다. 하나의 작업에 research, plan, review, handoff 등을 모두 만들 필요는 없습니다.

작업을 이어가는 데 필요하면 현재 상태, 판단 근거, 미해결 사항, 다음 행동과 관련 source·Issue·PR 링크를 남깁니다. 원본이나 Git 기록에 있는 내용을 장황하게 복제하지 않고, 현재 상태는 재개할 때 다시 확인합니다.

## Lifecycle

- 장기적으로 유효한 결정과 지식은 적절한 canonical owner에 반영합니다. Inbox 문서 자체는 정본이 아닙니다.
- 작업이 끝난 artifact는 다시 사용할 가치에 따라 유지·삭제하거나 `inbox/archive/YYYY-MM-DD/<artifact-or-directory>`로 옮길 수 있습니다. 이 날짜는 **아카이브한 날짜**이며, 필요한 경우 원래 작업 식별자를 유지합니다.
- 변경 이력은 Git history와 PR을 기본으로 사용합니다. 쉽게 재구성할 수 있는 기록을 보존 목적으로 중복 저장하지 않습니다.

정본 승격과 보존의 공통 원칙은 [Documentation — Working Knowledge](../docs/documentation/README.md#working-knowledge)를 따릅니다.

## Boundary

`inbox/`는 파일 배치 규칙이지 별도 branch, task tracker 또는 workflow engine이 아닙니다. GitHub 식별자를 경로에 사용할 수 있지만 GitHub 기능이나 플랫폼 전용 metadata는 artifact의 필수 조건이 아닙니다. Secret이나 불필요한 민감 정보는 저장하지 않습니다.
