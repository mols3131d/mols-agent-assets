# Provider 통합 구현 계획

[인계 요약](00-handoff-promptfoo.md)에서 목표와 작업 기준을 확인한다. 이 계획은 제안이며 구체적인 CLI 문법과 구현 방식은 upstream contract를 검증한 뒤 결정한다.

## 1. 버전과 기존 계약 확인

- [Runner](../../scripts/agent_assets/promptfoo_run.py)는 `npx --yes promptfoo@<pin>`을 실행한다. 현재 pin은 0.126.0, 최소 Node 선언은 22.22.0이며 [mise.toml](../../mise.toml)은 Node 26.13.0을 지정한다. 최신 안정 릴리스, npm engines, Node/Windows 호환성, CLI·schema·Python adapter 변경을 실제 설치된 버전 또는 upstream tag로 확인한다. 자동 latest로 대체하지 않는다.
- Codex SDK의 optional/opt-in 설치 변경을 확인한다. SDK가 필요하다면 runner와 같은 실행 환경에서 해석되는 설치 경로를 사용하고 전역 설치나 숨은 다운로드에 의존하지 않는다.
- 여러 config를 병합할 때 provider가 추가 실행될 수 있다. 0.126.0의 merge 및 CLI override 동작을 확인하기 전에는 overlay를 provider 교체 수단으로 사용하지 않는다.

## 2. 공통 실행 계약

기존 `mise run eval`을 하나의 진입점으로 유지한다. 사용자가 config/fixture, runtime provider와 model을 지정하며 semantic grader가 필요한 경우 grader provider/model도 지정한다. 기본 Ollama 호출, 빈 값 fallback, 자동 provider 선택을 제거하거나 실행 전에 차단한다. 설정값은 로컬 `.env` 또는 실행 시 명시값으로 제공할 수 있으나 단순히 설정이 존재한다는 사실은 평가 요청이 아니다.

| 입력 | 기대 동작 |
| --- | --- |
| 인수 없음 또는 도움말 | 사용법 표시; 모델과 불필요한 CLI 설치·실행 없음 |
| 평가 config 누락, model/provider 누락·공백·오류 | 모델 실행 전에 명확한 실패; 다른 제공자로 대체하지 않음 |
| 유효한 명시 선택 | 선택한 config와 provider/model만 사용 |
| semantic grader 필요 | 별도 명시 선택 확인; 기본 Ollama 등으로 자동 fallback하지 않음 |
| fixture-only smoke | 모델 호출 없이 별도로 구분; 자동 실행하지 않음 |
| 지원하지 않는 config/provider 조합 | 실행 전 실패 또는 지원 범위 안내 |

`PROMPTFOO_RUNTIME_PROVIDER` 전체 ID를 활용하는 방식을 우선 검토한다. 별도 `provider`/`model` 플래그가 필요하면 하나의 선택 계약으로 정규화한다. `.env`와 CLI 인수 우선순위, mise 환경 로딩, Promptfoo의 provider·env override에 따른 최종 호출 대상을 검증한다. 기존 필터 및 결과 저장 옵션을 보존하되 선택 계약을 우회하지 않도록 한다.

## 3. Provider별 구현 경계

| Provider | 우선 검토할 방식 | 주의 사항 |
| --- | --- | --- |
| Ollama | native `ollama:chat:<model>` | 모델 다운로드 금지; 기존 reference 평가와 JSON/schema 계약 보존 |
| Codex | native `openai:codex-sdk:<model>` 또는 `openai:codex-app-server:<model>` | SDK 의존성, 인증 선택, 명시적인 모델·sandbox·approval·작업 디렉터리 |
| Antigravity | 공식 headless CLI의 고정 fixture 호출을 위한 최소 custom provider | 정확한 CLI 명령·모델 플래그·JSON envelope·인증·이용약관 검증 선행 |

Codex는 단순 final-output 평가에는 SDK를 우선 검토하고 App Server는 rich event가 필요한 경우에만 추가한다. 둘 다 지원해야 한다는 요구는 없다. 구독 로그인과 API key 인증이 섞여 다른 결제 또는 계정으로 넘어가지 않도록 인증 경계를 검증한다.

Antigravity는 Promptfoo 전용 native provider가 확인되지 않았다. 공식 CLI를 사용하는 고정 평가 케이스의 외부 래핑이 현재 허용되는지 먼저 확인한다. 직접 작성한 deterministic script/CI에 대한 허용 근거를 모든 제3자 평가 프레임워크에 확대하지 않는다. 명시적으로 허용된 인증·사용 형태로만 구현하며, 개인 구독 OAuth의 임의 재사용, 외부 자율 agent backend, 동적 prompt 생성 및 반복 제어는 도입하지 않는다. 공식 API 인증이 지원되고 그 사용이 허용되면 별도 선택 경로로 검토한다. 합법적·기술적으로 성립하는 경로가 없으면 Antigravity는 차단된 상태로 PR에 기록한다. Gemini API 호출을 Antigravity 런타임 검증으로 대체하지 않는다.

