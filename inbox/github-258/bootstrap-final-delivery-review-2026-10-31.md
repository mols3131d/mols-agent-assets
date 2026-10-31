# 부트스트랩 최종 인계 및 PR #258 완료 검토

> **상태:** 검토 및 검증 완료 (2026-10-31). PR Gate #41206679705 통과.
> **정본:** [개발환경 운영 정책 정본](../../docs/development/development-environment.md). 실행 안내는 [mise 안내](../../docs/references/tooling/mise.md), 실행기는 [`scripts/development_bootstrap.py`](../../scripts/development_bootstrap.py).
> **대상 PR:** [PR #258](https://github.com/mols3131d/mols-agent-assets/pull/258) · 브랜치 `mols/feat/repository-dev-bootstrap`

---

## 1. PR #258 작업 완료 총괄

PR #258은 PR #256에서 분리되어 저장소 개발환경의 실제 부트스트랩 실행기와 운영 거버넌스를 완성했다.

| 작업 영역 | 이전 상태 | 최종 해결 내용 | 관련 문서/코드 |
| --- | --- | --- | --- |
| **F1: Git target 격리** | 외래 Git 환경변수로 다른 repo 검사 가능 | child git 실행 시 `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE` 제거 | [`development_bootstrap.py`](../../scripts/development_bootstrap.py) |
| **F2: uv group 격리** | 상속된 `UV_NO_GROUP`으로 dev/test 누락 가능 | `uv sync` 시 `UV_NO_GROUP`, `UV_NO_DEV` 제거 (proxy/auth/cache 보존) | [`development_bootstrap.py`](../../scripts/development_bootstrap.py) |
| **F3: .venv 격리** | 시스템 패키지 노출 venv 오염 가능 | `include-system-site-packages = true`, 외부 symlink/junction 차단 | [`development_bootstrap.py`](../../scripts/development_bootstrap.py) |
| **Update 검사 최적화** | 무관한 Rulesync·Skill 수정까지 차단 | `UPDATE_INPUTS` 5개 파일(`mise.toml`, `pyproject.toml`, `.python-version`, `uv.lock`, `mise.lock`)로 한정 | [`development_bootstrap.py`](../../scripts/development_bootstrap.py) |
| **CLI 버전 정책** | 단순 exact pin 나열 | 4개 케이스 분류 정립 및 7개 도구 매핑 완료 | [`docs/references/tooling/mise.md`](../../docs/references/tooling/mise.md) |
| **잠금 체계 완성** | `mise.lock` 도입 차단 상태 | `mise.lock` 생성(7도구/7플랫폼) 및 정책 파일 연동 완료 | [`mise.lock`](../../mise.lock) |
| **실행기 간소화** | `MISE_TASK_RUN_AUTO_INSTALL` 강제 | `mise.toml` native 설정과 중복되는 환경변수 제거, Windows/Node 방어 보존 | [`development_bootstrap.py`](../../scripts/development_bootstrap.py) |
| **문서 구조 정돈** | 명령과 정책 혼재 | 일반 거버넌스(격리·재사용·버전) vs 부트스트랩 섹션 분리 | [`docs/development/development-environment.md`](../../docs/development/development-environment.md) |

---

## 2. 검증 증거

1. **GitHub Actions CI:**
   - **Branch Check:** Success
   - **PR Gate ([Run #41206679705](https://github.com/mols3131d/mols-agent-assets/actions/runs/41206679705)):** **Success** (`1m 4s`)
1. **로컬 테스트 스위트:**
   - `uv run pytest`: **323 passed** (100% 성공)
   - `tests/scripts/test_development_bootstrap.py`: 58개 회귀 테스트 포함
1. **부트스트랩 명령 실행:**
   - `uv run python scripts/development_bootstrap.py setup --dry-run` → `Result: PLAN` (정상)
   - `uv run python scripts/development_bootstrap.py update --dry-run` → `Result: PLAN` (정상)
1. **정적 분석 및 포맷팅:**
   - `rumdl check`: 0 issues
   - `ruff check` & `ruff format`: 0 issues

---

## 3. 남은 제한 및 후속 권장 과제

- **다중 OS 실기 Smoke:** Windows 임시 snapshot 및 Linux 워크스페이스 검증은 완료했으나, macOS/WSL 및 완전 cold-cache 상태에서의 클린 설치 테스트는 후속 과제로 권장.
- **도구 허용 범위(Range) 점진 도입:** `mise.lock`이 안정적으로 도입되었으므로, 향후 도구별 하위 호환성 검증을 거쳐 `biome`, `rumdl` 등 Case 1 도구부터 `~X.Y` 단위의 bounded range 도입 검토 가능.
