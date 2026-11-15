# CI · Lefthook 품질 게이트 개선 인계

## 목표

로컬 코딩 에이전트의 Lefthook은 빠른 피드백을, GitHub Actions는 **GitHub Plugin·API·웹 UI·클라우드 에이전트의 Hook 없는 변경까지 포함하는 독립 검증**을 맡는다. `main`에서 거부해야 할 오류는 required `PR Gate`에서 차단하고, 검사 선택·설치·실행 비용은 근거에 따라 최소화한다.

- **원칙:** Hook의 통과 여부를 서버 검증의 근거로 쓰지 않는다. Hook과 CI의 중복 제거는 허용하지만 당연히 최적이라고 가정하지 않는다.
- **비목표:** Hook 자동 설치, 일반 소스 자동 포맷·stage, CI commit/push, 유료 LLM 평가 상시화, 새 CI provider·거대 검사 라우터·OS matrix, Ruleset 무단 변경.
- **작업 상태:** 리뷰 지적 2건을 수정하고 정식 setup READY, 프로젝트 환경의 전체 pytest 454개·subtest 4개, 변경 Python의 Ruff 검증을 완료했다. 개선 커밋 `52ce92a9`는 정상 hook을 통과해 기존 PR 브랜치에 push됐고 Branch Check·PR Gate가 성공했다. 후속 인계 문서 변경의 최종 head·run은 PR 본문에서 확인한다. 실제 Windows 래퍼·Git 유형 변경·부분 스테이징 E2E와 사람의 Merge 승인은 별도 경계로 남긴다.

기준: `main` @ `c39d094f72cfb331217bc70abb303c738493dd4c`, 브랜치 `mols/chore/ci-lefthook-quality-gates`. 구현 시작 시 최신 ref와 이미 반영된 변경을 확인하되, 이 PR의 base를 승인 없이 변경하지 않는다.

## 구현 이전 기준선과 근거

