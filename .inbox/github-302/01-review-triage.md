# PR 302 리뷰 수용 판단 및 작업 정리

이 문서는 [PR 302 독립 다관점 리뷰 보고서](00-review-scoped-indexes.md)에서 제기한 관찰(`F1`–`F11`)을 소스 코드와 대조 검증해 수용 범위, 비범위 경계, 작업 계획을 정리한 `.inbox/` 작업 기록입니다. 저장소 정본 정책이 아니며 영구 규칙·사용법 반영은 `docs/` 및 `.rulesync/` 정본 문서에 직접 수행합니다.

## 수용 판단 요약 (`F1`–`F11`)

| ID | 심각도 | 판단 | 수용 내용 및 대상 |
| --- | --- | --- | --- |
| `F1` | High | 수용 | `scripts/generated_artifacts_sync.py`의 `_is_docs_index_source`에서 `name.upper().startswith("INDEX")`를 `name.startswith("INDEX")`로 수정해 `docs/documentation/indexing.md` 추적 누락 해소, `tests/scripts/test_generated_artifacts_sync.py` 회귀 테스트 추가 |
| `F2` | Medium | 수용 | `scripts/generated_artifacts_sync.py`의 `_is_catalog_index_source` 숨김 파일 차단을 `name.startswith(".") and name.endswith(".md")`로 한정해 숨김 `.json` 추적 누락 해소, `tests/scripts/test_generated_artifacts_sync.py` 회귀 테스트 추가 |
| `F3` | Medium | 수용 | `src/rulesync/.rulesync/skills/mols-markdown-maintenance/scripts/generate_index.py`의 `sorted(found_paths)`를 `path.relative_to(directory).parts` 기준 정렬로 수정해 대소문자·밑줄 경로 결정성 확보, `tests/skills/mols-markdown-maintenance/test_generate_index_routing.py` 회귀 테스트 추가 (`docs/skills/mols-markdown-maintenance/README.md`는 기존 불변식과 충돌 없어 별도 수정 불필요) |
| `F4` | Medium | 후속 보완 완료 | 1차 반영에서 `empty_directories`·`blocked_root_subtrees`에 `glob.escape()`와 선행 `/` 고정을 적용했으나 `fnmatch`가 `/`를 넘어 매칭하는 잔존 결함을 [2차 리뷰 보고서](02-review-scoped-indexes.md) `F1`에서 식별해 [후속 수용 정리](03-review-triage.md)에서 세그먼트 경계·`fnmatchcase` 매칭과 `.internal/` 일관성까지 완결 |
| `F5` | Medium | 수용 | `scripts/indexes_generate.py`의 `_is_content_file`에 `not name.startswith("__index__")` 조건을 복원해 `generate_index.py`와 일치시키고 `__index__v2.md`·`__index__.json` 회귀 테스트 추가 |
| `F6` | Medium | 수용 | `docs/development/agent-assets/skills/README.md`, `docs/skills/README.md`, `docs/subagents/README.md` 신설(범위 설명 `description` frontmatter + 최소 진입점 안내) 후 `INDEX.tsv` 재생성으로 빈 설명과 README fallback 갭 해소 |
| `F7` | Medium | 수용 | `tests/scripts/test_generated_artifacts_validate.py`에 `check_docs_indexes`·`check_catalog_indexes`·`show_first_difference=True` 테스트 추가, `tests/scripts/test_indexes_generate.py`에 `PRESETS`·CLI 옵션/종료코드·`index.md`·숨김 재귀 제외·`prune=True` 정리 및 `F1`–`F5`/`F11` 회귀 테스트 추가 |
| `F8` | Low | 수용 | `docs/documentation/indexing.md`에 `PRESETS["docs"].traverse_roots` 등록 기준과 `references` 예약 근거를 명시하고 `agent-asset-management.md`와 정합성 유지 |
| `F9` | Low | 수용 | `docs/documentation/frontmatter.md` 및 `.rulesync/skills/prj-workflow-pattern/workflows/{publish,lifecycle}.md`의 단일 루트 `INDEX.tsv` 잔존 표현을 scoped `INDEX.tsv` 구조에 맞게 갱신 |
| `F10` | Low | 수용 | 워킹트리의 미커밋 `ruff format` 변경분(`scripts/generated_artifacts_sync.py`, `scripts/generated_artifacts_validate.py`)을 반영하고 PR 수정 파일 내 기존 `E501` 8곳을 정리해 PR 변경 `.py` 전체가 `ruff check` 및 `ruff format --check`를 통과하도록 정리 |
| `F11` | Low | 선별 수용 | `extensions` 공백/빈 문자열 정규화 검증, `sync_indexes`에서 `desired is None` 확인 후 파일 읽기(비-UTF-8 stale 파일 제거 가능), `_targets` 심볼릭 링크 디렉터리 제외, `config.root` 비어 있는 `.name`·`..` 안전 라벨 처리, 불필요한 `rglob` 반복 축소 |

