---
description: mols-stdd의 Change 중심 설계와 실행·검증 경계를 유지보수할 때 참고합니다.
---

# Mols STDD — Maintainer Notes

실행 정본은 [SKILL.md](../../../src/rulesync/.rulesync/skills/mols-stdd/SKILL.md), [Bootstrap](../../../src/rulesync/.rulesync/skills/mols-stdd/references/bootstrap.md), [Workflow](../../../src/rulesync/.rulesync/skills/mols-stdd/references/default-workflow.md), [Dispatch](../../../src/rulesync/.rulesync/skills/mols-stdd/references/dispatch.md)가 소유한다.

## Design Decision

Task와 Spec을 독립 객체·모드로 구분하면 같은 개발 변경의 상태와 종료 판단이 분리된다. 따라서 **Change ID 하나, 진행 상태 하나, 완료 gate 하나**로 통합했다. Change의 단위는 파일이나 컴포넌트가 아니라 함께 검증·완료할 수락 결과로 정한다. `work.md`는 작업 의존·상태·재개를 소유하고, 필요할 때 같은 ID 아래 명세 delta를 작성한다. 검증된 요구사항의 정본 반영은 해당 Change 완료 조건에 포함한다.

기존 Work·Spec 정본은 먼저 소유권과 호환성을 확인한다. 별도 상태 정본을 중복 도입하지 않으며, 호환되지 않는 기존 Work는 명시적 정본 선택·이관 없이 자동 통합하지 않는다. 신규 도메인은 존재하지 않는 baseline을 가정하지 않는다.

work/spec root와 Git ref 분리는 사용자 환경의 **저장 위치 선택**이지 서로 다른 객체·라이프사이클이 아니다. ref 간 원자적 쓰기가 없으므로 종료 시 실제 반영 상태를 검증한다. 부분 실패 후에는 이미 적용된 명세를 재적용하지 않는 **멱등적 재개**와 최신 `work.md` 재확인이 필요하다. 최신 정본과 충돌하지 않는 변경도 기준·검증을 다시 확인해야 하며, 재개 위치는 별도 registry 없이 기존 프로젝트 문서나 Change 기록에서 찾을 수 있게 한다.

## Ticket and Agent Delegation

`Change`가 티켓이다. 발행은 `todo` 기록이며 실행은 별도 요청이다. `ready`는 선행 관계로 계산하고 선점·작업 승인으로 해석하지 않는다. Dispatch는 네이티브 실행 능력과 권한을 조건부로 이용하며, Worker의 응답은 독립 검증 근거가 아니다. 향후 담당 역할은 실행 가능 여부가 미확인된 계획으로 지정할 수 있지만 실제 위임 전에는 런타임·권한을 확인한다. 지속적인 할당 기록이 필요할 때만 `assignee`를 선택적으로 사용하며 lock이나 Claim으로 취급하지 않는다.

동시 실행은 런타임의 실제 작업 격리와 원자적 Claim 또는 단일 조정자의 직렬 할당이 필요하다. 환경이 지원하지 않는 병렬 선점은 강행하지 않고 가능한 범위만 수행하거나 인계한다.

## Progressive Disclosure

`SKILL.md`는 단일 Change 상태·Ready 판정·권한 및 완료의 공통 불변조건을 보유한다. Bootstrap은 **최초 설정과 이후 신규 Change 발행**, Workflow는 **선택된 Change의 직접 수행·재개·완료**, Dispatch는 **할당·위임·Worker 결과 회수**에만 조건부로 적용한다. 단순 백로그·Ready 조회는 reference를 선로드하지 않는다.

Change 데이터도 백로그의 ID·상태·의존 관계부터 확인하고 선택된 `work.md`를 심화한 뒤 관련 명세·코드·테스트를 필요할 때만 읽는다. 이 구분은 별도 index나 scheduler를 요구하지 않으며, 상세 절차는 실행 원본에서만 관리한다.

## Deliberate Omissions

별도 Task ID·상태 동기화·manifest·index·dashboard·작업 scheduler·Git lock·필수 `assignee` 필드는 없다. 행동 변경이 없으면 빈 Spec을 만들지 않고, 간단한 수정에는 Change 기록을 강제하지 않는다. `mols-loops`의 Prepare → RPI → Finalize만 로컬 판단 흐름으로 가져오고 오케스트레이터·외부 Skill 설치 의존성은 추가하지 않는다.

구 `mols-spec-stdd`의 JSON workflow, Python scripts, 형식용 템플릿과 테스트는 호환 이관하지 않았다. 명세·Review·baseline 안전성은 새 계약에 반영했다.

## Validation

[평가 사례](../../../evals/skills/mols-stdd/cases.json)는 Change 상태·의존·재개·완료와 조건부 reference 선택을 다룬다. [Native Trigger/Behavior](../../../evals/promptfoo/mols-stdd.yaml)는 `SKILL.md`만 사용해 Skill 선택과 응답 행동을 평가하며 reference 로딩 검사는 의도적으로 제외한다. [Reference Selection](../../../evals/promptfoo/mols-stdd-references.yaml)은 기존 Python provider로 선택한 reference 경로를 관찰하고 기대 집합과 비교한다. 두 실행은 각각 `mise run eval -c evals/promptfoo/mols-stdd.yaml`, `mise run eval -c evals/promptfoo/mols-stdd-references.yaml`이다.

Reference 평가에는 로컬 Ollama 모델이 필요하며 선택된 reference로 행동 응답을 구성하는 호출도 포함된다. 평가 실행 전 provider·grader·비용·외부 전송 여부를 확인한다(`evals/README.md`). **평가 harness의 `loaded_references` 기록은 실제 IDE/CLI Agent의 파일 조회·도구 실행을 증명하지 않는다.** 구조·fixture 검사와 실제 모델 평가도 구분한다.
