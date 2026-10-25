# PR #258 — 로컬 에이전트 인계

> 저장소 `mols3131d/mols-agent-assets` · 브랜치 `mols/feat/repository-dev-bootstrap` · 2026-10-25. 시작할 때 최신 HEAD/working tree와 [PR 리뷰](https://github.com/mols3131d/mols-agent-assets/pull/258)를 다시 확인한다. 정책 정본은 [개발환경 문서](../../docs/development/development-environment.md)다.

## 반영 완료

- **Update 사전 검사 축소:** `scripts/development_bootstrap.py`의 dirty 검사는 `mise.toml`, `pyproject.toml`, `.python-version`, `uv.lock`만 대상으로 한다. 별도 Rulesync·Skill 파일의 기존 변경은 보존하며, 실행 도중의 예상치 않은 정책 파일 변경 감지는 유지했다.
- `tests/scripts/test_development_bootstrap.py`에 관련 5개 회귀 사례를 추가하고 `docs/references/tooling/mise.md`의 설명을 맞췄다. [PR Gate #40191470826](https://github.com/mols3131d/mols-agent-assets/actions/runs/40191470826)에서 **320 tests passed**를 확인했다. 후속 변경은 각각 재검증한다.
- 근거·남은 위험: [Skill ↔ 실행기 검토](bootstrap-skill-script-alignment-review-2026-10-25.md). 이전 F1 Git, F2 uv 그룹, F3 `.venv` 격리 수정은 그대로 유지했다.

## 남은 작업

1. **버전 정책부터 확정:** [리뷰](https://github.com/mols3131d/mols-agent-assets/pull/258#pullrequestreview-5642776539)에 따라 `mise.toml`의 7개 CLI를 실제 사용·호환성 기준으로 분류하고, 허용 범위/lock 소유자를 정한다. `setup`은 잠금을 재현하고 `update`만 승인된 범위 내에서 새 버전을 선택·검증하도록 native mise 기능을 우선한다. 검증 전 임의의 `latest`·range 선언 금지.
2. **실행기 간소화:** [리뷰](https://github.com/mols3131d/mols-agent-assets/pull/258#pullrequestreview-5642787295)를 기준으로 환경변수 강제 지정 7개·제거 6개, Node `PATH`, npm metadata 탐색, 중복 버전 확인을 검토한다. 기본값·기존 사용자 설정·mise/uv/Git native 기능으로 동등하게 처리할 수 있는 부분만 줄인다. Windows `.cmd`/pinned Node 실행 검증 없이 `tool_command()`을 제거하지 않는다.
3. **개발환경 문서 정돈:** `docs/development/development-environment.md`는 주제별 일반 정책을 중심에 두고, 부트스트랩 고유 절차·승인·setup/update는 부트스트랩 섹션으로 모은다. 중복 명령은 [mise 안내](../../docs/references/tooling/mise.md)를 참조한다.

## 변경·검증 경계

- 프로젝트 `.venv` 격리, setup lock 불변, update의 dirty input 보호, F1–F3, 실패 시 부분 상태 보존 및 필수 실패의 nonzero/미완료 표시를 지킨다. 호환되는 PATH·프록시·인증·캐시·Git 전역 설정을 불필요하게 초기화하지 않는다.
- 실제 사용자 컴퓨터·공유 cache에 설치/업데이트하기 **전에는 별도 명시적 허가가 필요**하다. HOME Skills·Rulesync projection·Git hook 자동 실행, OS 범위 확대, 범용 설치 프레임워크는 이번 작업에 추가하지 않는다. [PR #256](https://github.com/mols3131d/mols-agent-assets/pull/256)의 설계 Skill은 수정하거나 runtime prerequisite로 만들지 않는다.
- 변경 범위에 맞는 회귀 테스트와 native 확인을 수행하고 PR Gate를 확인한다. 실제 pinned mise/uv + Windows/macOS/WSL/cold-cache 검증이 없으면 미검증으로 보고한다. 완료 시 PR에 **결과·증거·남은 제한**만 남기고 Draft/미병합 상태를 유지한다.
