---
description: Artifact Inbox의 아티팩트를 날짜 대신 브랜치·Issue·Pull Request 등 지속적인 작업 단위로 묶을지 판단하고 경로를 설계할 때 참고하는 확장 패턴입니다.
---

# Artifact Inbox: Work Unit Containers

작업이 여러 조사·계획·리뷰 산출물로 이어질 때, 작성 날짜보다 **하나의 작업을 식별하는 기준**으로 [Artifact Inbox](artifact-inbox.md)의 아티팩트를 묶는 확장 패턴입니다.

## Core

관련 아티팩트를 함께 찾고 이어 가는 데 도움이 된다면 **work unit identity**를 container 이름에 사용할 수 있습니다. 브랜치, Issue, Pull Request는 대표적인 작업 단위이고, 날짜는 별도 식별자가 없을 때 유용한 대안입니다.

핵심은 특정 디렉터리명이나 우선순위가 아니라 **아티팩트 묶음과 그것이 지원하는 작업의 관계를 쉽게 복구하는 것**입니다. 단순히 PR을 언급한 문서라고 해서 그 PR의 container로 옮길 필요는 없습니다.

## Typical Forms

| 기준 | 유용한 상황 | Container 예시 |
| --- | --- | --- |
| 날짜 | 독립적인 조사, 일회성 작업 | `inbox/2026-09-29/` |
| 브랜치 | 하나의 코드 변경을 따라가는 작업 | `inbox/branch-feature-x/` |
| Issue | Issue의 조사·계획·해결 과정 | `inbox/github-241/` |
| Pull Request | PR의 변경·검증·리뷰 과정 | `inbox/github-242/` |

예를 들어 한 Inbox에서 다음과 같이 함께 사용할 수 있습니다.

```text
inbox/
├── 2026-09-29/
│   └── research.md
├── branch-feature-x/
│   ├── plan.md
│   └── review.md
└── github-242/
    ├── findings.md
    └── handoff.md
```

이 경로는 **구현 예시**입니다. 실제 naming, identifier scope, 디렉터리 깊이와 허용되는 bundle 구조는 프로젝트가 정합니다. 다른 hosting·tracking system도 사용할 수 있고, 여러 저장소의 동일 번호가 충돌한다면 repository나 work-unit type을 이름에 포함할 수 있습니다. 날짜와 브랜치를 조합하는 형태도 가능합니다.

## Choosing a Container

선택할 때는 다음을 살펴보면 좋습니다.

- **연속성:** 다음 작업자가 어느 묶음을 찾아야 하는지 쉽게 알 수 있는가?
- **식별 안정성:** 브랜치 이름·번호·날짜 가운데 작업 기간에 잘 유지되는 기준은 무엇인가?
- **관리 비용:** 한 문서만 있는데도 새 container가 필요하거나, 같은 아티팩트를 여러 곳에 복제하게 되지는 않는가?

예를 들어 Issue에서 시작해 여러 브랜치로 구현하는 작업은 Issue 중심이 편리하고, 하나의 PR을 준비·검토하는 작업은 PR 중심이 자연스러울 수 있습니다. 한 가지 고정된 선택 순서를 따를 필요는 없습니다.

## Work Unit Transitions

작업 단위는 브랜치에서 시작해 PR로 옮겨 갈 수 있습니다. 이때 기존 container를 새 식별자로 **이동하거나 그대로 두는 것 모두 가능**합니다. 이동한다면 기존 링크와 인계 기록의 유효성을 확인하는 편이 좋습니다.

목표는 이름 변경 자체가 아니라 **현재 작업의 소속과 재개 위치를 잃지 않는 것**입니다. 선택한 container 안에서도 조사·계획·리뷰 등 여러 아티팩트를 함께 둘 수 있으며, 탐색에 실제 도움이 될 때만 README나 추가 metadata를 둘 수 있습니다.

## Boundary

이 패턴은 [Artifact Inbox](artifact-inbox.md)의 working/non-canonical surface를 **어떤 작업 단위로 묶을지**에만 초점을 둡니다. 정본 승격·보존·삭제는 기본 Inbox 패턴과 프로젝트의 문서 정책이 소유합니다.

Git 브랜치·Issue·PR의 lifecycle, 전역 naming 규칙, archive 정책이나 특정 도구 사용을 정의하지 않으며, 프로젝트가 이 패턴을 채택했다고 해서 아티팩트 경로가 자동으로 생성·이동되는 것은 아닙니다.
