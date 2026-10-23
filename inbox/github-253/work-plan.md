# PR #253 — Review and Remediation Work Plan

## Goal and Scope

PR #253의 목표는 조사 보고서만 남기는 것이 아니라 **문서와 실제 정본의 확인 가능한 불일치를 고친 후 검증**하는 것이다. 대상은 `mols3131d/mols-agent-assets`이며 `main`이 아닌 PR head 브랜치에만 반영한다. 파일 삭제, 실행 자산 동작 변경, 역사 기록의 일괄 치환, 병합은 이 계획에 포함되지 않는다.

- PR: https://github.com/mols3131d/mols-agent-assets/pull/253
- 최초 재검토 기준: base `23d649b2eac6e9115ce0e97a823d59de4d37b3c5`, head `ff86e43b782e4fb24055b90d34275d425c66db0f`
- 당시 `main`: `7e595952aba994c46dd4c40cb95238c0eaf2b7f1` (PR과 기준이 달라 현재 `main`으로 검증을 대체하지 않음)

## Work Units and Durable Evidence

1. **Review:** [`review.md`](review.md)에 재현 가능한 근거, severity, 요구 조치, 범위·미확인 사항을 기록한다. 발견이 없는 영역을 전체 완료로 단정하지 않는다.
2. **Research:** [`consistency-evidence.md`](consistency-evidence.md)에 정본 ↔ 문서/경로 ↔ 사용·검증 관계를 기록한다. 기본 탐색은 역사적 이름, 현행 참조, 실제 링크, README inventory, CI 근거다.
3. **Implementation:** [`remediation-log.md`](remediation-log.md)에 finding별 수정 파일, 결정, 보존 제약, commit을 남긴다. 각 실제 변경 직후에 head와 보고서 근거를 대조한다.
4. **Validation:** [`validation.md`](validation.md)에 기계적으로 확인한 항목과 실행 불가능한 항목을 분리한다. GitHub PR Gate는 정확한 최신 head SHA의 완료 결과만 성공으로 기록한다.
5. **Handoff:** [`handoff.md`](handoff.md)에 마지막 확인 head, 현재 상태, 재개 방법, 열린 문제, 다음 조치를 작성한다.

## Acceptance Conditions

- 리뷰는 PR 자체의 품질과 원래 완료 목표를 구분한다.
- 확인된 오류는 가능하고 안전하면 같은 PR에서 수정하며, 수정하지 못한 항목은 미해결로 남긴다.
- 문서 원문·역사적 맥락·GitHub 자동 생성 anchor와 존재하는 직접 소비자를 함부로 깨지 않는다.
- PR에 존재하는 CI 결과는 근거일 뿐 의미 정합성 전체의 증명으로 보지 않는다.
- 사용자 승인 없이는 merge하지 않는다.

## Resumption Contract

새 세션에서는 `CHATBOT.md` → `AGENTS.md` → `.agents/route/ROUTE.md` 및 선택한 Skill과 이 계획을 확인한 뒤 **live PR head를 다시 조회**한다. `review.md`의 결함 목록, `remediation-log.md`의 완료 상태, `validation.md`의 최신 head 결과와 `handoff.md`를 교차 확인한다. 기록된 commit·CI를 새로운 head에 그대로 적용하지 않는다.

**Status:** work started; assessment and implementation outcomes are recorded separately, not assumed completed.
