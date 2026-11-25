# CI·자동화 작업군 로컬 에이전트 인계

이 문서는 네 PR의 재개 순서와 인계 조건을 정리하는 비정본 자료다. [통합 계획](00-plan-generated-writeback.md)에 수용 기준을 두고, 검증 결과와 승인 여부는 각 PR의 Checklist에 기록한다.

## Goal

로컬 hook과 원격 CI가 일관된 검증을 제공하고, GitHub API 등 hook을 거치지 않는 원본 변경에서도 공식 생성기가 허용된 생성물만 자동 복구한다. 자동 생성 커밋 이후의 최신 필수 PR Gate까지 검증한 뒤 운영 여부를 결정한다.

## 시작 상태

2026-11-25 인계 시점의 `main`은 `e839deafd3f1678f9ed50a8c8fcfe2bbdddc8e45`였다. 재개 시 각 ref, CI 및 승인 상태를 다시 확인한다.

| 순서 | PR / 작업 책임 | 관찰한 HEAD | 상태 |
| --- | --- | --- | --- |
| 1 | [#305](https://github.com/mols3131d/mols-agent-assets/pull/305) — CI·Lefthook 기준선 | `2dbdbd5961c5460760988b65e6fbf2a7a63f3687` | Draft, 기존 CI 성공 |
| 2 | [#308](https://github.com/mols3131d/mols-agent-assets/pull/308) — Trusted Writer | `8e71aacfd0b229736e46d3cd60c000a89eaa2b90` | Draft, 기존 CI 성공 |
| 3 | [#294](https://github.com/mols3131d/mols-agent-assets/pull/294) — read-only Producer | `b204bd23da0cea91d10f8d6aa9c3c524f059dc9a` | Draft, 기존 CI 및 sync 성공 |
| 4 | [#310](https://github.com/mols3131d/mols-agent-assets/pull/310) — 통합 수용·운영 검증 | 이 문서가 속한 브랜치 | Draft, 계획·인계만 포함 |

기존 성공은 당시 HEAD에 대한 결과다. 최신 main 통합, 독립 보안 검토 및 실제 원격 write-back은 아직 검증되지 않았다.

## 실행 순서와 완료 조건

각 PR의 기존 브랜치와 독립 worktree를 사용한다. 조사·개선·로컬 검증·독립 리뷰는 변경 충돌과 실제 의존성에 따라 병렬로 진행한다. 앞선 PR이 반영되면 다음 PR의 기준선을 갱신하고 변경된 검증과 리뷰를 다시 수행한다.

### 1. #305 — CI·Lefthook 기준선 확정

- [ ] 최신 main 통합 시 `scripts/generated_artifacts_validate.py`와 관련 테스트의 양쪽 변경을 대조한다. 최신 projection 선택·검증 계약을 보존한다.
- [ ] Windows npm 래퍼·공백 인수, Git typechange·symlink, 부분 스테이징을 실제 fixture로 검증한다. 기존 모킹 테스트의 성공을 실제 hook 동작의 근거로 확대하지 않는다.
- [ ] 공식 setup, deterministic tests, 생성물 검증, 실제 commit/push hook 및 최신 Branch Check/PR Gate를 확인한다.
- [ ] 로컬·branch·PR 검사의 책임과 중복 비용을 비교하고, 통제 표면에 대한 독립 검토 및 승인 요청을 마친다.

상세 인계: [#305 코멘트](https://github.com/mols3131d/mols-agent-assets/pull/305#issuecomment-7154624686). 종료 조건: 현재 main과 호환되는 CI 기준선이 확정되고 사람의 승인 후 반영된다.

### 2. #308 — 비활성 Trusted Writer bootstrap

- [ ] #305 반영 후 최신 main 기준으로 공식 `PROJECTIONS`와 writer의 output allowlist, 삭제·symlink/typechange 처리 및 artifact 계약을 비교한다.
- [ ] 로컬 bare Git E2E와 deterministic tests로 provenance, ZIP 제한·traversal, stale HEAD, non-fast-forward, token 비노출 및 권한 경계를 재검증한다.
- [ ] #294와 artifact 이름·manifest·repo/ref/source SHA·허용 출력 계약을 실제 fixture로 교차 검증한다.
- [ ] 수정 대상 workflow 자체에 의존하지 않는 독립 보안 리뷰를 확보하고, 비활성 bootstrap 반영에 대한 사람의 명시적 승인을 요청한다.

상세 인계: [#308 코멘트](https://github.com/mols3131d/mols-agent-assets/pull/308#issuecomment-7154625460). 종료 조건: 기본 비활성, 빈 allowlist fail-closed, secret 접근 없는 preflight, 최소 권한 및 강제 push 금지를 검증하고 승인된 비활성 bootstrap을 반영한다. 실제 원격 E2E는 bootstrap 이후 별도 승인 범위에서 수행한다.

### 3. #294 — read-only Producer 통합

- [ ] 최신 main과 #305/#308 반영 결과를 기준으로 path filter, 영향 선택, 공식 생성기 및 허용 출력 계약을 재검토한다.
- [ ] source-only/output-only 복구, 생성물 추가·수정·삭제, no-op/재진입, 비생성 경로·잘못된 provenance 거부를 테스트한다.
- [ ] 실제 producer payload를 trusted writer와 교차 검증하고 중복 구현을 최소화한다. Producer에는 secret 및 원격 쓰기 권한을 부여하지 않는다.
- [ ] 실행 런북과 검증 행렬의 변경이 필요한 경우 #294에서 갱신하고 최신 CI·독립 검토·승인 조건을 확인한다.

상세 인계: [#294 코멘트](https://github.com/mols3131d/mols-agent-assets/pull/294#issuecomment-7154624012), [검증 행렬](https://github.com/mols3131d/mols-agent-assets/blob/mols/chore/generated-sync-on-push/.inbox/github-294/11-verification-plan.md), [소유자 설정 런북](https://github.com/mols3131d/mols-agent-assets/blob/mols/chore/generated-sync-on-push/.inbox/github-294/13-owner-setup-runbook.md). 종료 조건: 최신 코드에서 읽기 전용 producer와 writer의 계약이 호환되고 실제 통합 검증에 사용할 준비가 완료된다.

### 4. #310 — 통합 수용 및 운영 검증

- [ ] 앞선 세 PR의 최신 SHA, 검증·독립 리뷰와 승인 근거를 확인한다.
- [ ] 소유자가 승인한 단일 저장소 App 설치, Environment 및 branch allowlist를 설정한다. 설정 작업은 소유자 또는 명시적으로 승인된 주체가 수행한다.
- [ ] 승인된 격리 PR에서 원본 변경 → producer artifact → trusted writer App commit → PR synchronize → 최신 required PR Gate 성공을 실증한다.
- [ ] 잘못된 provenance, stale HEAD, 권한 부족, no-op·재진입 등 실패/skip 경로와 비활성화·권한 회수·rollback 절차를 검증한다.
- [ ] [기존 통합 계획](00-plan-generated-writeback.md)의 수용 항목을 실제 증거로 판정하고 운영 확대 여부를 소유자에게 보고한다.

통합 순서 근거: [#310 코멘트](https://github.com/mols3131d/mols-agent-assets/pull/310#issuecomment-7154635229). 종료 조건: 정상 경로와 실패 경계의 실제 E2E가 확인되고 운영 승인이 이루어진다. #310 자체는 구현 PR이 아니므로 필요한 결정은 각 구현 PR과 정본에 남기고 중복 계획 PR의 close 여부를 판단한다.

## 공통 검증 및 인계

각 브랜치의 현재 하네스에 맞춰 실행 명령을 확인한다. 기준 명령은 `mise run setup`, `mise run test`, `mise run generated sync`, `mise run generated validate`, `mise run rulesync-validate`이다. 공식 생성기를 사용하고 생성 파일은 수동 편집하지 않는다. 관련 formatter 및 실제 hook 검증도 변경 범위에 맞게 수행한다.

PR별 결과는 해당 PR에 기록한다. base/head full SHA, 실제 실행한 명령과 결과, 최신 CI run URL, 미검증 사항, 해결한 finding, 남은 승인 또는 차단 사항을 남긴다. Push 후에는 최신 HEAD 기준 셀프 리뷰를 갱신한다. 통합 문서에는 다음 단계의 판단에 필요한 변경만 남긴다.

## 권한 경계

- 일반 검증과 개선은 기존 PR의 책임 범위에서 수행한다. main 직접 push, Ruleset bypass, 강제 push, 승인 없는 merge는 하지 않는다.
- GitHub App 등록·설치, private key/secret, Environment/Variables 변경, writer 활성화·운영 확대, 원격 write E2E는 각각 필요한 사람의 승인 전 수행하지 않는다.
- 원격 write 검증은 승인된 테스트 branch로 제한한다. 비밀값은 파일·PR·로그에 기록하지 않는다.
- 로컬 agent 실행이나 독립 검토를 하지 않았다면 완료로 표시하지 않는다. CI 성공은 실제 원격 write-back 또는 사람의 승인과 별개다.

지속적으로 유효한 계약은 `docs/development/ci.md`, `docs/development/github.md`, `docs/development/formatting.md`, 관련 공식 생성기 및 테스트 등 책임 있는 정본에 반영한다. 이 인계 문서는 별도 정책이나 중복 구현의 근거가 아니다.
