---
description: PR #283의 Spec/Test-driven Skill 설계·구현 근거와 범위, 결정 및 후속 검증 항목을 확인합니다.
---

# Software Spec Framework — Implementation Record

## Scope Decision

소프트웨어 변경의 명세·테스트·구현 정합성과 Review 기반 재작업은 이 Skill이 맡는다. 작업 분해, 여러 작업의 우선순위·의존성·진행·재개는 **별도 Work Management Skill PR #284**로 인계했다. 둘은 독립적으로 선택·설치되며 상호 호출이나 서로의 상태 저장소를 필수로 하지 않는다.

기본 워크플로 후보는 사용자가 제안한 **Proposal → Research → Plan → Specification → Test Design → Test Implementation → Code Implementation → Review**의 8단계이다. Review가 근거에 따라 해당 단계로 돌아가고 다시 검증한다. 단, 작은 변경에는 8개 문서와 단계를 강제하지 않는다.

## Implemented Design

- 단일 Skill의 작성 원본: `src/rulesync/.rulesync/skills/mols-software-spec/`.
- **Artifact Registry** `assets/artifacts.json`: 문서 5종과 코드 산출물 2종을 정의. Review는 활동이므로 artifact가 아니다.
- **Workflow** `assets/workflows/default.json`(8단계), `focused.json`(명세·구현·리뷰). 단계 순서와 `after` 의존성만 소유한다.
- **Skill과 references:** 활성화·명세·테스트 실행·Review 재확인 절차를 정의한다. 프로젝트의 기존 스펙 정본과 도구를 우선한다.
- **Bundled script:** `flow.py validate`, `flow.py route --review report.json`의 읽기 전용 결정적 subset. pass는 candidate로만 반환하며 실제 테스트/CI 실행과 구분한다.
- **Tests:** 기본·간소화 워크플로 검증, 잘못된 순서/참조 거부, 단일·여러 finding 복귀, PASS/BLOCKED 근거 경계 등을 다룬다.
- **Eval fixtures:** `evals/skills/mols-software-spec/cases.json`에서 선택·비선택 및 Review/기존 스펙 정본/ChatGPT 실행 제약 행동 사례를 정의한다. 실제 모델 실행 결과는 아직 없다.

초기 Draft는 스크립트 전체가 CLI 없는 ChatGPT Chat에서 실행될 것이라고 가정하지 않는다. 실제 GitHub 연결에서 원본 Skill 리소스를 읽고, 승인된 파일을 변경하며, 필요할 때 수동 전이 판정을 구현하는 경로와 **완전한 원본 스크립트 실행**을 구분한다.

## Design Tradeoffs

- **중복 상태 미생성:** 독립 task tracker/진행 DB, 자체 문제 관리 큐, 별도 스펙 sync service는 구현하지 않았다.
- **검증 범위 보수적:** `after` 의존 관계의 downstream을 재확인 후보로 반환하지만 모든 산출물 재작성·실패를 강제하지 않는다.
- **기본 test-first:** 코드보다 테스트 구현을 먼저 하는 기본값을 제공하되, 기존 프로젝트의 테스트·코드 상태와 사용자 선택에 따라 focused 워크플로 사용 가능.
- **계획서의 잠정성:** 기본 순서는 사용자 제안을 존중하나, 스펙보다 먼저 작성된 Plan을 최종 구현 계약으로 오인하지 않는다.
- **OpenSpec과 공존:** OpenSpec의 별도 canonical store를 만들거나 공식 CLI 결과와 동일하다고 주장하지 않는다.

## Review and Next Validation

1. 변경된 구조의 JSON 및 Python 테스트를 실행하고, `mols-agent-asset`의 Skill review/validate 기준으로 activation·portable context·리소스 연결을 검토한다.
2. `mise run rulesync-validate`, `mise run generated sync/validate` 등 저장소 정책의 정본 도구가 필요한지 확인한다. Chat GitHub Plugin만으로 실행하지 못하면 미검증으로 기록한다.
3. **Runtime dogfood 미완료:** 실제 외부 샘플 프로젝트의 8단계 작업 한 건, Specification 결함→테스트·코드 재확인, test assertion 오류→test stage 복귀, 작은 변경의 경량 경로, 연결 읽기 전용/스크립트 미지원, 새 Chat 세션에서 최신 ref 재조회가 필요하다.
4. 필요 시 README·참조·스크립트에 최소 수정한다. 실제 결함 없이 별도 CLI 제품·복잡한 상태 엔진·템플릿 수를 늘리지 않는다.

이 문서는 Draft PR의 작업 근거로, Skill이나 소비 프로젝트의 정본 실행 계약이 아니다.
