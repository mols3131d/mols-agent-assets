# PR #258 로컬 에이전트 인계

> 2026-11-01 확인. 저장소 `mols3131d/mols-agent-assets`, PR head `mols/feat/repository-dev-bootstrap`의 `f70a8bd258895dbdd5616157131abb32b48d5836` 기준이다. 시작할 때 최신 HEAD/working tree와 [PR 리뷰](https://github.com/mols3131d/mols-agent-assets/pull/258)를 다시 확인한다. 정책 정본은 [개발환경 문서](../../docs/development/development-environment.md)와 [mise 운영 안내](../../docs/tools/mise.md)다.

## 현재 상태

PR은 open·Ready for review·미병합 상태다. 기준 head의 [Branch Check](https://github.com/mols3131d/mols-agent-assets/actions/runs/41239130051)와 [PR Gate](https://github.com/mols3131d/mols-agent-assets/actions/runs/41239133679)는 성공했다. 이 결과는 이후 로컬 변경이나 미게시 커밋의 검증 근거가 아니다.

현재 운영 범위는 **CLI 7종 exact pin과 Python-only update**다. CLI bounded update는 구현 완료 항목이 아니라 별도 후속 작업이다. 과거 로컬 브랜치 `agents/pr-258-task-assignment`의 미게시 커밋 `b7fe4233239c205161b8fef3664dfc2d6be10618`은 범위와 실행 위임 방식이 다르므로 그대로 이식하지 않는다. 결정과 실증은 [후속 검증 기록](bootstrap-simplification-review-2026-11-01.md)을 따른다.

## 반영 완료

- **Strict locked install:** [`scripts/development_bootstrap.py`](../../scripts/development_bootstrap.py)는 `mise install --locked <tool@version>`을 사용한다. `mise.lock`은 바이너리 4종의 7개 플랫폼별 URL·체크섬과 npm CLI 3종의 최상위 버전을 잠근다. npm 전이 의존성 그래프 잠금은 포함하지 않는다.
- **정책과 실행 범위 정합성:** 일반 개발환경 정책과 부트스트랩 승인·운영 절차를 분리했다. `setup`은 잠금을 보존하고 `update`는 `uv.lock`만 변경할 수 있다. 예상치 못한 `mise.lock` 변경은 자동 복원하지 않고 실패로 처리한다.
- **Update 입력 보호:** dirty 검사는 `mise.toml`, `pyproject.toml`, `.python-version`, `uv.lock`, `mise.lock`을 대상으로 한다. Git의 `assume-unchanged`·`skip-worktree` 플래그로 변경이 숨겨지거나 index 조회가 실패해도 중단한다. 별도 Rulesync·Skill 파일의 기존 변경은 보존한다.
- **필요한 방어만 유지:** setup의 연속 중복 환경 검사 1회와 중복 `MISE_TASK_RUN_AUTO_INSTALL` 설정을 제거했다. native mise 위임 후보에서 호스트 PATH fallback이 재현되어 npm package identity·managed prefix·pinned Node 검증은 유지한다. Git target, uv 그룹, `.venv` site-packages 격리와 실패 시 부분 상태 보존도 유지한다.

## 추가 도구 문서 작업

사용자 요청에 따라 [Tools](../../docs/tools/README.md)에 프로젝트 도구 안내를 정리했다. 기본 설정과 최신 안정 버전을 우선하되 Node LTS, 출력 일관성, 평가 조건, 외부 자산 revision과 선택적 설치의 예외를 구분한다. CLI pin·lock과 bootstrap 실행 동작은 변경하지 않는다.

mise 운영 안내는 새 위치로 모으고 기존 section 연결은 `docs/development/tooling/mise.md`에 유지했다. 기존 Rulesync·skills reference의 core bootstrap 자동 설치 표현을 수정했다. 문서 인덱스 생성기는 `tools`를 일반 프로젝트 문서로 포함하며 기존 경계 테스트로 확인한다. 이 추가 작업은 사용자 요청에 따라 PR #258 head를 base로 한 별도 문서 PR로 게시하며, 기준 head의 CI 결과를 후속 변경의 검증 근거로 사용하지 않는다.

후속 요청에 따라 `docs/references/agent-assets/`와 `docs/references/tooling/`를 각각 `docs/development/agent-assets/`와 `docs/development/tooling/`로 옮겼다. 상위 탐색과 내부 링크를 새 위치로 갱신하고 비어 있는 references 진입점을 제거했다. 프로젝트 도구의 설정·버전 정책은 계속 [Tools](../../docs/tools/README.md)가 맡으며 설계 지식과 공식 source routing의 본문은 보존한다.

추가 작업 검증은 문서 인덱스 회귀 11개와 전체 deterministic tests 335개, 변경 Python 파일의 Ruff check, pinned rumdl의 변경 문서 검사, 문서 frontmatter와 생성 인덱스 validator를 통과했다. 설치·버전 갱신·model 평가는 실행하지 않았다.

## 검증 근거와 남은 작업

2026-11-01 인계 세션에서 기준 head의 source를 별도 worktree에 고정하고 기존 Python `3.13.11` 가상환경으로 재검증했다. bootstrap 회귀 **72개**, 전체 deterministic tests **335개**가 통과했다. 실행기·직접 관련 테스트의 Ruff check, 문서 frontmatter validator, 이 인계 문서의 rumdl check도 통과했다. `setup --dry-run`과 `update --dry-run`은 모두 `PLAN`으로 종료했으며 실제 설치·resolver 실행이나 host readiness 검증은 수행하지 않았다.

Windows 격리 cold-cache 설치·setup 반복·Python-only update·update 후 setup은 [후속 검증 기록](bootstrap-simplification-review-2026-11-01.md)에 있다. 설치 source는 `8f7bf537f0d17d88f54eb4956463b5e65ed9f395`이며, 기존 mise와 Python을 재사용했다. 이를 최신 head의 신규 설치 실증이나 전체 호스트 초기 설치로 해석하지 않는다.

1. Linux/WSL·macOS native bootstrap E2E는 미검증으로 남긴다. 해당 환경과 실행 허가가 확보되면 Windows 기록과 같은 격리 설치·복구 절차를 재현한다.
1. 후속 문서 PR의 Branch Check를 확인한다. PR Gate는 `main` 대상 PR에서만 실행되므로 #258 병합 뒤 후속 PR의 base를 `main`으로 바꾸고 새 merge candidate의 PR Gate를 확인해야 한다. 최종 결과에는 검증 범위와 미검증 제한을 구분하고, 병합은 별도 명시적 승인 없이 수행하지 않는다.

## 변경·검증 경계

- 호환되는 PATH·프록시·인증·캐시·Git 전역 설정을 불필요하게 초기화하지 않는다. 잠금 실패나 부분 설치를 성공으로 표시하지 않으며 사용자 파일을 자동 rollback하지 않는다.
- 실제 사용자 컴퓨터·공유 cache에 설치/업데이트하기 **전에는 별도 명시적 허가가 필요**하다. HOME Skills·Rulesync projection·Git hook 자동 실행, OS 범위 확대, 범용 설치 프레임워크는 추가하지 않는다. [PR #256](https://github.com/mols3131d/mols-agent-assets/pull/256)의 설계 Skill은 수정하거나 runtime prerequisite로 만들지 않는다.