## 구현 반영 내역 (`F1`–`F11`)

- **`F1`·`F2`·`F10` (`scripts/generated_artifacts_sync.py`, `scripts/generated_artifacts_validate.py`)**: `_is_docs_index_source`의 `name.upper().startswith("INDEX")`를 `name.startswith("INDEX")`로, `_is_catalog_index_source`의 `name.startswith(".")`를 `name.startswith(".") and name.endswith(".md")`로 수정하고 `ruff format` 및 `E501`·`I001` 정리를 적용했습니다.
- **`F3`·`F4`·`F10` (`src/rulesync/.rulesync/skills/mols-markdown-maintenance/scripts/generate_index.py`)**: `_collect_entries` 정렬 키를 `item.relative_to(directory).parts`로 바꾸고, `_is_excluded`에서 선행 `/` 및 `/` 포함 `exclude_globs` 패턴이 basename과 오매칭되지 않도록 분리했습니다.
- **`F4`·`F5`·`F11` (`scripts/indexes_generate.py`)**: `extensions` 공백·빈 값 검증 정규화, `_is_content_file`의 `__index__` 접두사 제외 복원, `_empty_directory_globs`·`blocked_root_subtrees`의 `glob.escape()` + 선행 `/` 상대 경로 고정 및 단일 스캔화, `_targets` 심볼릭 링크 디렉터리 제외, `sync_indexes`의 `desired is None` 선검사·비-UTF-8 안전 처리·LF 쓰기(`newline="\n"`)·`.`/`..` 안전 라벨(`_display_index_path`)을 반영했습니다.
- **`F6`·`F8`·`F9` (`docs/`, `.rulesync/skills/prj-workflow-pattern/`)**: `docs/development/agent-assets/skills/README.md`, `docs/skills/README.md`, `docs/subagents/README.md`를 신설하고 `docs/documentation/indexing.md`, `docs/documentation/frontmatter.md`, `.rulesync/skills/prj-workflow-pattern/workflows/{publish,lifecycle}.md`를 정합화한 뒤 `docs/INDEX.tsv`와 `docs/development/agent-assets/INDEX.tsv`를 재생성했습니다.
- **`F7` (`tests/`)**: `tests/scripts/test_generated_artifacts_sync.py`, `tests/scripts/test_generated_artifacts_validate.py`, `tests/scripts/test_indexes_generate.py`, `tests/skills/mols-markdown-maintenance/test_generate_index_routing.py`에 `PRESETS`·CLI·`check_*_indexes`·`show_first_difference` 및 `F1`–`F5`·`F11` 회귀 테스트를 추가했습니다.

## 비범위 및 보류 경계

- PR에서 수정하지 않은 기존 `.py` 파일의 저장소 전역 `ruff format` 정리는 이 PR 범위를 벗어나므로 제외합니다.
- `generate_index.py` 수정은 공유 skill 스크립트 변경이므로 `tests/skills/mols-markdown-maintenance/`와 `mise run rulesync-validate`까지 함께 검증합니다.
- 기존 `.inbox/github-302/00-review-scoped-indexes.md` 원문은 변경하지 않고 보존합니다.
- PR #302 머지는 사용자 명시 승인 전까지 수행하지 않습니다.

## 검증 및 마무리 기준

- PR 수정 `.py` 전체(`generate_index.py` 및 수정 테스트 포함) `ruff check` 및 `ruff format --check` 통과
- 이번 작업에서 작성·수정한 `.md` 전체 `rumdl check` 및 `docs_frontmatter_validate.py` 통과
- `pytest -q tests`, `generated_artifacts validate --all`, `generated_artifacts validate --changed-from origin/main`, `mise doctor project`, `mise run rulesync-validate` 통과
- 논리적 단위 커밋·푸시 후 `PR Gate` / `Branch Check` CI 통과 및 PR #302 본문 메타데이터(`revision`, `Validation`, `Review Focus`) 최신화
