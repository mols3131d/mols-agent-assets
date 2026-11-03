---
description: 개인용 통합 Project Workflow Skill을 신규 구현하고 구 Spec Skill을 정리하는 실행 계획입니다.
---

# Personal Project Workflow — Implementation Plan

## Outcome

PR #284에서 **`mols-project-workflow` Skill 하나로 작업 관리 + Spec/Test-driven 개발**을 제공한다. 개인 토이 프로젝트를 대상으로 하며 **레거시 호환성·기존 데이터 자동 이관·병행 지원은 범위 밖**이다.

사용자 지정 Task/Spec 디렉터리와 Git ref, 사람 중심 Markdown, 가벼운 ready 판단·세션 재개, 변경 delta → 계층형 도메인 스펙 반영과 검증 안전성을 구현한다. 구 `mols-spec-stdd`는 **필요한 동작의 참고 원본**이지 그대로 복사할 패키지가 아니다. 상세 설계는 [Design](design.md)이 소유한다.

**현재 상태:** Draft / 설계·계획만 반영. PR 브랜치는 `main`과 분기되어 기존 Spec source가 포함되지 않았다. 구현·테스트·기존 자산 제거·머지는 수행하지 않았다.

## Execution Order

| 순서 | 작업 | 완료 판단 |
| --- | --- | --- |
| 1. 기준점 정리 | 최신 `main`과 PR 브랜치를 동기화하고 현재 Spec 관련 source를 확인 | 기존 PR 계획 보존, 필요한 현재 원본을 같은 ref에서 조회 가능 |
| 2. 단일 진입점 | `src/rulesync/.rulesync/skills/mols-project-workflow/SKILL.md` 신설, task-only/spec-only/combined/단순 수정 분기 | 요청과 무관한 자료·파일·개발 단계는 만들거나 로드하지 않음 |
| 3. 작업 관리 | 사용자가 정한 task directory/ref에서 파일 식별·의존 관계·ready/blocked/unknown·상태·재개 구현 | Markdown만으로 직접 읽고 수정 가능; 별도 task branch 지원 |
| 4. Spec 기능 | `changes/` delta, 계층형 `specs/`, 필요에 따른 테스트·구현·Review 복귀, 근거·baseline 확인 후 정본 반영 구현 | 기존 패키지 형식에 종속되지 않고 안전한 스펙 변경 가능 |
| 5. 정리·검증 | 필요한 테스트·행동 사례를 새 계약 기준으로 작성하고, 구 Skill의 원본·불필요한 resources·문서·route·eval·tests 제거/갱신 | **새 Skill 하나**가 발견되고 현재 문서·참조가 일치; 검증 결과 확인 |

단계 4에서 기존 `store.py`의 로직을 참고할 수는 있지만 전체 스크립트를 기본 이관하지 않는다. 반복적으로 발생하는 위험을 줄일 때만 작은 deterministic helper를 추가한다. 포괄적인 템플릿·Registry·JSON Workflow 엔진이나 해당 테스트를 그대로 옮기는 일은 하지 않는다.

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

구 `mols-spec-stdd`의 삭제는 **동일 PR에서 통합 Skill 및 새 검증 계약 완성 후** 수행한다. 구 이름의 외부 소비자까지 호환되게 유지하려는 별도 작업은 하지 않는다. 다만 저장소에 남은 잘못된 route·문서·테스트 참조는 삭제 범위에 포함해 정리한다. 생성 결과물과 lock은 정본인 척 수동 수정하지 않는다.

구현에 착수할 때는 최신 head·base, 프로젝트 하네스와 실제 GitHub 계정·쓰기 권한을 확인한다. 이번 계획 수정으로 Skill 구현, 브랜치 병합 또는 구 자산 삭제를 수행했다고 주장하지 않는다.
