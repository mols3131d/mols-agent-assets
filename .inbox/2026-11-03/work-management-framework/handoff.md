---
description: 개인용 통합 Project Workflow Skill을 신규 구현하고 구 Spec Skill을 정리하는 실행 계획입니다.
---

# Personal Project Workflow — Implementation Plan

## Outcome

PR #284에서 **`mols-stdd` Skill 하나로 작업 관리 + Spec/Test-driven 개발**을 제공한다. 개인 토이 프로젝트를 대상으로 하며 **레거시 호환성·기존 데이터 자동 이관·병행 지원은 범위 밖**이다.

사용자 지정 Task/Spec 디렉터리와 Git ref, 사람 중심 Markdown, 가벼운 ready 판단·세션 재개, 변경 delta → 계층형 도메인 스펙 반영과 검증 안전성을 구현한다. 구 `mols-spec-stdd`는 **필요한 동작의 참고 원본**이지 그대로 복사할 패키지가 아니다. 상세 설계는 [Design](design.md)이 소유한다.

**현재 상태:** `mols-stdd` 원본·부트스트랩·기본 흐름을 작성하고 최신 `main`을 반영했다. 구 `mols-spec-stdd` 원본·템플릿·스크립트·테스트를 제거하고 평가 사례·route·유지보수 문서를 새 이름에 맞췄다. 실제 모델 행동 평가, 다중 ref 실사용 및 머지는 미완료다.

## Execution Order

| 순서 | 작업 | 완료 판단 |
| --- | --- | --- |
| 1. 기준점 정리 | 최신 `main`과 PR 브랜치를 동기화하고 현재 Spec 관련 source를 확인 | 기존 PR 계획 보존, 필요한 현재 원본을 같은 ref에서 조회 가능 |
| 2. 단일 진입점·기본 흐름 | `SKILL.md`와 `references/default-workflow.md` 초안 작성. Prepare → RPI → Finalize로 모드 선택·Review 복귀·종료 판단을 구현하고 다듬음 | 원본 작성 완료, 정적 검사는 PR Gate 근거로 판정 |
| 3. 작업 관리 | 사용자가 정한 task directory/ref에서 파일 식별·의존 관계·ready/blocked/unknown·상태·재개 구현 | Markdown만으로 직접 읽고 수정 가능; 별도 task branch 지원 |
| 4. Spec 기능 | `changes/` delta, 계층형 `specs/`, 필요에 따른 테스트·구현·Review 복귀, 근거·baseline 확인 후 정본 반영 구현 | 기존 패키지 형식에 종속되지 않고 안전한 스펙 변경 가능 |
| 5. 정리·검증 | 필요한 테스트·행동 사례를 새 계약 기준으로 작성하고, 구 Skill의 원본·불필요한 resources·문서·route·eval·tests 제거/갱신 | **새 Skill 하나**가 발견되고 현재 문서·참조가 일치; 검증 결과 확인 |

단계 4에서 기존 `store.py`의 로직을 참고할 수는 있지만 전체 스크립트를 기본 이관하지 않는다. 반복적으로 발생하는 위험을 줄일 때만 작은 deterministic helper를 추가한다. 포괄적인 템플릿·Registry·JSON Workflow 엔진이나 해당 테스트를 그대로 옮기는 일은 하지 않는다.

## Bootstrap — Newly Added

- **작성 원본:** `src/rulesync/.rulesync/skills/mols-stdd/references/bootstrap.md`, `SKILL.md`에서 신규 프로젝트의 최초 설정에 한해 로드.
- **절차:** 기존 정본 탐색 → Task/Spec 사용 여부 결정 → 사용자 지정 `repository/ref/root` 선택 → 필요한 첫 파일만 생성 → ref별 재조회와 위치·다음 작업 보고.
- **디렉터리:** Task는 선택한 root 아래 작업별 Markdown, Spec은 선택한 root 아래 `changes/` 및 `specs/`. 두 영역은 같은 브랜치 또는 서로 다른 브랜치에서 관리 가능.
- **검증 대상:** 위치 미지정, 기존 owner가 있는 프로젝트, 단일 Task 첫 파일, Spec-only 시작, 별도 Task ref, 권한·참조 누락, 빈 저장소. 평가 fixture 작성 완료. 실제 모델 행동 평가는 미실행.

