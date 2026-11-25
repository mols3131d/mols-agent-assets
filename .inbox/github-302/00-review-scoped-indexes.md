# PR #302 — 독립 다관점 리뷰 보고서

> [!IMPORTANT]
> **권고 판단: Request changes (`🟠 High` 1건 · `🟡 Medium` 6건 · `🔵 Low` 4건).** 범위별 `INDEX.tsv` 생성과 단일 [`indexes_generate.py`](../../scripts/indexes_generate.py) 통합, 14개 인덱스 정합성, 446개 테스트와 `PR Gate` 통과를 확인했습니다. 그러나 [`generated_artifacts_sync.py`](../../scripts/generated_artifacts_sync.py)의 source 판별이 새 생성기와 어긋나 `docs/documentation/indexing.md` 변경이 CI·pre-commit에서 조용히 누락되는 결함(`High`)이 있고, Win/Linux 정렬 불일치·`exclude_globs` 경계·`__index__` 필터 누락·탐색 fallback 공백을 머지 전에 보완할 필요가 있습니다. 이 보고서는 사람의 승인이나 GitHub PR Review를 대신하지 않습니다.

| 항목 | 값 |
| --- | --- |
| 대상 | [PR #302](https://github.com/mols3131d/mols-agent-assets/pull/302) |
| 브랜치 | `mols/feat/scoped-indexes` |
| 비교 base | `c39d094f72cfb331217bc70abb303c738493dd4c` |
| 리뷰 기준 head | `18ab18156946537f3393cc8391e244d50284d5d5` |
| 스냅샷 주의 | 이 문서는 `18ab1815` 기준 임시 clean worktree에서 검증한 읽기 전용 리뷰 스냅샷이며, `_workspace/pr-302`의 미커밋 `generated_artifacts_sync.py`·`generated_artifacts_validate.py` 포맷 변경은 리뷰 대상에서 제외했습니다. 이 보고서 커밋 이후의 새 head에 대한 검증은 별도로 확인해야 합니다. |
| 방법 | 컨텍스트를 공유하지 않은 4개 독립 리뷰어 subagent 병렬 검토 + 코디네이터 직접 재현·결정론적 검증 |

## Findings

### 🟠 High

#### F1. `_is_docs_index_source`가 `docs/documentation/indexing.md`를 변경 감지에서 누락함

- **위치:** [`scripts/generated_artifacts_sync.py`](../../scripts/generated_artifacts_sync.py) (`18ab1815` 기준 62행, `_is_docs_index_source`)
- **근거:** `_is_docs_index_source`가 `if name.upper().startswith("INDEX") or name.startswith("__index__"): return False`를 사용해 `sync._is_docs_index_source("docs/documentation/indexing.md")`가 `False`를 반환합니다. 반면 [`scripts/indexes_generate.py`](../../scripts/indexes_generate.py#L56)와 [`generate_index.py`](../../src/rulesync/.rulesync/skills/mols-markdown-maintenance/scripts/generate_index.py#L103)는 대소문자를 구분해 `INDEX` 접두사만 제외하므로 [`docs/documentation/INDEX.tsv`](../../docs/documentation/INDEX.tsv#L3)는 실제로 `indexing.md`를 인덱싱하며, 이번 PR 자체가 `docs/documentation/indexing.md`의 frontmatter `description`을 수정했습니다.
- **영향:** 이후 `docs/documentation/indexing.md`(또는 `index.md` 외의 `docs/**/index*.md`)만 수정하는 PR은 [`.github/workflows/pr-gate.yml`](../../.github/workflows/pr-gate.yml#L44)의 `validate --changed-from`에서 `No generated projections affected.`로 통과하고, `lefthook` `pre-commit`(`sync --staged`)도 `docs/documentation/INDEX.tsv`를 재생성하지 않습니다.
- **필요 조치:** `_is_docs_index_source`의 `name.upper().startswith("INDEX")`를 대소문자 구분 `name.startswith("INDEX")`로 맞추거나 `indexes_generate.py`와 판정 규칙을 공유하고, [`tests/scripts/test_generated_artifacts_sync.py`](../../tests/scripts/test_generated_artifacts_sync.py)에 `docs/documentation/indexing.md` 케이스를 추가합니다.

### 🟡 Medium

#### F2. `_is_catalog_index_source`가 `indexes_generate.py`의 숨김 `.json` 지원 계약과 불일치함

- **위치:** [`scripts/generated_artifacts_sync.py`](../../scripts/generated_artifacts_sync.py) (`18ab1815` 기준 86행, `_is_catalog_index_source`)
- **근거:** PR #302는 [`scripts/indexes_generate.py`](../../scripts/indexes_generate.py#L57)에서 `not (name.startswith(".") and name.endswith(".md"))`로 바꾸고 [`tests/scripts/test_indexes_generate.py`](../../tests/scripts/test_indexes_generate.py#L288-L318)에 `.hidden.json`·`patterns/.special.json` 보존 테스트를 추가했습니다. 그러나 `_is_catalog_index_source`는 여전히 `name.startswith(".")`를 일괄 거부해 `sync._is_catalog_index_source("catalog/patterns/.special.json")`이 `False`를 반환합니다.
- **영향:** 현재 저장소 `catalog/`에 dot-prefixed `.json`이 없어 당장 실패하지는 않지만, PR이 명시적으로 약속한 `.json` 인덱싱 대상이 `pre-commit`과 `PR Gate`의 영향 라우팅에서 빠집니다.
- **필요 조치:** `_is_catalog_index_source`도 `name.startswith(".") and name.endswith(".md")`만 제외하도록 일치시키고 테스트를 추가합니다.

#### F3. Win/Linux 행 순서 정렬 수정(`c7846dfb`)이 `generate_index.py`에는 적용되지 않음

- **위치:** [`generate_index.py`](../../src/rulesync/.rulesync/skills/mols-markdown-maintenance/scripts/generate_index.py#L131) (`for path in sorted(found_paths):`) ↔ [`scripts/indexes_generate.py`](../../scripts/indexes_generate.py#L85)
- **근거:** 커밋 `c7846dfb`은 `indexes_generate.py`의 `_targets()`와 `sync_indexes()`(drift 보고 순서)만 문자열 키로 정렬했고, 실제 TSV 행 순서를 정하는 `generate_index.py:131`은 raw `Path` 객체를 `sorted()`합니다. Python 3.13 검증에서 `PureWindowsPath`는 `['__history.md', 'b.md', 'C.md']`, `PurePosixPath`(`ubuntu-slim` CI)는 `['C.md', '__history.md', 'b.md']`로 다르게 정렬됩니다.
- **영향:** 현재 `docs/`·`catalog/` 인덱싱 대상 파일명이 모두 소문자라 당장은 통과하지만, 대문자·혼합 대소문자 파일이 추가되면 Windows에서 `mise run generated sync`한 결과가 Linux `PR Gate`에서 `outdated`로 실패합니다.
- **필요 조치:** `generate_index.py:131`도 `key=lambda path: path.relative_to(directory).parts`(또는 `.as_posix()`) 기준으로 정렬하고 혼합 대소문자·언더바 순서 테스트를 추가합니다.

#### F4. `_desired_index`의 unescaped `exclude_globs` 전달이 `depth != 0`·메타문자·숨김 디렉터리에서 오동작함

- **위치:** [`scripts/indexes_generate.py`](../../scripts/indexes_generate.py#L97-L119), [`generate_index.py`](../../src/rulesync/.rulesync/skills/mols-markdown-maintenance/scripts/generate_index.py#L22-L33)
- **근거:** `empty_directories`와 `blocked_root_subtrees`가 glob 이스케이프 없이 `exclude_globs`로 넘어가고, `_is_excluded`는 `fnmatch(path.name, pattern)`과 `fnmatch(relative_path, pattern)`를 모두 평가합니다. 빈 디렉터리 `[a-z]`와 정상 `x/guide.md`를 함께 두고 `expected_indexes()`를 실행하면 루트 `INDEX.tsv`에서 `x/`가 빠지고 빈 `[a-z]/`가 노출됨을 직접 재현했습니다. 또한 `depth != 0`에서는 루트의 빈 디렉터리명(`assets`)이 하위 `guide/assets/`와 basename 충돌하고, `.internal/guide.md` 같은 숨김 디렉터리 안의 문서는 `_has_content == True`로 하위 `INDEX.tsv`를 만들면서 `.*.md`에 의해 상위 목록에서 제외됩니다.
- **영향:** 저장소 기본 preset(`depth=0`, 일반 디렉터리명)에서는 잠복 상태이나 `--depth 1/-1` 또는 `--root` 재사용 계약을 깹니다.
- **필요 조치:** `empty_directories`·`blocked_root_subtrees` 경로는 `glob.escape` 및 상대 경로 prefix 일치로 처리하거나 `exclude_globs`와 분리합니다.

#### F5. `_is_content_file`의 `startswith("__index__")` 누락으로 유령 디렉터리 행이 생성됨

- **위치:** [`scripts/indexes_generate.py`](../../scripts/indexes_generate.py#L47-L59) ↔ [`generate_index.py`](../../src/rulesync/.rulesync/skills/mols-markdown-maintenance/scripts/generate_index.py#L103)
- **근거:** 기존 `docs_indexes_generate.py`와 `generate_index.py`는 모두 `name.startswith("__index__")`를 제외하지만 `_is_content_file`은 `__*__.md`만 제외합니다. `only_idx/__index__v2.md`로 재현 시 루트 `INDEX.tsv`에는 `only_idx/` 행이 생기지만 `generate_index`가 파일을 건너뛰어 `only_idx/INDEX.tsv`는 생성되지 않습니다(`__index__.json`도 동일).
- **필요 조치:** `_is_content_file`에 `and not name.startswith("__index__")`를 복원하고 `__index__.json`·`__index__v2.md` 테스트를 추가합니다.

#### F6. `docs/development/agent-assets/skills/` 탐색 신호 저하 (및 `docs/skills/`, `docs/subagents/` README fallback 부재)

- **위치:** [`docs/development/agent-assets/INDEX.tsv`](../../docs/development/agent-assets/INDEX.tsv#L6), [`docs/INDEX.tsv`](../../docs/INDEX.tsv#L5-L6)
- **근거:** 기존 `c39d094f:docs/INDEX.tsv`에서는 `development/agent-assets/skills/` 아래 `skill-authoring-conventions.md`·`specification.md`와 설명이 루트에서 바로 보였으나, 범위별 분할 후 [`docs/development/agent-assets/INDEX.tsv`](../../docs/development/agent-assets/INDEX.tsv#L6)는 `skills/`를 빈 설명으로만 노출하고 `docs/development/agent-assets/skills/README.md`가 없습니다. 또한 [`docs/INDEX.tsv`](../../docs/INDEX.tsv#L5-L6)의 `skills/`·`subagents/`도 설명이 비어 있고 해당 디렉터리에 `README.md`가 없습니다(이전부터 없던 상태이나 루트가 7행으로 축소되면서 [`indexing.md`](../../docs/documentation/indexing.md#L19)와 [`AGENTS.md`](../../AGENTS.md#L10)의 README fallback이 빈 디렉터리로 연결됨).
- **필요 조치:** `docs/development/agent-assets/skills/README.md`에 scope `description` frontmatter를 추가해 `docs/skills/`와의 경계를 드러내고(권장: `docs/skills/README.md`·`docs/subagents/README.md`도 함께 보완), `mise run generated sync`를 실행합니다.

#### F7. `PRESETS`, 신규 CLI 옵션/에러, scoped `validate` 및 삭제된 기존 테스트 시나리오의 커버리지 공백

- **위치:** [`tests/scripts/test_indexes_generate.py`](../../tests/scripts/test_indexes_generate.py), [`tests/scripts/test_generated_artifacts_validate.py`](../../tests/scripts/test_generated_artifacts_validate.py)
- **근거:** `test_indexes_generate.py`가 `PRESETS`를 import하지 않고 `main()` CLI 테스트가 `--root ... --extensions .json` 1건뿐이라 `--target`, `--directory-entry-files`, `--index-depth`, `--depth`, `--min-entries`, `--traverse-roots`, `--prune`, `parser.error` 종료(exit 2) 경로가 미테스트입니다. `test_generated_artifacts_validate.py`는 `route/*.jsonl`만 테스트하고 `check_docs_indexes()`·`check_catalog_indexes()`·`show_first_difference=True`를 단위 테스트하지 않습니다. 삭제된 `test_docs_indexes_generate.py`에 있던 기본 `README.md` 설정 시 `index.md` 일반 문서 유지, 숨김 파일만 있는 하위 디렉터리(`hidden/.private.md`) 재귀 제외, 콘텐츠가 있는 `index_depth` 초과 하위 디렉터리의 기존 `INDEX.tsv` `stale` 정리 검증도 빠졌습니다.
- **필요 조치:** 위 CLI·preset·scoped validate·회귀 케이스를 단위 테스트로 보강합니다.

### 🔵 Low

#### F8. `PRESETS["docs"].traverse_roots` 폐쇄 목록과 `docs/documentation/indexing.md` 설명 간 괴리

- **위치:** [`scripts/indexes_generate.py`](../../scripts/indexes_generate.py#L40), [`docs/documentation/indexing.md`](../../docs/documentation/indexing.md#L20)
- **근거:** `traverse_roots`에 현재 존재하지 않는 `"references"`가 포함돼 있고([`agent-asset-management.md`](../../docs/development/agent-assets/agent-asset-management.md#L40)의 비자산 유형 목록과는 일치), 향후 `docs/` 아래 새 일반 문서 디렉터리를 추가해도 preset을 함께 수정하지 않으면 하위 `INDEX.tsv`가 생성되지 않고 `prune=True`로 삭제됩니다. `indexing.md`에 이 등록 경계가 명시돼 있지 않습니다.

#### F9. `.rulesync/skills/prj-workflow-pattern` 형제 워크플로 및 `frontmatter.md`의 단일 루트 인덱스 표기 잔존

- **위치:** [`publish.md`](../../.rulesync/skills/prj-workflow-pattern/workflows/publish.md#L6), [`lifecycle.md`](../../.rulesync/skills/prj-workflow-pattern/workflows/lifecycle.md#L17), [`docs/documentation/frontmatter.md`](../../docs/documentation/frontmatter.md#L19)
- **근거:** 커밋 `92101ca3`은 `create.md`·`validate.md`만 범위별 `catalog/` 인덱스로 수정했으나 같은 Skill의 `publish.md`·`lifecycle.md`와 `frontmatter.md:19`는 여전히 `catalog/INDEX.tsv` 또는 `docs/INDEX.tsv` 단수 표현만 남겼습니다.

#### F10. PR에서 수정한 기존 Python 파일의 `ruff format --check` 및 `ruff check` 미통과

- **위치:** [`tests/scripts/test_generated_artifacts_sync_dependencies.py`](../../tests/scripts/test_generated_artifacts_sync_dependencies.py#L29-L35)(PR 수정 블록 포함), [`scripts/generated_artifacts_sync.py`](../../scripts/generated_artifacts_sync.py), [`scripts/generated_artifacts_validate.py`](../../scripts/generated_artifacts_validate.py), [`tests/scripts/test_generated_artifacts_sync.py`](../../tests/scripts/test_generated_artifacts_sync.py) (`18ab1815` 기준)
- **근거:** 커밋 `18ab1815`가 import 정렬만 수행해 위 4개 파일이 `ruff format --check`에서 실패하고, `generated_artifacts_validate.py`·`test_generated_artifacts_sync.py`에는 기존 `E501` 8건이 남아 있습니다(PR Gate는 ruff 미실행, PR 본문도 신규 2개 파일과 `I001` 통과로 범위를 한정함). `mise run format-changed` 기준으로 정리하는 편이 안전합니다.

#### F11. `indexes_generate.py` 입력 정규화·방어 처리 및 순회 효율

- **위치:** [`scripts/indexes_generate.py`](../../scripts/indexes_generate.py#L51-L54)
- **근거:** ① `extensions`의 공백·빈 문자열(`("",)`, `(" .md ",)`)을 `_targets`·`_is_content_file`에서 선제 정규화·검증하지 않아 `generate_index._normalize_extensions`와 어긋남, ② `sync_indexes`가 `if desired is None` 분기 전에 `path.read_text(encoding="utf-8")`를 호출해 비-UTF-8 stale `INDEX.tsv`에서 `UnicodeDecodeError` 발생, ③ `_targets`의 `child.is_dir()`가 symlink 디렉터리를 추적(순환 위험)하는 반면 `rglob`은 `recurse_symlinks=False`, ④ `config.root` 끝이 `..`일 때 `relative_to(config.root.parent)` 예외, ⑤ `depth=0`에서도 `_desired_index`가 매 디렉터리마다 `rglob("*")`을 반복 실행함.

## Perspectives

| 관점 (독립 subagent) | 검토 방법·초점 | 평가 요약 |
| --- | --- | --- |
| 구현·엣지케이스 | 격리 컨텍스트 읽기 전용 검토(`indexes_generate.py` vs 구 생성기, `generate_index.py` 연동, OS·경로·CSV·glob 재현) | Medium 4 · Low 2 |
| CI·테스트·포맷 | 격리 컨텍스트 읽기 전용 검토(`generated_artifacts_sync/validate`, `lefthook`, `pr-gate.yml`, 삭제된 테스트 비교, `ruff`/`rumdl`) | High 1 · Medium 2 · Low 2 |
| 문서·IA·정책 | 격리 컨텍스트 읽기 전용 검토(`indexing.md`, `catalog/README.md`, 14개 `INDEX.tsv`, `prj-workflow-pattern`, `language.md`/`github.md`) | Medium 2 · Low 2 |
| 적대적·호환성 | 격리 컨텍스트 읽기 전용 검토(저장소 전역 잔존 참조·링크, source/sync 드리프트, OS 정렬, `traverse_roots`·`sys.path` 파괴 시나리오) | High 2 · Medium 2 · Low 1 |

## Candidate Decisions

1. **Accept → F1 (`🟠 High`):** `indexing.md`의 `_is_docs_index_source` 누락 (구현·CI·적대적 3관점 일치 + 코디네이터 직접 재현)
1. **Accept → F2 (`🟡 Medium`):** 숨김 `.json`의 `_is_catalog_index_source` 누락 (CI·적대적 2관점 + 코디네이터 직접 재현)
1. **Accept → F3 (`🟡 Medium`):** `generate_index.py:131` raw `Path` 정렬 (구현·적대적 2관점 + Win/Posix `PurePath` 재현; 현재 소문자 파일명 조건 고려해 Medium 조정)
1. **Accept → F4 (`🟡 Medium`):** `exclude_globs` basename 충돌·메타문자·숨김 디렉터리 (구현·적대적 2관점 + `[a-z]`/`x/` 직접 재현)
1. **Accept → F5 (`🟡 Medium`):** `_is_content_file`의 `startswith("__index__")` 누락 (구현·CI·적대적 3관점 + `__index__v2.md` 직접 재현)
1. **Accept → F6 (`🟡 Medium`):** `docs/development/agent-assets/skills/` 탐색 신호 저하 및 `docs/skills/`·`docs/subagents/` README 부재 (문서·정책 관점 + 전후 `INDEX.tsv` 비교 확인)
1. **Accept → F7 (`🟡 Medium`):** `PRESETS`/CLI/scoped validate/삭제 테스트 시나리오 공백 (CI 관점 + 테스트 파일 직접 확인)
1. **Accept → F8 (`🔵 Low`):** `traverse_roots` 폐쇄 목록 문서화·예약 경로 (`agent-asset-management.md`에 이미 유형 정의가 있으므로 Low 조정)
1. **Accept → F9 (`🔵 Low`):** `prj-workflow-pattern`(`publish.md`·`lifecycle.md`) 및 `frontmatter.md:19` 잔존 표현 (문서·정책 관점 직접 확인)
1. **Accept → F10 (`🔵 Low`):** PR 수정 Python 4개 파일 `ruff format --check` 실패 및 기존 `E501` 8건 (CI 관점 + 코디네이터 직접 실행)
1. **Accept → F11 (`🔵 Low`):** `extensions` 선제 정규화, 비-UTF-8 stale `read_text`, symlink/`..` 경로, 반복 `rglob` (구현·적대적 관점 확인)
1. **Drop (결함 아님):** `pre-commit`의 삭제된 `INDEX.tsv` staging(`git ls-files --cached` + `git add -A` 정상 동작 확인), `catalog/*.json` 및 `catalog/templates/review*.md`의 빈 description(의도된 계약), 구 스크립트 이름·상대 링크 잔존(0건)

## Validation (`18ab1815` clean worktree 실행 기준)

- `❌ Fail` — **`ruff format --check` (PR 변경 Python 6개 파일):** `scripts/indexes_generate.py`·`tests/scripts/test_indexes_generate.py`는 통과, 나머지 4개(`generated_artifacts_sync.py`, `generated_artifacts_validate.py`, `test_generated_artifacts_sync.py`, `test_generated_artifacts_sync_dependencies.py`)는 reformat 필요 (exit 1)
- `❌ Fail` — **`ruff check` (PR 변경 Python 6개 파일):** 4개 파일은 0건, `generated_artifacts_validate.py`(5건)·`test_generated_artifacts_sync.py`(3건)에 기존 `E501` 8건 잔존 (exit 1)
- `⚪ Not Verified` — **실제 `lefthook` `pre-commit` hook 실행 / Linux `ubuntu-slim`에서의 로컬 `generated sync` 대조 / `biome check`:** 읽기 전용 리뷰 제약으로 미실행(단위 테스트와 Python 모의로 보완; GitHub Actions `PR Gate`·`Branch Check`는 `18ab1815`에서 SUCCESS 기록 확인)
- `✅ Pass` — **`docs_frontmatter_validate.py`:** `PASS documentation frontmatter`
- `✅ Pass` — **`pytest -q tests`:** `446 passed in 10.50s`
- `✅ Pass` — **`python -m scripts.generated_artifacts validate --all`:** `docs-indexes`, `catalog-indexes`, `distribution-routes`, `repository-routes` 모두 PASS
- `✅ Pass` — **`python -m scripts.generated_artifacts validate --changed-from c39d094f72cfb331217bc70abb303c738493dd4c`:** `docs-indexes`, `catalog-indexes` PASS
- `✅ Pass` — **`scripts/agent_assets/rulesync_validate.py`:** `config`, `configured-projection` PASS (단 `src/rulesync/` 대상이며 루트 `.rulesync/` Skill 검증은 아님)
- `✅ Pass` — **`mise doctor project`:** `python-lock`, `rulesync-root` 2 passed
- `✅ Pass` — **`rumdl check --no-cache` (PR 수정 Markdown 4개 파일):** 0 issues (`indexing.md`, `catalog/README.md`, `create.md`, `validate.md`)

## Risks and Limits

1. **통제 표면(Control Surface) 승인 경계 ([`docs/development/github.md`](../../docs/development/github.md#L103)):** PR #302가 `.rulesync/skills/prj-workflow-pattern/workflows/create.md`·`validate.md`를 수정했으므로, `PR Gate` 통과 외에 해당 Skill에 의존하지 않는 리뷰 근거와 사람의 명시적 승인이 필요합니다.
1. **후속 작업 시 작업트리 주의:** `_workspace/pr-302` 작업트리에 `scripts/generated_artifacts_sync.py`·`scripts/generated_artifacts_validate.py`의 미커밋 포맷 변경이 남아 있으므로 후속 수정 시 먼저 의도 여부를 확인하세요.
