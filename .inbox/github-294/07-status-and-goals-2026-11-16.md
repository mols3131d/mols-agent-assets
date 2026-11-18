# PR #294 목표와 작업 현황

> 기준: 2026-11-16 조회. 이 문서는 작업 기록이며 실행 승인이나 저장소 정책이 아니다.

## 목표

로컬 hook을 거치지 않은 편집으로 생성 파일이 누락되어도 GitHub Actions가 기존 생성기를 실행해 파일을 자동 생성·커밋한다. 이미 열린 PR에서도 사람이 후속 push를 하지 않고 최신 PR 후보에 필요한 `PR Gate`까지 검증하는 것을 목표로 한다.

GitHub App, PAT, 추가 Secret 없이 기본 `GITHUB_TOKEN`을 사용하고 가능한 한 간결하게 구성한다. Ruleset 우회, 임의의 성공 상태 보고, `main` 직접 수정 및 자동 merge는 범위 밖이다.

## 현재 상태

| 항목 | 현황 |
| --- | --- |
| PR | [PR #294](https://github.com/mols3131d/mols-agent-assets/pull/294)는 Open / Draft. 조회 기준 base는 `fa5be3bd63e9c29c30017b9e8c833018c092b9a7`, head는 `544fd551ea8c366f8f22c4398f3e1d659e3ab270`이다. 후속 작업 전 다시 조회한다. |
| 자동 생성 | [generated-sync.yml](../../.github/workflows/generated-sync.yml)에 기존 generator 실행·검증, 생성 파일 staging, 변경 시 봇 커밋과 push가 구현돼 있다. 원격 write 경로의 실제 동작은 미검증이다. |
| 브랜치 제한 | 태그 dispatch 차단과 브랜치 push ref 명시(F2)는 정적 수정 완료. 실제 실행 검증은 별개다. |
| 필수 체크 | 봇 커밋 이후 열린 PR의 최신 후보에 `PR Gate`가 자동으로 충족되는 경로(F1/R1)는 미해결이다. 기존 [PR Gate](../../.github/workflows/pr-gate.yml)는 생성 결과를 검증하지만 자동 커밋하지 않는다. |
| 기존 체크 | 위 head에 대한 [Branch Check](https://github.com/mols3131d/mols-agent-assets/actions/runs/43156239087/job/130976726548)와 [PR Gate](https://github.com/mols3131d/mols-agent-assets/actions/runs/43156244323/job/130976743368)는 성공했다. 이는 신규 write workflow E2E의 성공 근거가 아니다. |
| 승인·E2E | 조회된 GitHub PR 리뷰는 없고 사람의 독립적인 write workflow 테스트 승인은 확인되지 않았다. 봇 커밋, no-op, 최신 필수 체크와 원격 실패 복구는 Not Verified다. |
| 기록 | PR 본문의 revision과 파일 목록은 최신 상태보다 오래됐다. 후속 작업에서 실제 결과와 함께 갱신한다. |

이전 [인계](01-handoff.md)와 [심층 리뷰](05-review-report-deep-2026-11-12.md)는 당시 근거와 대안이다. 수동 후속 push를 기본 운영으로 수용하거나 재설계를 별도 PR로 미루는 기존 제안은 위 자동화 목표를 대체하지 않는다.

## 완료 조건

- [ ] 기본 토큰만으로 봇 커밋 후 최신 head 또는 merge candidate의 실제 required `PR Gate`가 자동으로 보고되고 통과하는 경로를 설계·입증한다. `workflow_dispatch`와 `repository_dispatch`는 검토 후보이며 해결이 확인된 것은 아니다.
- [ ] 생성 파일만 커밋하고 no-op에서는 커밋하지 않는다. 브랜치 경합, 중복 실행, base 변경과 오래된 SHA를 안전하게 처리하고 강제 push 없이 실패를 확인할 수 있다.
- [ ] write 권한, 실행 ref, 신뢰 경계를 독립적으로 검토하고 사람이 테스트를 명시적으로 승인한다. Draft 자체는 실행 차단 장치가 아니다.
- [ ] 승인 후 별도 격리 브랜치와 열린 테스트 PR에서 no-op, source 변경 → generated-only bot commit → 최신 필수 체크 및 실패·경합 복구를 검증한다. source/bot SHA, merge candidate, 변경 파일, run URL과 미검증 항목을 기록한다.
- [ ] 최신 PR의 변경 범위, 체크와 본문을 동기화하고 사람의 최종 검토·승인을 받는다. Draft 해제와 merge는 별도 명시적 승인 전 수행하지 않는다.

## 다음 작업

1. 실제 required check와 GitHub 이벤트·SHA 계약을 조사하여 기본 토큰만으로 목표를 충족하는 최소 설계와 보안 경계를 제안한다. 기존 PR Gate 수정이나 추가 workflow의 필요성은 조사 결과로 판단한다.
1. 구현 범위와 검증 방법을 확정하고 기존 생성 대상·no-op·브랜치 제한을 유지한다. 기존 권한 경계를 넘거나 실현할 수 없다면 근거와 대안을 보고한다.
1. 사람의 명시적 테스트 승인 전에는 write workflow를 실행하지 않는다. 승인 후 격리 E2E를 수행하고 결과를 기록한다.
