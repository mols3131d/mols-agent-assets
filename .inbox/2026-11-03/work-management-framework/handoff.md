---
description: 개인용 통합 Project Workflow Skill을 구현하기 위한 작업 순서, 검증 기준과 기존 Spec Skill 이관 조건입니다.
---

# Personal Project Workflow — Implementation Plan

## Goal and Current State

PR #284의 목표를 독립 Work Management Skill 생성에서 **`mols-project-workflow` 단일 Skill로 작업 관리 + Spec/Test-driven 개발을 통합**하는 것으로 변경한다. 대상은 개인 토이 프로젝트·소규모 개발이다. 작업만 필요한 경우 스펙을 강제하지 않고, 스펙만 필요한 경우 백로그를 강제하지 않는다.

**현재는 설계와 구현 계획만 완료한 Draft.** Skill source 변경, 기존 Spec 자산 이동·은퇴, 정적/실행 검증, PR 머지는 아직 수행하지 않았다. 현재 PR head는 `main`과 분기되어 있어 `mols-spec-stdd` 작성 원본이 없는 상태다. 최신 `main`을 먼저 통합한다. 설계의 의미·저장 모델은 [Design](design.md)을 따른다.

## Ordered Work

| 단계 | 작업 | 완료 기준 |
| --- | --- | --- |
| 0. 기준점 맞추기 | 최신 `main`을 PR branch에 안전하게 통합, 실제 diff·충돌 확인 | 기존 Spec Skill·테스트·유지보수 문서가 같은 ref에 보이고 기존 PR 문서가 보존됨 |
| 1. 소유권·이관 지도 | 기존 `mols-spec-stdd`의 entrypoint, references, templates, workflow JSON, Python scripts, tests, eval, docs, route/consumer 참조 조사 | 새 Skill로 **보존·단순화·은퇴**할 항목별 판정과 수정 범위 정리 |
| 2. 통합 패키지 | Rulesync 작성 원본 `src/rulesync/.rulesync/skills/mols-project-workflow/`에 **하나의 SKILL.md** 진입점과 조건부 Spec 자원 이동·정리 | task-only·spec-only·combined 요청이 서로 불필요한 단계·context를 강제하지 않음 |
| 3. 경량 작업 관리 | 사용자 지정 directory/task ref/code ref, 사람 중심 Markdown 파일·의존성·ready 판단·중단 재개 구현 | 외부 task DB/서비스 없이도 작은 작업을 관리, 별도 task branch에서 정확한 ref 사용 |
| 4. 정합성·최적화 | 기존 Spec 안전 계약, task→change 연결, 실제 소규모 예제를 리뷰하고 중복 문서·메타데이터 제거 | task `done`과 spec delta 흡수는 별도 근거로 판정; 핵심 Spec 기능 유지 |
| 5. 검증과 전환 | 기존 Spec deterministic tests, 새 task 케이스, routing/behavior eval, 문서·route·lock/소비자 영향 점검 | 이관 후 동작 근거 확보. 기존 `mols-spec-stdd`는 대체 가능성 확인 후만 은퇴, PR Ready 조건 보고 |

각 단계에서 실제 파일 수정 전 현재 branch·계정·권한을 확인한다. 별도 브랜치/commit/PR 생성, 작업별 문서 생성, 스크립트 실행을 무조건 강제하지 않는다. 이 표는 구현 우선순위이며 날짜·예상 소요 시간은 약속하지 않는다.

## Migration and Artifact Inventory

