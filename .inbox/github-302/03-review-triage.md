# PR 302 2차 리뷰 수용 판단 및 개선 정리

이 문서는 [PR 302 2차 다관점 리뷰 보고서](02-review-scoped-indexes.md)에서 채택된 관찰(`F1`–`F4`)과 제외 항목(`C5`–`C9`)에 대한 반영 내역을 정리한 `.inbox/` 작업 기록입니다. 저장소 정본 정책을 대체하지 않습니다.

## 수용 반영 요약 (`F1`–`F4`)

| ID | 심각도 | 판단 | 반영 내용 및 대상 |
| --- | --- | --- | --- |
| `F1` | Medium | 수용 | `src/rulesync/.rulesync/skills/mols-markdown-maintenance/scripts/generate_index.py`에 `_normalize_pattern_parts`·`_segments_match`를 도입해 `_is_excluded`가 `/` 없는 패턴은 `path.name`만, `/` 포함(선행 `/` 포함) 패턴은 세그먼트 경계를 지키는 상대 경로만 매칭하도록 수정(`/*.md`·`test*.md`·`__*__.md`·`.*.md` `/` 초과 매칭 해소). Dot-prefixed 디렉터리(`.internal/`)는 `_is_content_file`·`_targets`·`generated_artifacts_sync.py`·`docs_frontmatter_validate.py`와 일치하게 허용(`.*.md` 파일만 제외)하고, `01-review-triage.md`의 1차 `F4` 상태와 회귀 테스트를 현행화 |
| `F2` | Low | 수용 | `generate_index.py`의 `_is_excluded`·`_segments_match`를 `fnmatch.fnmatchcase`로 통일해 Windows/POSIX 대소문자 결과를 일치시키고, `--exclude-glob` `--help` 문구에 대소문자 구분 및 basename·`/` 경로 스코핑 규칙(`**` 포함)을 명시 |
| `F3` | Low | 수용 | `docs/skills/README.md`, `docs/subagents/README.md`, `docs/development/agent-assets/skills/README.md`에 `src/<vendor>/` 작성 원본 경로를 추가하고, `docs/skills/README.md`·`docs/subagents/README.md`의 `description`을 `재사용` 한정에서 `개별 Skill과 Skill family`·`개별 Subagent와 Subagent family`로 넓혀 본문 범위와 일치시킨 뒤 `docs/INDEX.tsv`를 재생성 |
| `F4` | Low | 수용 | `tests/scripts/test_indexes_generate.py`에서 설정값 복제 스냅샷 테스트(`test_presets_match_repository_boundaries`)를 제거해 `docs/development/testing.md`와 일치시키고, 알 수 없는 `--target` preset 종료코드(`2`), `--root ... --prune` 오버라이드, `expected` 비-UTF-8 `INDEX.tsv`(`outdated` 보고·복구), `depth=-1` 심볼릭 링크 하위 제외(`/{escaped}/**`), 루트 `README.md` 자체 제외, `.internal/` depth 일관성 테스트를 추가 |

## 비수용(`C5`–`C9`) 및 경계

- PR #302 이전(`c39d094f`)부터 존재하던 코드·구성의 개선 요구(`C5`), 기존 커밋 `00-review-scoped-indexes.md`의 `#L` 링크 `[MD051]`(`C6`), 과도한 문구·구조 변경 요구(`C7`–`C9`)는 2차 리뷰의 Drop 판단 그대로 PR 범위에서 제외했습니다.
- `.rulesync/skills/prj-workflow-pattern/` 워크플로 4건과 공유 `generate_index.py` 통제 표면 변경의 최종 승인은 사람 리뷰어가 소유합니다.
