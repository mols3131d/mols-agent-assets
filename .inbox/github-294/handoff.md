# PR #294 — 코딩 에이전트 인계 보고서

> 상태: **HANDOFF / Draft 유지** (2026-11-10). 독립 리뷰 스냅샷은 base `fa5be3bd63e9c29c30017b9e8c833018c092b9a7`, head `49b594ca8a5962cd2db01ba9c9bed3781be6a895`. 보고서 반영 커밋 이후의 head와 체크는 반드시 새로 확인한다. 이 문서는 작업 인계 근거이지 실행 승인이나 저장소 정책 정본이 아니다.

## 작업 목표와 범위

[독립 리뷰](review-report.md)의 미완료 게이트를 해소하여 [PR #294](https://github.com/mols3131d/mols-agent-assets/pull/294)의 병합 판단에 필요한 근거를 확보한다. 기본 목표는 **기존 generator로 생성 파일을 자동 동기화하되, `main` 입장에 필요한 최신 PR 검증을 보존**하는 것이다.

- 저장소: `mols3131d/mols-agent-assets`; PR: `#294`; 작업 브랜치: `mols/chore/generated-sync-on-push`; 연결: **`main-dev` / `mols3131d`만** 사용한다. 다른 계정이나 명의로 전환하지 않는다.
- 변경 범위: [generated-sync.yml](../../.github/workflows/generated-sync.yml) 및 이에 직접 관련된 인계·리뷰 기록. 기존 [PR Gate](../../.github/workflows/pr-gate.yml), [Branch Check](../../.github/workflows/branch-check.yml), generator, Ruleset, `main`은 변경하지 않는다.
- 구현 상태: `contents: write`, source push/수동 dispatch, `sync` → `validate --all` → generated-only staging → 변경 시 봇 커밋. 이전 F2 태그 ref 문제는 **이미 수정 완료**; 재구현 금지.
- 설계 경계: PAT, 별도 GitHub App/secret, 신규 CI workflow, 자동 머지, required check 우회는 이번 인계의 기본 범위가 아니다.

## 시작 전 확인

1. `CHATBOT.md`, `AGENTS.md`, [GitHub 정책](../../docs/development/github.md), [CI 정책](../../docs/development/ci.md), [VCS 정책](../../docs/development/vcs-git.md), [리뷰 보고서](review-report.md)를 확인한다. 정확한 head ref의 applicable Skill/Rule을 선택한다.
2. PR의 **현재** base/head SHA, Draft 상태, diff, 사람의 변경·리뷰, branch/check 상태와 `protect-main`의 required check를 새로 읽는다. 과거 SHA를 최신이라고 가정하지 않는다.
3. 이미 다른 에이전트나 사용자가 수정한 부분은 보존한다. 예상 밖의 branch 이동/동시 작업이 있으면 충돌 대상을 격리하고 history를 강제로 재작성하지 않는다.
4. 사람이 새 write-capable workflow를 **독립 검토하고 명시적으로 테스트를 승인했는지** 확인한다. 승인 전에는 아래 E2E를 실행하지 않는다. 이 보고서 작성과 기존 CI 성공은 승인이 아니다.

## 우선순위별 인계

| 우선순위 | 작업 | 완료 조건 |
| --- | --- | --- |
| P0-1 | 독립 승인 확보 | 사람의 명시적 승인 여부가 분명하고 기록됨. 없으면 write 테스트 중단 |
| P0-2 | no-op + source 변경 E2E | 원본 변경에서 `Sync Generated Artifacts`가 실제 실행, 예상 생성 결과만 커밋; no-op에서는 무커밋 |
| P0-3 | bot commit 이후 PR check 관찰 | 최신 head/merge candidate에 `PR Gate`가 실제로 보고됐는지, 승인 대기인지, 누락인지 정확히 기록 |
| P0-4 | 운영 수용/설계 결정 | 제한적 자동화의 수동 검증 절차를 사람이 수용했는지 또는 설계 변경이 필요한지 명시 |
| P1 | 최신 revision·증거 동기화 | PR 본문과 인계/리뷰 기록의 head/base, run URL, 미검증 상태를 갱신 |

### 승인 이후 E2E 실행 순서

1. **격리 브랜치 준비:** `main`이나 기존 PR 브랜치에 실험 커밋을 넣지 않는다. 같은 계정의 승인된 전용 테스트 브랜치에서 확인한다. 임의의 다른 계정·토큰을 사용하지 않는다.
2. **No-op:** 인덱스/라우팅 결과가 달라지지 않는 승인된 source 수정을 작업 브랜치에 push한다. `Sync Generated Artifacts` run 성공, `changed=false`, 추가 bot commit 없음, SHA와 run URL을 확보한다. Workflow가 기본 브랜치에 없는 병합 전 단계에서는 `workflow_dispatch`를 유효한 수동 실행 경로로 가정하지 않는다.
3. **Generated delta:** `docs/` 또는 명확한 source의 작은 수정으로 `INDEX.tsv` 또는 route 출력이 실제 변하게 한다. 워크플로 성공과 **generated-only** 커밋, 원본 브랜치에 대한 fast-forward push, `validate --all` 성공 및 변경 파일 목록을 확인한다.
4. **PR 재검증:** 승인된 테스트 브랜치로 PR을 열거나 기존의 안전한 PR에서 bot commit 이후 `pull_request`/check 동작을 관찰한다. `GITHUB_TOKEN`의 일반 `push` 후속 workflow 억제와, 토큰으로 **PR 자체를 생성·갱신할 때 승인 대기 CI가 생기는 2026-06 예외**를 혼동하지 않는다. 예상이 아니라 **실제 최신 SHA**의 `PR Gate` 상태, 승인 배너 유무, run URL로 판단한다.
5. **실패·경합:** 재현을 위해 무리하게 브랜치를 덮어쓰지 않는다. 관찰 가능한 `non-fast-forward`, 권한 부족, generator 실패 사례를 확인하고 실제 발생하지 않은 테스트는 **Not Verified**로 남긴다.
6. **결과 정리:** 테스트 커밋·branch/run ID와 이상 여부를 짧게 기록한다. 테스트 잔여 브랜치의 정리는 별도 권한·소유권이 확인된 경우에만 수행한다.

### 최신 PR Gate가 없을 때

- 먼저 `PR Gate`가 최신 PR head 또는 merge candidate에 실제로 존재하는지 조회한다. 과거 성공한 run을 새로운 SHA의 성공으로 취급하지 않는다.
- 기본 P0 운영은 **원본 push → 생성 커밋 완료 → 최초 PR 생성**이다. 이미 열린 PR에서 bot commit 후 required check가 없다면, 사람의 승인 아래 **같은 계정의 정상 후속 push/PR 이벤트**로 재검증한 뒤 최신 체크를 확인한다. 빈 커밋은 불가피한 경우에만 사용하고 정상 자동화의 성공으로 보지 않는다.
- `workflow_dispatch`로 신규 생성 workflow를 실행하거나 과거 check를 재시도했다는 사실만으로 최신 required `PR Gate` 충족을 선언하지 않는다.
- 완전 무인 운영이 요구되거나 수동 절차가 반복 비용을 유발하면 재설계안을 **별도 PR**로 제출한다. 인증 확장·Ruleset 완화·검증 우회는 임의로 실행하지 않는다.

## 장애 복구

| 증상 | 안전한 대응 |
| --- | --- |
| generator/validate 실패 | 실패한 step, source, lock/network 의존성 확인 → 격리 브랜치에서 수정 → 다시 정상 push. 검사 비활성화 금지 |
| `403 Resource not accessible by integration` | workflow의 `contents: write`, repo 정책, 실행 ref 확인. 계정이나 토큰 임의 교체 금지 |
| `non-fast-forward` | remote tip과 runner checkout SHA 비교 → 변경 소유권을 확인한 후 최신 ref에서 재동기화. 강제 push 금지 |
| 변경이 있는데 자동 실행 없음 | source path filter, workflow가 해당 ref에 존재하는지, 이벤트/skip 기록 확인 |
| 최신 `PR Gate` 미보고 | PR 이벤트·approval 필요·check 미생성 중 무엇인지 분류. 검증 전 머지 금지 |

## 인수 기준 및 종료 조건

- **기존 증거:** 리뷰 기준 head `49b594ca8a5962cd2db01ba9c9bed3781be6a895`에서 [Branch Check](https://github.com/mols3131d/mols-agent-assets/actions/runs/42673980412)와 [PR Gate](https://github.com/mols3131d/mols-agent-assets/actions/runs/42673991539) 성공. 이전 작업 기록의 `mise check`, `mise test`(434 passed), generated validation은 과거 시점의 증거다.
- **미완료:** 사람의 독립 승인, 새 workflow no-op/봇 커밋 E2E, 열린 PR의 bot commit 이후 최신 required check 상태 확인, 운영 방식 승인. 수행하지 않은 것은 Pass로 기록하지 않는다.
- **완료 판단:** 코드/보안 문제가 없고, 승인된 E2E 결과와 최신 필수 checks가 수용 가능한 상태이며, 사람이 제한적 자동화 운영과 병합을 명시적으로 승인했을 때만 Draft 해제 및 **squash merge**를 검토한다.
- **중단 판단:** 승인 없음, 예상 밖 쓰기·계정·권한, 보호 규칙 충돌 또는 회복 불가능한 검증 공백이 있으면 `BLOCKED`로 기록하고 실행·병합을 중단한다.
- **기록 위치:** [리뷰 보고서](review-report.md)에 판단과 미검증 항목을, PR 본문에는 변경 후 실제 `revision.base/head`와 최신 check 근거만 갱신한다. 중복된 정책 정의는 정본에 맡긴다.

**이 인계는 리뷰 완료가 아닌 실행과 승인 조건의 전달이다.** 신규 write workflow의 활성화 및 병합 승인은 별도의 사람 결정으로 남긴다.