- **이전할 핵심:** `src/rulesync/.rulesync/skills/mols-spec-stdd/SKILL.md`, `references/{artifacts,spec-store,workflow}.md`, `assets/artifacts.json`, `assets/templates/`, `assets/workflows/`, `scripts/{flow,store}.py` 및 이에 결합된 테스트.
- **기존 검증 기반:** `tests/skills/mols-spec-stdd/`, `evals/skills/mols-spec-stdd/cases.json`. 새 이름으로 경로를 이전할 때 expectation과 import/path 참조를 함께 갱신한다. 기존의 task-priority **비활성화** case는 통합 Skill에서 **활성화**되는 사례로 바뀐다.
- **문서/발견:** `docs/skills/mols-spec-stdd/README.md`, `route/skills.jsonl`, 관련 유지보수/사용 문서·하네스의 참조를 범위 내에서 확인하고 이전한다. 생성 라우트·lock은 독립 정본으로 직접 편집하지 않는다.
- **중복 정본 금지:** 새 패키지를 완성하기 전 구패키지·문서를 제거하지 않고, 이전한 후에는 장기적인 중복 Skill 소유권을 남기지 않는다. 설치된 외부 소비자·권한을 확인할 수 없다면 구 Skill의 은퇴는 별도 후속 작업으로 넘긴다.
- **범위 제외:** Beads/Dolt 도입, DB·daemon·scheduling, 조직적 다중 에이전트 협업, Git remote 필수화, 프로젝트 전체에서 항상 적용하는 글로벌 workflow 정책.

## Acceptance and Test Scenarios

| 구분 | 확인할 동작 |
| --- | --- |
| Task-only | 사용자 지정 폴더·task branch에서 파일 생성/조회, 순위·의존·ready/blocked/unknown 판정. 스펙 산출물 없음 |
| Spec-only | task 파일 없이 계층 도메인 변경 delta, Review 복귀, stale baseline 거절, 완료 시 정본 흡수 |
| Combined | `Work Item ↔ Change ↔ Domain Spec`의 참조 연결. 하나의 작업이 여러 변경에, 하나의 변경이 여러 작업에 연결되어도 중복 상태 없음 |
| Small change | 단일 이름 변경·작은 버그 등은 task/spec 문서와 8단계 workflow를 강제하지 않음 |
| Human readability | 탐색기·에디터·Git diff에서 의미 있는 파일명·H1·목적·완료 조건·다음 행동을 명확히 인식 |
| Git/ref | task와 code/spec ref가 다를 때 각각 올바른 원본에서 읽고 씀. 읽을 수 없는 ref를 기본 branch로 자동 대체하지 않음 |
| Resume | 중단 후 최신 task 파일·code ref·spec 정본을 조회, 오래된 기록·경쟁 수정 확인 |
| Safety | `done`만으로 spec 흡수 금지, 리뷰 PASS만으로 task 완료 금지, 계정 전환·실행 증거 없는 완료 주장 금지 |
| Regression | `flow.py`/ `store.py`의 동작·테스트, 경로·route·eval fixtures·관련 문서 정합성 유지 |

정적 검증, 의미 검토, 실제 모델/도구 행동 평가는 별도 근거다. 실행하지 않은 CI·스크립트·ChatGPT Chat 호환성 검증은 PASS로 기록하지 않는다.

## Implementation Guardrails

- 사용자에게 task 저장 디렉터리와 필요시 task Git ref를 선택할 권한을 둔다. `.work/`·`spec/`를 **강제 생성하지 않는다**. 스펙의 `changes/`와 `specs/` 상대 구조는 spec root 안의 기존 기능으로 보존한다.
- 기존 `mols-spec-stdd`의 stale baseline, Review·정본 흡수·아카이브 보호 조건은 유지한다. 8단계 Default workflow는 모든 작은 변경의 필수 순서가 아니다.
- Skill의 가벼운 진입점이 일반적인 작업 관리와 스펙 작업을 선택하고, 복잡한 Spec 자료는 **필요한 경우에만 로드**한다. 소유권만 합쳤다는 이유로 전체 스펙 패키지를 매번 로드하지 않는다.
- GitHub 연결 등 실제 제공 도구의 능력·계정·쓰기 권한을 확인하고, 로컬 파일/Git CLI 접근을 임의로 가정하지 않는다.
- PR을 먼저 머지하거나 기존 스펙 Skill을 선삭제하지 않는다. 증거가 부족하면 Task 관리 기능만 먼저 평가하고 은퇴를 후속 조치로 남긴다.

## Immediate Next Action

**단계 0부터 시작한다.** 현재 PR branch와 `main`이 분기되어 있으므로 기존 Spec Skill과 최신 저장소 문서가 같은 ref에 있도록 통합 전략·충돌 범위를 확인한 뒤 implementation에 착수한다. 이미 기록한 인계·설계 텍스트는 보존한다.
