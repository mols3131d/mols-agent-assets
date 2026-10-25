# 개발환경 부트스트랩 구현 — PR #258 인계

> 2026-10-25 · 이전 [PR #256](https://github.com/mols3131d/mols-agent-assets/pull/256)에서 실행 코드·운영 정책·안전 검토 아티팩트를 분리한 작업 기록. 운영 정책 정본은 [Development Environment](../../docs/development/development-environment.md)이다.

## 소유 범위

- **PR #258:** `mise.toml` setup/update, `scripts/development_bootstrap.py`, `tests/scripts/test_development_bootstrap.py` 및 Git fixture, 프로젝트 부트스트랩 운영 정책·mise 안내·조사/검토 문서.
- **PR #256:** 외부 프로젝트에 이식 가능한 `mols-dev-env-bootstrap-design` 설계 Skill, canonical Skill·유지보수 문서·trigger/behavior 평가·배포 route.
- 독립 PR이므로 #258의 실행 코드/테스트와 #256의 Skill은 서로를 build-time/runtime prerequisite으로 요구하지 않는다. 두 PR은 각각 `main` 대상으로 리뷰·머지한다.

## 현재 구현 근거

- 전 통합 브랜치 HEAD `540222f25dc26713aa4d8e94f27dea126281fb37`에서 실행 코드와 문서를 이관했다. 그 이전에 보고된 테스트 308개 및 Windows 기존 캐시 기반 재실행은 참고일 뿐, 현재 분리 PR의 통과 증거가 아니다.
- 기본 경로는 exact-pinned CLI 및 project Python. `setup`은 locked sync, `update`는 Python dependency constraints 안에서 `uv lock --upgrade`; CLI tool range/`mise.lock`은 미구현.
- Rulesync projection, HOME Skills, Git hooks는 기본 READY 범위에서 제외한 선택적 연동. 실제 설치 실행은 사용자 승인 정책을 따른다.

## 머지 전 필수

1. [격리·안전성 리뷰](bootstrap-isolation-review-2026-10-25.md) F1 외부 `GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE` 상속, F2 `UV_NO_GROUP`에 의한 false READY, F3 기존 `.venv`의 system-site-packages 노출에 대한 최소 수정과 회귀 검증.
2. 문서 INDEX 생성·검증 및 PR Gate 통과. (이관 시 docs index 누락 행은 추가함. 실제 gate는 별도 확인.)
3. 기존 exact CLI pin과 사용자 허가를 유지한 채 초기 의도인 bounded tool update를 이 PR에 구현할지, 별도 후속으로 이관할지 acceptance 확정.
4. Windows warm cache 증거와 clean/cold 및 Linux/macOS/WSL 근거를 혼동하지 않기.

## 관련 기록

- [기존 통합 PR의 high finding](https://github.com/mols3131d/mols-agent-assets/pull/256#discussion_r4367794052)
- [부트스트랩 명세](development-environment-bootstrap-spec.md)
- [복잡성 리뷰](bootstrap-overengineering-review-2026-10-25.md)
- [범용 Skill PR #256](https://github.com/mols3131d/mols-agent-assets/pull/256)

이전 아티팩트 내부의 `PR #256` 및 과거 commit SHA 표기는 역사적 조사 시점의 근거일 수 있으며, 현재 PR #258의 코드 검증이나 작업 완료 상태로 대체하지 않는다.
