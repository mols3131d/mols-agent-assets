---
description: mols-stdd의 Change 중심 설계와 실행·검증 경계를 유지보수할 때 참고합니다.
---

# Mols STDD — Maintainer Notes

실행 정본은 [SKILL.md](../../../src/rulesync/.rulesync/skills/mols-stdd/SKILL.md), [Bootstrap](../../../src/rulesync/.rulesync/skills/mols-stdd/references/bootstrap.md), [Workflow](../../../src/rulesync/.rulesync/skills/mols-stdd/references/default-workflow.md)가 소유한다.

## Design Decision

Task와 Spec을 독립 객체·모드로 구분하면 같은 개발 변경의 상태와 종료 판단이 분리된다. 따라서 **Change ID 하나, 진행 상태 하나, 완료 gate 하나**로 통합했다. `work.md`는 작업 의존·상태·재개를 소유하고, 필요할 때 같은 ID 아래 명세 delta를 작성한다. 검증된 요구사항의 정본 반영은 해당 Change 완료 조건에 포함한다.

work/spec root와 Git ref 분리는 사용자 환경의 **저장 위치 선택**이지 서로 다른 객체·라이프사이클이 아니다. ref 간 원자적 쓰기가 없으므로 종료 시 실제 반영 상태를 검증한다.

## Deliberate Omissions

별도 Task ID·상태 동기화·manifest·index·dashboard·작업 scheduler·Git lock은 없다. 행동 변경이 없으면 빈 Spec을 만들지 않고, 간단한 수정에는 Change 기록을 강제하지 않는다. `mols-loops`의 Prepare → RPI → Finalize만 로컬 판단 흐름으로 가져오고 오케스트레이터·외부 Skill 설치 의존성은 추가하지 않는다.

구 `mols-spec-stdd`의 JSON workflow, Python scripts, 형식용 템플릿과 테스트는 호환 이관하지 않았다. 명세·Review·baseline 안전성은 새 계약에 반영했다.

## Validation

[평가 사례](../../../evals/skills/mols-stdd/cases.json)는 한 Change의 상태·명세 연결, 선행 의존·재개, 복수 도메인, 별도 Git ref, stale 정본, 불완전한 검증과 Skill 선택 경계를 대상으로 한다. **평가 자료를 작성한 것과 실제 모델 행동을 검증한 것은 다르다.** CI 구조 검사와 소비 프로젝트의 실행 검증도 구분한다.
