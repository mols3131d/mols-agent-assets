# Evaluations (`evals/`)

`evals/`는 repository-owned behavioral/model evaluation fixture를 저장합니다.

- Skill별 trigger, behavior, adversarial fixture → `evals/skills/<skill-name>/`
- Subagent 또는 subagent family의 delegation, ownership, handoff behavior fixture → `evals/subagents/<subagent-or-family>/`
- Tool-specific eval config → `evals/promptfoo/`
- Agent behavior를 실행하지 않아도 판정할 repository correctness → `tests/`
- Deployable Agent Asset package 안에는 repository eval을 두지 않습니다.

평가 대상은 로컬 runtime에 설치된 자산 목록이 아니라 이 저장소가 관리하는 작성 원본을 기준으로 합니다. 자산을 삭제하거나 이름을 바꿀 때는 해당 fixture와 tool config도 같은 변경에서 제거하거나 새 owner로 이관합니다. `tests/evals/`는 Skill별 fixture 디렉터리와 Subagent fixture의 `system_under_evaluation`이 현재 작성 원본을 가리키는지 검사합니다. 테스트 시나리오에 명시적으로 주입한 가상 routing candidate는 이 저장소의 평가 대상 자산과 구분합니다.

Asset별 차이는 fixture와 tool config가 소유합니다. 같은 평가 contract를 실행하기 위해 asset마다 별도 adapter를 만드는 대신 재사용 가능한 evaluator가 실제로 필요할 때 `scripts/agent_assets/`의 공통 실행 surface를 확장합니다.

Eval을 언제 추가하고 어떤 evidence로 해석할지는 [`docs/development/evaluation.md`](../docs/development/evaluation.md)가 소유합니다. 이 README는 `evals/`의 fixture placement와 local boundary만 소유합니다.

Promptfoo CLI는 사용자가 평가를 명시적으로 요청할 때 실행합니다. CI, bootstrap, check와 hook은 모델과 grader를 호출하지 않습니다. 저장소 테스트는 root `tests/`에 두며 Promptfoo 평가의 공통 진입점은 `mise run eval`입니다.

## Promptfoo Provider Selection

`mise run eval`은 실행할 저장소 평가 설정 파일 하나를 요구합니다. 인수 없는 실행과 `--help`는 runner 사용법을 출력합니다. 모델 평가에는 `--provider`와 `--model`을 지정합니다. `--grader none`은 semantic rubric을 제외하며 Trigger, 출력 형식, Reference 선택 등 deterministic assertion은 그대로 적용합니다. Semantic grading을 사용하려면 `--grader ollama|codex`와 `--grader-model`을 따로 지정합니다.

| 평가 설정 | Runtime | Grader |
| --- | --- | --- |
| `mols-dev-env-bootstrap-design.yaml` | Ollama native chat 또는 Codex native SDK | `none`, Ollama 또는 Codex |
| `mols-implementation-guidance.yaml` | Ollama native chat 또는 Codex native SDK의 routing-only 평가 | `none` |
| `mols-test-design.yaml` | Ollama 전용 Python provider | `none`, Ollama 또는 Codex |
| `mols-dev-env-bootstrap-design-grader.yaml` | 저장된 응답을 재생하는 Echo | Ollama 또는 Codex 필수 |
| `mols-dev-env-bootstrap-design-smoke.yaml --fixture` | 고정 fixture | 모델 옵션 없이 실행 |

아래 모델 ID는 선택 형식을 보여 줍니다. 사용 가능한 Ollama 모델을 미리 준비하고 Codex 모델은 선택한 인증에서 사용할 수 있는 ID로 지정합니다.

```bash
mise run eval -c evals/promptfoo/mols-dev-env-bootstrap-design-smoke.yaml --fixture
mise run eval -c evals/promptfoo/mols-dev-env-bootstrap-design.yaml \
  --provider ollama --model qwen3.5:4b --grader none --filter-metadata suite=trigger
mise run eval -c evals/promptfoo/mols-dev-env-bootstrap-design.yaml \
  --provider codex --model gpt-5.2-codex --codex-auth chatgpt \
  --grader ollama --grader-model qwen3.5:4b --filter-metadata suite=behavior
mise run eval -c evals/promptfoo/mols-dev-env-bootstrap-design-grader.yaml \
  --grader codex --grader-model gpt-5.2-codex --codex-auth api
mise run eval -c evals/promptfoo/mols-test-design.yaml \
  --provider ollama --model qwen3.5:4b --grader none
```

