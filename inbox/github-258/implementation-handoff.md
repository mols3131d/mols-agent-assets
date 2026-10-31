# PR #258 — 로컬 에이전트 인계

> 저장소 `mols3131d/mols-agent-assets` · 브랜치 `mols/feat/repository-dev-bootstrap` · 2026-10-25. 시작할 때 최신 HEAD/working tree와 [PR 리뷰](https://github.com/mols3131d/mols-agent-assets/pull/258)를 다시 확인한다. 정책 정본은 [개발환경 문서](../../docs/development/development-environment.md)다.

## 반영 완료

- **mise.lock 도입 및 strict locked install 강제:** `mise lock`을 통해 네이티브 바이너리 4종의 7개 플랫폼별 아티팩트 URL·체크섬과 npm 3종의 버전을 `mise.lock`으로 잠금 관리한다. `development_bootstrap.py`에서 `mise.lock`을 정책 파일 및 update 입력에 편입하고 `mise install --locked <tool@version>`으로 native strict locked install을 강제했다.
- **CLI 버전 정책 확정:** 7개 CLI 도구를 4개 케이스(1. 패치 준수 최신, 2. 마이너 준수 최신, 3. 메이저 준수 최신, 4. 최신 안정)로 분류하고, 허용 범위·잠금 소유자·`setup`(잠금 재현) vs `update`(범위 내 갱신) 원칙을 [`docs/references/tooling/mise.md`](../../docs/references/tooling/mise.md)에 정립했다. [`mise.toml`](../../mise.toml)에는 exact pin 정책과 문서 참조를 명시했다.
- **실행기 간소화:** `scripts/development_bootstrap.py`에서 `mise.toml`의 `[settings] task.run_auto_install = false`와 중복되는 `MISE_TASK_RUN_AUTO_INSTALL` 강제 설정을 제거했다. Windows `.cmd`/pinned Node 격리를 위한 `tool_command()` 및 버전 검증은 안전하게 유지했다.
- **개발환경 정본 문서 구조 정돈:** [`docs/development/development-environment.md`](../../docs/development/development-environment.md)를 주제별 일반 거버넌스 정책(격리 경계, 재사용 원칙, 버전 수명 주기)과 부트스트랩 운영 절차(에이전트 승인 게이트, Core vs 선택적 연동, setup/update 경계)로 체계화하고 세부 명령은 `mise.md`로 연결했다.
- **Update 사전 검사 축소:** `scripts/development_bootstrap.py`의 dirty 검사는 `mise.toml`, `pyproject.toml`, `.python-version`, `uv.lock`만 대상으로 한다. 별도 Rulesync·Skill 파일의 기존 변경은 보존하며, 실행 도중의 예상치 않은 정책 파일 변경 감지는 유지했다.
- `tests/scripts/test_development_bootstrap.py`에 관련 5개 회귀 사례를 추가하고 `docs/references/tooling/mise.md`의 설명을 맞췄다. [PR Gate #40191470826](https://github.com/mols3131d/mols-agent-assets/actions/runs/40191470826)에서 **320 tests passed**를 확인했다. 후속 변경은 각각 재검증한다.
- 근거·남은 위험: [Skill ↔ 실행기 검토](bootstrap-skill-script-alignment-review-2026-10-25.md). 이전 F1 Git, F2 uv 그룹, F3 `.venv` 격리 수정은 그대로 유지했다.

## 남은 작업

1. **최종 검증 및 PR 코멘트 인계:** 전체 320개 deterministic test 통과 및 포맷/린트 검증 후 PR #258에 최종 결과 요약.

## 변경·검증 경계

- 프로젝트 `.venv` 격리, setup lock 불변, update의 dirty input 보호, F1–F3, 실패 시 부분 상태 보존 및 필수 실패의 nonzero/미완료 표시를 지킨다. 호환되는 PATH·프록시·인증·캐시·Git 전역 설정을 불필요하게 초기화하지 않는다.
- 실제 사용자 컴퓨터·공유 cache에 설치/업데이트하기 **전에는 별도 명시적 허가가 필요**하다. HOME Skills·Rulesync projection·Git hook 자동 실행, OS 범위 확대, 범용 설치 프레임워크는 이번 작업에 추가하지 않는다. [PR #256](https://github.com/mols3131d/mols-agent-assets/pull/256)의 설계 Skill은 수정하거나 runtime prerequisite로 만들지 않는다.
- 변경 범위에 맞는 회귀 테스트와 native 확인을 수행하고 PR Gate를 확인한다. 실제 pinned mise/uv + Windows/macOS/WSL/cold-cache 검증이 없으면 미검증으로 보고한다. 완료 시 PR에 **결과·증거·남은 제한**만 남기고 Draft/미병합 상태를 유지한다.
