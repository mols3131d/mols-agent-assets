# 평가 (`evals/`)

`evals/`는 repository-owned behavioral/model evaluation fixture를 저장합니다.

- Skill별 trigger, behavior, adversarial fixture → `evals/skills/<skill-name>/`
- Subagent 또는 subagent family의 delegation, ownership, handoff behavior fixture → `evals/subagents/<subagent-or-family>/`
- Tool-specific eval config → `evals/promptfoo/`
- Agent behavior를 실행하지 않아도 판정할 repository correctness → `tests/`
- Deployable Agent Asset package 안에는 repository eval을 두지 않습니다.

평가 대상은 로컬 runtime에 설치된 자산 목록이 아니라 이 저장소가 관리하는 작성 원본을 기준으로 합니다. 자산을 삭제하거나 이름을 바꿀 때는 해당 fixture와 tool config도 같은 변경에서 제거하거나 새 owner로 이관합니다. `tests/evals/`는 Skill별 fixture 디렉터리와 Subagent fixture의 `system_under_evaluation`이 현재 작성 원본을 가리키는지 검사합니다. 테스트 시나리오에 명시적으로 주입한 가상 routing candidate는 이 저장소의 평가 대상 자산과 구분합니다.

Asset별 차이는 fixture와 tool config가 소유합니다. 같은 평가 contract를 실행하기 위해 asset마다 별도 adapter를 만드는 대신 재사용 가능한 evaluator가 실제로 필요할 때 `scripts/agent_assets/`의 공통 실행 surface를 확장합니다.

Eval을 언제 추가하고 어떤 evidence로 해석할지는 [`docs/development/evaluation.md`](../docs/development/evaluation.md)가 소유합니다. 이 README는 `evals/`의 fixture placement와 local boundary만 소유합니다.

기본 Trigger/Behavior 평가 중 `mols-loops`와 `mols-dev-env-bootstrap-design`은 선택 가능한 Promptfoo native provider를 사용합니다. 공통 Python generator는 canonical fixture로부터 case별 system prompt와 assertion을 구성하지만 모델 HTTP 호출은 하지 않습니다. Reference를 조건부로 선택해야 하는 `mols-test-design`과 fixture-mode smoke는 기존 Python provider를 사용합니다. 모든 경로는 실제 IDE/CLI agent의 tool·routing 실행을 재현하지 않습니다.

Promptfoo CLI는 기본적으로 개발자의 로컬 환경에서 실행하며, 모델 호출 위치는 선택한 provider가 결정합니다. Repository correctness는 root `tests/`가 검증하며, Promptfoo 공통 진입점은 `mise run eval`이며, 평가 설정 파일과 필터를 인수로 전달합니다. 예시:

```bash
mise run eval -c evals/promptfoo/mols-loops-smoke.yaml
mise run eval -c evals/promptfoo/mols-loops.yaml
mise run eval -c evals/promptfoo/mols-dev-env-bootstrap-design.yaml
mise run eval -c evals/promptfoo/mols-dev-env-bootstrap-design-grader.yaml
```

## Promptfoo provider 선택

기본값으로 실행할 때는 `.env`가 필요하지 않습니다. 설정을 바꿀 때는 프로젝트 루트의 [`.env.example`](../.env.example)을 복사해 변수 값을 수정합니다. 예제의 로컬 Ollama 기본값은 주석 없이 활성화되어 있습니다. `.env`와 API credential은 Git에 포함하지 않습니다.

```powershell
Copy-Item .env.example .env
```

