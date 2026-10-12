# 평가 (`evals/`)

`evals/`는 repository-owned behavioral/model evaluation fixture를 저장합니다.

- Skill별 trigger, behavior, adversarial fixture → `evals/skills/<skill-name>/`
- Subagent 또는 subagent family의 delegation, ownership, handoff behavior fixture → `evals/subagents/<subagent-or-family>/`
- Tool-specific eval config → `evals/promptfoo/`
- Agent behavior를 실행하지 않아도 판정할 repository correctness → `tests/`
- Deployable Agent Asset package 안에는 repository eval을 두지 않습니다.

Asset별 차이는 fixture와 tool config가 소유합니다. 같은 평가 contract를 실행하기 위해 asset마다 별도 adapter를 만드는 대신 재사용 가능한 evaluator가 실제로 필요할 때 `scripts/agent_assets/`의 공통 실행 surface를 확장합니다.

Eval을 언제 추가하고 어떤 evidence로 해석할지는 [`docs/development/evaluation.md`](../docs/development/evaluation.md)가 소유합니다. 이 README는 `evals/`의 fixture placement와 local boundary만 소유합니다.

Promptfoo와 model/runtime을 사용하는 behavioral eval은 기본적으로 local에서 실행합니다. Repository correctness는 root `tests/`가 검증하며, 현재 mols-loops Promptfoo entrypoint는 다음과 같습니다.

```bash
mise run eval-mols-loops-smoke
mise run eval-mols-loops
```

Deterministic assertion이 가능한 behavioral contract는 model grader보다 우선하지만, **문장 동기화나 semantic prose consistency를 문자열 regression으로 고정하지 않습니다.** 그런 의미는 authoritative source와 해당 behavioral review/eval이 소유합니다.

Fixture가 존재해도 compatible runner와 실제 model/runtime을 실행하지 않았다면 runtime behavior가 통과했다고 주장하지 않습니다.

## Native Skill Eval (local, non-blocking)

Ollama 기반 contract/fixture lane과 별도로 **Codex SDK가 실제 Skill을 읽고
호출했는지** 확인하는 native-runtime lane을 제공합니다.

```bash
mise run eval-mols-loops-native
mise run eval-asset-routing-native
# 반복 시행은 직접 지정합니다.
uv run --locked --no-default-groups python -m scripts.agent_assets.native_eval_run mols-loops --suite trigger --repeat 3 --output .tmp/evals/mols-loops-trigger.json
# Grader를 설정한 다음 Behavior만 별도로 실행할 수도 있습니다.
uv run --locked --no-default-groups python -m scripts.agent_assets.native_eval_run mols-loops --suite behavior --repeat 3 --output .tmp/evals/mols-loops-behavior.json
```

- 실행 전 canonical `src/rulesync/.rulesync/skills/<name>/` 전체를
  저장소 밖의 별도 임시 workspace에 복사합니다. 평가가 끝나면
  workspace를 제거하며 source/derived projection은 변경하지 않습니다.
- Promptfoo `openai:codex-sdk`로 실행하며 Node.js >= 22.22.0, npx,
  Codex SDK 및 인증이 필요합니다. API key (`OPENAI_API_KEY` 또는
  `CODEX_API_KEY`)가 있으면 별도 임시 `CODEX_HOME`을 생성합니다.
  ChatGPT 로그인으로 실행하려면 **명시적으로**
  `CODEX_EVAL_HOME=/path/to/codex-home`을 지정합니다. 로그인
  Home에 들어 있는 개인 설정·Skill이 측정에 영향을 줄 수 있어
  baseline 비교에는 **전용 Codex Home**을 권장합니다.
  API key와 `CODEX_EVAL_HOME`을 동시에 지정한 실행은 인증 방식이
  모호하므로 거부합니다. 로그인 Home 사용 시 API key를 해제하세요.
- 기본 model은 `gpt-5.5`이며 `CODEX_EVAL_MODEL`로 변경할 수 있습니다.
  Codex는 read-only / no-approval / network-off로 제한합니다. 비교 실행 시
  model, runtime, fixture revision, 인증 조건을 기록해야 합니다.
- `asset-routing` profile은 `--suite all` 요청에서도 Routing만 실행하고 manifest에 `trigger`로 기록합니다.
- `--suite trigger`는 Grader 없이 native routing만 평가합니다.
  `--suite behavior`는 `PROMPTFOO_GRADER_PROVIDER` (기본 Ollama)와
  실제 grader runtime이 필요합니다. 기본 `--suite all`은 두 영역을 함께
  실행합니다.
- Native **Routing**은 원래 요청만 전달합니다. `mols-loops`와
  `mols-agent-asset`을 함께 배치하여 전문 Skill 단독 선택과 RPI 복합 선택도
  평가합니다. Skill 파일 읽기 기록으로 **동시 사용 여부만** 확인하며
  어느 Skill이 primary였는지는 증명하지 않습니다.
- Native **Behavior**는 `$<skill-name>` 직접 호출을 선행해 이미 선택된
  Skill의 **응답 수준** 결과를 평가합니다. Domain Skill 협업 사례도 포함하지만
  현재 rubric은 실제 tool call, 승인 확인, 외부 side effect를 검증하지 않습니다.
  그 behavior를 검증하려면 별도의 observable state/trajectory grader가 필요합니다.
  Routing과 Behavior를 하나의 Skill 성능 점수로 혼합하지 않습니다.
- Routing은 `skill-used` / `not-skill-used` (Codex Skill 파일 읽기에서
  추론한 **heuristic evidence**)를 사용합니다. 선택 우선순위나 업무 결과의
  품질까지 입증하지 않습니다. Behavior는 사용 여부에 더해
  기존 `llm-rubric`을 적용하므로 별도 `PROMPTFOO_GRADER_PROVIDER`
  설정 또는 기본 Ollama grader가 필요합니다.
- 기존 `cases.json`을 재사용하며 기대 selection/criteria는 target prompt에
  노출하지 않습니다. 실패 시 실제 사용 trace 및 grader output을 확인합니다.
- 이 실행은 CI `PR Gate`에 포함하지 않습니다. 로컬 Codex + grader
  실행 결과가 없는 상태를 PASS로 보고하지 않습니다.

- `--output .tmp/evals/<profile>.json`은 로컬에서 재실행 결과를
  확인하는 선택적 기록 경로입니다. 결과 옆에
  `<profile>.json.manifest.json`을 작성하여 profile/suite/repeat, Git HEAD,
  model·인증 방식, Promptfoo 버전, 실제 Skill package·fixture·config·result
  해시, 평가 adapter 해시, Grader provider 식별 문자열의 SHA-256
  (비밀 문자열을 그대로 출력하지 않음), 종료 코드를 기록합니다.
  Routing-only 실행에서는 Grader 식별 해시가 `null`입니다.
  이 manifest는 실행 성공을 주장하지 않으며
  npx가 해석하는 optional Codex SDK의 **정확한 설치 버전은 미확인(null)** 으로
  남깁니다. 비교 전 SDK 버전을 별도로 확인하고 output과 manifest를 함께
  untracked/disposable로 유지합니다.
  Positive Skill-use control이 성공하지 않으면
  `not-skill-used`만 통과한 negative case를 routing 성공으로
  단정하지 않습니다. 실제 실패를 Skill, fixture, runtime, grader,
  telemetry 누락으로 나눠 해석합니다.
