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

## 로컬 Promptfoo / Ollama 설정

프로젝트 루트의 `.env.example`을 복사해 개발자별 `.env`를 생성합니다. `.env`는 Git에 포함하지 않습니다.

```bash
cp .env.example .env
```

`.env`에서 평가 대상 `PROMPTFOO_RUNTIME_MODEL`, 채점용 `PROMPTFOO_GRADER_PROVIDER`, `OLLAMA_BASE_URL`, `PROMPTFOO_RUNTIME_TIMEOUT_SECONDS`를 선택합니다. 사용할 모델은 로컬 Ollama에 준비되어 있어야 합니다. `mise run eval-mols-loops-smoke`는 모델 없이 fixture 연결만 확인하며, `mise run eval-mols-loops`는 실제 모델을 실행합니다.

`mise.toml`은 파일이 존재할 때만 `.env`를 읽습니다. 파일이 없으면 runner의 기존 기본값이 유지됩니다. mise가 읽은 `.env` 값은 부모 셸의 동일한 환경변수보다 우선할 수 있으므로, 일회성 변경은 `.env`를 편집하거나 mise가 시작한 자식 프로세스에서 설정합니다. `npm run ...`을 직접 실행하면 mise의 `.env` 로딩을 거치지 않으므로, 로컬 설정을 사용하는 공식 경로는 `mise run ...`입니다.

Deterministic assertion이 가능한 behavioral contract는 model grader보다 우선하지만, **문장 동기화나 semantic prose consistency를 문자열 regression으로 고정하지 않습니다.** 그런 의미는 authoritative source와 해당 behavioral review/eval이 소유합니다.

Fixture가 존재해도 compatible runner와 실제 model/runtime을 실행하지 않았다면 runtime behavior가 통과했다고 주장하지 않습니다.