Native 평가의 `PROMPTFOO_RUNTIME_PROVIDER`에는 `ollama:chat:qwen2.5`, `openai:chat:gpt-4o-mini`, `anthropic:messages:claude-sonnet-4-5`처럼 모델을 포함한 **전체 Promptfoo provider ID**를 지정합니다. Provider를 바꾸기 위해 fixture나 Python HTTP adapter를 수정하지 않습니다. 지원 ID와 필수 credential은 [공식 provider 문서](https://www.promptfoo.dev/docs/providers/)를 확인합니다. 모델 예시는 호환성·가용성·성능을 검증했다는 뜻이 아닙니다.

| 설정 | 적용 |
| --- | --- |
| `PROMPTFOO_RUNTIME_PROVIDER` | 두 native Skill 평가의 provider ID. 명시하면 `PROMPTFOO_RUNTIME_MODEL`보다 우선 |
| `PROMPTFOO_RUNTIME_MODEL` | 전체 ID 미지정 시 `ollama:chat:<model>`을 구성하는 기존 설정. 기본 `qwen2.5`; custom Ollama 평가에서도 계속 사용 |
| `PROMPTFOO_GRADER_PROVIDER` | 독립적인 semantic grader ID. 기본 `ollama:chat:qwen2.5`; runtime 변경에 따라 자동 변경하지 않음 |
| `OLLAMA_BASE_URL` | Ollama를 선택한 runtime 또는 grader의 endpoint |
| `REQUEST_TIMEOUT_MS` | Native·custom 경로에 공통으로 적용되는 요청별 timeout. 기본 `120000`; 양의 정수 밀리초 |
| `PROMPTFOO_RUNTIME_TIMEOUT_SECONDS` | 기존 초 단위 호환 설정. `REQUEST_TIMEOUT_MS` 미지정 시에만 사용하며 유한한 `0.001`초 이상 값 |

예를 들어 `.env`에서 다음과 같이 선택할 수 있습니다. 선택한 provider의 API key 또는 인증은 해당 제공자의 공식 방식으로 별도 설정합니다.

```dotenv
PROMPTFOO_RUNTIME_PROVIDER=openai:chat:gpt-4o-mini
PROMPTFOO_GRADER_PROVIDER=openai:chat:gpt-4o-mini
```

Model·provider·grader 선택과 timeout의 빈 값·공백은 미지정으로 처리합니다. Timeout은 **명시한 `REQUEST_TIMEOUT_MS` → 기존 초 단위 값 → 기본 120초** 순서로 하나만 해석합니다. 유효한 밀리초 값을 지정하면 사용하지 않는 초 단위 값이 잘못돼도 실행을 막지 않습니다. 선택된 timeout이 잘못되면 모델 호출 전에 nonzero와 변수명 기반 오류를 반환하고, custom provider는 같은 오류를 provider error로 보고합니다. Credential·endpoint 등 native 제공자 변수는 임의로 정규화하거나 이름을 바꾸지 않습니다. 요청별 timeout과 retry/backoff를 포함한 전체 실행 시간은 다릅니다.

Runtime만 원격으로 바꾸면 기본 grader는 계속 Ollama이므로 behavior 평가에는 로컬 grader 모델도 필요합니다. 모든 모델 호출을 다른 제공자로 실행하려면 runtime과 grader를 각각 선택합니다. 기존 로컬 경로는 전체 ID를 미지정하고 `PROMPTFOO_RUNTIME_MODEL`, `OLLAMA_BASE_URL`을 설정하면 유지되며, 사용할 모델이 이미 준비되어 있어야 합니다.

`mise run eval-mols-loops-smoke`는 모델 없이 fixture 연결만 확인합니다. 조건부 Reference를 읽는 `mols-test-design`은 기존 custom Ollama 경로여서 `PROMPTFOO_RUNTIME_PROVIDER`의 적용 대상이 아닙니다.

**원격 provider 또는 grader를 선택하면 Skill·평가 prompt 또는 응답·rubric이 외부로 전송될 수 있으며 비용이 발생합니다.** Telemetry·sharing·remote generation 비활성화는 이 전송을 막는 통제가 아닙니다. 데이터 전송과 비용 허가를 먼저 확인하며 모델 다운로드나 유료 API 실행은 자동 수행하지 않습니다.

### Provider별 옵션

공통 config는 `temperature: 0`만 지정하고 Trigger의 JSON 응답은 system의 schema 지시와 기존 strict assertion으로 판정합니다. 제공자마다 다른 JSON 강제 옵션을 공통으로 주입하지 않으며, JSON을 따르지 않은 출력은 실패입니다. Grader 선택과 별개로 runtime의 모델·sampling·structured-output 설정도 평가 조건에 기록합니다.

Endpoint·인증은 선택한 [native provider 문서](https://www.promptfoo.dev/docs/providers/)의 환경변수 또는 `config`를 사용합니다. 추가 generation 옵션이 필요하면 [Promptfoo native 설정](https://www.promptfoo.dev/docs/configuration/reference/)에서 해당 provider의 `config`를 지정합니다. 예를 들어 OpenAI Trigger의 JSON mode는 다음 형태입니다.

```yaml
providers:
  - id: "{{ env.PROMPTFOO_RUNTIME_PROVIDER }}"
    label: mols-loops-trigger
    config:
      temperature: 0
      response_format:
        type: json_object
```

위는 전체 suite가 아니라 provider 항목 예시입니다. 전체 config에서 기존 Trigger/Behavior label과 generator 연결을 보존하고 Trigger 전용 설정을 Behavior에 일괄 적용하지 않습니다. Bootstrap 평가는 해당 Skill의 label을 사용합니다. Ollama의 JSON mode는 `passthrough.format: json` 등 해당 provider의 옵션을 사용하며 다른 제공자에 그대로 복사하지 않습니다. `PROMPTFOO_RUNTIME_THINK`는 custom Python Ollama provider 전용이므로 native 경로에 자동 적용되지 않습니다.

Promptfoo 0.122.0에서 여러 `--config` 파일의 provider 항목은 ID나 label 기준으로 덮어쓰지 않고 합쳐질 수 있습니다. Provider 설정 변경을 단순 overlay로 간주하지 않습니다. CLI·native provider 호환성 확인과 실제 모델의 응답 품질 평가는 별도이며, 한 제공자의 성공을 다른 제공자의 검증으로 확대하지 않습니다.

`mise.toml`은 파일이 존재할 때만 `.env`를 읽습니다. 파일이 없으면 runner의 기존 기본값이 유지됩니다. mise가 읽은 `.env` 값은 부모 셸의 동일한 환경변수보다 우선할 수 있으므로, 일회성 변경은 `.env`를 편집하거나 mise가 시작한 자식 프로세스에서 설정합니다. 로컬 설정을 사용하는 공식 경로는 `mise run ...`이며, Bootstrap 평가와 grader 보정도 위 진입점을 사용합니다. 두 Bootstrap task는 `--` 뒤의 인자를 기존 npm script로 전달합니다.

`mise run eval ...`은 runner가 기본값을 정하기 전에 `.env` 설정을 로드합니다. Python runner 또는 Promptfoo CLI를 직접 실행하면 같은 환경 로딩을 보장하지 않으므로, 평가 조건을 재현하려면 필요한 환경변수를 명시적으로 전달합니다.

Deterministic assertion이 가능한 behavioral contract는 model grader보다 우선하지만, **문장 동기화나 semantic prose consistency를 문자열 regression으로 고정하지 않습니다.** 그런 의미는 authoritative source와 해당 behavioral review/eval이 소유합니다.

Fixture가 존재해도 compatible runner와 실제 model/runtime을 실행하지 않았다면 runtime behavior가 통과했다고 주장하지 않습니다.
