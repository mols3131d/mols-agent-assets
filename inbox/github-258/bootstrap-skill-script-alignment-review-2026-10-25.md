# PR #256 설계 Skill ↔ PR #258 실행기 검토 (2026-10-25)

## 판정

[설계 Skill](https://github.com/mols3131d/mols-agent-assets/blob/b381dbdbfa91cf8a72517a5286daebc2a753e3f1/src/rulesync/.rulesync/skills/mols-dev-env-bootstrap-design/SKILL.md)은 **설계·리뷰 전용**이다. 실행기는 [개발환경 정책](../../docs/development/development-environment.md)과 기존 native tool 계약을 우선한다. 현재 `setup`의 locked sync, 프로젝트 `.venv` 격리, 부분 실패 보고 및 HOME·hook 자동 쓰기 제외는 유지해야 한다. 스킬에 없는 범용 설치 엔진이나 승인 옵션을 새로 구현할 근거는 없다.

## 이번에 직접 수정한 항목

- **불필요한 update 차단 제거:** [실행기](../../scripts/development_bootstrap.py)의 Git 사전 dirty 검사를 실제 bootstrap 입력 4개(`mise.toml`, `pyproject.toml`, `.python-version`, `uv.lock`)로 축소했다. 무관한 `rulesync.jsonc`/`rulesync.lock`/`skills-lock.json`의 기존 사용자 변경만으로 Python update를 막지 않는다.
- **안전장치는 유지:** 업데이트 대상 Git worktree 식별, 대상 4개 입력의 dirty 차단, 실행 도중 7개 policy 파일의 예상치 않은 수정 감지, F1 Git 오염·F2 uv 그룹·F3 `.venv` 격리를 보존했다.
- [회귀 테스트](../../tests/scripts/test_development_bootstrap.py)에 별도 자산의 기존 수정 허용/보존 1건과 부트스트랩 입력별 dirty 거부 4건을 추가했다. [mise 운영 안내](../../docs/development/tooling/mise.md)도 이 경계를 반영했다.

## 로컬 에이전트에게 남긴 판단

1. **CLI 정책:** `mise.toml`의 7개 도구는 현재 모두 exact pin이며 `update`는 Python lock만 갱신한다. 호환성 우선과 bounded 최신 stable 지향 도구를 실제 사용처·native lock 지원에 근거해 구분한다. 검증 전에는 무조건 `latest`·range로 바꾸지 않는다.
1. **스크립트 경량화:** 강제 설정 7개, 제거 6개, Node `PATH` 조정과 `tool_command()`의 npm metadata 탐색을 항목별로 평가한다. 특히 Windows `.cmd` 실행과 정확한 pinned Node 선택을 native `mise exec`로 동등하게 처리하는지 확인하기 전에는 기존 구현을 삭제하지 않는다. 무관한 사용자 프록시·인증·캐시 설정은 유지한다.
1. **문서 구조:** `development-environment.md`의 주제별 책임을 정리하고 부트스트랩 고유 내용을 별도 섹션에 모은다. 명령 상세는 mise 가이드로 연결한다.

## 검증 경계

이번 변경은 **GitHub의 코드·테스트·문서 수정**이며 사용자 시스템에서 설치·갱신하지 않았다. 기존 PR Gate 315 tests 성공은 과거 revision의 근거다. 새 회귀 테스트를 포함한 [PR Gate #40191470826](https://github.com/mols3131d/mols-agent-assets/actions/runs/40191470826)은 코드·테스트·초기 인계 커밋 `a6c181708d21b46d143c7335994877bbe43094a2`에서 **320 tests passed / 성공**이었다. 후속 문서 커밋의 CI는 별도 결과로 구분한다. pinned mise/uv의 오염 환경과 Windows/macOS/WSL cold-cache 실제 실행은 아직 검증하지 않았다. 상세 작업 순서는 [구현 인계](implementation-handoff.md)에 둔다.
