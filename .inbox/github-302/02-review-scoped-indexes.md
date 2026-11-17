# PR #302 — 다관점 리뷰 보고서

> [!IMPORTANT]
> **조건부 보류 (`🟡 Medium` 1건 · `🔵 Low` 3건)** — `docs/`·`catalog/` 범위별 `INDEX.tsv` 전환(14개 인덱스, 전후 엔트리 `docs` 47건·`catalog` 40건 완전 일치), 단일 [`indexes_generate.py`](../../scripts/indexes_generate.py) 통합, 동기화·검증 연동과 `pytest` 465개·`PR Gate` 통과를 확인했습니다. 저장소 기본 프리셋(`depth=0`)에는 블로커가 없으나, PR이 새로 바꾼 [`generate_index.py`](../../src/rulesync/.rulesync/skills/mols-markdown-maintenance/scripts/generate_index.py)의 `_is_excluded`가 `/`를 넘어 매칭해 `--depth -1`·`--root`·공유 Skill 호출에서 경로 스코핑 및 숨김 디렉터리 일관성이 깨지는 결함(`F1`)이 있고, 통제 표면 변경에 대한 사람의 명시적 승인이 필요합니다. 이 문서는 `.inbox/`의 비정본 작업 근거이며 사람의 승인이나 GitHub PR Review를 대신하지 않습니다.

