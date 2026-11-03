---
description: 개인 개발용 통합 Project Workflow Skill의 설계 이유와 기본 워크플로 유지보수 기준입니다.
---

# Personal Project Workflow — Maintainer Notes

실행 계약은 [SKILL.md](../../../src/rulesync/.rulesync/skills/mols-project-workflow/SKILL.md)와 [Default Workflow](../../../src/rulesync/.rulesync/skills/mols-project-workflow/references/default-workflow.md)가 소유한다. 이 문서는 실행 지침을 복제하지 않고 변경 이유와 검증 기준만 기록한다.

## Decision

`mols-loops`는 범용 다단계 Run/Loop 조율자다. 이 프레임워크에서는 **Prepare → Research/Plan/Work/Review → Finalize**만 개인 개발의 공통 실행 흐름으로 차용한다. 별도 루프 상태 DB·카운터·workflow JSON·외부 Skill 설치는 필요하지 않다.

가벼운 Task-only 요청에서 Spec과 RPI 전체 절차를 로드할 이유가 없으므로, 진입점은 작업 모드·정본·안전 조건만 소유하고 다단계 개발에서만 Default Workflow를 읽는다. 범용 `mols-loops`가 같은 런타임에서 독립적으로 활성화되면 바깥 Run 조율을 중복하지 않는다.

## Bootstrap Decision

실제 최초 설정 절차는 [Project Bootstrap](../../../src/rulesync/.rulesync/skills/mols-project-workflow/references/bootstrap.md)가 소유한다. 설정 manifest·전용 CLI 대신 **사용자 지정 Task/Spec 디렉터리와 각 Git ref**, 필요한 첫 Markdown만 쓰도록 설계했다. 기존 프로젝트 지침이 위치를 소유하면 그 선택을 재사용한다. 빈 저장소에 가짜 작업을 만들지 않고, 경로가 미정이면 부트스트랩을 완료했다고 주장하지 않는다.

## Maintenance and Evaluation

- **Activation:** 단순 코드 수정은 불필요한 task/spec 생성을 일으키지 않아야 한다. Task-only/Spec-only/Combined 요청은 서로 필요한 파일만 선택해야 한다.
- **Work management:** 사용자 지정 task root·branch, 읽기 쉬운 Markdown, ready/blocked/unknown, 중단·재개를 확인한다.
- **Spec:** 계층형 delta→domain spec 반영, 검증 없는 promotion 및 stale baseline 거절을 확인한다.
- **Workflow:** Review finding이 올바른 근거 지점으로 돌아가는지, 불필요한 전 단계 재시작이나 문서 강제가 없는지 확인한다.
- **Tool boundary:** Git CLI 없는 GitHub 연결, 접근 불가 ref, task/spec/code 간 다른 ref, 쓰기 실패를 검증한다.

**현재 단계:** 기본 `SKILL.md`와 워크플로 reference만 초안으로 작성되었다. 기존 `mols-spec-stdd`의 실제 제거, 경로·route 정비, 정적/실행 테스트, 실사용 평가와 최신 `main` 동기화는 완료되지 않았다. 작성 원본의 존재를 배포·설치·행동 품질의 증거로 취급하지 않는다.
