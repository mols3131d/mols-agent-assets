---
description: 외부 프로젝트에 재사용할 Work Management Skill을 설계할 때 기존 도구 비교, 책임 경계, 행동 시나리오와 실패 조건을 확인합니다.
---

# Work Management Skill — Design Context

## Problem

소프트웨어 변경 스펙·테스트·구현의 8단계를 작업 관리에도 적용하면 작은 버그, 운영 이슈, 여러 작업 사이의 의존성 관리에 불필요한 문서·단계·상태가 발생한다. 반대로 전용 작업 관리 Skill이 스펙 문서와 테스트 결과까지 소유하면 책임이 중복된다. **두 개의 독립 선택 가능한 Skill**을 후보로 두되, 두 프레임워크를 강제로 연동하거나 새 백엔드를 만드는 것이 목표는 아니다.

## Existing Capability Baseline

- [GitHub Issues dependencies](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies): blocked-by/blocking의 정본 관계 지원. [Sub-issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues): 작업 분해·계층 지원. [Projects best practices](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects): 기존 Issue/PR 데이터와 프로젝트 관리 활용.
- [Beads quickstart](https://github.com/gastownhall/beads/blob/main/docs/getting-started/quickstart.md) 및 [core concepts](https://github.com/gastownhall/beads/blob/main/docs/core-concepts/index.md): dependency와 ready work queue를 제공. 이 도구는 로컬 runtime 및 별도 저장 상태가 필요하므로 Chat에서 실행 가능하다고 추정하면 안 된다.
- [Agent Skills format](https://agentskills.io/specification): `SKILL.md` + 필요시 references/scripts/assets로 하나의 실행·배포 단위를 구성. Script 동작은 실제 host가 지원할 때만 가능하다.

**가설:** 새 tracker를 만들지 않고 기존 provider의 native task API/CLI를 사용하는 Skill이라면 가치가 있을 수 있다. 그러나 '일반 task 관리 사용법'만 반복하는 Skill이라면 별도 제품의 가치가 부족하다.

## Boundary and Collaboration

| User intent | Work Management | Spec/Test-driven |
| --- | --- | --- |
| 여러 이슈 중 다음 작업을 정해줘 | 주 담당 | 불필요 |
| 이 기능의 API 동작·수락 조건을 명세해줘 | 불필요 | 주 담당 |
| 이슈를 쪼개고 blocker를 추적해줘 | 주 담당 | 스펙 하위 계약을 변경하지 않음 |
| 스펙 결함 때문에 테스트를 수정해야 해 | 영향받은 work item의 진행에 필요할 때만 반영 | 원인·스펙·테스트·구현 영향 검토 주 담당 |
| 한 작업의 RPI 개선 루프를 실행해줘 | 작업 기록이 필요할 때만 | 스펙/테스트가 관련할 때만 |

**Workflow 소유권:** Work Management는 **작업 간**의 우선순위·의존성·재개를 소유한다. Spec/Test-driven은 **한 소프트웨어 변경 안**의 산출물·검증 의존성을 소유한다. 작업 내부 반복 방법을 전역적으로 지배하는 제3의 엔진은 만들지 않는다.

**Persistence 소유권:** 원본 task tracker의 상태가 정본이다. 연결이 없으면 사용자가 제공한 작업과 현재 세션의 확인 가능한 정보로 제안을 작성할 수 있으나 영구 상태를 갱신했다고 선언하지 않는다. 별도의 tracker나 동기화 미들웨어는 범위 밖이다.

## Representative Design Tests

1. **Tiny fix:** 단일 버그 수정에 제안서·스펙·테스트 설계 또는 추적 task 생성이 자동 강제되지 않아야 한다.
2. **Priority change:** GitHub Issues의 blocker 관계가 우선순위보다 먼저 고려되어야 하지만, 실제 조회가 불완전하면 준비된 작업을 확정적으로 주장하지 않는다.
3. **Planning:** 소프트웨어 스펙 1개가 작업 5개에 대응하거나, 여러 소프트웨어 변경이 하나의 Issue 아래에 있어도 매핑 가능해야 한다.
4. **Interrupted work:** 새로운 세션에서 이전 메시지의 task state를 믿지 않고, 실제 provider와 마지막 작업 근거를 다시 조회한다.
5. **Permissions:** 특정 GitHub 연결 계정만 사용하도록 명시되면 다른 계정 전환 없이 부분 수행/차단한다.
6. **No tracker:** tracker 선택·설치·외부 기록을 무단으로 수행하지 않고 로컬 제안 또는 기존 프로젝트 수단을 제시한다.
7. **Near miss:** `mise` 작업 명령 설계, Spec/Test-driven 검증, 테스트 코드 품질, 단순 개인 일정 관리 요청에는 활성화하지 않는다.

## Decisions to Defer Until Evidence

- 지원할 provider 종류와 portable adapter 추상화. 처음부터 provider 플러그인 레지스트리를 만들지 않는다.
- 자체 상태 파일, 재개 로그, 양방향 sync가 필요한지. 첫 dogfood 전까지 불필요하다.
- 언제 task를 자동 생성·수정할 수 있는지와 승인 범위. 실제 provider 권한·부작용에 따라 판단한다.
- 스크립트가 제공할 수 있는 결정적 가치가 있는지. native API와 동일한 래퍼는 만들지 않는다.

## Recommended Work Sequence

(1) 독립 Skill이 필요한 실패 사례 확인 → (2) source owner·activation·두 Skill 간 경계 확정 → (3) 최소 Skill 작성 → (4) GitHub read-only·write-confirmed·unavailable 환경의 행동 평가 → (5) 발견된 문제에만 필요한 script/reference 추가.

이 자료는 **설계 및 인계 근거**이며, 새 Skill의 실행 규칙이나 repository policy 정본이 아니다.
