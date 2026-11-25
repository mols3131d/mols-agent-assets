# 검증 및 완료 계획

[인계 요약](00-handoff-promptfoo.md)과 [구현 계획](01-plan-provider-integration.md)의 완료 조건을 현재 PR diff와 대조한다. 모델 평가를 실행하지 않고 확보할 수 있는 증거부터 수집한다.

## 자동 검증과 모델 호출의 분리

다음은 repository correctness를 위한 테스트다. 실제 CLI·HTTP·모델 호출은 test double로 대체하고 모델 다운로드, 로그인, credential 접근을 수행하지 않는다. 기존 CI의 deterministic test를 재사용한다.

| 검증 | 최소 관찰 기준 |
| --- | --- |
| 실행 진입점 | bare/help, config 누락, 유효하지 않은 선택이 모델 실행·설치 전에 종료 |
| Provider/model 선택 | 명시값 우선순위, 빈 값 및 미지원 조합 거부, fallback 없음 |
| Grader | semantic suite에서 grader 누락 시 조기 실패, fixture-only에서 모델 호출 없음 |
| CLI adapter | 명령 인수·모델·인증 경계·cwd·timeout·exit code·JSON parsing을 mock으로 검증 |
| 회귀 | 기존 trigger/behavior label, strict assertion, reference fixture, grader calibration 의미 보존 |
| 자동 실행 경로 | CI, hook, bootstrap, check, task dependency에서 Promptfoo 모델·grader 호출 없음 |
| 데이터 경계 | 평가 캐시·log·결과·환경정보의 Git 유출 방지; 실제 credential을 테스트에 사용하지 않음 |

기존 테스트 위치는 [tests/scripts/agent_assets/](../../tests/scripts/agent_assets/)다. `test_promptfoo_run.py`, `test_promptfoo_env.py`, `test_skills_promptfoo*.py`를 우선 확인한다. 현재 runner defaults 테스트는 암묵적 Ollama fallback을 계약으로 고정하므로 명시 선택 요구에 맞춰 변경한다. 기존 테스트의 실패를 삭제하거나 약화하여 숨기지 않는다.

## 로컬 검증 순서

1. 현재 PR head와 base를 확인하고 적용 지침·개발 도구 상태를 읽는다.
2. 구현 후 모델 호출이 없는 해당 단위 테스트와 전체 repository test를 실행한다. 예: `uv run --locked --no-default-groups --group test pytest -q tests/scripts/agent_assets`, `uv run --locked --no-default-groups --group test pytest -q tests`. 실행 전 테스트가 실제 모델을 부르지 않는지 확인한다.
3. [mise.toml](../../mise.toml)과 [검증 정책](../../docs/development/validation.md)에 따른 formatting, quality-check, generated projection 검증을 적용한다. 정본 변경에 따라 필요할 때만 공식 생성 명령을 사용한다.
4. 설치된 Promptfoo의 version/help, config schema 및 provider contract를 모델 호출 없이 확인한다. 의존성 설치가 필요하면 저장소 정책에 맞춰 수행하며 모델 설치와 구분한다.
5. 전체 diff와 Goal/Boundaries를 self-review한다. 실패·미검증 사유를 PR에 기록하고 수정 후 최신 HEAD 기준으로 재검토한다.

Promptfoo fixture-only integration smoke도 실제 eval 명령이므로 사용자 요청 없이 실행하지 않는다. 일반 pytest의 fixture/mock 검증은 smoke 실행과 구분한다.

## 사용자 요청 시에만 수행할 수동 검증

실행 전에 대상 config와 case 범위, provider/model, 필요한 grader, 인증 명의·방식, 데이터 전송과 예상 비용, 네트워크·작업 공간을 확인한다. 이 자료 자체는 실행 승인이 아니다.

| 선택 | 최초 수동 확인 |
| --- | --- |
| Ollama | 이미 설치된 선택 모델로 지정한 최소 trigger case 실행 |
| Codex | 공식 native provider, 선택한 로그인/API 인증과 모델, 제한된 작업 공간에서 같은 case 실행 |
| Antigravity | 허용 근거와 실행 격리가 확인된 공식 CLI 경로에서 같은 case 실행; 불명확하면 실행하지 않음 |
| Semantic behavior | 승인된 독립 grader를 명시하고 대상·grader 오류를 구분 |

명시 승인된 최소 case에서 시작하고 실제 사용한 runtime/provider/model, 평가 revision, grader 및 결과·오류만 기록한다. 하나의 provider가 통과해도 다른 provider의 성공으로 해석하지 않는다. 비용이 발생하거나 평가 범위를 확대하려면 별도 승인을 확인한다.

## 완료 판정

- 최신 안정 버전 pin과 upstream compatibility를 확인했다.
- 세 provider의 명시적인 선택 및 지원 범위가 구현·문서·테스트에 일치한다. Antigravity는 허용 근거가 없으면 차단 상태로 남긴다.
- 자동 평가 실행 경로가 없고 미지정·오류 시 모델을 호출하지 않는다.
- 모델 없는 deterministic 검증과 최신 HEAD self-review가 통과했다.
- 수동 runtime 검증을 하지 않은 경우 미검증으로 남기고 구현 성공과 실제 호출 성공을 구분한다. 사용자 요청이 없다는 이유로 자동 실행하거나 검증 결과를 허위로 채우지 않는다.
- PR 본문의 작업 상태·검증 근거·Reviewed HEAD·revision을 최신 상태와 일치시켰다. 남은 권한·정책 차단은 분명히 표시한다.

지속적으로 유효한 실행 방법과 정책은 관련 정본에 반영한다. 인계 자료는 비정본이므로 이를 대신하지 않는다.
