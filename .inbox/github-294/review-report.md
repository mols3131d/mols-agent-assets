# PR #294 — 생성 파일 자동 동기화 정적 리뷰 보고서

> 2026-11-10 검토 스냅샷. 이 문서는 PR 작업을 위한 비정본 검토 근거이며, GitHub Actions·CI 정책·Ruleset을 대체하지 않는다.

## 결론

**수정 후 재검토 권고 / Draft 유지.** 구현은 기존 generator를 재사용하고 쓰기 워크플로를 PR Gate와 분리하지만, 브랜치 전용 실행 조건의 누락 1건과 자동 커밋 후 필수 체크 공백 1건이 남아 있다. 사람의 독립 승인 및 신규 워크플로 E2E는 아직 확보되지 않았다.

- 대상: [PR #294](https://github.com/mols3131d/mols-agent-assets/pull/294) (`mols3131d/mols-agent-assets`).
- 검토 기준: base `fa5be3bd63e9c29c30017b9e8c833018c092b9a7`, head `0e9905b3f3ceb4ce8a4b76453471ee4d358294ff`. 후속 커밋이 생기면 최신 diff·check를 다시 확인한다.
- 검토 표면: [generated-sync.yml](../../.github/workflows/generated-sync.yml), [generator](../../scripts/generated_artifacts.py), [PR Gate](../../.github/workflows/pr-gate.yml), [CI 정책](../../docs/development/ci.md), [GitHub 정책](../../docs/development/github.md), Ruleset `protect-main`.

## Findings

### F1 — High: 자동 커밋 직후 최신 PR Gate 근거 공백 (기존에 알려진 제한)

- 위치: `generated-sync.yml` 62–73행; 관련 운영 결정은 [review-brief.md](review-brief.md)에 기록되어 있다.
- 원인: 워크플로가 기본 `GITHUB_TOKEN`으로 생성 파일을 push해도 일반적인 후속 `push` workflow run은 발생하지 않는다. 이미 열린 PR에서 해당 bot commit 직후 `PR Gate`가 최신 후보를 다시 검증했다고 간주할 수 없다.
- 영향: source push를 받은 검사 결과가 이후 bot commit의 최종 merge candidate를 검증하지 못할 수 있다. 해당 커밋의 required check를 실제 조회해야 한다.
- 구분: 구현이 이 제약을 숨기지는 않는다. 현재 P0 설계는 **최초 PR 생성 전에 bot commit 완료**를 기본 경로로 하고, 기존 PR의 후속 변경은 사람의 승인된 정상 push로 재검증하는 제한적 자동화를 택했다.
- 처리: 코드 수정 없이도 운영 제약을 명시적으로 수용할 수 있으나, 수용 주체가 이를 결정해야 한다. 완전 무인 동기화·검증이 필수라면 현 설계로 완료 처리하지 말고 별도 설계 변경을 요청한다.
- 근거: [GitHub — Triggering a workflow](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow), [Required status checks](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks).

### F2 — Medium: 수동 dispatch에서 태그 ref를 브랜치로 오인할 수 있음 (수정 완료)

- 위치: `generated-sync.yml` 19, 30, 72행.
- 원인: `workflow_dispatch`는 브랜치뿐 아니라 태그를 대상으로 실행할 수 있다. 수정 전 job 조건 `github.ref != 'refs/heads/main'`은 `refs/tags/*`도 허용했으며, `git push origin "HEAD:${GITHUB_REF_NAME}"`는 브랜치 전용 대상임을 명시하지 않았다.
- 수정 내용: job 실행 조건에 `startsWith(github.ref, 'refs/heads/')`를 추가하여 `startsWith(github.ref, 'refs/heads/') && github.ref != 'refs/heads/main'`으로 변경하고, push 대상은 `HEAD:refs/heads/${GITHUB_REF_NAME}`으로 브랜치 ref를 명시했다.
- 확인: 브랜치(main 제외)만 실행, main·태그는 skip. 변경이 없으면 commit/push 생략. 로컬 정적·결정적 검증(mise check, mise test, generated_artifacts validate --all) 통과.
- 근거: [GitHub — workflow_dispatch 이벤트](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#workflow_dispatch), [GitHub — Contexts](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts).

### G1 — 필수 승인 게이트: 쓰기 가능한 Actions 통제 표면

- `permissions: contents: write`를 사용하는 신규 workflow이므로 [GitHub 정책](../../docs/development/github.md)에 따라 사람의 독립 검토와 명시적 승인이 필요하다.
- 기존 `Branch Check`·`PR Gate` 통과나 AI 정적 리뷰를 사람 승인 또는 write-path E2E 성공으로 대체하지 않는다.
- `main` 직접 수정, Ruleset bypass, 강제 push, 추가 계정·PAT·Secret 도입은 현 범위에 포함하지 않는다.

## 검증 근거

| 검증 항목 | 기준 스냅샷 결과 | 한계 |
| --- | --- | --- |
| [Branch Check](https://github.com/mols3131d/mols-agent-assets/actions/runs/42529764845/job/128881154510) | Pass — head `0e9905b3` | 정적·deterministic 검증에 한정 |
| [PR Gate](https://github.com/mols3131d/mols-agent-assets/actions/runs/42529769819/job/128881169458) | Pass — head `0e9905b3` | 새 write workflow의 생성·push 동작을 증명하지 않음 |
| 생성 경로·generated-only stage·no-op 분기 | 정적 코드 대조 | 실제 bot commit 없음 |
| 원본 변경 → 생성 파일 bot commit → 최신 PR Gate | Not Verified | 별도 실행·체크 관찰 필요 |
| 태그 dispatch 차단·경합·복구 | Not Verified | 수정·승인 후 검증 필요 |
| 사람의 독립 승인 | Not Verified | 병합 전 필수 |

## 유지할 설계와 범위

- 기존 `scripts.generated_artifacts sync`와 `validate --all`을 재사용하며 생성기의 의미를 YAML에 복제하지 않는다.
- `Branch Check`·`PR Gate`는 읽기 전용 검증, `generated-sync.yml`만 유지보수 write를 담당한다.
- 생성 결과만 stage하고 diff가 없는 경우 커밋하지 않는다. 별도 자동화, App/PAT/Secret, Ruleset 변경, 자동 병합을 추가하지 않는다.
- source path filter와 실제 source-to-projection mapping의 대응은 구현 후 다시 확인하되, 새로운 범위 확대는 별도 근거가 있을 때만 진행한다.

## 코딩 에이전트 인계

실행 순서, 완료 조건, 안전 경계는 [handoff.md](handoff.md)의 **2026-11-10 코딩 에이전트 작업 지시**를 따른다. 다른 검토자가 판단할 수 있도록 코드 수정과 검증 결과(HEAD, check/run URL, 미검증 항목)를 PR에 남긴다. 이 보고서의 판정은 해당 head 스냅샷에만 유효하다.