`--filter-metadata`, `--filter-pattern`, `--filter-first-n`, `--repeat`, `--output` 등은 Promptfoo로 전달합니다. 입력을 교체하거나 선택 범위를 넓히는 다중 config, provider override, watch, resume, 공유와 확장 옵션은 runner에서 거부합니다. 캐시·공유·기본 결과 저장은 suite에서 끕니다. `--output .tmp/<name>.json`을 지정하면 결과 파일을 저장합니다.

### Authentication and environment

Codex는 runtime 또는 grader로 선택할 때 `--codex-auth chatgpt|api`를 요구합니다. 같은 실행에서 두 역할 모두 Codex를 사용하면 인증 방식은 공유하고 모델은 독립적으로 선택합니다.

- `chatgpt`는 저장소 밖의 평가 전용 Codex home에 이미 준비한 ChatGPT 로그인을 사용합니다. 절대 경로를 `PROMPTFOO_CODEX_CHATGPT_HOME`에 지정합니다. 평가 전용 home은 아래처럼 공식 CLI에서 준비하며 사용자 설정, Skill 또는 플러그인 설정 없이 유지합니다. Runner는 CLI의 로그인 상태를 확인하고 기존 ChatGPT 세션을 사용합니다.
- `api`는 해당 실행에 제공한 `PROMPTFOO_CODEX_API_KEY`만 사용합니다. 세션은 새 임시 Codex home에서 시작하며 API 인증을 메모리로 제한합니다. 키를 인수, 생성 config 또는 Git에 기록하지 않습니다. 기존 `OPENAI_API_KEY`와 `CODEX_API_KEY`는 선택을 대신하지 않습니다.

```bash
CODEX_HOME="$PROMPTFOO_CODEX_CHATGPT_HOME" codex login
```

mise가 읽는 [`.env.example`](../.env.example)은 비밀값 없이 사용 가능한 환경 설정을 보여 줍니다. 인증은 별도로 준비하고 실행 시 전달합니다. 설정에 키나 모델이 있다는 사실만으로 평가를 시작하지 않습니다.

| 변수 | 적용 |
| --- | --- |
| `OLLAMA_BASE_URL` | Ollama runtime·grader가 사용할 HTTP(S) 서버. 기본 `http://127.0.0.1:11434` |
| `OLLAMA_API_KEY` | 선택한 Ollama 서버에 필요한 경우 전달하는 bearer credential |
| `REQUEST_TIMEOUT_MS` | Ollama native·custom HTTP 요청 제한. 기본 `120000` |
| `PROMPTFOO_RUNTIME_TIMEOUT_SECONDS` | `REQUEST_TIMEOUT_MS` 미지정 시 적용하는 초 단위 Ollama 호환 설정 |
| `PROMPTFOO_RUNTIME_THINK` | Python Ollama provider에만 전달하는 `true` 또는 `false` |
| `PROMPTFOO_CODEX_TIMEOUT_MS` | Codex runtime·grader 호출별 제한 시간. 기본 `120000`. Ollama 요청에는 Ollama 제한 시간이 적용됩니다. |

### Inputs, outputs, and evidence

Ollama native는 system/user 채팅 메시지와 `temperature: 0`을 사용합니다. Python Ollama provider는 Reference 선택과 응답의 구조화된 JSON을 읽고 선택한 경로를 provider metadata에 남깁니다. Codex SDK는 실행 지침과 사용자 과업을 한 agent prompt에 담아 전달하며, Trigger와 semantic grader에는 각각 별도 출력 schema를 지정합니다. Codex 응답은 SDK가 최종 메시지로 변환합니다.

Codex는 비어 있는 임시 작업 디렉터리, 평가 전용 읽기 권한, 네트워크 및 웹 검색 끄기, 승인 없음, 별도 셸 환경으로 실행합니다. Fixture 기대값과 rubric은 runtime에 노출하지 않습니다. ChatGPT 로그인의 전용 Codex home에는 네이티브 CLI의 세션 기록이 남을 수 있습니다. 사용한 OS의 Codex sandbox 지원과 인증 상태는 실제 실행 환경에서 확인합니다.

원격 runtime이나 grader를 선택하면 Skill, 과업, 응답 또는 rubric이 선택 서버로 전송될 수 있고 비용이 발생할 수 있습니다. Telemetry 및 공유 설정은 provider 요청을 통제하는 기능과 별개입니다. 모델 다운로드와 평가 호출은 사용자의 실행 요청에 따릅니다. Fixture smoke와 가짜 provider의 테스트는 배선과 평가 조건을 확인하며 실제 모델 품질·가용성, IDE/CLI의 Skill discovery 또는 도구 실행을 입증하지 않습니다. [Promptfoo Codex SDK](https://www.promptfoo.dev/docs/providers/openai-codex-sdk/), [Ollama provider](https://www.promptfoo.dev/docs/providers/ollama/)
