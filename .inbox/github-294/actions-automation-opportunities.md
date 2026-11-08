# PR #294 — GitHub Actions 추가 자동화 후보 조사

## 결론과 범위

**우선 해결할 문제는 새 workflow 개수가 아니라 `generated-sync.yml`의 자동 커밋 이후 PR 검증 공백이다.** 이후에는 기존 CLI·hook으로 이미 정의한 계약을 API·ChatGPT 변경 경로에서도 검증하도록 보완하는 순서가 비용 대비 효과가 크다. 새로운 bot 계정, PAT, 외부 서버, 자동 merge, 광범위한 model eval은 기본안에서 제외한다.

- 조사 대상: [`mols3131d/mols-agent-assets`](https://github.com/mols3131d/mols-agent-assets), [Draft PR #294](https://github.com/mols3131d/mols-agent-assets/pull/294), `main` 및 `mols/chore/generated-sync-on-push`.
- 조사 기준: 2026-11-09; PR head `bf2968a09157d8d7e558968d925c116f78db451d`, main `fa5be3bd63e9c29c30017b9e8c833018c092b9a7`. 후속 커밋이 생기면 재확인한다.
- 종류: **설계 후보·의사결정용 조사 기록(비정본)**. 새로운 workflow나 Ruleset 변경을 구현·승인한 문서가 아니다.
- 권한/경계 정본: [CI 정책](../../docs/development/ci.md), [GitHub 정책](../../docs/development/github.md), [VCS 정책](../../docs/development/vcs-git.md), [PR #294 handoff](handoff.md). 이 문서는 재정의하지 않는다.

## 이미 존재하는 자동화 — 중복 방지

| Surface | 현재 실제 역할 | 남는 경계 |
| --- | --- | --- |
| [`branch-check.yml`](../../.github/workflows/branch-check.yml) | non-main push마다 frontmatter, 전체 pytest, local generated projection 드리프트 검사(읽기 전용) | commit-msg/formatter 미포함; repository-local 외부 route 전체 검증은 제외 |
| [`pr-gate.yml`](../../.github/workflows/pr-gate.yml) | main 대상 PR에서 frontmatter, pytest, affected projection, mise doctor, Rulesync 구조 검증. required `PR Gate` | bot 추가 커밋 직후 새 required run 생성 보장 없음 |
| [`lefthook.yml`](../../lefthook.yml) | local pre-commit: staged 영향 projection sync; commit-msg validator; pre-push: pytest | GitHub Contents API/ChatGPT/GitHub UI write에는 로컬 훅이 실행되지 않음 |
| [`mise.toml`](../../mise.toml) | `generated sync/validate`, `format-changed`, `check`, `eval`, `skills-sync` 등 공통 실행 진입점 | 일부 작업은 명시적으로 실행할 때만 수행 |
| [PR #294의 `generated-sync.yml`](../../.github/workflows/generated-sync.yml) | 관련 source push → `sync` → `validate --all` → generated-only commit(`GITHUB_TOKEN`) | 실제 E2E 미검증, 새 bot commit 이후 required check 공백; 이 PR은 아직 Draft |

## 우선순위: 신규 자동화 및 보완 후보

| 순위 | 후보 | 제안 시점/형태 | 효과 | 비용·위험 및 판단 |
| --- | --- | --- | --- | --- |
| **P0 / 선행 결정** | **#294 자동 커밋 ↔ PR Gate 연계** | source push 후 생성 파일 커밋이 일어난 경우 최신 head 검사 보장 | merge-blocking 검증 공백 해결 | 기존 토큰으로는 이벤트 재트리거가 제한됨. 새 이벤트만 더 붙여 해결됐다고 주장 금지. **먼저 설계 결정** |
| **P1 / 개선** | **영향받은 projection만 생성** | #294의 push workflow 내부에서 changed-path 선택 | docs-only 편집마다 무관한 route/외부 fetch 실행 감소 | 기존 `select_projections` 재사용; `sync --staged`는 clean checkout이라 그대로 쓰면 안 됨; 영향 불확실 시 all fallback |
| **P1 / 보완** | **원격 commit message 검증** | PR Gate에서 PR에 포함된 commit 대상 read-only check | ChatGPT/API commit이 local `commit-msg` 훅을 우회하는 문제 해소 | 기존 [validator](../../scripts/commit_message_validate.py) 재사용; merge-generated commit/자동 bot commit 예외와 squash 정책 조정 |
| **P2 / 조건부** | **변경 파일 포맷 read-only 확인** | PR Gate 또는 nonblocking branch feedback에서 changed-only | 수동 `format-changed` 누락 조기 발견 | `ruff`, `rumdl`, `biome` 추가 설치/시간. 순수 스타일을 무조건 merge blocker로 올리지 말 것 |
| **P2 / 선택** | **lock/Skill dependency dry-run 검사** | `skills-lock.json`, `rulesync.lock` 등 영향 때만 `skills-sync --dry-run` | 외부 Skill adapter·lock 계약 오류 조기 발견 | `mise doctor` 및 기존 Rulesync 검사와 실제 coverage 중복 여부 먼저 측정; native installer 자동 실행/lock update 금지 |
| **P3 / 선택** | **주기적 전체 projection health check** | 주 1회 또는 `workflow_dispatch`에서 main `validate --all`, read-only | PR과 무관한 외부 route 접근 실패/드리프트 관찰 | pinned external source 확인은 네트워크 실패·노이즈 발생 가능; 변경 없는 정상 저장소에서는 효용 제한. Issue/자동 커밋 남발 금지 |
| **P3 / 보류** | **Promptfoo smoke/eval 수동 실행** | `evals/`·관련 source 변경에만 수동 또는 선택적 job | 선택된 behavioral fixture 점검 | [evals README](../../evals/README.md)에 모델 없는 smoke는 있으나 전체 runtime eval은 provider/Ollama/credential/비용·외부 전송 조건이 존재. 기본 PR Gate 자동 편입 비추천 |

### P0 — required check는 일반적인 수동 재실행으로 해결되지 않음

- GitHub 공식 문서: 기본 [`GITHUB_TOKEN`의 이벤트](https://docs.github.com/en/actions/concepts/security/github_token)로 만든 **push**는 새로운 `push`/`pull_request` workflow run을 만들지 않는다(예외 trigger는 따로 존재). PR #294에서 최초 source push로 실행된 gate는 추가 bot commit에 대한 별도 검증을 대신하지 못할 수 있다.
- 더 중요한 제한: [required status check 문서](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks)에 따르면 `workflow_dispatch`로 돌린 **Actions job check 자체는 PR의 required check를 충족하지 않는다**. 따라서 'generated-sync에서 `workflow_dispatch`로 PR Gate를 한 번 더 실행'하는 방식만으로 P0를 해결했다고 보지 않는다.
- 선택지:
  1. **최소 변경 수용:** #294를 자동 *생성/커밋*까지만 맡기고, 최신 required `PR Gate`가 없으면 사람이 정상 PR event를 유발할 수 있는 리뷰 가능한 새 커밋을 push해 검증. 자동 검증 완료까지 보장하지 못한다고 명시.
  2. **완전 자동 필요:** 새 PR/브랜치 워크플로 아키텍처 또는 GitHub App 인증 방식을 별도 설계·리뷰하고, required check를 실제 head/merge candidate에 대해 어떻게 보장하는지 통합 테스트로 검증. **GitHub App은 선택지일 뿐 필수 조건으로 미리 고정하지 않는다.**
- 둘 다 기존 Ruleset `PR Gate` requirement를 제거하거나 성공 상태를 위조하지 않는다. 사용자의 'App 없이 단순한 Actions' 선호를 기본 제약으로 둔다. 현재 단계에서는 1을 임시 운영안으로 보고, 완전 자동화를 요구하면 2를 별도 의사결정으로 올린다.

### P1 — 영향 기반 생성: 스크립트를 재사용하되 CI 전용 의미를 복제하지 않기

- [`generated_artifacts_sync.py`](../../scripts/generated_artifacts_sync.py)는 `select_projections(paths)`와 docs/catalog/distribution/repository 4개 projection별 source mapping을 이미 제공한다.
- #294의 `sync`는 매번 **전체** projection을 생성한다. [`routes_repository_generate.py`](../../scripts/agent_assets/routes_repository_generate.py)는 잠긴 외부 GitHub Skill 원본을 fetch하는 경로가 있어, 단순 `docs/` 편집에도 불필요한 외부 네트워크 의존이 생긴다.
- 실행안을 검토한다면 CLI에 **원본 branch diff 기반 선택 옵션**을 신설해 기존 `select_projections`만 재사용하고, diff 획득 실패·공통 스크립트 수정·원본 매핑 미확인 시 전체 생성/검증을 수행해야 한다. local `--staged`를 그대로 부르면 runner의 staged set은 비어 **생성 작업을 건너뛸 수 있으므로 금지**.
- 수락 조건: docs-only 변경은 docs-indexes만 생성; `rulesync.lock` 변경은 repository-routes; 공통 generator source 변경은 관련 dependent 모두; 알 수 없는 diff는 fail-safe; 실제 생성 결과와 committed output 일치.

### P1/P2 — 중복 검사보다 'API write gap'을 좁히기

- **Commit 규칙:** local hook이 쓰는 [`scripts/commit_message_validate.py`](../../scripts/commit_message_validate.py)를 PR 커밋 열거에 재사용한다. `git log`로 대상과 base 범위를 명확히 하고, merge/squash 임시 커밋의 목적이 다름을 반영한다. 기존 validator를 두 번째 YAML regex로 복제하지 않는다.
- **Formatter:** [`scripts/changed_files_format.py`](../../scripts/changed_files_format.py)는 **쓰기 명령**이므로 PR 체크에서 직접 실행하지 않는다. 변경 파일 목록을 얻어 formatter의 `--check` 같은 읽기 전용 동작만 사용한다. 포맷은 semantic correctness와 다르므로 필요하면 nonblocking 결과부터 시작.
- **Dependency sanity:** [`skills_sync.py`](../../scripts/agent_assets/skills_sync.py)의 `--dry-run`은 설치가 아니라 계획 검토에만 사용한다. 모델/API 호출·패키지 자동 업그레이드·서드파티 설치를 PR Gate에 암묵 추가하지 않는다.

## 별도로 만들지 말 것

- 프런트매터, pytest, Rulesync 구조 검증, generated drift의 **동일 의미**를 가진 별도 Actions: 기존 `Branch Check`/required `PR Gate`가 이미 소유한다.
- 기본 토큰으로 자동 PR 댓글/Issue/merge를 반복해 후속 CI를 속이는 장치: 인증·트리거 경계를 우회하지 못하고 노이즈와 권한 위험만 증가한다.
- `main` 병합 후 자동 생성 커밋: 이 저장소의 `main` 직접 수정 금지·PR 입장 검증과 충돌.
- 무조건적인 자동 formatter write-back 또는 모든 Skill에 대한 비싼 모델 evaluation: 의도하지 않은 diff, provider 비용, 불필요한 blocking을 만든다.
- Path filter가 달린 workflow를 그대로 required check로 지정: [skipped required check](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/skip-workflow-runs)가 Pending으로 남아 병합을 차단할 수 있다. 조건부 작업은 required 상위 job에 안전하게 내장하는 편이 낫다.

## 이행 제안 및 인계

1. **#294 Draft의 P0 의사결정**을 먼저 한다. 자동 생성만으로 충분하면 bot commit 후 검증 절차를 문서로 운영하고, 완전 무인이 목표라면 별도 검토 후 구조 변경. [기존 리뷰 브리프](review-brief.md)와 [인계](handoff.md)가 이 작업의 정본이 아닌 진행 근거다.
2. P0가 정리되면 **영향 기반 생성**부터 별도 변경으로 구현·테스트한다. 실제 비용이 크지 않으면 전체 생성 유지가 더 단순할 수 있으므로 실행 시간과 외부 fetch 실패 빈도를 먼저 관찰한다.
3. **Commit message validator**는 작은 PR로 기존 `PR Gate`에 read-only 추가해 API 경로를 보강한다. 위반이 merge-critical이라고 합의했을 때만 required gate 실패로 반영.
4. **Formatter/lock dry-run**은 중복·실행 비용을 확인한 뒤 필요할 때만 선택한다.
5. **Scheduled health check / Promptfoo**는 운영상 문제나 반복적 수동 비용이 확인될 때 `workflow_dispatch` 또는 비차단으로 시범 도입한다.
6. 새 권한이 생기는 workflow 추가/수정은 기존 [GitHub 정책](../../docs/development/github.md)에 따라 독립 검토와 사람의 명시적 승인이 필요하다. `main`은 직접 변경하지 않는다.

### 다음 작업자의 검증 기준

- 조사에서 '이미 자동화된 일'과 '새로 추가할 일'이 구분되는가?
- 각각 어떤 이벤트/경로에서 실행되고 어떤 실패를 방지하는가?
- Required `PR Gate`의 검증이 최신 head/merge candidate에 남는가?
- 권한은 read-only를 기본으로 하고 유지보수 write와 분리했는가?
- `GITHUB_TOKEN` recursion, `workflow_dispatch` required-check 불인정, path-filter Pending을 해결 없이 우회했다고 주장하지 않는가?
- CI 실행을 실제 측정하지 않았다면 비용·성능 절감을 '예상 효과'로 표기했는가?

## 1차 근거

- Repository: [Branch Check](../../.github/workflows/branch-check.yml) · [PR Gate](../../.github/workflows/pr-gate.yml) · [Lefthook](../../lefthook.yml) · [Mise tasks](../../mise.toml) · [Generator](../../scripts/generated_artifacts.py) · [Validator](../../scripts/generated_artifacts_validate.py)
- GitHub: [`GITHUB_TOKEN` recursion](https://docs.github.com/en/actions/concepts/security/github_token) · [Required checks](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks) · [Workflow path filters](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) · [Scheduled workflow limitations](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows)