공통 chat prompt의 system/task 역할을 보존하고 provider별 입력과 설정을 올바르게 변환한다. Codex/Antigravity agent 평가에는 공통 `temperature: 0`을 무조건 전달하지 않는다. Agent 작업 공간에 기대 결과, grader rubric, 실제 저장소 credential 또는 불필요한 파일을 노출하지 않는다. 파일 쓰기·network·tool 권한은 최소화하고 격리할 수 없는 실행은 차단한다. Custom CLI adapter는 구조화된 인수, timeout, 종료 코드와 JSON 오류를 처리하고 인증정보나 민감한 원문을 로그에 남기지 않는다.

## 4. 평가 범위와 정본

| 경로 | 책임 및 확인할 변경 |
| --- | --- |
| [promptfoo_run.py](../../scripts/agent_assets/promptfoo_run.py), [promptfoo_env.py](../../scripts/agent_assets/promptfoo_env.py) | 실행·pin·명시 선택·timeout·환경값 |
| [skills_promptfoo.py](../../scripts/agent_assets/skills_promptfoo.py) | fixture 변환·assertion·custom reference 평가 |
| [evals/promptfoo/](../../evals/promptfoo/) | suite별 prompt·provider·grader·설정 |
| [skill-chat.json](../../evals/promptfoo/skill-chat.json) | 기존 chat 입력 계약 |
| [.env.example](../../.env.example), [mise.toml](../../mise.toml) | 예제 설정·공통 task; 실제 credential은 비추적 |
| [evals/README.md](../../evals/README.md), [docs/tools/promptfoo.md](../../docs/tools/promptfoo.md) | 실행법·지원 범위·버전·데이터 경계 |
| [docs/development/evaluation.md](../../docs/development/evaluation.md), [ci.md](../../docs/development/ci.md) | 평가 증거와 자동 실행 금지 정책 |

`mols-loops`, `mols-dev-env-bootstrap-design`, `mols-stdd`의 native suite는 동일한 fixture/label 계약을 유지한다. `mols-test-design`, `mols-stdd-references`의 기존 custom Ollama 경로는 선택한 모델과 일치해야 하며, 다른 provider로 reference 평가를 일반화할 필요가 있는지는 비용과 평가 목적을 기준으로 판단한다. 미지원 조합은 문서와 실행에서 명확히 드러내고 선택하지 않은 Ollama를 호출하지 않는다. Grader calibration은 runtime이 echo여도 semantic 호출이 필요할 수 있다.

모델 입력에 Skill을 주입한 결과와 실제 IDE/CLI의 Skill discovery·tool trajectory를 구분한다. Native suite를 agent로 실행했다는 사실만으로 실제 하네스 평가를 증명하지 않는다.

## 5. 공식 조사 출처

2026-11-25 조사 당시 참고한 출처다. 최신성·정확한 사용 조건을 구현 시점에 재확인한다. 실제 CLI 실행이나 개별 계정의 약관 적합성 검증은 아직 하지 않았다.

- [npm Promptfoo versions](https://www.npmjs.com/package/promptfoo?activeTab=versions), [0.126.0 release](https://github.com/promptfoo/promptfoo/releases/tag/0.126.0), [0.126.0 package source](https://github.com/promptfoo/promptfoo/blob/0.126.0/package.json): 버전·Node·의존성.
- [Provider 목록](https://www.promptfoo.dev/docs/providers/), [Codex SDK](https://www.promptfoo.dev/docs/providers/openai-codex-sdk/), [Codex App Server](https://www.promptfoo.dev/docs/providers/openai-codex-app-server/), [Custom Script](https://www.promptfoo.dev/docs/providers/custom-script/), [Python provider](https://www.promptfoo.dev/docs/providers/python/): 지원 방식·입출력·설정.
- [OpenAI Codex 인증](https://developers.openai.com/codex/auth/): 구독/API 인증과 제한.
- [Antigravity 추가 약관](https://antigravity.google/terms), [FAQ](https://antigravity.google/docs/faq), [Headless CLI](https://antigravity.google/docs/cli/headless/): 직접 자동화와 제3자 래핑의 권한 경계.
- [Antigravity CLI Issue #1493](https://github.com/google-antigravity/antigravity-cli/issues/1493): 관련 설명의 보조 근거이며 약관과 공식 문서보다 우선하지 않는다.

최종 검증은 [02-plan-verification.md](02-plan-verification.md)를 따른다.
