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
uv run --locked --no-default-groups python -m scripts.agent_assets.native_eval_run mols-loops --repeat 3
```

- 실행 전 canonical `src/rulesync/.rulesync/skills/<name>/` 전체를
  저장소 밖의 별도 임시 workspace에 복사합니다. 평가가 끝나면
  workspace를 제거하며 source/derived projection은 변경하지 않습니다.
- Promptfoo `openai:codex-sdk`로 실행하며 로컬 Codex 인증 또는 API key,
  Node.js 및 npx가 필요합니다. 기본 model은 `gpt-5.5`이며 `CODEX_EVAL_MODEL`로
  명시적으로 변경할 수 있습니다. 실행 중 Codex는 read-only / no-approval /
  network-off로 제한합니다. 비교 실행 시 모델, 런타임 버전과 인증 조건을 별도로 기록해야 합니다.
- Routing은 `skill-used` / `not-skill-used` (Codex Skill 파일 읽기에서
  추론한 **heuristic evidence**)를 사용합니다. 선택 우선순위나 업무 결과의
  품질까지 입증하지 않습니다. Behavior는 사용 여부에 더해
  기존 `llm-rubric`을 적용하므로 별도 `PROMPTFOO_GRADER_PROVIDER`
  설정 또는 기본 Ollama grader가 필요합니다.
- 기존 `cases.json`을 재사용하며 기대 selection/criteria는 target prompt에
  노출하지 않습니다. 실패 시 실제 사용 trace 및 grader output을 확인합니다.
- 이 실행은 CI `PR Gate`에 포함하지 않습니다. 로컬 Codex + grader
  실행 결과가 없는 상태를 PASS로 보고하지 않습니다.
