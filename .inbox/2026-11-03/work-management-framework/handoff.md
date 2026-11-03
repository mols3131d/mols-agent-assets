---
description: 소규모 프로젝트용 파일·Git 기반 Work Management Skill의 구현 범위와 검증·인계 조건을 정리합니다.
---

# Work Management — Handoff

## Goal and Current State

**개인 토이 프로젝트와 국지적 개발 작업을 위한 경량 Work Management Skill**을 구현한다. Beads의 dependency-aware ready queue와 세션 간 재개 원칙은 참고하되, Beads 자체나 Dolt/CLI/MCP를 설치하거나 복제하지 않는다.

PR #284의 현재 단계는 **설계 완료·Skill 미구현**이다. 확정한 설계와 예시는 [Design](design.md)에 둔다. `.inbox/`는 작업 근거이며 Skill의 실행 정본이 아니다.

## Implementation Boundary

- 재사용 작성 원본 후보: `src/rulesync/.rulesync/skills/mols-work-management/SKILL.md`, 초기에는 **단일 Skill 파일**.
- 프로젝트가 파일 기반 관리를 채택한 경우, 기존 작업 루트를 우선하고 없으면 `.work/<id>.md`를 제안한다. 파일명은 안정적 ID이며 파일 하나가 작업 상태의 정본이다.
- 데이터 필드는 제목, `status: todo | doing | done | cancelled`를 기본으로 한다. `depends_on`, 우선순위, 완료 조건·다음 행동은 필요할 때만 기록한다.
- 선행 작업이 완료된 `todo`만 ready, 미완료/취소된 선행 작업·외부 차단은 blocked, 누락·순환·조회 불가는 unknown. `doing`은 재개 대상으로 별도 취급한다.
- 작업 발견·선택·분해·상태 변경·짧은 중단 메모·재개를 지원한다. 단일 수정과 한 작업 내부 개발 과정에는 과잉 활성화하지 않는다.
- Git은 변경 이력/브랜치/충돌 확인에만 재사용하고, 작업별 branch·commit·PR이나 외부 호스트를 강제하지 않는다. Git이 task lock이라고 가정하지 않는다.
- 허용된 파일 작업 도구가 없으면 읽거나 쓴 것으로 주장하지 않는다. 원격 쓰기 전 현재 연결 계정·명의·권한·ref를 확인하고 임의 전환하지 않는다.

**초기 구현에서 제외:** DB, daemon, scheduler, provider adapter, 별도 인덱스·일지·아카이브, 프로젝트 전체 작업 단계, Beads의 claim/gate/molecule/formula, 다중 에이전트 조정 체계, 자동 마이그레이션. `mols-spec-stdd`는 독립적인 기존 Skill이며 이 Skill의 실행 전제가 아니다.

## Acceptance

1. 작은 작업 5개로 선행 의존성과 우선순위에 따른 다음 작업 선택을 설명할 수 있다.
2. blocked/unknown을 ready로 잘못 올리지 않고, 중복 ID·누락·순환을 인지한다.
3. 중단 후 다음 세션에서 `doing` 기록과 실제 파일·Git 상태를 재확인할 수 있다.
4. 같은 작업을 다른 ref에서 수정한 경우 동시성 보장을 과장하거나 무단 덮어쓰지 않는다.
5. CLI·Git 원격 없이 허용된 파일 읽기/쓰기만으로 사용 가능하고, 기능 제한을 정직하게 보고한다.
6. 단일 버그, 개별 스펙/테스트, build/task runner 요청에는 자동 개입하지 않는다.
7. 단일 Skill·최소 파일 수를 유지하며 구조 검증, 의미 리뷰, 실제 행동 평가의 근거 수준을 구분한다.

## Next Work

1. `mols-agent-asset`의 Skill 설계·검증·평가 절차로 하나의 `SKILL.md`를 작성한다.
2. 위 7개 사례를 대상으로 과도한 필드·의무 절차를 제거하는 개선 검토를 수행한다.
3. 작성 원본 변경 시 유지보수 문서 영향과 발견/배포 경로를 검토한다. 현재 Inbox 설계만으로 정본 문서 작업이 완료된 것으로 보지 않는다.
4. 검증 결과와 미검증 항목을 PR 설명에 반영한다. 머지는 별도 권한과 조건에 따른다.
