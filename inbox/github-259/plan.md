# PR #259 — 로컬 Eval dotenv 인계

## 목표와 경계

- 저장소의 로컬 Promptfoo/Ollama eval 설정을 개발자별 `.env`에서 선택한다.
- `.env.example`만 추적하고 `.env`는 `.gitignore`에 따라 비추적으로 둔다. GitHub PR에서 실제 `.env` 파일을 생성하거나 커밋하지 않는다.
- 모델 선정·벤치마크, eval fixture/contract 변경, 전역 개발 환경 변경은 범위 밖이다.

## 준비 완료 (2026-10-25)

- Draft PR: https://github.com/mols3131d/mols-agent-assets/pull/259
- Branch: `mols/chore/eval-local-env`
- Base: `main` @ `b29aa490d0c251d5ca478fa5c787b90258f09d79`
- `.env.example`: runtime model, grader provider, Ollama URL, timeout, Promptfoo local-only flags 예시
- `mise.toml`: `[env] _.file = ".env"`로 선택적 파일 로딩. 미존재 파일은 무시됨([mise 공식 문서](https://mise.jdx.dev/environments/#env-file)).
- `.gitignore`: 기존 `.env` 무시, `.env.example` 허용 확인. 변경 불필요.
- 기존 runner(`scripts/agent_assets/promptfoo_run.py`, `skills_promptfoo.py`)의 환경변수 기본값은 유지했다. 즉 `.env` 없는 체크아웃에서 동작 기본값이 유지되어야 한다.

## 후속 구현·검증

1. **실제 로컬 파일:** 각 개발자가 `cp .env.example .env`로 생성하고 원하는 Ollama 모델을 입력한다. Git에는 `.env`를 올리지 않는다.
2. **환경변수 책임 확인:** 사용자가 선택하는 model/grader/URL/timeout은 `.env`에 둔다. runner가 계산하는 Python interpreter, cache/log/config 경로와 로컬 전용 안전 기본값까지 억지로 `.env`로 이동하지 않는다. 필요하면 관련 기본값과 override의 경계를 문서화한다.
3. **로딩 우선순위:** mise의 `_.file`은 기존 프로세스 환경값을 덮어쓸 수 있다. CLI 일회성 override와 `.env` 편집 UX를 확인하고 문서에 명시한다.
4. **실행 경로:** `mise run eval-mols-loops-smoke` 및 `mise run eval-mols-loops`에서 로딩 검증. `npm run ...` 직접 실행은 mise를 통하지 않으므로 자동 로딩이 보장되지 않는다.
5. **회귀 확인:** `.env`가 없는 상태와 있는 상태 각각의 모델 선택, JSON output, error handling을 확인하고 적절한 최소 테스트만 추가한다.
6. **문서화:** `evals/README.md` 또는 `docs/development/evaluation.md` 중 기존 정본에 setup/우선순위/로컬 파일 생성 안내를 간결하게 연결한다.
7. **기록:** 사용한 mise/Ollama/Promptfoo 버전, 실제 모델, 실행한 명령 및 결과를 PR Validation에 남긴다. smoke는 모델 동작 검증이 아니다.

## 검증 현황 및 완료 조건

- 확인: GitHub diff에 `.env.example`과 `mise.toml` 변경만 있었고 `.env`는 추적되지 않았다.
- 미실행: 로컬 `mise` dotenv 로딩, Promptfoo smoke, 실제 Ollama runtime eval.
- 완료: 선택한 모델이 `.env`에서 재현 가능하게 로딩되고 `.env` 부재 시 기존 기본값이 유지되며, 로컬 검증 근거와 사용법이 기록된 상태.

## 참고

- mise dotenv: https://mise.jdx.dev/environments/#env-file
- 기존 Eval 소유 정책: `docs/development/evaluation.md`
- 실행 진입점: `mise.toml`, `evals/README.md`
