# PR #294 — 심층 리뷰 후속 작업 인계 (2026-11-12)

> **상태: HANDOFF / Draft 유지.** [심층 리뷰](review-report-deep-2026-11-12.md)의 R1·R2와 승인·E2E 게이트를 해소한다. 이 문서는 실행 권한이나 사람의 승인이 아니다.

## 작업 기준

- 저장소: [`mols3131d/mols-agent-assets`](https://github.com/mols3131d/mols-agent-assets), [PR #294](https://github.com/mols3131d/mols-agent-assets/pull/294).
- 작업 브랜치: `mols/chore/generated-sync-on-push`; **리뷰 시작 시점**의 base `fa5be3bd63e9c29c30017b9e8c833018c092b9a7`, head `e533656aea161764c5d7f1aceb5fd1390cd09e21`. 이후 문서 커밋으로 head는 달라진다.
- 실행 계정: `mols3131d`의 승인된 GitHub 연결 `main`. 승인 없이 다른 연결·계정·명의를 사용하지 않는다.
- 본 작업은 이미 존재하는 [generated-sync.yml](../../.github/workflows/generated-sync.yml)의 안전한 사용 가능성을 확인하는 범위다. 기존 generator·`PR Gate`·`Branch Check`·Ruleset·`main`은 임의 변경하지 않는다.
- [GitHub 정책](../../docs/development/github.md), [CI 정책](../../docs/development/ci.md), [기존 인계](handoff.md), 최신 PR 상태가 충돌하면 정책과 실제 상태를 우선하고 차이를 기록한다.

## 우선순위별 작업

| 단계 | 작업 | 종료 기준 |
| --- | --- | --- |
| P0-1 | 독립 검토·사람의 테스트 승인 확인 | write-capable workflow의 trigger·permission·쓰기 범위 승인 기록; 없으면 실행 중단 |
| P0-2 | 승인 전 자동 실행 통제 확인(R2) | Draft만으로 차단되지 않는 점을 반영하여 실제 Actions 설정·워크플로 실행 상태 조사 및 허용 방식 확정 |
| P0-3 | 격리 E2E | no-op 무커밋, 생성 차이 발생 시 generated-only commit, push SHA/run URL 확보 |
| P0-4 | 최신 필수 check 검증(R1) | 봇 커밋 후 PR head/merge candidate의 `PR Gate` 상태 확인; 승인된 재검증 경로 입증 |
| P0-5 | 운영 방식 확정 | 수동 후속 이벤트를 수용하는 제한적 자동화인지, 재설계가 필요한지 사람 결정 |
| P1 | PR 본문·스냅샷 정비(R3) | 실제 최신 `revision.base/head`, 파일 목록, 검증 근거 동기화 |

## 실행 순서와 관찰값

### 1. 실행 전 게이트

1. PR과 브랜치의 실제 head/base, mergeability, 변경·리뷰·checks를 다시 조회한다. 기존 리뷰 SHA를 최신이라고 가정하지 않는다.
2. `contents: write`를 가진 신규 워크플로의 호출 조건, `uv` 의존성, generator가 읽는 원본, stage 범위와 저장소의 Actions 실행/승인 통제를 사람이 독립적으로 검토한다.
3. **사람의 명시적 테스트 승인 전에는** 관련 source push, 새 workflow dispatch, 실험용 쓰기 작업을 시작하지 않는다. Draft는 실행 차단 장치가 아니다.
4. 예상 밖 동시 수정·권한·보호 규칙 문제를 발견하면 브랜치나 history를 덮어쓰지 않고 중단한다.

### 2. 승인 이후 격리된 E2E

1. 기존 PR 브랜치와 `main`을 실험 대상으로 사용하지 않는다. 승인된 별도 브랜치를 만들고 workflow 파일과 필요한 source가 해당 ref에 존재하는지 확인한다.
2. **No-op:** 생성 출력이 바뀌지 않는 관련 원본 변경을 승인된 방식으로 push. `Sync Generated Artifacts`의 실제 실행 여부, `changed=false`, 추가 bot commit 부재, run URL을 기록한다.
3. **Generated delta:** index나 route의 예상 변경을 발생시키는 작은 source 수정. `sync`·`validate --all` 성공 여부, 생성 파일만 stage/commit됐는지, ref로의 정상 fast-forward push, 전후 SHA를 확인한다.
4. **열린 PR:** 봇 커밋 이전·이후 SHA와 `PR Gate` run의 대상 head/merge candidate, 누락·pending·approval 상태를 각각 확인한다. GitHub 기본 토큰의 일반 `git push`가 후속 workflow를 시작하지 않는 계약을 실제 repo 결과와 대조한다.
5. **재검증:** 사람의 승인된 정상 후속 `push` 또는 PR 이벤트로 최신 후보의 required check를 다시 실행하고 성공 근거를 확보한다. 단순 `workflow_dispatch`나 과거 run 재시도만으로 통과했다고 선언하지 않는다.
6. **경합·실패:** 실제 확인한 non-fast-forward, 권한 실패, generator 오류만 기록한다. 일부러 위험한 충돌을 만드는 테스트는 필수로 간주하지 않는다. 재현하지 않았다면 `Not Verified` 유지.
7. 테스트 브랜치·PR·작업 기록의 정리는 생성 주체와 소유권 확인 후 별도 승인된 범위에서 수행한다.

`workflow_dispatch`는 해당 workflow가 기본 브랜치에 존재해야 이벤트를 받을 수 있으므로, 병합 전 격리 검증의 확실한 대체 경로라고 가정하지 않는다. [GitHub 이벤트 공식 문서](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#workflow_dispatch).

### 3. 증거 기록

최소한 다음을 리뷰 보고서 또는 승인된 기존 인계 표면에 남긴다.

- 검증한 브랜치/ref, 원본 push SHA, 생성 봇 커밋 SHA, 원격 run URL
- no-op의 commit 수와 generated delta의 실제 변경 파일 목록
- `PR Gate`가 무엇을 검증했는지(최신 head 또는 merge candidate), required check의 최종 상태
- 사람의 승인 여부 및 제한적 운영 모델의 수용 여부
- 실패했거나 실행하지 않은 테스트의 `Fail` / `Not Verified` 구분

현재 확보된 [PR Gate run 42682286312](https://github.com/mols3131d/mols-agent-assets/actions/runs/42682286312)의 성공은 **이전 리뷰 기준 head의 CI 근거**다. 새 자동 write 경로의 성공 증거가 아니며, 이 인계 문서 추가 후의 커밋도 검증하지 않는다.

## 대응 제한과 복구

| 상황 | 대응 |
| --- | --- |
| 승인이 없거나 실행 통제가 불명확 | write 테스트를 중단하고 승인·설정 확인으로 인계 |
| 생성 또는 검증 실패 | 출력·lock·원본·network 실패를 분류; validator 비활성화 금지 |
| `403` 등 토큰 실패 | 실제 `contents: write` 및 repository setting 확인; 다른 계정/토큰 자동 전환 금지 |
| non-fast-forward | 원격 최신 commit과 checkout SHA를 비교하고 안전한 새 revision에서 재생성; force push 금지 |
| 최신 `PR Gate` 없음 | 최신 head/merge candidate 기준 run·approval·required 상태를 분류하고 승인된 정상 이벤트로 재검증 |
| 수동 재검증이 반복되어 운영 비용 초과 | 인증 확대나 Ruleset 완화 없이 별도 설계안을 제안하고 사람 결정 요청 |

## 최종 인수 기준

- [ ] 사람이 새 write workflow를 독립 검토하고 실행을 명시적으로 승인했다.
- [ ] 자동 실행 제약과 Draft의 비차단 특성을 확인했다.
- [ ] 승인된 격리 E2E에서 no-op 무커밋을 관찰했다.
- [ ] 생성 변경 시 예상한 파생 파일만 봇 커밋되고 push가 성공했다.
- [ ] 열린 PR의 봇 커밋 후 최신 `PR Gate` 상태와 승인된 재검증 결과를 확인했다.
- [ ] Actions-only 제한적 운영을 수용할지 명시적으로 결정했다.
- [ ] 최신 PR 본문의 revision·Changes·검증 결과와 실제 상태가 일치한다.
- [ ] 머지에 필요한 최신 checks 및 사람 승인이 확인됐다.

**종료:** 위 게이트에 미해결 고위험 항목이 있으면 Draft 유지. 검증과 사람 승인이 충족된 경우에만 별도 명시적 머지 승인 아래 squash merge를 검토한다. 불필요한 새 workflow, PAT, App, 자동 merge, Ruleset 우회는 이번 작업의 기본 범위가 아니다.
