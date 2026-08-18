# Review Loops

이 문서는 2026-08-03 최종 고도화 과정의 구현·리뷰·개선 기록이다.

## Loop 1 — Functional Baseline

| Area | Finding | Improvement |
| --- | --- | --- |
| Rendering | Jinja whitespace trimming으로 표와 다음 heading 사이 빈 줄이 사라졌다. | Template의 aggressive whitespace marker를 제거하고 section 사이 빈 줄을 유지했다. |
| Status semantics | `planned` 예제가 `1/2` progress를 사용해 정의와 충돌했다. | 해당 item을 `in_progress`로 수정하고 planned/not-started의 completed=0 규칙을 검증한다. |
| Markdown safety | YAML text에 pipe나 newline이 있으면 표 열이 깨질 수 있었다. | `markdown_cell` filter로 pipe escape와 line-break normalization을 추가했다. |
| Consistency | Gap 개수와 남은 Requirement 수의 drift를 탐지하지 못했다. | Implementation gap count와 `total-completed`의 일치를 강제했다. |
| Parser boundary | Markdown validation이 dashboard 구조를 알지 못했다. | Dashboard context를 받아 row label과 optional section 존재를 검증하게 했다. |

**Result:** Functional render path와 기본 semantic validation을 확보했다.

## Loop 2 — Agent And Schema Quality

| Area | Finding | Improvement |
| --- | --- | --- |
| Verification meaning | Progress를 pass count로 해석하면 `10/10 + Failing`을 표현할 수 없다. | 현재 결과가 확보된 Target을 분자에 넣고 pass/fail은 status로 분리했다. |
| Verification gaps | 미검증 gap과 실패 gap이 progress에 미치는 영향이 모호했다. | `failing`은 결과가 있으므로 분자 포함, `unverified/blocked/manual`은 미포함으로 고정했다. |
| Drift detection | Verification progress와 unresolved gap 수가 어긋나도 통과했다. | Non-result gap 개수와 `total-completed` 일치를 검증한다. |
| Input robustness | Pipe와 multiline text에 대한 regression test가 없었다. | Markdown cell escape test를 추가했다. |
| Conditional output | 빈 Risks와 References section이 생기지 않는지 검증이 없었다. | Optional section omission test를 추가했다. |

**Result:** Status, progress와 gap의 의미가 기계적으로 일관되게 됐다.

## Loop 3 — Maintainability And Release

| Area | Finding | Improvement |
| --- | --- | --- |
| Schema durability | 에이전트가 오타 필드를 추가해도 값이 조용히 무시될 수 있었다. | 모든 schema level에서 unknown field를 경로와 함께 거부한다. |
| Internal model | Positional tuple과 mutable-looking boundary가 장기 수정에 취약했다. | Immutable slot dataclass와 이름 있는 `GapRow`를 사용한다. |
| Output safety | 직접 파일 쓰기는 중간 실패 시 파일을 손상시킬 수 있다. | Temporary file 후 `os.replace`하는 atomic write를 적용했다. |
| Aggregate severity | Blocked가 실제 failing 결과보다 먼저 보일 수 있었다. | Verification aggregate에서 Failing을 Blocked보다 높은 우선순위로 둔다. |
| Example drift | 예제 Markdown이 renderer 변경을 따라가지 못하거나 중복 사본이 생길 수 있었다. | YAML을 재렌더링해 checked-in Markdown과 비교하고 reference 중복본을 제거했다. |
| Quality reproducibility | 검증 명령이 사람 기억에 흩어져 있었다. | `uv`, `ruff`, `ty`, `rumdl`, compile, pytest를 단일 스크립트에 고정했다. |
| Recovery | 후속 에이전트가 핵심 구조를 훼손해도 복구 기준이 분산됐다. | `.docs/baseline/DIRECTIVE.md`를 요구사항·결정사항의 정본으로 강화했다. |

**Result:** `uv`를 통한 test 실행에서 40개 테스트가 통과했다. Python line-length와 compile 검증도 통과했다.

## Environment Constraint

현재 생성 환경에서는 외부 DNS와 제공 패키지 미러가 `ruff`, `ty`, `rumdl`, `pyromark` 설치를 제공하지 않았다.
따라서 이 도구들과 실제 pyromark binary를 이 세션에서 성공 실행했다고 기록하지 않는다.

다음은 번들에 완료돼 있다.

- Dev dependency와 최신 설정을 `pyproject.toml`에 고정
- `scripts/check_quality.py`에 품질 순서 고정
- pyromark 공식 event shape를 사용하는 parser boundary 구현
- pyromark boundary regression test
- 도구 누락 시 명시적으로 exit `127` 반환

네트워크가 가능한 환경에서는 `uv sync --all-groups && uv run python scripts/check_quality.py`로 최종 release gate를 재현한다.

## Verification Matrix

| Check | Result in this session |
| --- | --- |
| `uv run ... pytest` | ✅ 40 passed |
| `uv run ... compileall` | ✅ Passed |
| Example render and drift | ✅ Project/domain examples matched |
| Python line-length surrogate | ✅ Passed |
| Markdown structure/line-length surrogate | ✅ Passed |
| Relative Markdown links | ✅ Passed |
| `uv sync --all-groups` | ⚠️ Registry reported `jinja2` unavailable |
| `ruff check` / `ruff format --check` | ⚪ Not executable in this environment |
| `ty check` | ⚪ Not executable in this environment |
| `rumdl check` | ⚪ Not executable in this environment |
| Real pyromark binary parse | ⚪ Package unavailable; event boundary tested |