| 실행면 | 현행 검증 | 한계 및 유지 사항 |
| --- | --- | --- |
| [Lefthook](../../lefthook.yml) | pre-commit의 staged projection sync, commit-msg validator, pre-push pytest | 로컬 Git에서 **설치된 경우에만** 동작; source 자동 포맷·stage 금지. staged 경로 선택과 실제 worktree/index 내용의 차이를 주의 |
| [Branch Check](../../.github/workflows/branch-check.yml) | non-main push의 frontmatter, pytest, 로컬 projection 3종 | 초기 피드백. 현재 uv만 설정하며 mise/rumdl/Biome은 준비하지 않음. 필수 merge gate는 아님 |
| [PR Gate](../../.github/workflows/pr-gate.yml) | main 대상 PR merge 후보의 frontmatter, pytest, 영향 projection, mise Doctor, Rulesync | required check 유지. 현재 mise는 `install: false` 후 Rulesync에 필요한 도구만 설치 |
| [mise](../../mise.toml), [pyproject](../../pyproject.toml) | Ruff·rumdl·Biome 버전과 formatter write task | Ruff는 `dev` group에만 존재; `test` group에서 사용 불가. `mise run check`는 전체 소스 린트가 아닌 도구/설정 진단 |
| [Projection selector](../../scripts/generated_artifacts_sync.py) · [validator](../../scripts/generated_artifacts_validate.py) | Git 변경 경로를 네 projection에 매핑, git diff 실패 시 전체 검사 | 공통 제어 코드 변경은 매핑되지 않을 수 있음. `--local-only`는 네트워크 의존 repository route 검사를 제외 |
| [Ruleset](https://github.com/mols3131d/mols-agent-assets/rules/21094860) | required `PR Gate`, squash-only, 리뷰 대화 해결 | 승인 리뷰 0개, strict-base 비활성. 운영 정책 검토 사항이며 이번 PR에서 설정 자동 변경 금지 |

구현 이전 기준 실행: [Branch Check](https://github.com/mols3131d/mols-agent-assets/actions/runs/43710194442), [PR Gate](https://github.com/mols3131d/mols-agent-assets/actions/runs/43710198355) 성공. 단일 실행에서 약 12초/29초가 관측되었을 뿐, 새 검사나 비용 개선의 증거는 아니다.

### Authoring 경로별 동작

| 경로 | Hook | 서버 검증 |
| --- | --- | --- |
| 로컬 Git·코딩 에이전트 | 설치 상태에 따라 실행 | push: **head** Branch Check; PR: **merge candidate** PR Gate |
| ChatGPT GitHub Plugin·Contents API·웹 UI | 실행되지 않음 | 정상 push/PR 이벤트 발생 시 동일한 CI 적용. 실제 run 생성 및 required check 상태를 확인 |
| 클라우드 자동화 | 미보장 | 사용 토큰·이벤트 종류에 따라 실행 여부 확인. **`GITHUB_TOKEN` push는 후속 Actions 실행을 유발하지 않음**; `GITHUB_TOKEN`에 의한 특정 PR 이벤트는 승인 대기 실행이 될 수 있음 |

GitHub 공식 근거: [GITHUB_TOKEN의 workflow trigger 예외](https://docs.github.com/en/actions/concepts/security/github_token), [PR merge ref의 SHA 의미](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows). 원격 쓰기 성공이나 agent의 검증 진술을 CI 실행 증거로 간주하지 않는다. 권한을 늘리거나 다른 토큰을 사용하여 이벤트를 강제하는 변경은 자동으로 도입하지 않는다.

## 실패 → 최소 검증 근거

| 실패 유형 | Merge admission | 실행 위치 |
| --- | --- | --- |
| Python·generator·validator 동작 회귀 | 차단 | pytest: PR Gate 필수; Branch Check의 조기 피드백은 비용 비교 후 선택 |
| Frontmatter·source 계약 오류 | 차단 | 기존 validator; 로컬·branch·PR 중 적절한 조기 검사 |
| INDEX/route 산출물 drift, 영향 매핑 실패 | 차단 | PR merge 후보에서 공식 checker; 선택 불가 시 fail-safe 확대. Branch는 local projection 유지 |
| Rulesync 관리 자산의 구조 불일치 | 차단 | 변경 영향에 필요한 strict doctor/dry-run; 기존 PR Gate 유지 |
| Ruff·rumdl·Biome 진단 | **분류 후 결정** | 명시한 안전·파싱·규약 위반만 PR blocking, 단순 스타일은 로컬 피드백/선택적 검사 가능 |
| Hook 설정 문법·실행 불일치 | 관련 변경 시 확인 | `lefthook validate` 및 필요한 동작 테스트. CI가 Hook을 설치/실행했다고 추정하지 않음 |
| LLM 동작/semantic | 변경 위험에 필요한 경우 별도 판단 | 기존 deterministic fixture만 PR 기본 대상, 모델 호출은 필요한 경우에만 한정 |
| commit-msg 규칙 | 추가 검토 | 현재 로컬 Hook만 검사. Plugin/API commit과 squash PR 제목의 적용 필요성을 먼저 확인하고 무조건 gate에 추가하지 않음 |

## 구현 설계 및 적용 순서

1. **기준선·검증 계약:** `mise.toml`, `.rumdl.toml`, `biome.json`, `pyproject.toml`과 기존 소스에서 read-only formatter/linter 결과를 확보한다. `ruff check`/`ruff format --check`, `rumdl check`/`rumdl fmt --check`, `biome format`(read-only) 및 필요시 `biome lint`/범위가 더 넓은 `biome check`를 구분한다. 실제 잠긴 버전의 지원 옵션을 확인한다. **기존 `biome format --write`와 신규 `biome check`를 동등하게 취급하지 않는다.** 적용 범위/강제 여부를 검증 규약별로 정하고 기존 전체 파일을 일괄 수정하지 않는다.
1. **Projection 선택기 보강:** `scripts/generated_artifacts_sync.py`의 공유 매핑을 재사용하면서 `scripts/generated_artifacts.py`, `scripts/generated_artifacts_validate.py` 등 공통 생성·판별 코드의 변경이 필요한 검사 대상으로 확산되게 한다. 경로 자체가 무관한 변경과 영향 판별 실패를 구별한다. `git diff` 실패의 현행 전체 fallback은 보존한다. source 삭제, output 삭제/변경, 공통 코드 변경과 영향이 없는 변경을 `tests/scripts/`에서 테스트한다.
1. **로컬 Hook:** 기존 projection sync/stage를 유지하고, 필요한 staged 파일 정적 검사를 빠르게 추가한다. 읽기 전용 원칙을 지키며 `stage_fixed`와 일반 파일 `git add`는 금지한다. **staged 파일 목록 ≠ index blob 내용**임을 전제로 부분 스테이징, unstaged 수정, 공백/비ASCII 경로, 삭제·이름 변경, 순서·실패 전파의 현재 동작을 확인한다. 인덱스 스냅샷 검사가 과도하면 Hook의 검증 한계를 명시하고 PR Gate의 committed tree 검증을 필수로 남긴다.
1. **서버 CI:** `Branch Check`와 `PR Gate`에서 필요한 정적 검사를 수행하도록 구성한다. Branch는 현재 uv만 있고, PR은 mise는 있으나 Ruff·rumdl·Biome이 준비된 상태가 **아니므로**, 필요한 `uv --group dev`와 pinned mise 도구의 설치 범위를 먼저 설계한다. 각 단계는 최소 권한(`contents: read`), `uv --locked`, read-only 검사를 유지한다. PR Gate의 merge ref/첫 부모 변경 범위와 required check 이름을 보존한다.
1. **중복 비용 판단:** Branch는 head, PR은 merge candidate를 실행하므로 둘을 단순히 "같은 SHA의 중복 테스트"로 간주하지 않는다. 실측 setup 시간·검사 시간·오류 조기 발견·merge 후보 독립성을 비교한다. branch pytest, Rulesync 설치, lint 반복 등은 **실제 이익이 있고 admission 기준이 유지될 때만** 줄인다. 조건부 path filter·추가 workflow·cache/matrix는 필요성이 확인되지 않으면 도입하지 않는다.
1. **정합성:** 정본 의미가 바뀐 문서만 [CI](../../docs/development/ci.md)·[Formatting](../../docs/development/formatting.md)·[Validation](../../docs/development/validation.md)·[Lefthook](../../docs/tools/lefthook.md) 등에 반영한다. 워크플로처럼 통제 표면을 변경한 PR은 별도의 독립 검토 근거와 사람의 명시적 merge 승인을 받는다. Ruleset의 사람 승인/최신-base 설정 변경은 이 PR 범위 밖이다.

## 완료 조건

- [x] GitHub Plugin/API의 대표적인 Hookless commit → branch/PR run 증거를 확보한다. 로컬 Git·웹 UI·클라우드 자동화는 트리거 계약과 실제 검증된 범위를 구분한다. `GITHUB_TOKEN`의 미트리거·승인 대기 예외를 누락하지 않는다.
- [x] Ruff·rumdl·Biome 검사 경로·도구 설치·적용 파일·차단 여부·실패 종료 코드가 구체적으로 검증된다. 기존 순수 스타일을 근거 없이 merge-blocking으로 바꾸지 않는다.
- [x] 생성물 검사에서 공통 코드 변경·source/output 삭제·영향 판별 실패가 누락되지 않고, 무관한 변경은 불필요한 원격 설치를 일으키지 않는다.
- [ ] Hook은 일반 파일을 포맷·stage하지 않으며 부분 스테이징에서 false pass 여부와 한계를 명시한다.
- [x] required `PR Gate`는 merge 후보·read-only 권한·lock 검증·기존 deterministic tests를 유지한다. 신규 검사 실패를 실제 Actions 또는 동등한 신뢰할 수 있는 독립 실행으로 확인한다.
- [x] 유지/제거한 중복 검사는 measured cost와 evidence boundary로 정당화한다. 런타임·model 호출·새 provider는 불필요하게 추가하지 않는다.
- [ ] 관련 정본·구성·테스트의 변경 범위가 일관되며, 통제 표면 수정분은 수정된 검증에 의존하지 않는 리뷰와 사람의 명시적 승인 이후에만 merge한다.

## 구현 결과와 검증 근거

- **Projection:** `scripts/generated_artifacts_validate.py`에서 공통 변경 시 전체 projection 검증으로 확대하고, 해당 선택 규칙의 pytest를 추가했다. 로컬 pre-commit의 generation/stage 범위는 유지했다.
- **공통 검사:** `scripts/source_quality_check.py`가 staged·변경 커밋 범위·전체 tracked 파일을 선택한다. Ruff/rumdl/Biome lint와 format을 각각 읽기 전용으로 검사하며 위반은 0이 아닌 상태로 전파한다. `mise run quality-check` 및 Lefthook이 동일 구현을 사용한다.
- **서버:** Branch Check는 push의 head와 변경 범위, PR Gate는 merge candidate의 변경 범위를 검사한다. PR Gate는 Biome 설정과 변경된 Lefthook 구성을 검증하며, 기존 테스트·Rulesync·lock 단계 및 `contents: read` 권한을 보존한다.
- **성공:** 개선 전 기능 구현은 [Branch Check](https://github.com/mols3131d/mols-agent-assets/actions/runs/43719868355)와 [PR Gate](https://github.com/mols3131d/mols-agent-assets/actions/runs/43719872708)로 검증했다. 이번 셀프 리뷰 수정은 [Branch Check](https://github.com/mols3131d/mols-agent-assets/actions/runs/43722514733) 및 [PR Gate](https://github.com/mols3131d/mols-agent-assets/actions/runs/43722518956)에서 확인했고, pytest **451개**, frontmatter, projection 4종, Rulesync, Biome·Lefthook 설정 검증이 통과했다.
- **실패 감지 증거:** [PR Gate 실패 사례](https://github.com/mols3131d/mols-agent-assets/actions/runs/43718613641)에서 실제 Ruff·rumdl 위반으로 검사 단계가 실패했으며, 해당 파일 수정 후 통과했다. 검증 실패를 무시하거나 autofix로 덮지 않는다.
- **비용 비교:** 종전 별도 커밋의 대표 실행에서 Branch Check 12초·PR Gate 29초, 확장 검사 이후 성공 실행에서 31초·54초를 관측했다. 설치·검사 범위가 늘어난 비용이며 **속도 개선 근거가 아니다**. 변경 파일 범위 검사를 적용하고 기존 branch/PR의 독립 테스트를 유지하는 결정을 우선했다. 단일 표본 비교는 장기 성능 추세가 아니다.
- **남은 경계:** 실제 로컬 Lefthook 설치·실발화·부분 스테이징 E2E 및 통제 표면의 독립 검토·사람 승인. Draft 상태를 유지하고 Merge하지 않는다.

## 셀프 리뷰 개선 결과

1. **Staged 내용과 worktree 내용의 불일치 (수정):** 이전 품질 검사는 경로만 index에서 선택해 부분 스테이징의 잘못된 통과 가능성이 있었다. 이제 검사 대상의 unstaged 변경이 겹치면 실패한다. 선택된 소스가 삭제됐거나 심볼릭 링크이면 검사를 생략하지 않고 실패한다. 실제 Git index를 사용하는 회귀 테스트 3개를 추가했다.
1. **새 브랜치·force-push의 비교 기준 (수정):** Branch Check에서 `github.event.before`가 0이거나 없는 커밋이면 `origin/main`과의 merge-base를 사용한다. 공통 조상이 없으면 전체 tracked 소스를 검사해 조용히 넘어가지 않는다.
1. **표현 규약과 CI 계약 (정합성 수정):** [CI 정본](../../docs/development/ci.md)에 *추가·수정된 파일*의 lint/format을 명시적 병합 계약으로 기록했다. 저장소 전체의 기존 스타일을 일괄 정리하지 않는다.
1. **중복 제거 (유보):** Branch의 head와 PR의 merge 후보는 증명 대상이 달라 pytest 이중 실행을 유지한다. 검사 추가로 총 시간이 증가했으므로 순수 성능 최적화로 간주하지 않는다.

**검증:** [Branch Check](https://github.com/mols3131d/mols-agent-assets/actions/runs/43722514733)와 [PR Gate](https://github.com/mols3131d/mols-agent-assets/actions/runs/43722518956) 모두 성공. PR Gate에서 deterministic pytest 451개 통과.

**잔여 경계:** 실제 개발자 장비의 `lefthook install`/Hook 실행과 부분 스테이징 E2E는 검증하지 않았다. Hook 설치는 opt-in이며, 통제 표면의 독립 검토와 사람의 Merge 승인 역시 남아 있다.

## 리뷰 후 개선 루프 및 후속 인계

검토 기준은 base `c39d094f72cfb331217bc70abb303c738493dd4c`, head `8c3d1a0d7546f42ed874f5e5bba27f2ffbee8bed`다. 전용 작업 브랜치를 해당 head로 fast-forward한 뒤 수정 → 회귀 검증 → 직접 재검토 1회를 수행했다. 수정된 workflow의 성공을 독립 검토나 사람의 승인으로 간주하지 않는다.

### 수정한 지적

- **Windows npm 실행 경로:** [source quality checker](../../scripts/source_quality_check.py)의 `_run()`이 명령 이름을 그대로 전달하면 Windows에서 npm `.cmd` 래퍼 대신 다른 `.exe`를 찾거나 실행에 실패할 수 있었다. 기존 formatter의 경로 해석 패턴을 따라 `shutil.which()`로 먼저 해석한 경로를 전달하고, 도구가 없으면 명시적인 오류를 반환하도록 했다. 인수와 도구 종료 코드의 전달은 유지했다.
- **Git 유형 변경 누락:** staged·committed 선택기의 `--diff-filter=ACMR`이 `T`를 제외해 일반 파일 ↔ symlink 변경이 안전 검사에 도달하지 않았다. 두 경로 모두 `ACMRT`로 바꿔 유형 변경을 포함하고, 선택된 symlink는 기존 guard에서 거부한다. 삭제 제외와 staged/unstaged 충돌 검사는 유지했다.
- [기존 품질 검사 테스트](../../tests/scripts/test_source_quality_check.py)에 표준 라이브러리 `unittest` 3개를 추가했다. 해석된 Windows 래퍼 경로·공백 인수·실패 종료 코드 전달, 도구 누락의 오류 보고, staged/committed × 일반 파일/symlink의 유형 변경 선택을 검증한다. [Formatting 정본](../../docs/development/formatting.md)에 변경된 검사 계약을 반영했으며 workflow·도구 버전·lock은 바꾸지 않았다.

### 검증 증거와 한계

- ✅ Pass — `python -m unittest tests.scripts.test_source_quality_check.SourceQualityRegressionTests -v`: 수정 전 테스트 3개에서 실패 사례 6개를 확인했고, 수정 후 3개 모두 통과했다. 유형 변경 테스트는 4개 subcase를 포함한다. 실행 Python은 기존 uv 관리 CPython 3.13.11이며 site-packages나 외부 도구를 테스트 의존성으로 사용하지 않았다.
- ✅ Pass — 기존 `test_chosen_tools_do_not_mutate_files_or_confuse_format_and_lint()` assertion을 직접 실행해 도구 선택·읽기 전용 인수가 유지됨을 확인했다. 변경 Python 2개 파일의 AST parsing과 88열 점검, `git diff --check`도 통과했다.
- ✅ Pass — 게시 준비에서 설치된 pinned rumdl 0.3.2의 `rumdl check --no-cache .inbox/github-305/00-plan-ci-quality-gates.md docs/development/formatting.md`와 `rumdl fmt --check --no-cache .inbox/github-305/00-plan-ci-quality-gates.md docs/development/formatting.md`가 통과했다. 전체 소스 검사나 실제 Hook E2E 결과로 확대하지 않는다.
- ✅ Pass — 사용자 재시도 요청 후 `mise run setup --dry-run`, `mise run setup`이 성공했다. Setup은 exact CLI 7종의 설치 경로·버전과 `uv sync --locked --all-groups`, `uv sync --check`를 확인해 **READY**를 반환했다. 프로젝트 `.venv`에서 PyYAML 6.0.3·Ruff 0.15.15·pytest 9.0.3의 존재를 확인했고 manifest·lock 변경은 없다. `update`, 외부 Agent Asset·HOME Skills·Git hook 설치는 실행하지 않았다.
- ✅ Pass — `mise exec -- uv run --locked --no-sync --no-default-groups --group dev pytest -q tests/scripts/test_source_quality_check.py tests/scripts/test_generated_artifacts_validate.py tests/scripts/test_changed_files_format.py`: **25 passed, 4 subtests passed**.
- ✅ Pass — `mise exec -- uv run --locked --no-sync --no-default-groups --group dev pytest -q tests`: **454 passed, 4 subtests passed**.
- ✅ Pass — `mise exec -- uv run --locked --no-sync --no-default-groups --group dev ruff check scripts/source_quality_check.py tests/scripts/test_source_quality_check.py` 및 `mise exec -- uv run --locked --no-sync --no-default-groups --group dev ruff format --check scripts/source_quality_check.py tests/scripts/test_source_quality_check.py`: lint 통과, Python 2개 파일의 format 일치.
- ⚪ Not Verified — 실제 Windows npm 래퍼 실행·실제 Git 유형 변경 fixture·Hook 전체의 부분 스테이징 E2E. 래퍼와 유형 변경의 동적 재현은 앞선 리뷰에서 권한 제한으로 거부됐다. 새 회귀 테스트는 외부 실행과 Git 상태·symlink 여부를 모킹하므로 실제 런타임 동작의 증거로 확대하지 않는다.
- ✅ Pass — 개선 커밋 `52ce92a9b8a7f7afa0bea1700582a48cad94e715`의 정상 pre-commit(`generated-artifacts`, Ruff·rumdl source quality), commit-msg(`conventional`), pre-push(`repository-tests`: **454 passed, 4 subtests passed**)가 pinned Lefthook 2.2.2에서 성공했고 기존 PR 브랜치에 fast-forward push했다. `gh pr checks 305 --repo mols3131d/mols-agent-assets --watch --interval 10`으로 [Branch Check](https://github.com/mols3131d/mols-agent-assets/actions/runs/43745717947) **32초**, [PR Gate](https://github.com/mols3131d/mols-agent-assets/actions/runs/43745724017) **52초** 성공을 확인했다.
- 이전 head `8c3d1a0`의 [Branch Check](https://github.com/mols3131d/mols-agent-assets/actions/runs/43722810166)·[PR Gate](https://github.com/mols3131d/mols-agent-assets/actions/runs/43722814677)와 pytest 451개 결과는 위 후속 수정의 근거와 구분한다. 인계 문서 갱신 이후의 최신 head·run은 PR 본문이 소유한다.

### 환경 준비 누락과 차단 해소

PyYAML은 이미 `test`, Ruff는 `dev` 그룹에 선언돼 있고 `dev`가 `test`를 포함한다. 의존성 선언 누락이 아니라 현재 작업 트리의 개발환경을 준비하지 않은 것이 이전 hook 실패의 원인이었다. 별도 임시 환경의 초기 리뷰 테스트를 현재 작업 트리의 환경 준비 완료로 간주하지 않는다.

- 최초 정상 `git commit`은 기존 pre-commit hook의 `ModuleNotFoundError: No module named 'yaml'`, `Required source quality tool not found: ruff`로 실패해 커밋이 생성되지 않았다. 자동 의존성 동기화를 막았어도 uv가 빈 `.venv`를 생성했고, 기존 Lefthook 2.1.10은 shared hook sync를 수행했다고 출력했다. Hook 우회·signing 비활성화·API 대체 커밋은 하지 않았다.
- 앞선 실행에서는 `mise exec -- uv run --locked --no-sync --no-default-groups --group dev pytest --version`, 뒤이은 `mise run setup --dry-run` 포함 사전 점검, `gh pr edit 305 --repo mols3131d/mols-agent-assets --body ...` 상태 보고가 실행 권한으로 거부됐다. 당시에는 재시도·우회하지 않고 중단해 상태를 보존했다.
- 이후 사용자의 명시적인 "다시 시도해봐" 요청으로 재시도했고 정식 setup과 위 전체 테스트가 성공했다. 정상 hook 경로로 개선 커밋·push 및 새 CI 확인까지 완료해 환경·게시 blocker를 해소했다. Hook 우회·amend·force-push·merge는 하지 않았다. 최종 head와 CI 증거는 PR 본문과 Git 이력이 소유한다.

### 남은 인계

- 환경 준비·개선 커밋·push·서버 검증의 인계는 완료했다. 후속 작업에서는 PR의 최신 head·run을 확인하고 서버 증거와 로컬 E2E 미검증을 구분한다.
- 실제 Windows npm 래퍼와 Git 유형 변경 fixture·로컬 Hook E2E는 허가된 환경에서 별도로 검증한다. Hook 설치·환경 설치·Ruleset 변경·merge 권한을 이번 인계나 push 요청에서 추론하지 않는다.
- Draft를 유지한다. 코드 리뷰와 후속 직접 재검토는 수행했지만 GitHub 승인 리뷰나 사람의 명시적 merge 승인을 대신하지 않는다.

## 인계

이 파일은 비정본 작업 인계 및 검증 기록이다. 최종 검토·추가 구현 전에 [GitHub 정책](../../docs/development/github.md)과 해당 경로 `AGENTS.md`를 확인한다. 필요하면 `mols-ci-design` 및 `mols-loops`의 원본을 적용한다. PR의 체크박스는 **구현을 끝낸 항목만** 완료 처리한다. 실행하지 않은 테스트와 측정하지 않은 비용은 통과·개선으로 보고하지 않는다.
