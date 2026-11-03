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

## First Implementation Design

이 절은 구현 전 설계 결정이다. 실제 Skill 동작 계약은 이후 작성 원본이 소유하며, 이 Inbox 문서는 정본 지침이 아니다.

### Scope and Activation

- 제안 이름: `mols-work-management`. 재사용 작성 원본은 `src/rulesync/.rulesync/skills/mols-work-management/SKILL.md` 한 개로 시작한다. 스크립트·데이터베이스·provider adapter는 만들지 않는다.
- 여러 작업의 발견·분해·선택, 의존 관계와 우선순위, 중단·재개·인계를 요청할 때 활성화한다. 단일 코드 수정, 스펙·테스트 구현, 한 작업 안의 RPI 루프, 개인 일정, build/test 명령 관리에는 기본적으로 개입하지 않는다.
- 기존 tracker가 이미 충분한 판단을 제공하면 반복 절차·상태 파일을 추가하지 않는다. 독립 가치는 불완전한 증거, 다양한 도구, 세션 경계에서 실행 가능한 다음 작업을 안전하게 판단하는 데 있다.

### Work Item and State

- Work Item은 고정 schema가 아닌 기존 issue/task/PR 등 원본 객체의 **참조 단위**다. Issue와 소프트웨어 변경 사이에 1:1 관계를 강제하지 않는다.
- 정본 상태·우선순위·담당자·의존 관계는 원본 tracker가 소유한다. Skill의 `ready / blocked / unknown`은 이번 판단의 임시 결과이지 provider에 기록하는 별도 상태가 아니다.
- 실행 가능성 판단은 실제 blocker·권한·프로젝트 제약을 먼저 고려한다. 실행 가능한 후보 사이에서만 기존 우선순위·긴급도·목표로 다음 작업을 선택한다. 확인되지 않은 선행 작업이 있으면 `ready`를 확정하지 않는다.
- 이전 대화나 인계 문서는 단서일 뿐 재개의 정본이 아니다. 최근 상태, 남은 blocker, 계정·권한을 다시 조회한다. 별도 `tasks.json` 또는 중복 백로그를 생성하지 않는다.

### Execution Boundary

1. 사용자 목표, 작업 집합, 프로젝트의 원본 tracker와 요청된 읽기·쓰기 범위를 확인한다.
2. 실제 연결 계정·명의·허용된 도구 액션·권한을 확인한다. 플랫폼 native 기능과 현재 plugin/CLI가 실제 노출하는 기능을 구별한다.
3. 선택에 필요한 후보 및 중요한 의존 관계만 현재 조회해 ready/blocked/unknown을 구분한다. 데이터가 부족하면 조건부 권고로 남긴다.
4. 요청된 작업 분해·선택·상태 갱신을 가능한 native 도구로 수행한다. 쓰기 전 객체·계정·중복·부작용·승인 조건을 확인한다. 하위 이슈/의존성 API가 없으면 조작을 완료한 것으로 표시하지 않는다.
5. 기본 출력은 다음 작업과 이유, 막힌 요소·미확인 요소, 다음 행동이다. 인계가 필요할 때만 기존 객체 링크와 마지막 확인 근거를 추가한다. 영속 문서 생성은 강제하지 않는다.
6. 재개 시 원본과 비교하여 오래된 판단을 교체한다. 관찰한 것, 추론한 것, 실행한 것, 실패·미검증을 분리한다.

### Ownership and Portability

- Work Management는 **작업들 사이**의 선택·연결·진행을 다룬다. `mols-spec-stdd`와 실행 workflow는 **각 작업 안**의 명세·테스트·구현을 다룬다. 두 Skill은 서로 필수 의존성이 아니다.
- 외부 프로젝트의 자체 workflow, 다른 provider, 로컬 CLI 없는 환경을 고려하되 해당 저장소 하네스·연결·설치 도구를 숨은 전제로 요구하지 않는다.

### Verification and Deferrals

- Design Tests 1–7로 활성화/비활성화, blocker 우선, multi-mapping, 새 세션 재조회, 지정 계정 준수, tracker 부재, near-miss를 평가한다. native 도구만 사용한 기준선과 불필요한 파일·호출·절차를 비교한다.
- 구조적 검증, 책임·activation의 semantic review, 실제 runtime 행동 평가는 별개로 기록한다. 실제 실행이 없으면 통과로 보고하지 않는다.
- 자체 스케줄러·영속 상태·provider registry·양방향 동기화·범용 CLI·복잡한 상태 머신은 실패 사례가 정당화할 때까지 보류한다.
