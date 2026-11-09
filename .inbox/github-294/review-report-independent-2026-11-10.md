# PR #294 — 독립 리뷰 보고서 (2026-11-10)

**판정: 조건부 보류 — Draft 유지.** 신규 workflow의 정적 구현에서 추가 확정 코드 결함은 찾지 못했다. 그러나 봇 커밋 후 필수 검증 공백, 쓰기 권한 승인, 신규 write 경로의 E2E 미검증이 남아 있어 현 상태로는 머지를 권장하지 않는다.

- 대상: [PR #294](https://github.com/mols3131d/mols-agent-assets/pull/294) · `mols3131d/mols-agent-assets`
- 리뷰 스냅샷: base `fa5be3bd63e9c29c30017b9e8c833018c092b9a7`, head `5a0c39101a3aa25ea4e302633302b9cc3501f47f`
- 변경: [`generated-sync.yml`](../../.github/workflows/generated-sync.yml) 1개와 `.inbox/github-294/` 문서 4개. 기존 generator, `Branch Check`, `PR Gate`, Ruleset 변경 없음
- 이전 [리뷰 보고서](review-report.md)는 이전 revision의 근거로 보존한다. 본 문서는 위 SHA의 **독립적인 읽기 전용 검토 스냅샷**이며, 보고서 추가 후의 새 head를 검증한 것은 아니다

## Findings 및 판단

### F1 · High · 미해결 — 봇 커밋 후 required PR Gate 검증 공백

[`generated-sync.yml`](../../.github/workflows/generated-sync.yml)은 `GITHUB_TOKEN`으로 생성 결과를 작업 브랜치에 `git push`한다. [`pr-gate.yml`](../../.github/workflows/pr-gate.yml)은 `pull_request` 이벤트에 반응하지만, 기본 토큰이 만든 일반적인 push는 후속 `push`/`pull_request` workflow를 재시작하지 않는다. 따라서 이미 열린 PR에 봇 커밋이 추가되면 **최신 PR 후보에 필수 check가 없을 수 있다**. 이전 SHA의 성공을 최신 커밋의 성공으로 해석하면 안 된다.

- **처분:** 현재 P0 운영안(`원본 push → 봇 커밋 완료 → 최초 PR 생성`)은 제한적 자동화로만 수용 가능하다. 이미 열린 PR에 대해서는 승인된 정상 후속 이벤트로 최신 SHA의 required check를 확인한다. 완전 무인화를 요구한다면 별도 설계 결정이 필요하다.
- **주의:** 2026년 GitHub의 토큰 기반 PR 생성·갱신 이벤트 예외를 단순한 브랜치 `git push`까지 확대 해석하지 않는다.
- **근거:** [GitHub — Triggering a workflow](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow), [Required status checks](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks)

### G1 · High · 승인 게이트 — 쓰기 가능한 Actions

신규 workflow는 `permissions: contents: write`를 사용한다. `persist-credentials: false`, commit 단계에서만 `GH_TOKEN` 사용, 생성 대상 파일만 stage, force push와 별도 PAT·App·secret 미사용은 합리적인 제한이다. 그러나 [GitHub 정책](../../docs/development/github.md)이 요구하는 **사람의 독립 검토와 명시적 승인**은 확인되지 않았다. Draft는 workflow 실행을 차단하는 권한 통제가 아니다. 이 보고서와 기존 checks는 사람 승인을 대체하지 않는다.

### G2 · High · 검증 게이트 — 신규 write 경로 E2E 미확인

PR 브랜치에서 확인한 Actions 실행 기록 35건 중 신규 `Sync Generated Artifacts`의 성공적인 E2E 결과를 확인하지 못했다. 아래 항목은 모두 **Not Verified**다.

- 관련 원본 push 후 실제 projection 변경과 generated-only 봇 커밋
- no-op에서 불필요한 커밋이 발생하지 않는지
- 실제 토큰 쓰기 권한·브랜치 push 성공
- 봇 커밋 이후 최신 PR 후보의 required check
- 경합·권한 오류의 실패 및 복구

사람의 테스트 승인 후 격리 브랜치에서 실행해야 한다. 신규 workflow가 아직 기본 브랜치에 없을 때 `workflow_dispatch`를 병합 전 실행 경로로 당연시하지 않는다.

### R1 · Medium · 잔여 운영 위험

`push.paths`는 현재의 알려진 generator 원본 경로를 대상으로 한다. 향후 원본 위치를 추가하면 트리거도 재검토해야 한다. 동시 branch 갱신 시 non-fast-forward 실패가 가능하지만 force push로 우회하지 않는 것이 적절하다. 현 revision에서 새로운 확정 source 누락이나 덮어쓰기 결함은 발견하지 못했다.

## 정적 구현 검토

| 항목 | 결과 | 근거 |
| --- | --- | --- |
| 브랜치/ref 제한 | 정적 Pass | `main` 제외, job에서 `refs/heads/*`만 허용 |
| 과거 태그 dispatch 결함 | 수정 확인 | 태그 ref 차단 및 명시적 `HEAD:refs/heads/${GITHUB_REF_NAME}` |
| 생성·검증 | 정적 Pass | 기존 `scripts.generated_artifacts sync` / `validate --all`, `uv --locked` |
| Stage 범위 | 정적 Pass | `docs/**/INDEX.tsv`, `catalog/INDEX.tsv`, `route/*.jsonl`, `.agents/route/*.jsonl` |
| no-op 분기 | 정적 Pass | staged diff가 없으면 commit 생략 |
| 안전성 | 정적 Pass | force push, 별도 credential, `main` 직접 push 없음 |
| 신규 workflow runtime | Not Verified | 원격 E2E 확인 없음 |

정적 Pass는 소스·설정 검토이며 원격 실행 성공의 증거가 아니다. 이 독립 리뷰에서 신규 Actions, 로컬 테스트, 별도 Git pathspec 실험을 실행하지 않았다.

## 최신 CI 근거

리뷰 기준 head `5a0c39101a3aa25ea4e302633302b9cc3501f47f`:

| 대상 | 판정 | 근거 |
| --- | --- | --- |
| Branch Check | Pass | [run 42676522031](https://github.com/mols3131d/mols-agent-assets/actions/runs/42676522031) |
| 필수 PR Gate | Pass | [run 42676529917](https://github.com/mols3131d/mols-agent-assets/actions/runs/42676529917) |
| 신규 Sync Generated Artifacts E2E | Not Verified | 해당 브랜치에서 확인된 성공 기록 없음 |
| 사람의 쓰기 워크플로 승인 | Not Verified | CI 성공 및 AI 리뷰와 별개 |

`PR Gate`는 `main` 보호 Ruleset의 required check다. 이 표의 통과는 **보고서 커밋 전 head**에 한정된다. 보고서 추가로 새 commit이 생기면 해당 head의 checks를 다시 확인해야 한다.

## 후속 작업 및 종료 조건

1. 사람이 쓰기 권한, 실행 트리거, stage 대상, generator 호출을 독립 검토하고 테스트 실행을 명시적으로 승인한다.
2. 승인된 격리 브랜치에서 [handoff.md](handoff.md)의 no-op, generated-only bot commit, 실패·복구 사례를 실행하고 SHA·run URL을 기록한다. 미수행 검증은 Not Verified로 보존한다.
3. 기존 PR에 봇 커밋이 생긴 뒤 최신 PR 후보의 필수 check가 실제로 유효한지 확인한다. 수동 재검증 비용을 수용할지 결정한다.
4. 최신 base/head와 required checks, 사람 승인 후에만 Draft 해제 및 squash merge를 검토한다. 인증 확장·Ruleset 완화·검증 우회는 별도 승인 없이 수행하지 않는다.

**최종 결론:** 정적 구현은 대체로 수용 가능하지만, F1 운영 모델 결정과 G1·G2 승인·검증 조건이 해소되기 전에는 머지를 보류한다. `.inbox/` 자료는 인계 근거이며 정본 정책은 아니다.
