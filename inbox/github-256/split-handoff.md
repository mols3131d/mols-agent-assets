# PR #256 — 범용 부트스트랩 설계 Skill 인계

> 2026-10-25 · 프로젝트 전용 개발환경 실행 코드·운영 정책·구현 검토 문서는 [PR #258](https://github.com/mols3131d/mols-agent-assets/pull/258)로 이관. 이전 통합 브랜치 HEAD는 `540222f25dc26713aa4d8e94f27dea126281fb37`.

## 현재 PR 책임

- 배포 가능한 portable `mols-dev-env-bootstrap-design` 단일 canonical Skill 및 generated route
- 유지보수 설명과 사용 조건 (일반 패키지 업데이트·단일 도구 설치·CI-only 작업은 선택하지 않음)
- Trigger/behavior Eval fixture와 기존 공통 Promptfoo 실행 경로
- Skill 조사·이식성·과잉 작업량 리뷰 및 작동 품질 개선

## 이관한 책임

- `mise run setup/update`, `scripts/development_bootstrap.py`, bootstrap regression tests 및 Git fixture
- 이 저장소의 개발환경 구축 정책 정본·mise 운영 문서·CLI/OS/UX/안전성 조사·설계 자료
- Git 환경 상속, uv group, `.venv` system site 문제의 구현 수정과 테스트

## 이후 필요한 Skill 작업

1. [과도한 작업 유발 리뷰](bootstrap-skill-workload-review-2026-10-25.md)를 바탕으로 요청 범위에 맞게 Procedure/Handoff 최소 간소화 (설계 스킬이지 설치·실행 스킬이 아님).
2. 다른 프로젝트·언어·tool manager의 관리/격리 계약을 무조건 Python 관행으로 일반화하지 않도록 검토.
3. 최신 11-case Promptfoo eval 및 near-miss/리뷰 전용 behavior 재평가. 기존 Qwen/Nemotron 시험 수치를 새로운 head의 pass로 해석하지 않음.
4. Route/formatter/Skill validation·PR Gate를 새 분리 head에서 확인. 사용자 환경 설치 없이 수행.

**독립성:** 이 PR을 merge할 때 PR #258의 스크립트·설치·운영 정책 파일은 변경하지 않는다. 양쪽 모두 `main`을 기준으로 독립 검토·merge한다.