## Default Workflow — Newly Created

- **작성 원본:** `src/rulesync/.rulesync/skills/mols-stdd/SKILL.md`와 [Default Workflow](../../../src/rulesync/.rulesync/skills/mols-stdd/references/default-workflow.md). 별도 JSON workflow engine이 아니다.
- **진입 조건:** 다단계 개발·반복 검토에서만 상세 흐름을 읽는다. Task-only 목록 조회나 작은 단일 수정에는 별도 루프·계획 문서·Spec 파일을 강제하지 않는다.
- **기준 흐름:** Prepare(목표·저장 위치·권한·ready 확인) → Research/Plan/Work/Review(필요한 단계만 복귀) → Finalize(Spec/Task 독립 완료 판정·인계).
- **`mols-loops` 관계:** 범용 Skill은 수정하지 않고 개인용 프레임워크에 필요한 단계 원칙만 적용했다. 둘 다 선택되면 외부 조율을 중복 수행하지 않는다.
- **남은 검증:** 실제 사용자 프로젝트의 다른 ref에서 파일 갱신·Spec delta 흡수, 모델 라우팅·행동 평가. 기존 Skill 원본/route 정리는 완료되었으며 평가 fixture 존재만으로 모델 실행이 검증되지는 않는다.

## Explicitly Drop

- 구 Skill 이름/파일 레이아웃을 지원하는 alias, 호환 layer, 데이터 migration, deprecation stub, 다중 버전 지원
- `artifacts.json`, 8단계 Workflow JSON, `flow.py`, 형식만 위한 proposal/research/plan/test-design 템플릿
- Task/Spec의 N:M 관계 모델, 교차 브랜치 자동 완료·흡수, 상태 cache/index/dashboard
- Beads/Dolt/DB·MCP·서버, 작업 claim/lock, scheduler, 필수 Git 원격·PR 생성
- 필수 `.work/`·`spec/` 경로, 모든 일상 작업의 파일 등록, 자동 archive

**드랍하지 않을 핵심:** delta와 도메인 정본 구분, 계층형 도메인, 근거 없는 완료/흡수 차단, 오래된 정본 덮어쓰기 방지, 필요한 단계만 재검토하는 Review.

## Verification

| 시나리오 | 수락 조건 |
| --- | --- |
| Task-only | 서로 다른 위치의 작업 5개, 선행·취소·누락·순환 참조 처리, 다음 작업·중단·재개 |
| Spec-only | 작업 파일을 추가하지 않고 변경 delta를 도메인 정본으로 안전하게 반영 |
| Combined | 작업 기록에서 spec change를 링크하되 두 객체의 상태를 중복 관리하지 않음 |
| Different refs | task·spec·code가 서로 다른 ref여도 실제 선택한 위치에만 쓰고 미조회 ref로 대체하지 않음 |
| Human readability | 의미 있는 제목·파일명·핵심 완료 조건/다음 행동으로 사람이 쉽게 분류·이해 |
| Simple edit | 불필요한 skill activation·spec/task 기록·8단계 절차 없음 |
| Safety | stale baseline, write conflict, 미실행 테스트, 권한 부족을 PASS·완료로 처리하지 않음 |

검증은 구조/링크·필수 정본 갱신의 **결정적 검사**, Skill 설계·가독성 **의미 리뷰**, 실제 환경에서의 **행동 평가**를 구별한다. 설치·호환성·실제 런타임 평가는 수행한 근거만 보고한다.

## Closure

구 `mols-spec-stdd`의 삭제는 **동일 PR에서 새 통합 Skill 작성 후 수행했다**. 구 이름의 외부 소비자까지 호환되게 유지하려는 별도 작업은 하지 않는다. 다만 저장소에 남은 잘못된 route·문서·테스트 참조는 삭제 범위에 포함해 정리한다. 생성 결과물과 lock은 정본인 척 수동 수정하지 않는다.

구현에 착수할 때는 최신 head·base, 프로젝트 하네스와 실제 GitHub 계정·쓰기 권한을 확인한다. 브랜치 동기화와 구 자산 정리는 수행했다. 실제 모델 행동 평가와 다중 ref 실사용은 별도로 검증해야 한다.
