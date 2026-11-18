# PR #294 — 로컬 에이전트 구현 인계

> 2026-11-16 인계. 상세 설계는 [09-github-app-design.md](09-github-app-design.md), 검증 계약은 [11-verification-plan.md](11-verification-plan.md). 본문은 **작업 범위 제안**이며 계정 전환, credential 취급, privileged workflow 실행·merge 승인을 부여하지 않는다.

## 시작점과 성공 기준

- 작업 대상: [`mols3131d/mols-agent-assets` PR #294](https://github.com/mols3131d/mols-agent-assets/pull/294), branch `mols/chore/generated-sync-on-push` → `main`. 당시 상태는 Open/Draft였다. **실행 시 현재 PR ref, branch HEAD, base, diff, checks, 권한을 새로 조회**하고 이전 세션 스냅샷을 현재 상태로 사용하지 않는다.
- 실행 주체: 소유 계정 `mols3131d`만 허용. ChatGPT Plugin에서는 연결 `main`에 해당하는 소유 계정을 확인한 상태였다. **로컬 에이전트는 자신의 실제 `git`/`gh` 인증 주체를 독립적으로 확인**한다. 다른 연결·명의로 자동 전환하거나 권한 오류를 우회하지 않는다.
- 성공: ChatGPT Contents API 등 hookless source commit 이후 **기존 projection 자동 동기화 → App으로 generated-only commit → 열린 PR에 synchronize → 최신 실제 required `PR Gate` 성공**. no-op이면 불필요한 commit 없음. 권한/검증 미충족이면 fail-closed, 원인 진단 가능.
- 변경하지 않는 것: 기존 Python projection generator·validator의 정본 의미, `PR Gate`의 read-only admission, `Branch Check`의 조기 검증, `main` 직접 수정 금지, Ruleset 우회 금지, 자동 merge 금지. 별도 PAT, 새로운 모델 테스트, 리포지터리 구조 대개편 불필요.
- **선행 사용자 결정:** 기존 “GitHub App/Secret 금지”는 설계 방향상 해제됐다. **App 설치·개인키 등록·프로덕션 활성화·보안 control surface 실행·merge에 대한 별도 명시적 인간 승인 필요**.

## 먼저 읽을 정본

1. 루트 `AGENTS.md` → 작업 경로의 `AGENTS.md`, `docs/development/ci.md`, `docs/development/github.md`, `docs/development/vcs-git.md`.
2. `.github/workflows/generated-sync.yml`, `pr-gate.yml`, `branch-check.yml` 및 `scripts/generated_artifacts_sync.py`/`generated_artifacts_validate.py`/`generated_artifacts.py`.
3. 해당 작업에 필요한 `github-context`, `coding-context`, `mols-ci-design`, `mols-loops` 등 Skill을 로컬 런타임의 네이티브 발견으로 선택하고, 발견이 부족할 때만 `.agents/route/ROUTE.md`를 활용한다.
4. [기술 조사](08-generated-sync-architecture-research.md), [기존 심층 리뷰](05-review-report-deep-2026-11-12.md). 이전 `01-handoff.md`/`07-status-and-goals-2026-11-16.md`의 App 금지·수동 후속 push 경로는 **현재 합의보다 이전 기록**이다.

## 작업 단위

### P0 — 사전 정합성·권한 확인

- [ ] 현재 PR과 작업 tree의 실제 SHA·dirty state·branch owner를 확인한다. 다른 작업자의 최신 변경을 보존하고 강제 재작성하지 않는다.
- [ ] 실제 Rulesets의 required check 이름·source·strictness, merge queue 여부, Actions setting, App push permissions, 현재 workflow 등록/활성 상태를 확인한다. API 조회 권한이 없다면 **Not Verified**로 기록하고 설정을 임의 추정하지 않는다.
- [ ] GitHub 공식 `workflow_run` default branch와 `GITHUB_TOKEN` 이벤트 억제 계약을 다시 확인한다. `workflow_dispatch`로 required Gate를 대체하는 안은 채택하지 않는다.
- [ ] 설계에 대한 독립적 보안 검토 및 privileged workflow 실행에 대한 인간 승인 경로를 정한다. 승인이 없다면 **읽기 전용 개발·모의 테스트까지만** 진행한다.

### P1 — Producer를 read-only로 전환

- [ ] `.github/workflows/generated-sync.yml`을 branch source 변경을 감지하는 **읽기 전용 Producer**로 리팩터링한다. 기존 `contents:write`, `gh auth setup-git`, `git push` 및 Secret 사용을 제거한다.
- [ ] 현재 generator의 네 종류 projection 선택과 예상 출력만 생성하고 `validate --all`을 실행한다. 기존 명령의 재사용을 우선하며 장황한 wrapper를 만들지 않는다.
- [ ] 결과가 필요한 경우 **metadata + generated-file payload만** Artifact로 업로드한다. 변경 없을 때의 완료 신호를 명확히 하고, 실패 때 writer가 아예 실행되지 않도록 한다. 원본 SHA/branch/producer run ID를 인계한다. Artifact의 고유성·크기·경로 계약을 테스트한다.
- [ ] API로 생성 파일만 고친 변경도 자동 복구할지 포함 범위를 정한다. 포함한다면 App bot output-only 커밋은 재동기화 루프를 만들지 않도록 actor+실제 changed paths 또는 결정적 no-op으로 제한한다. source 수정이 동반된 경우에는 단순 actor filtering으로 누락시키지 않는다.

### P2 — Trusted Writer와 검증기

- [ ] 별도 `workflow_run` + `completed` writer를 **default branch의 trusted workflow**로 설계한다. 처음부터 write-enabled 운영하지 않도록 비활성/승인 게이트를 설계한다. source ref를 `GITHUB_REF_NAME`에서 취하지 않는다.
- [ ] 기본 브랜치의 별도 trusted script에서 **`workflow_run` provenance, source repository ID, branch/HEAD SHA, run conclusion, artifact provenance/shape, expected generated-only diff**를 검증한다. 재검증 없는 성공 claim 금지.
- [ ] 모의 artifact로 생성/수정/삭제·크기/경로·symlink·stale SHA·잘못된 source repo·runner 실패·동시성 등을 unit test한다. Artifact 파일을 명령·스크립트로 실행하지 않는다. PR branch의 script/tool/lock을 writer 환경에서 실행하지 않는다.
- [ ] Writer가 결과를 적용할 때도 final `git diff --cached --name-only`/status로 allowed paths만 남는지 검증하고 **`main`은 허용하지 않는다**. Source checkout과 generated artifact를 분리해 복수 쓰기/rename/삭제를 안전하게 처리한다.
- [ ] 커밋 직전 최신 브랜치 SHA 일치와 실제 변경을 다시 확인한다. non-fast-forward나 concurrent source update면 **폐기·재큐잉의 안전성**을 판단하고, 불확실할 경우 실패/수동 복구로 남긴다. `--force`/`--force-with-lease` push 금지.
- [ ] 실제 변경에만 `actions/create-github-app-token`으로 App installation token을 발급한다. `client-id` + `private-key` + `permission-contents: write`를 사용하고 **현재 저장소만** 대상이다. 공식 action의 현재 버전을 검증된 **commit SHA**로 고정한다.
- [ ] bot author/committer는 App slug 기반 실제 bot identity를 사용한다. credential은 push 직전부터 해당 job에서만 접근하고 `persist-credentials: false`, 출력 masking, token 만료/자동 revoke를 확인한다.

### P3 — 독립적인 bootstrap·권한 부여

- [ ] writer가 default branch에 존재해야 하는 `workflow_run` 제약을 반영해 **별도 bootstrap PR**을 필요 시 설계한다. default branch로 disabled/fail-closed trusted writer만 올리는 단계도 보안 control-surface 변경이다.
- [ ] bootstrap PR 자체의 리뷰·merge는 사람이 **명시적으로 승인해야만** 진행한다. 독립적 E2E 검증이 어려우면 승인된 테스트 저장소에서 동일 구조를 우선 검증한다.
- [ ] 사람이 `mols3131d` 소유 GitHub App을 한 repo에 제한 설치하고 `main` 제한 Environment `generated-writeback`의 Variable `GENERATED_SYNC_APP_CLIENT_ID`와 Secret `GENERATED_SYNC_APP_PRIVATE_KEY`를 설정한다. GitHub 요금제에서 Environment 접근 제한을 사용할 수 없는 경우 Repository Secret으로 임의 대체하지 않고 사람의 대안 승인을 받는다. **로컬 에이전트가 개인키를 읽거나 Git·Chat·CI artifact에 기록하지 않는다**. [소유자 절차](13-owner-setup-runbook.md)를 따른다.
- [ ] 실제 writer enable/rollback 스위치가 fail-closed로 작동하는지 확인한다. 변경은 담당자의 승인 후 수행한다.

### P4 — 검증 수렴과 PR 인계

- [ ] [검증 행렬](11-verification-plan.md)의 필수 시나리오를 deterministic test부터 실행하고, 승인된 독립 테스트 브랜치/기존 테스트 PR에서 실제 GitHub event/run 증거를 확보한다.
- [ ] 필요한 `docs/development/ci.md`/`github.md` **정본 정책 반영** 여부를 평가한다. 이 인박스 문서만 정본 반영으로 간주하지 않는다.
- [ ] 구현이 안정되면 PR 본문 `Summary`, `Goal`, `Changes`, `Boundaries`, `Validation` 및 끝의 `author`/`revision.base/head`를 실제 diff/SHA에 맞춰 갱신한다. 해당 저장소의 PR template·provenance 규칙을 준수한다.
- [ ] 독립 리뷰, 실제 required `PR Gate`, 사람의 명시적 최종 승인 전에는 Draft 해제·merge를 자동 실행하지 않는다.

## 진행·커밋 단위

가능하면 다음 의미 단위로 분리한다. 브랜치 충돌·bootstrap 필요성에 따라 PR 분리는 판단하되 **작업을 여러 PR로 나누었다는 사실이 권한 승인이나 검증 완료를 뜻하지 않는다.**

| 단위 | 변경 | 외부 부작용 |
| --- | --- | --- |
| A | Producer 읽기 전용 변경 + deterministic tests | PR branch 코드, 원격 write 없음 |
| B | Trusted verifier/script + 단위 테스트 + disabled writer | 권한 표면 코드, default branch 배포는 별도 승인이 필요 |
| C | GitHub App 운영 정보·설치·Secret 설정 | **사람의 계정 소유권·승인 필요** |
| D | 승인된 격리 E2E/권한 활성화 및 관측 | **실제 봇 push가 발생할 수 있음** |
| E | PR 본문·정본 문서·인수 evidence 동기화 | 리뷰 가능 상태로 인계, 자동 merge 없음 |

실행할 수 없는 단위는 건너뛰어 완료 표시하지 말고 **Blocked + 확인해야 할 사람 작업 + 최소 재개 명령/조건**을 기록한다. 불확실한 권한을 다른 연결이나 계정으로 우회하지 않는다.

## 로컬 검증 명령의 기준

리포지터리 설정을 최신 checkout에서 확인한 후 해당 명령으로 수행한다. 현재 저장소에 `generated sync`/`generated validate`의 직접 Python CLI가 있고 `PR Gate`는 `pytest -q tests`를 실행한다.

```bash
uv run --locked --no-default-groups --group test python -m scripts.generated_artifacts sync
uv run --locked --no-default-groups --group test python -m scripts.generated_artifacts validate --all
uv run --locked --no-default-groups --group test pytest -q tests
```

이 명령은 **실제 실행할 때만 Pass로 기록**한다. Local checkout이 없거나 의존성을 실행할 수 없으면 미검증으로 표시한다. `main`에서 생성 결과를 직접 커밋하지 않는다.

## 중단 조건

- 사람의 독립 승인이 없는데 Secret/write job을 활성화·실행해야 하는 경우.
- branch/repository/actor 인증 주체가 예상과 다르거나 Ruleset 우회 없이는 진행할 수 없는 경우.
- App 토큰이 untrusted Producer 환경으로 넘어가거나 writer가 branch의 미검증 스크립트를 실행해야 하는 경우.
- 원격 HEAD가 바뀌었는데 안전한 재처리 경로를 입증하지 못한 경우.
- 생성 봇 커밋 후 required `PR Gate`가 최신 PR 후보에 실제 성공하지 않은 경우.

문서만 생성한 상태를 implementation done, security approved, E2E passed 또는 merge ready로 해석하지 않는다.
