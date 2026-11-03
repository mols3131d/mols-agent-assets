---
description: Git-native Work Management Skill 구현을 인계받을 때 범위·소유권·미완료 검증과 다음 작업을 확인합니다.
---

# Work Management — Handoff

## Objective and Status

**목표:** 파일 시스템의 Markdown 작업 파일을 정본으로 사용하고 Git으로 변경·협업·인계를 추적하는 **벤더 중립적 Work Management Skill**을 구현한다. 별도 task SaaS, GitHub Issues, Beads, DB, 서버가 없어도 기본 작업 관리가 가능해야 한다.

PR #284는 설계·인계 작업 단계의 Draft다. Skill 작성 원본과 동작 평가는 아직 없다. 현재 설계의 상세 모델과 시나리오는 [Design](design.md)을 따른다.

## Decisions

| Concern | Direction |
| --- | --- |
| 작업 상태 정본 | 소비 프로젝트가 채택한 작업 디렉터리의 개별 Markdown 파일 |
| 기본 저장 레이아웃 | 제안 기본값 `.work/items/<stable-id>.md`; 기존 지정 경로 우선 |
| 감사·변경·협업 | Git의 diff/commit/ref/merge를 재사용. Git 호스트는 불필요 |
| 에이전트 책임 | 발견·분해·선택·의존성·상태·중단·재개·인계 |
| 자체 저장 서비스 | 만들지 않음. 별도 index/cache/DB도 기본 생성하지 않음 |
| 외부 tracker | 필요한 경우 optional reference/integration이며 기본 상태 정본이 아님 |
| 작업 내부 개발 | 호출자 워크플로가 소유. `mols-spec-stdd`와 독립적으로 선택 가능 |

대상 프로젝트가 이미 다른 정본 시스템을 운영한다면 별도 파일 정본을 무단 도입하지 않는다. 이 Skill의 자체 파일 저장 방식은 **명시적으로 채택한 프로젝트**에 적용한다.

## First Implementation Scope

- `mols-work-management`를 재사용 Rulesync Skill의 **단일 작성 원본**으로 개발한다: `src/rulesync/.rulesync/skills/mols-work-management/SKILL.md`.
- 작은 파일 계약: 안정적 ID, `todo/doing/paused/done/cancelled`, 선택적 우선순위·선행 작업, 목표·완료 조건·진행 기록. `blocked` 및 `unknown`은 데이터로부터 판정한다.
- 새 작업 생성, 작업 분해, 실행 가능 작업 선택, 상태 전환, 중단 기록, 새 세션 재개의 간결한 동작을 정의한다.
- 실제 Git ref·파일 최신성을 확인한다. 브랜치 간 수정 충돌과 중복 작업을 탐지하며 Git이 분산 lock을 제공한다고 가정하지 않는다.
- Git/CLI/API가 없는 환경에서는 파일 기능만, 파일도 쓸 수 없으면 근거 기반 제안·인계만 한다. Git 작성 계정·명의 또는 연결을 임의로 바꾸지 않는다.
- 동작에 필요하지 않은 CLI, 서버, 외부 API, migration layer, 모든 작업의 강제 문서화는 도입하지 않는다. 반복 검증에서 필요할 때만 번들 스크립트를 고려한다.

## Acceptance

1. 파일 기반 5개 작업의 선행 관계·우선순위를 판정해 다음 작업을 결정한다.
2. 누락 참조, 순환 의존성, 중복 ID, 외부 차단 때문에 잘못된 `ready`를 주장하지 않는다.
3. 하나의 작업을 분해하거나 여러 스펙·코드 변경과 참조해도 중복 정본을 만들지 않는다.
4. 세션 중단·재개와 서로 다른 Git 브랜치의 stale/충돌 사례를 안전하게 처리한다.
5. GitHub 없는 로컬·Git 호스팅을 사용하는 환경·파일 접근만 가능한 ChatGPT 환경의 능력 차이를 보고한다.
6. 단일 코드 수정, 명세/테스트, build-task 명령에는 과잉 활성화하지 않는다.
7. deterministic validation, semantic review, 실제 runtime eval을 **서로 분리**해 결과를 보고한다. 실행하지 않은 검증은 PASS로 처리하지 않는다.

기존 도구를 직접 사용하는 방식 대비 추가 파일·호출·절차와 재개 성공을 비교한다. **이제 비교 기준의 중심은 외부 이슈 도구가 아니라 순수 파일+Git 작업 흐름**이다.

## Next Work

1. 현재 PR head/base, 루트 하네스와 `repository-agent-asset-workflow`, `mols-agent-asset`의 design/review/validate/eval 절차를 확인한다.
2. 작은 샘플 작업 파일로 ID·상태·의존 관계·Git 충돌 계약을 검토하고 필요 이상인 필드를 제거한다.
3. Skill source와 필요한 만큼의 최소 유지보수 문서를 구현한다. `.inbox/` 인계를 정본으로 오인하지 않는다.
4. Design 시나리오로 재검토·검증·행동 평가를 진행하고, 근거를 구분해 PR 본문을 갱신한다.
5. PR #283의 `mols-spec-stdd`는 이미 별도로 머지되었으며, 그 Skill의 산출물과 구현 코드를 이 PR로 복제하지 않는다.

작성 원본 변경 시 저장소 라이프사이클에 따라 **정본·유지보수 문서 영향**을 별도로 판정한다. 머지는 이 인계의 범위 밖이다.
