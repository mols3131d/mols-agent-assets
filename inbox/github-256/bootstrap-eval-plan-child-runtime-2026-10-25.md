# 재귀 Child — Eval 실행 환경의 안전성·재현성

> 2026-10-25 · 부모 [Review 2](bootstrap-eval-plan-review-2026-10-25.md)에서 push한 strict-subset 과제
>
> **Goal:** 평가 계획이 사용자의 기존 환경/캐시/네트워크를 무단으로 바꾸거나 데이터를 외부 전송하지 않도록, 현재 runner의 실제 조건을 기준으로 실행 전 확인 사항을 확정한다. 상위 Scope·권한·설치 금지 상속. 실제 명령 실행과 신규 환경설정 생성은 하지 않는다.

## Child Research

**Verified — repository 원본 관찰**

- `scripts/agent_assets/promptfoo_run.py::build_env`는 이미 설정된 `PROMPTFOO_CONFIG_DIR`, `PROMPTFOO_LOG_DIR`, `PROMPTFOO_CACHE_PATH`, `PROMPTFOO_PYTHON`, `PROMPTFOO_RUNTIME_MODEL`, `PROMPTFOO_GRADER_PROVIDER`를 `setdefault`로 **보존**한다. 기본 로그 경로는 `.tmp/promptfoo`이나 현재 사용자 override가 있으면 다를 수 있다.
- `resolve_npx`는 Node>=22.22.0와 npx 실행 파일을 확인하고, `subprocess.run([npx,"--yes","promptfoo@0.122.0",...])`를 실행한다. 캐시 부재 시 원격 package 취득/캐시 쓰기 가능성은 실행 전 영향으로 판단해야 한다.
- `package.json`의 `npm run eval:promptfoo:mols-dev-env-bootstrap-design`은 `uv run --locked --no-default-groups --group test`로 Python 환경을 준비할 수 있다. `--locked`는 lock rewrite 방지이지 `.venv`/캐시 무변경 보장이 아니다.
- `skills_promptfoo.py::_ollama_request`는 `OLLAMA_BASE_URL`이 없다면 `http://127.0.0.1:11434`를 사용하지만, 상속된 값이 있으면 해당 엔드포인트로 Skill 전문·user prompt가 전송될 수 있다. 원격 서버를 로컬이라고 가정하면 안 된다.
- grader는 `PROMPTFOO_GRADER_PROVIDER`를 사용한다. `ollama:chat:<local-model>`이 아닌 provider가 이미 설정되어 있다면 사용자의 기대와 다른 전송 경로가 될 수 있다.
- `evals/promptfoo/mols-dev-env-bootstrap-design.yaml`은 `sharing:false`, `writeLatestResults:false`, cache/write/noShare 설정을 가진다. 이 옵션만으로 다른 도구들의 네트워크·로컬 캐시 쓰기 전체가 없어지는 것은 아니다.

## Child Plan — 실행 전 안전 게이트

1. **읽기 전용 확인:** 실제 실행 셸의 `node`, `npx`, `uv`, Ollama 서비스/모델 목록과 Python group 환경 충족 여부를 조회한다. 도구가 없으면 **수동 설치 제안만**, 자동 설치/프로필 수정 금지.
2. **영향 경로 확인:** 현재 `PROMPTFOO_CONFIG_DIR`, `LOG_DIR`, `CACHE_PATH`, `PYTHON` 등 상속 설정의 유무와 실제 저장 대상, `npm/npx`와 `uv` 캐시/프로젝트 `.venv` 쓰기 가능성을 점검한다. 값이나 토큰·민감 경로를 PR에 원문 저장하지 않는다.
3. **전송 대상 확인:** `OLLAMA_BASE_URL`의 현재 유효 엔드포인트가 로컬인지, grader provider가 실제로 로컬 Ollama인지 확인한다. 원격을 쓸 필요가 없다면 사용자 전역 설정을 변경하지 않고 **안전한 로컬 실행 경로를 제안**한다. 원격 전송 경로가 불분명하면 실행 보류.
4. **승인 분리:** 실행 때문에 **새 package fetch, model pull, shared cache write, 프로젝트 환경 동기화**가 발생한다면 영향 대상과 네트워크·디스크 비용을 설명한 뒤 승인받는다. `--yes`/평가 요청은 별도 설치 승인으로 치지 않는다.
5. **최소 실행 조정:** 기존 기본 설정이 안전하고 충족하면 그대로 사용한다. 충돌이 있으면 전체 전역 설정을 지우거나 늘리지 말고, 승인받은 실행의 **해당 프로세스 한정** 설정으로만 좁게 해소하거나 blocker로 보고한다.
6. **실험 격리와 종료:** PR 대상 branch/ref/dirty 상태를 보존하고 실행기 내부 작업 디렉터리/캐시 변경은 가능한 한 기존 정책 내로 묶는다. 마무리 시 실제로 무엇이 쓰였는지, 어떤 설치·네트워크 접근이 있었는지 확인 가능한 범위만 기록한다.

## Child Review

- **absorb / High:** 기존 env에 대한 `setdefault`는 격리 보장과 다르다. 상속 경로를 실행 전에 반드시 확인하는 최소 read-only preflight를 parent에 추가해야 한다.
- **absorb / High:** grader와 `OLLAMA_BASE_URL`의 유효 endpoint를 확인하지 않으면 source/prompt가 의도치 않은 외부로 나갈 수 있다. local-only 성능이라고 주장하려면 실제 로컬 조건을 검증해야 한다.
- **absorb / Medium:** `uv run --locked`/npx가 write-free로 보장된다는 가정 제거. 필요 설치 단계는 따로 승인받는다.
- **reject:** 새 환경정화 스크립트, CLI wrapper, 수십 개 환경변수 지정, Docker/가상화 필수화. 현 목표에 비해 과설계.
- **residual unknown:** 사용자 시스템의 실제 inherited config, endpoint, cached dependencies는 작업자가 자신의 환경에서 확인해야 한다.
- **Dispatch:** 부모 [계획](bootstrap-eval-plan-2026-10-25.md)의 preflight/permissions 단계와 [Review](bootstrap-eval-plan-review-2026-10-25.md)의 최종 확인 항목에 반영.
- **Run accounting:** Child Review 종료, 공유 카운터 `loops_used=4`. 하위 계획 목표는 충족; 실제 실행 증거는 `not_run`.
