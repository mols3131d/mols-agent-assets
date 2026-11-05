---
description: mols-stdd의 Change 중심 설계와 실행·검증 경계를 유지보수할 때 참고합니다.
---

# Mols STDD — Maintainer Notes

실행 정본은 [SKILL.md](../../../src/rulesync/.rulesync/skills/mols-stdd/SKILL.md), [Bootstrap](../../../src/rulesync/.rulesync/skills/mols-stdd/references/bootstrap.md), [Workflow](../../../src/rulesync/.rulesync/skills/mols-stdd/references/default-workflow.md)가 소유한다.

## Design Decision

Task와 Spec을 독립 객체·모드로 구분하면 같은 개발 변경의 상태와 종료 판단이 분리된다. 따라서 **Change ID 하나, 진행 상태 하나, 완료 gate 하나**로 통합했다. `work.md`는 작업 의존·상태·재개를 소유하고, 필요할 때 같은 ID 아래 명세 delta를 작성한다. 검증된 요구사항의 정본 반영은 해당 Change 완료 조건에 포함한다.

work/spec root와 Git ref 분리는 사용자 환경의 **저장 위치 선택**이지 서로 다른 객체·라이프사이클이 아니다. ref 간 원자적 쓰기가 없으므로 종료 시 실제 반영 상태를 검증한다. 부분 실패 후에는 이미 적용된 명세를 재적용하지 않는 **멱등적 재개**와 최신 `work.md` 재확인이 필요하다.

## Deliberate Omissions

별도 Task ID·상태 동기화·manifest·index·dashboard·작업 scheduler·Git lock은 없다. 행동 변경이 없으면 빈 Spec을 만들지 않고, 간단한 수정에는 Change 기록을 강제하지 않는다. `mols-loops`의 Prepare → RPI → Finalize만 로컬 판단 흐름으로 가져오고 오케스트레이터·외부 Skill 설치 의존성은 추가하지 않는다.

구 `mols-spec-stdd`의 JSON workflow, Python scripts, 형식용 템플릿과 테스트는 호환 이관하지 않았다. 명세·Review·baseline 안전성은 새 계약에 반영했다.

## Validation

[평가 사례](../../../evals/skills/mols-stdd/cases.json)는 단일 Change 상태, 의존·재개, 복수 도메인, 별도 Git ref, stale 정본, 불완전한 검증과 Skill 선택을 다룬다. 모델 평가 실행 진입점은 [Promptfoo 설정](../../../evals/promptfoo/mols-stdd.yaml)이며 `mise run eval -c evals/promptfoo/mols-stdd.yaml`로 호출한다. 실행 전 로컬 provider와 grader·비용·외부 전송 여부를 확인한다(`evals/README.md`). **이 설정은 `SKILL.md` 기반 단일 모델 응답 평가이며** 별도 reference 로딩, 도구 조작·실제 Git 작업·에이전트 런타임 실행의 증거가 아니다. 구조 CI 통과와 실제 모델 평가 통과를 혼동하지 않는다.
