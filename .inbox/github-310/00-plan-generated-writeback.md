# Generated Artifacts — 자동 복구 통합 준비

> 상태: **Draft / 원격 쓰기 검증 대기**. [Producer PR #294](https://github.com/mols3131d/mols-agent-assets/pull/294)와 [Trusted Writer PR #308](https://github.com/mols3131d/mols-agent-assets/pull/308)의 통합 수용 기준을 정의하는 비정본 자료다. 각 PR의 Checklist에서 최신 코드, CI, 독립 리뷰 및 승인 근거를 확인한다.

## Goal

GitHub Contents API·Plugin·agent·로컬 Git 등으로 **원본만 변경한 동일 저장소의 브랜치**에서 generated projection drift가 생기면 CI가 공식 생성기를 통해 복구 결과를 만들고, **허용된 생성 파일만 PR 브랜치에 자동 commit·push**한다. 최신 봇 커밋에 대한 필수 **`PR Gate`** 는 정상적인 PR 이벤트로 실행·통과해야 한다.

## Context / Authority

- 기준 브랜치는 `main`이다. 각 검증의 base와 head는 해당 PR에 기록한다.
- 정본: `docs/development/ci.md` (읽기 전용 admission), `docs/development/github.md` (사람 승인·권한·squash merge), `docs/development/source-authority.md` (생성물은 파생 결과), `scripts/generated_artifacts_sync.py` (`PROJECTIONS`와 영향 범위).
- 실제 Ruleset `protect-main`: 필수 **`PR Gate`**, squash merge, 선형 이력, review thread resolution. GitHub-hosted 설정은 코드나 문서만으로 변경되지 않는다.
- 기존 구현: **#294**는 읽기 전용 `Sync Generated Artifacts` Producer, **#308**은 `main` 소유 `workflow_run` Trusted Writer. 두 PR은 현재 Draft이며 Writer 기본 비활성이다.
- 기본 `GITHUB_TOKEN`으로 만든 push는 일반적인 후속 workflow 실행을 일으키지 않는다. 일부 PR 이벤트는 실행에 승인이 필요하다. 이 계획은 App 커밋에 대한 실제 `pull_request` 이벤트와 `PR Gate` 성공을 요구한다. [GitHub 토큰 동작](https://docs.github.com/en/actions/concepts/security/github_token)
- 관련 기존 상세 근거: #294 브랜치 `.inbox/github-294/09-github-app-design.md`, `11-verification-plan.md`, `13-owner-setup-runbook.md`. 이 문서는 해당 상세 설계/런북을 복제하지 않고 **통합 완료 기준**만 소유한다.

## In Scope

- `docs/**/INDEX.tsv`, `catalog/**/INDEX.tsv`, `route/*.jsonl`, `.agents/route/*.jsonl`에 한정한다. 공식 `generated_artifacts` CLI와 `PROJECTIONS`의 source/output matcher를 재사용하고, 생성 결과의 **추가·수정·삭제**를 포함한다.
- #294 Producer와 #308 Writer의 최신 `main` 호환성·인터페이스(artifact 이름·manifest·SHA·경로·선택/검증 범위)를 확인하고, 필요 시 **각 코드 소유 PR에서** 충돌·계약 결함을 수정한다. 새로운 제3의 generator/validator를 만들지 않는다.
- `Branch Check`는 빠른 브랜치 피드백, `PR Gate`는 merge candidate 검증으로 유지한다. Writer만 별도 maintenance capability로 분리한다.
- 자동화가 성공적으로 복구하지 못한 실패는 사용자에게 진단되며 검증 통과/머지 가능으로 가장하지 않는다.

## Required acceptance (미충족이면 구현 완료·운영 준비 완료로 간주 금지)

- [ ] **Architecture:** #308 Writer가 신뢰된 `main` 코드에서만 실행되고 먼저 비활성 상태로 squash merge되었다. #294 Producer는 외부 PR 코드에서 credential·secret·쓰기 권한 없이 실행한다.
- [ ] **Write scope:** repo/ref/branch allowlist·입력 run SHA·현재 branch tip·artifact provenance를 확인한 뒤 `PROJECTIONS`가 허용하는 generated output만 커밋한다. 임의 파일, symlink, path traversal, 과대/변조 artifact를 거부한다.
- [ ] **Safe push:** non-fast-forward·동시 수정 충돌·삭제·stale HEAD를 덮어쓰지 않는다. `main` 직접 push·Ruleset bypass·자동 merge는 하지 않는다.
- [ ] **Idempotency:** no-op에서는 추가 commit/token 발급 없이 종료하고, 봇 output-only push가 무한 자동 생성 루프를 만들지 않는다. Source-only·output-only 입력이 모두 계획대로 처리된다.
- [ ] **Failure paths:** 잘못된 metadata·generator 오류·fork/타 저장소·권한 부족·App 미설치·변조 artifact가 안전하게 실패 또는 skip되며 기존 PR Gate 실패를 숨기지 않는다.
- [ ] **Required check:** 격리된 테스트 PR에서 원본 변경 → Producer artifact → Trusted Writer App commit → PR `synchronize` → **최신 생성 커밋의 required `PR Gate` 성공**을 실제 run URL과 full SHA로 확인한다. `workflow_dispatch` 결과만으로 완료 처리하지 않는다.
- [ ] **Independence:** 쓰기 가능한 GitHub workflow의 신뢰 경계에 대해 수정 대상 workflow 자체에 의존하지 않는 보안 리뷰와 사람의 명시적 승인을 확보한다.
- [ ] **Operations:** Environment/Secret/App 설치 범위, branch allowlist와 비활성화/롤백 절차를 사람이 검토·설정하고, 운영 대상 branch 확대는 별도 승인한다.
- [ ] **Regression:** deterministic tests, `generated_artifacts validate --all`, source frontmatter validation, `Branch Check`와 실제 `PR Gate`가 최종 코드·커밋 기준으로 통과한다.

## Work sequence

1. **Reconcile:** `main` 최신 baseline과 #294/#308 diff·문서·테스트를 비교한다. 충돌·stale assumption 및 #305 CI 개선과의 영향도 식별한다.
2. **Review bootstrap:** #305를 승인·반영한 뒤 #308의 검증 기준선을 갱신한다. 독립 리뷰와 사람 승인 후 기본 비활성인 Writer를 먼저 반영한다.
3. **Verify producer:** #294의 읽기 전용 CI와 Producer–Writer 로컬 호환성은 선행 PR 검토와 병행한다. 선행 PR 반영 뒤 최신 `main`과 다시 검증한다. 영향이 불명확하면 fail-safe로 범위를 확장한다.
4. **Approve & isolate:** 소유자 `mols3131d`의 권한으로 App/Environment/Repository Variables를 수동 설정하고, 특정 테스트 branch만 허용하도록 제한한다. **이 단계는 별도 사람 승인 전 실행 금지**.
5. **E2E:** 별도 테스트 branch와 열린 PR에서 #294 검증 행렬 E01~E10 중 필수 경로를 실제로 실행한다. Source SHA/봇 SHA/검사 SHA, run URL, 실패·skip 기록을 남긴다.
6. **Decide:** 원격 E2E 결과와 사람의 승인으로 #294의 squash merge 및 운영 활성화를 각각 판단한다. 구현 PR과 검증 기록을 확정한 뒤 #310의 종료 여부를 판단한다.

## Boundaries and risks

- #310에는 통합 수용 기준과 작업 인계를 둔다. Producer·Writer 개선은 각각의 구현 PR에서 진행한다.
- 동일 파일의 구현·수정 owner는 기존 #294/#308이다. 이 통합 브랜치에서 그 코드에 병렬 수정을 가하지 않는다.
- #294/#308의 메인 브랜치 기준은 현재와 다르므로 최신성 검증 없이는 기존 테스트 성공을 새 HEAD에 일반화하지 않는다.
- 주 위험: 높은 권한의 `workflow_run`이 변조 artifact를 신뢰하는 문제, 정상 `PR Gate` 재실행 누락, 비밀키 노출, 비승인 branch 자동 write 및 비용 증가. 기본 비활성·allowlist·권한 격리·실제 E2E를 완료 게이트로 삼는다.

## Current evidence

- [x] 최신 `main`의 `PR Gate`, `Branch Check`, required Ruleset과 생성물 ownership 확인.
- [x] 기존 #294/#308의 Producer/Writer 설계와 미완료 E2E·사람 설정 의존성 확인.
- [ ] App 토큰을 사용하는 격리 원격 E2E와 최신 봇 커밋의 required `PR Gate` 검증. Writer 반영과 소유자 설정·승인이 필요하다.
