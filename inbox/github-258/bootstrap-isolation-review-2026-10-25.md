# 개발환경 부트스트랩 조사·다관점 검토 루프 보고서

> **상태:** Review finding / 개선 인계 (비정본). [PR #258](https://github.com/mols3131d/mols-agent-assets/pull/258)의 구현 개선에 이전된 검토 근거이며, 이 문서만으로 코드를 수정하거나 검증을 통과시킨 것은 아니다.
>
> **이관:** 원래 PR #256의 통합 변경을 검토한 당시 기록이므로 아래 revision은 분리 이전의 기준이며, 코드 결함 개선은 PR #258에서 담당한다.
>
> **대상 revision:** base `b29aa490d0c251d5ca478fa5c787b90258f09d79` → head `530bc8b31d543e45ea7470131f705ba33f64388a` (2026-10-25). 이후 브랜치 head 이동 시 재검증이 필요하다.
>
> **정본:** [개발환경 구축·승인 정책](../../docs/development/development-environment.md). [mise 운영 안내](../../docs/references/tooling/mise.md)와 [스킬 원본](../../src/rulesync/.rulesync/skills/mols-dev-env-bootstrap-design/SKILL.md)은 각자의 책임만 소유한다.

## 결론

**현재 Draft PR을 이 상태로 머지하는 것은 권장하지 않는다.** 사용자 요구였던 **설계 전용 Skill**, 개발환경 구축 문서 정본화, 설치 전 사용자 허가, **도구별 관리 주체와 Python 격리 우선**은 문서에 적절히 반영됐다. 그러나 실제 runner에 **3개의 High급 결함/경계 누락**이 남아 있고, 새 정본 문서의 생성 인덱스도 갱신되지 않았다.

| ID | 중요도 | 관점 | 결론 |
| --- | --- | --- | --- |
| F1 | 🟠 High | Git 상태/사용자 변경 보호 | 외부 Git 환경변수가 `update` dirty-lock 검사를 다른 저장소로 우회시킴 |
| F2 | 🟠 High | Python 완전성/환경 상속 | `UV_NO_GROUP=dev`가 `--all-groups`를 무력화하고도 `READY`가 가능 |
| F3 | 🟠 High | Python 격리/재사용 | 기존 `.venv`의 `include-system-site-packages = true`를 허용해 전역 패키지 노출 가능 |
| F4 | 🟡 Medium | 문서 정본/파생 아티팩트 | `docs/development/development-environment.md`가 `docs/INDEX.tsv`에 누락됨 |

F1은 이전 PR 리뷰에도 제출된 문제이며 **이번 revision에서도 수정되지 않았다**. F2·F3은 이번 환경 재사용/격리 토론을 반례로 확장하다 확인했다. F4는 생성물 정합성 문제다. 모든 항목의 실제 영향과 테스트 환경을 아래에 구분한다.

## 검토 범위와 루프 기록

### Loop 1 — Research / 현재 계약 수집

- `CHATBOT.md` → `AGENTS.md` → `.agents/route/ROUTE.md` → `github-context`, `mols-agent-asset`, `mols-loops`, `mols-documentation`과 Skill review 기준을 확인했다.
- [정본](../../docs/development/development-environment.md), [mise 안내](../../docs/references/tooling/mise.md), [`mise.toml`](../../mise.toml), [runner](../../scripts/development_bootstrap.py), [테스트](../../tests/scripts/test_development_bootstrap.py), [Skill](../../src/rulesync/.rulesync/skills/mols-dev-env-bootstrap-design/SKILL.md), [평가 fixture](../../evals/skills/mols-dev-env-bootstrap-design/cases.json), [`docs/INDEX.tsv`](../../docs/INDEX.tsv), PR 리뷰 이력을 교차 읽었다.
- 프로젝트 구현은 exact-pin mise CLI, `uv.lock`을 따르는 프로젝트 `.venv`, `setup`/명시적 `update` 분리다. HOME Skill·Rulesync projection·Git hook 자동 설치는 기본 core 경로에서 제외한다. 사용자의 **실제 설치 승인 확인은 호출 에이전트의 책임**이며 스크립트 자체에는 대화형 승인 게이트가 없다. 이는 정본에 명시된 경계다.
- 버전 semantics 확인: [uv group 우선순위](https://docs.astral.sh/uv/reference/cli/#uv-sync), [uv exact sync](https://docs.astral.sh/uv/concepts/projects/sync/#handling-of-extraneous-packages), [Python venv](https://docs.python.org/3/library/venv.html), [Python site](https://docs.python.org/3/library/site.html), [mise 자동 설치](https://mise.jdx.dev/dev-tools/) 등 공식 문서. 외부 문서의 최신 정보와 PR의 pinned `uv=0.12.1`을 동일한 실행 증거로 간주하지 않는다.

### Loop 2 — Adversarial / 반례 실험

사용자 컴퓨터나 해당 PR checkout은 변경하지 않고 **독립된 임시 디렉터리**에서 다음을 확인했다.

1. **Git 교차 저장소:** 임시 Git 저장소 A의 `uv.lock`을 dirty하게 만들고 저장소 B는 clean 유지. A에서 일반 `git status --porcelain --untracked-files=all -- uv.lock`은 ` M uv.lock`; `GIT_DIR=B/.git`, `GIT_WORK_TREE=B`를 상속시키면 같은 A cwd에서 **출력 없음**.
2. **uv group 상속:** 로컬 `uv 0.10.0`, 임시 Python 3.13 프로젝트, dependency group `dev`의 로컬 wheel `probe-group-tool==1.0.0`으로 네트워크 없이 테스트. `UV_NO_GROUP=dev uv sync --locked --all-groups ...`는 dev 패키지를 설치하지 않았고, 동일 env에서 `uv sync --check --locked --all-groups ...`는 **exit 0**. 변수를 제거하자 패키지 설치 및 import 성공.
3. **시스템 패키지 노출 venv:** `python -m venv --system-site-packages .venv`를 만들고 임시 단순 프로젝트에서 `uv sync --locked`와 `uv sync --check --locked` 실행. 둘 다 성공한 뒤에도 `pyvenv.cfg`는 `include-system-site-packages = true`, Python `sys.path`에는 시스템 패키지 경로가 남았다. 이 시험 역시 로컬 `uv 0.10.0` 기준이다.
4. **문서 인덱스 정적 대조:** 정본 신규 Markdown에는 유효한 `description` frontmatter가 있지만 `docs/INDEX.tsv`에 해당 상대 경로 행이 없다. generator·validator가 docs Markdown source와 `INDEX.tsv`를 대응시키는 코드를 확인했다.

### Loop 3 — Review / 반증·우선순위·범위 정리

- **품질:** core만 `READY`이고 선택적 integration은 명시적으로 제외한 점, `.venv` 외부 링크/절대 경로 차단, 잠금 파일 보존 의도는 적절하다. 그 성공을 모든 환경의 격리·준비 완료로 확대하지 않는다.
- **적대적 관점:** `cwd=self.root`만으로 Git 대상이 고정되지 않으며, `--all-groups`만으로 필요한 그룹이 강제되지 않는다는 반례를 확인했다.
- **성능/단순성:** 추가 프레임워크·범용 전역 도구 탐색·매 도구 승인 시스템은 요구하지 않는다. **기존 Git/uv/관리자 semantics에 맞는 최소 preflight 및 회귀 검사**가 우선이다.
- **문서/권한:** 개발환경 정책은 `docs/development/development-environment.md`, 사용 명령은 mise 안내, 실제 설치 기능은 runner, Skill 행동은 SKILL.md로 소유권 분리되었다. 문서에 허가 정책이 있어도 외부 caller 전체의 실제 승인 준수를 이 리뷰가 보증하지는 않는다.
- **증거 경계:** 로컬 uv가 PR exact pin `0.12.1`과 다르다. F2/F3의 실행 재현은 독립 uv 0.10.0 근거이며, pinned 도구·Windows/macOS 등에서의 완료/실패 결과는 **미검증**이다. 코드의 빠진 보호 조건과 공식 계약은 별도의 정적 근거다.

## Finding 상세

### F1 🟠 High — 외부 Git 환경 상속으로 update 보호 우회

- **근거:** [runner `Bootstrap.__init__`](../../scripts/development_bootstrap.py)은 `self.env = {**env, ...}`로 Git repository 선택 환경을 상속하고 `GIT_OPTIONAL_LOCKS`만 덮어쓴다. [`check_update_state()`](../../scripts/development_bootstrap.py)는 `cwd=self.root`에서 `git status --porcelain --untracked-files=all -- *POLICY_FILES`를 실행하지만 Git이 실제 root를 선택했는지 확인하지 않는다.
- **영향:** 외부 `GIT_DIR`/`GIT_WORK_TREE`가 설정된 셸·Git hook·에이전트 실행에서 다른 clean checkout을 검사해 실제 대상의 수정된 `uv.lock`을 놓칠 수 있다. 이후 `uv lock --upgrade`가 사용자 미커밋 상태를 바꿀 위험이 있다.
- **재현:** Loop 2의 저장소 A/B 테스트. 동일 사안 [기존 PR inline 리뷰](https://github.com/mols3131d/mols-agent-assets/pull/256#discussion_r4367794052).
- **최소 조치:** Git subprocess에 한해 repository/index/worktree 선택용 상속 환경을 제거하고 대상 root를 확인한다. 호출자의 global Git config를 변경하지 않는다.
- **회귀:** dirty A + clean B + 외부 `GIT_DIR`/`GIT_WORK_TREE` 및 `GIT_INDEX_FILE` 변형에서 update가 lock resolution 전에 `BLOCKED`가 되고 A의 작업은 보존돼야 한다.

### F2 🟠 High — UV_NO_GROUP가 설치 대상 및 verify를 동시에 축소

- **근거:** runner `Bootstrap.__init__`은 `VIRTUAL_ENV`, `UV_PROJECT`, `UV_WORKING_DIR`, `UV_CONFIG_FILE`, `UV_PYTHON`, `UV_FROZEN`만 제거한다. **`UV_NO_GROUP`/`UV_NO_DEV`는 상속된다.** `python_environment()`의 설치/검사는 둘 다 `--all-groups`를 사용한다. uv 공식 CLI는 `--no-group`가 `--all-groups`보다 우선함을 명시한다.
- **영향:** `UV_NO_GROUP=dev`라면 `pyproject.toml`의 `dev`에 속한 **Ruff** 등과 이에 포함된 테스트 그룹이 생략될 수 있다. 설치 및 `--check`가 동일하게 축소되어 **`READY`/exit 0의 의미가 무너진다**.
- **재현:** Loop 2에서 단일 로컬 wheel로 dev 누락 및 verify exit 0 확인; uv **0.10.0**, PR pin **0.12.1**은 별도 재현 필요.
- **최소 조치:** 목표 그룹을 바꿀 수 있는 `UV_NO_GROUP`, `UV_NO_DEV` 등 실제 uv 옵션의 상속을 차단하거나 해당 환경이면 명시적으로 fail-closed한다. 전체 `UV_*`를 임의 삭제해 인증/사내 인덱스까지 손상시키는 방식은 피한다.
- **회귀:** `UV_NO_GROUP=dev` 및 `UV_NO_DEV` 상태에서도 계약한 `--all-groups`의 설치/검증을 보장하거나, 누락 시 `READY` 없이 차단. 실제 `uv=0.12.1`에서 먼저 확인.

### F3 🟠 High — 기존 .venv의 system-site-packages 허용

- **근거:** [`check_environment()`](../../scripts/development_bootstrap.py)는 기존 `.venv/pyvenv.cfg`가 일반 파일인지, 일부 내부 디렉터리가 외부 symlink인지 검사하지만 **`include-system-site-packages`의 값은 확인하지 않는다**.
- **영향:** 이미 `--system-site-packages`로 만들어진 `.venv`를 프로젝트 격리 환경으로 오인한다. `uv.lock`으로 동기화한 프로젝트 패키지와 별개로 시스템 설치 패키지가 Python import 경로에 노출될 수 있어 **'전역 Python 의존성을 재사용하지 않는다'**는 신규 정본과 실제 READY 의미 사이에 간극이 생긴다.
- **재현:** Loop 2에서 `include-system-site-packages = true` 상태로 `uv sync --locked`와 `--check`가 성공하고 시스템 site 경로가 남음을 확인. Python 공식 `venv`·`site` 설명도 동일. 로컬 uv **0.10.0** 기반 시험이며 PR pin 재확인 필요.
- **최소 조치:** 기존 venv의 설정을 안전하게 읽고 시스템 패키지 노출을 허용하지 않는 프로젝트에서는 `include-system-site-packages = true`를 **사전 차단**한다. 사용자 기존 venv를 자동 삭제·교체하지 말고 복구 방법과 사용자 승인 범위를 안내한다.
- **회귀:** 정상 격리 venv 허용, `true` venv는 native install 전 `BLOCKED`, symlink·junction 테스트 유지, 실제 Python import 경로 검증.

### F4 🟡 Medium — 문서 정본 신설 이후 INDEX.tsv 누락

- **근거:** [개발환경 구축 정본](../../docs/development/development-environment.md)은 `description` frontmatter가 있는 신규 Markdown인데 [`docs/INDEX.tsv`](../../docs/INDEX.tsv)에 `development/development-environment.md` 행이 없다. [generated artifact sync](../../scripts/generated_artifacts_sync.py)와 [validate](../../scripts/generated_artifacts_validate.py)가 docs source→index 투영/검증을 관리한다.
- **영향:** index 기반 검색이 새 정본을 놓치고, projection freshness 검사에서는 drift가 발생할 가능성이 높다. 앞선 문서 작성 커밋을 CI 통과 상태로 취급하면 안 된다.
- **최소 조치:** 기존 native `mise run generated-sync`로 생성한 결과를 반영하고 `generated-validate`를 실행한다. `INDEX.tsv` 행을 수동으로 고정하지 않는다.
- **회귀:** generated validator에서 정본 경로가 확인되고 다른 docs-index 출력에 불필요한 변경이 없는지 확인.

## 검증 상태 및 인계

| 점검 | 근거 수준 | 상태 |
| --- | --- | --- |
| PR/ref 및 정책·Skill/runner 소스 확인 | GitHub head 직접 조회 | ✅ Pass |
| F1 Git 우회 재현 | 임시 A/B Git repo, 실제 Git 명령 | ❌ Fail — 보호 우회 |
| F2 UV group 우회 재현 | 임시 오프라인 wheel/project, uv 0.10.0 | ❌ Fail — 그룹 누락+check 성공 |
| F3 시스템 패키지 노출 재현 | 임시 venv, uv 0.10.0 | ❌ Fail — 격리 누락 |
| F4 index source/output 대조 | GitHub 파일·validator 정적 분석 | ❌ Fail — 행 누락 |
| 프로젝트 pinned uv 0.12.1에서 F2/F3 | 실제 동일 버전 실행 없음 | ⚪ Not Verified |
| PR head에서 전체 test·generated validate | 저장소 전체 checkout 및 native CI 실행 없음 | ⚪ Not Verified |
| 수정 후 Windows/macOS/Linux setup/update | 수정 자체 없음 | ⚪ Not Verified |
| Skill 추가 11번째 fixture의 실제 모델 평가 | 새 fixture만 추가된 상태 | ⚪ Not Verified |

### 우선 작업 순서

1. **P0:** F1 Git worktree/index 환경 고정 및 dirty-lock 회귀 테스트.
2. **P0:** F2 uv dependency group override 차단 및 실제 도구 버전에서 누락/거짓 READY 재현 테스트.
3. **P0:** F3 기존 venv `pyvenv.cfg` 격리 preflight·회귀. 기존 venv 보존, 무단 reset/삭제 금지.
4. **P1:** F4 docs index를 기존 generator로 재생성하고 validation 수행.
5. **검토 마감:** 수정된 diff에 대해 isolation/permission 관점 재리뷰, 관련 pytest, generated validation, Skill fixture(capability) 평가를 **각각 별도의 근거**로 수집한다. 변동하는 runtime 버전 및 추가 플랫폼은 미검증으로 남긴다.

### 의도적으로 확대하지 않은 범위

- 이 검토는 **보고서 작성** 요청이므로 runner·Skill·lock·OS 설치 코드를 수정하지 않았다. 외부 도구의 전역 설치나 프로젝트 `setup`도 실행하지 않았다.
- 에이전트 설치 승인이 정본에서 호출자 책임이라는 결정은 일관되어 있다. 이를 무조건적인 CLI `--yes`·프롬프트 기능 추가 요구로 확대하지 않는다. **실제 caller 권한 준수는 미검증**이다.
- 사용자가 선호한 Ruff/Biome 최신 업데이트를 모든 도구의 무제한 latest로 바꾸는 일은 별도 버전 정책 결정이 필요하다. 현재 exact-pin CLI update 제한은 이미 공개된 수용 범위이며 본 보고서의 신규 결함으로 중복 계산하지 않는다.
- 실제 기본 경로에서 HOME Skill·Rulesync projection·Git hook을 건드리지 않는 분리는 유지한다. 이 범위에서 OS-level sandbox나 전용 승인 프레임워크를 새로 설계할 필요는 없다.

## 외부 확인 출처

- [uv CLI: dependency group selection and precedence](https://docs.astral.sh/uv/reference/cli/#uv-sync)
- [uv: locking, exact sync, and check](https://docs.astral.sh/uv/concepts/projects/sync/)
- [uv: project environment target](https://docs.astral.sh/uv/concepts/projects/config/#project-environment-path)
- [Python 3.13 venv](https://docs.python.org/3.13/library/venv.html) 및 [Python site](https://docs.python.org/3.13/library/site.html)
- [mise dev tools auto-install](https://mise.jdx.dev/dev-tools/)