- **Target** — [PR #302](https://github.com/mols3131d/mols-agent-assets/pull/302) (`mols/feat/scoped-indexes`, 40 files changed, +1459 / -884)
- **Revision** — `c39d094f72cfb331217bc70abb303c738493dd4c..7ae40bad461b0ed1c330becffd7d316c3a231ebb`
- **Scope** — `main`(`c39d094f`) 대비 PR #302(`7ae40bad`) 전체 변경분(인덱스 생성기 통합, `mols-markdown-maintenance` 공유 스크립트 수정, `generated_artifacts` 동기화·검증, `docs/`·`catalog/` 14개 `INDEX.tsv` 및 문서·신설 `README.md`, `prj-workflow-pattern` 워크플로, 테스트 스위트 재편)

## Findings

### F1 · 🟡 Medium — 변경된 `generate_index._is_excluded`의 `/` 넘김 `fnmatch` 매칭으로 `/` 스코핑 및 숨김 디렉터리(`.internal/`) 일관성이 깨짐

- **Evidence** — PR #302는 [`generate_index.py`](../../src/rulesync/.rulesync/skills/mols-markdown-maintenance/scripts/generate_index.py) 30–42행의 `_is_excluded`를 수정해 선행 `/` 루트 앵커링과 `/` 포함 패턴의 `relative_path` 한정 매칭을 도입했고, [`indexes_generate.py`](../../scripts/indexes_generate.py) 158행에서 `exclude_globs=[".*.md", "__*__.md", *blocked_root_subtrees, *empty_directories]`를 넘깁니다. 그러나 Python `fnmatch.fnmatch`는 `*`가 `/`를 넘어 매칭하므로, 선행 `/` 패턴(`/*.md`)이 루트 직속 외에 `nested/guide.md`까지 제외하고(`True`), `/`가 없는 패턴(`".*.md"`, `"__*__.md"`, `"test*.md"`)도 38–40행의 `or fnmatch(relative_path, pattern)` 분기 때문에 `.internal/guide.md`, `__dir/foo__.md`, `testing/guide.md`를 제외합니다. 반면 `indexes_generate.py` 75–84행의 `_is_content_file`과 [`generated_artifacts_sync.py`](../../scripts/generated_artifacts_sync.py) 49–93행(`_is_docs_index_source`·`_is_catalog_index_source`)은 파일 basename(`path.name`)만 검사합니다. 그 결과 `.internal/README.md`와 `.internal/guide.md`가 있을 때 `depth=0`과 `depth=-1` 모두 `.internal/INDEX.tsv`와 루트 `INDEX.tsv`의 `.internal/` 행을 생성하지만, `--depth -1`·`--depth >= 1`에서는 `.internal/guide.md`만 루트 인덱스에서 조용히 탈락합니다(Python 3.13 직접 재현 확인; PR에 포함된 [01-review-triage.md](01-review-triage.md) 12행의 `F4` 상태도 `.internal/` 미해결 상태에서 `수용`으로 남아 있습니다).
- **Impact** — 현재 저장소의 `docs/`·`catalog/` 프리셋(`depth=0`, dot-prefixed 하위 디렉터리 없음)에서는 드러나지 않지만, `--depth -1`·`--root` 옵션 사용자와 재사용 Skill `generate_index` 호출자가 기대하는 `/` 경로 스코핑 및 숨김 디렉터리 처리 계약이 어긋납니다.
- **Action** — `_is_excluded`에서 `/`가 없는 패턴은 `path.name`만 비교하거나 세그먼트 경계를 지키는 매칭으로 바로잡아 `/*.md`·`test*.md`의 `/` 초과 매칭을 막고, dot-prefixed 디렉터리를 허용할지 제외할지 `_is_content_file`·`_targets`·`generated_artifacts_sync.py` 간 규칙을 통일합니다(함께 커밋된 `01-review-triage.md` `F4` 기록도 실제 상태에 맞춥니다).

### F2 · 🔵 Low — PR #302의 `_is_excluded` 수정에 `fnmatchcase` 및 `--exclude-glob --help` 갱신이 빠짐

- **Evidence** — PR #302는 [`generate_index.py`](../../src/rulesync/.rulesync/skills/mols-markdown-maintenance/scripts/generate_index.py) 140행과 [`indexes_generate.py`](../../scripts/indexes_generate.py) 194행의 정렬에서 Windows 대소문자 무시로 인한 OS 간 출력 차이를 수정했지만, 같은 PR에서 새로 작성한 `_is_excluded`(33–40행)는 `fnmatch.fnmatch`를 유지해 Windows에서만 대소문자를 무시합니다(예: `exclude_globs=["/assets/**"]`가 Windows에서 `Assets/guide.md`를 제외하고 Linux CI에서는 유지함). 또한 [`SKILL.md`](../../src/rulesync/.rulesync/skills/mols-markdown-maintenance/SKILL.md) 54행이 glob 옵션 명세를 `--help`에 위임하는데, 새로 도입한 선행 `/`·`/` 포함 패턴의 basename 제외 규칙이 `generate_index.py` 476행 `--exclude-glob` help 문자열(`"Exclude entries when basename or relative path matches a glob"`)에 반영되지 않았습니다.
- **Impact** — 저장소 `docs/`·`catalog/`는 소문자 경로만 사용해 당장 실패하지 않지만, 재사용 Skill `mols-markdown-maintenance`의 Windows/POSIX 결과 동등성과 `--help` 계약 설명이 부족합니다.
- **Action** — `_is_excluded`를 `fnmatch.fnmatchcase`로 바꾸고 `--exclude-glob` help 문자열에 `/` 경로 스코핑 규칙을 명시합니다.

### F3 · 🔵 Low — PR #302가 신설한 `README.md` 3종의 `src/<vendor>/` 누락 및 `description` 범위 불일치

- **Evidence** — PR #302가 추가한 [`docs/skills/README.md`](../../docs/skills/README.md) 9행과 [`docs/development/agent-assets/skills/README.md`](../../docs/development/agent-assets/skills/README.md) 11행은 Skill 작성 원본 위치를 `src/rulesync/.rulesync/skills/`와 `.rulesync/skills/` 두 곳만 안내해, [Source Authority](../../docs/development/source-authority.md) 78–82행·`AGENTS.md`가 정한 `src/<vendor>/`를 빠뜨렸습니다(실제로 `docs/skills/mols-chatgpt-chat-asset/`·`mols-openspec-cli-compat/`의 정본은 `src/openai-chatgpt-chat/skills/`에 위치). 또한 `docs/skills/README.md` 2행([`docs/INDEX.tsv`](../../docs/INDEX.tsv) 5행)과 [`docs/subagents/README.md`](../../docs/subagents/README.md) 2행(`docs/INDEX.tsv` 6행)의 `description`은 `"재사용 Skill별..."`·`"재사용 Subagent..."`로 한정하지만, 본문 9행은 저장소 전용(`.rulesync/...`)까지 함께 다룬다고 명시합니다.
- **Impact** — `docs/skills/`와 `docs/INDEX.tsv` 진입점에서 vendor-native 원본 경로와 문서 대상 범위를 오해할 수 있습니다.
- **Action** — `src/<vendor>/` 안내를 보완하고 `description`과 본문 범위(`재사용` vs `재사용 및 저장소 전용`)를 일치시킨 뒤 `mise run generated sync`로 `docs/INDEX.tsv`를 갱신합니다.

### F4 · 🔵 Low — 신설 `test_indexes_generate.py`의 설정 스냅샷 중복 및 PR #302 신규 분기 커버리지 공백

- **Evidence** — PR #302가 추가한 [`test_indexes_generate.py`](../../tests/scripts/test_indexes_generate.py) 347–359행(`test_presets_match_repository_boundaries`)은 `PRESETS["docs"].traverse_roots` 등 정적 설정값을 그대로 복제해 [Testing 정책](../../docs/development/testing.md) 17행("현재 설정값이나 upstream schema를 그대로 복제하는 snapshot test는 두지 않습니다")과 어긋납니다. 반면 PR #302가 새로 구현한 분기 중 ① `test_non_utf8_stale_index_is_unlinked_without_decoding`(529–542행)은 `desired is None`인 `stale` 파일만 테스트해 [`indexes_generate.py`](../../scripts/indexes_generate.py) 213–216행의 `except UnicodeDecodeError` 분기를 실행하지 못하고, ② `test_symlink_directory_is_ignored_during_index_traversal`(545–561행)은 `depth=0`만 검증해 `depth != 0`용 `/{escaped}/**` 제외(136행)가 미테스트며, ③ `test_cli_supports_presets_overrides_check_and_validation_errors`(375–400행)는 이미 `prune=True`인 monkeypatch preset에 `--prune`을 전달해 `--root ... --prune` 오버라이드(268행)를 검증하지 못합니다(삭제된 `test_docs_indexes_generate.py`에 있던 루트 `README.md` 자체 제외 직접 테스트도 소실됨).
- **Impact** — 설정 상수 변경 시 불필요한 테스트 수정이 발생하고, 새로 넣은 예외·CLI·심볼릭 링크 분기의 회귀를 놓칠 수 있습니다.
- **Action** — 설정 복제 assertion을 정리하고 `expected` 비-UTF-8 파일, `depth != 0` 심볼릭 링크, `--root --prune`, 루트 `README.md` 제외 동작 테스트를 보강합니다.

## Perspectives

### 구현·엣지케이스

- **Reviewer / Method** — 독립 `research` subagent (`e64034d2`), 컨텍스트 격리 상태에서 PR #302 코드·구 생성기 대비·Python 3.13 재현 검토
- **Focus** — `indexes_generate.py` 대 삭제된 `docs_indexes_generate.py`·`catalog_indexes_generate.py`, `generate_index.py` 공유 Skill 계약·하위 호환성, Windows/POSIX·glob·symlink·줄바꿈·인코딩 엣지케이스
- **Assessment** — Critical/High 없음, Medium 3 · Low 6 후보 제기 (`_is_excluded` `/` 넘김·대소문자, 기존 `--output` CRLF/유니버설 개행, 입력 방어 코드 포함)
- **Evidence** — `scripts/indexes_generate.py`, `src/rulesync/.rulesync/skills/mols-markdown-maintenance/{SKILL.md,scripts/generate_index.py}`, Python 3.13 읽기 전용 재현

### CI·동기화·검증·테스트

- **Reviewer / Method** — 독립 `research` subagent (`07f2dabf`), 컨텍스트 격리 상태에서 CI·Hook·테스트 전수 검토
- **Focus** — `generated_artifacts_{sync,validate}.py`, `pr-gate.yml`·`branch-check.yml`·`lefthook.yml`, 삭제된 테스트 대비 신규/수정 테스트 커버리지, `ci.md`·`validation.md`·`testing.md`·`formatting.md` 정합성
- **Assessment** — Critical/High 없음, Medium 2 · Low 3 후보 제기 (`indexes_generate` 비-UTF-8 테스트 분기 누락 및 기존 `compare_outputs` 비대칭, 테스트 커버리지 공백, `PRESETS` 스냅샷 테스트, 기존 diff/rglob 관찰)
- **Evidence** — `scripts/generated_artifacts_{sync,validate}.py`, `tests/scripts/test_*.py`, `pytest` 465 passed, `ruff`/`rumdl`/`generated_artifacts validate` 실행 결과

### 문서·IA·정책

- **Reviewer / Method** — 독립 `research` subagent (`f04430fe`), 컨텍스트 격리 상태에서 `c39d094f` 대비 IA·문서·통제 표면 정책 검토
- **Focus** — `docs/**`·`catalog/**` 14개 `INDEX.tsv` 전후 엔트리 완전성, 신설/수정 문서 10개 링크·frontmatter·prose 스타일(`.rulesync/rules/markdown.md`), `github.md`·`source-authority.md`·`agent-asset-management.md` 준수 여부
- **Assessment** — Critical/High 없음 (`docs` 47건·`catalog` 40건 전후 엔트리 일치 확인), Medium 2 · Low 4 후보 제기 (`--exclude-glob --help`, 통제 표면 승인·검증 경계, `src/<vendor>/` 누락, `documentation/README.md`·`frontmatter.md` 표현)
- **Evidence** — `docs/**`, `catalog/**`, `.rulesync/skills/prj-workflow-pattern/workflows/*.md`, `rulesync_validate.py`, `docs_frontmatter_validate.py`, 10개 비-인박스 `.md` 링크/스타일 전수 확인

### 적대적·전역 호환성

- **Reviewer / Method** — 독립 `research` subagent (`3b59287f`), 저장소 전역 `git grep`·`rulesync` projection 및 PR #302 전체 커밋 대조 검증
- **Focus** — 구 생성기·단일 `INDEX.tsv` 가정 잔존 여부, `rulesync` 패키징/projection 영향, 커밋 내 자기 모순 및 억지성 nitpick 분리
- **Assessment** — 구 생성기·단일 루트 가정 잔존 0건 및 `rulesync` projection 정상 확인; `.internal/guide.md` 미해결 모순, 통제 표면 범위, `docs/{skills,subagents}/README.md` 범위 불일치, `00-review-scoped-indexes.md` `rumdl` 실패 제기 및 6건 nitpick 제외
- **Evidence** — `git diff c39d094f..7ae40bad`, 전역 `git grep`, `rulesync generate --dry-run --json`, `rumdl check`, Python 재현 결과

## Candidate Decisions

### C1 · Accept

PR #302가 바꾼 `generate_index._is_excluded`의 `/` 넘김 `fnmatch` 매칭으로 `/*.md`·`test*.md`·`.*.md` 스코핑이 깨지고, `--depth -1`에서 `.internal/guide.md`만 루트 목록에서 탈락한다.

- **Perspectives** — 구현·엣지케이스, 적대적·전역 호환성, CI·동기화·검증·테스트
- **Rationale** — 코디네이터가 `git diff c39d094f..7ae40bad`와 Python 3.13 재현으로 PR #302가 수정한 `_is_excluded`와 새 `indexes_generate.py` 사이의 실제 계약 불일치를 직접 확인했다. 저장소 기본 preset(`depth=0`)에는 영향이 없으므로 `Medium`으로 채택한다.
- **Finding** — F1

### C2 · Accept

PR #302가 수정한 `_is_excluded`의 Windows 대소문자 무시(`fnmatch` 대 `fnmatchcase`) 및 `--exclude-glob --help` 문구 미갱신.

- **Perspectives** — 구현·엣지케이스, 문서·IA·정책
- **Rationale** — `fnmatch.fnmatch` 케이스 불일치와 `--help` 계약 불일치 모두 PR #302의 `_is_excluded` 변경에서 직접 발생한 실재 불일치이므로 `Low`로 묶어 채택한다(반면 같은 파일의 기존 `main()` `--output` `newline="\n"` 누락과 Windows NTFS `rglob("INDEX.tsv")` 대소문자 무시는 PR #302 변경이 아니거나 OS 파일시스템 자체 동작이므로 제외).
- **Finding** — F2

### C3 · Accept

PR #302가 신설한 `docs/{skills,subagents,development/agent-assets/skills}/README.md`의 `src/<vendor>/` 누락 및 `description`의 `재사용` 한정 불일치.

- **Perspectives** — 문서·IA·정책, 적대적·전역 호환성
- **Rationale** — PR #302가 새로 추가한 문서 내부의 사실 불일치([Source Authority](../../docs/development/source-authority.md) 및 `docs/skills/mols-chatgpt-chat-asset/` 대비)이므로 `Low`로 채택한다.
- **Finding** — F3

### C4 · Accept

PR #302가 추가한 `test_indexes_generate.py`의 `PRESETS` 설정 스냅샷 테스트([Testing 정책](../../docs/development/testing.md)) 및 신규 구현 분기(`except UnicodeDecodeError`, `depth != 0` 심볼릭 링크, `--root --prune`, 루트 `README.md` 제외) 커버리지 공백.

- **Perspectives** — CI·동기화·검증·테스트
- **Rationale** — PR #302가 추가·재작성한 테스트 파일 자체의 설계 충돌과 새로 작성된 코드 분기의 미커버만 추려 `Low`로 채택한다.
- **Finding** — F4

### C5 · Drop

PR #302 이전(`c39d094f`)부터 존재하던 코드·구성의 개선 요구(`generate_index.py` `--output` `newline="\n"` 누락·`--max-depth -1`·`required_fields` 디렉터리 미적용·`.git`/`.venv` 미제외, `generated_artifacts_validate.py` `compare_outputs` `UnicodeDecodeError` 미처리·`root.rglob("*")` 4회 순회·`_first_line_difference` 끝 개행 누락, `pr-gate.yml` `sync`/`validate` 자체 변경 미감지, `docs/skills/*/` 6개 하위 README 부재).

- **Perspectives** — 구현·엣지케이스, CI·동기화·검증·테스트, 문서·IA·정책, 적대적·전역 호환성
- **Rationale** — `git diff c39d094f..7ae40bad` 대조 결과 PR #302가 도입하거나 변경한 동작이 아니므로 이 PR 리뷰의 결함으로 돌리는 것은 범위 이탈이다.
- **Finding** — —

### C6 · Drop

PR #302가 커밋한 `.inbox/github-302/00-review-scoped-indexes.md`의 `#L` 줄 번호 fragment `rumdl` `[MD051]` 실패(5–7건).

- **Perspectives** — 적대적·전역 호환성
- **Rationale** — `PR Gate` 검사 대상이 아니며 비정본 리뷰 스냅샷 원문 보존 및 PR 본문 사전 고지(`Validation`)와 일치하므로 별도 결함으로 재발행하지 않는다(실행 사실만 `Validation`에 분리 기록).
- **Finding** — —

### C7 · Drop

`docs/documentation/README.md` 18행 요약·`docs/documentation/frontmatter.md` 19행 `` `docs/` 계층 ``·`docs/documentation/indexing.md` CLI 표 중복에 대한 문구 수정 요구.

- **Perspectives** — 문서·IA·정책
- **Rationale** — `docs/documentation/README.md`는 목록 1줄 요약이고 `frontmatter.json`이 실제로 `docs/`만 검증하며 `indexing.md` 표는 진입 문서 역할에 부합하므로 과도한 문구 트집이다.
- **Finding** — —

### C8 · Drop

`generated_artifacts_sync._is_docs_index_source`의 `docs/skills/<skill>/...`·루트 `README.md` 매칭 및 `_is_content_file`과의 규칙 분리.

- **Perspectives** — CI·동기화·검증·테스트, 구현·엣지케이스, 적대적·전역 호환성
- **Rationale** — `docs/skills/` 내 마지막 `.md` 삭제 시 실제로 `docs/INDEX.tsv`에서 `skills/`가 제거되므로 [Continuous Integration](../../docs/development/ci.md)의 fail-safe 원칙에 부합하고, `sync.py`는 삭제된 파일의 Git 경로 문자열도 판별해야 해 `Path.is_file()` 기반 `_is_content_file`을 그대로 공유할 수 없다. 현재 전수 경계 매트릭스에서 양쪽 판정도 일치한다.
- **Finding** — —

### C9 · Drop

비현실적 합성 엣지케이스, 과도한 방어/최적화 요구, 의도된 설계 트집(YAML `description` 내 raw `\r` 포함 시 universal newline 불일치, `INDEX.tsv` 이름의 디렉터리 예외, `directory_entry_files` 요소 경로 검증 부재, 비-UTF-8 소스 파일 `argparse` exit 2, `_targets` 간 `rglob` 메모이제이션, `blocked_root_subtrees` 선행 `/` 표기 차이, `PRESETS["docs"].traverse_roots` `"references"` 예약, `scripts/` `<domain>/` 분리 미적용).

- **Perspectives** — 구현·엣지케이스, CI·동기화·검증·테스트, 적대적·전역 호환성
- **Rationale** — 발생 가능성이 희박한 합성 케이스이거나 기능 차이가 없으며, `principles.md`의 YAGNI 기준 및 `indexing.md`·`agent-asset-management.md`·`repository-layout.md`의 의도된 설계와 맞지 않는 과도한 요구다.
- **Finding** — —

## Validation

### ✅ Pass · `pytest -q tests` (`7ae40bad`)

`_workspace/pr-302`에서 `uv run --locked --no-default-groups --group test pytest -q tests` 실행 결과 **465 passed in 11.62s** (`0` failed, `0` skipped).

### ✅ Pass · `generated_artifacts validate --all` 및 `--changed-from c39d094f` (`7ae40bad`)

`docs-indexes`, `catalog-indexes`, `distribution-routes`, `repository-routes` 4종 모두 `PASS`, `--changed-from` 기준 `docs-indexes`·`catalog-indexes` `PASS`.

### ✅ Pass · `docs_frontmatter_validate.py` (`7ae40bad`)

`PASS documentation frontmatter` (exit `0`).

### ✅ Pass · `mise doctor project` 및 `mise run rulesync-validate` (`7ae40bad`)

`python-lock`·`rulesync-root` 2 passed, `rulesync_validate.py` `config`·`configured-projection` PASS (`src/rulesync/` 범위).

### ✅ Pass · `ruff check` 및 `ruff format --check` (`7ae40bad`)

PR #302 변경·신규 Python 파일 9개 전체(`generate_index.py` 포함) `All checks passed!` / `9 files already formatted`.

### ✅ Pass · `rumdl check --no-cache` (비-인박스 Markdown 및 `01-review-triage.md`)

PR #302의 비-인박스 Markdown 10개와 `01-review-triage.md` 총 11개 파일은 0 issues (단 기존 커밋된 `00-review-scoped-indexes.md`를 포함해 검사하면 `#L` 줄 번호 fragment 5건으로 `[MD051]` 실패, exit `1` — PR 본문에 이미 고지됨).

### ✅ Pass · GitHub Actions `PR Gate` 및 `Branch Check` (`7ae40bad`)

`gh pr checks 302` 조회 결과 `Branch Check` (`pass`, 21s) 및 `PR Gate` (`pass`, 34s) 모두 `7ae40bad` 기준 통과 확인.

### ⚪ Not Verified · Linux `ubuntu-slim` 로컬 실행 및 `lefthook` `pre-commit` 실제 훅 트리거

본 검토는 Windows 읽기 전용 환경에서 수행되었으므로 Linux에서의 로컬 `generated sync` 실행과 실제 Git `pre-commit` 훅 실행은 별도 수행하지 않았습니다(`PR Gate`의 `ubuntu-slim` 실행과 단위 테스트로 부분 보완).

## Risks and Limits

- **통제 표면 사람 승인 필수 ([GitHub 정책](../../docs/development/github.md)):** PR #302는 저장소 전용 Skill 워크플로 4건(`.rulesync/skills/prj-workflow-pattern/workflows/{create,lifecycle,publish,validate}.md`)과 재사용 Skill 스크립트(`src/rulesync/.rulesync/skills/mols-markdown-maintenance/scripts/generate_index.py`)를 수정합니다. `mise run rulesync-validate`는 `src/rulesync/`만 검증하고 `docs_frontmatter_validate.py`는 `docs/`만 검증하므로 루트 `.rulesync/` 워크플로 4건에는 `rumdl` 외 구조·의미 자동 검증이 적용되지 않습니다. `PR Gate` 통과나 AI 리뷰는 승인을 대신할 수 없으며, 사람의 직접 확인과 명시적 승인이 필요합니다.
- **재사용 Skill 배포·잠금 경계:** `generate_index.py` 수정은 `main`에 고정된 루트 `rulesync.lock`이나 외부 설치본을 자동 갱신하지 않으므로, 머지 후 소비자 환경 갱신이 필요하면 별도 동기화 후속 작업을 판단해야 합니다.
- **검토 범위:** 본 보고서는 `_workspace/pr-302` 읽기 전용 점검 결과이며 PR #302 브랜치 커밋, 코드 수정, GitHub 리뷰 게시, 머지를 수행하지 않았습니다.
