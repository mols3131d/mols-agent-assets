# 테스팅 및 품질 검증 가이드

이 문서는 repository verification의 **위치와 증거 수준**을 정의합니다. Workspace/source ownership은 [Rulesync](../references/tooling/rulesync.md)를 따릅니다. Tool version과 runtime ownership은 [mise](../references/tooling/mise.md)를 따릅니다.

## 구조

| 경로 | 역할 |
| --- | --- |
| `tests/scripts/` | repository automation의 deterministic test |
| `tests/skills/<skill>/` | Skill-specific deterministic test와 fixture |
| `tests/evals/` | eval fixture의 syntax/shape check |
| `evals/skills/<skill>/` | trigger, behavior, adversarial 등 model/evaluation fixture |
| `evals/regression/` | 여러 asset에 걸친 regression contract |

Repository verification은 deployable Skill package 밖에 둡니다. `scenarios/`도 독립 asset type이 아니라 그것을 소비하는 test/eval 쪽에 둡니다.

Generated `results/`는 기본적으로 일회성 output입니다. 별도 report/evidence로 지속 보존할 명확한 이유가 있을 때만 durable artifact로 승격합니다.

## 원칙

- Deterministic assertion으로 판정 가능한 계약은 model grader보다 우선합니다.
- Test/eval은 canonical asset을 검증하며 자체적으로 두 번째 source of truth가 되지 않아야 합니다.
- Skill/Subagent inventory, 문서의 특정 문장, 과거 migration 경로 같은 재생성 가능한 상태를 회귀 계약에 수동 복제하지 않습니다.
- Target-specific runtime claim이 성공 조건일 때만 실제 usage surface의 evidence를 요구합니다.
- Generated projection 성공만으로 runtime behavior parity를 주장하지 않습니다.

## Toolchain

처음 clone한 뒤 repository toolchain을 설치하고 Python environment와 Git hooks를 준비합니다.

```bash
mise install
mise run setup
```

`mise.toml`은 `uv`, Node.js, rumdl, Lefthook, Biome, Rulesync version을 고정합니다. Python version과 dependency environment는 `.python-version`, `pyproject.toml`, `uv.lock`을 통해 uv가 관리합니다.

Cross-tool 검증 entry point는 다음과 같습니다.

```bash
mise run check
mise run test
```

## PR Gate

`main` 대상 모든 PR은 하나의 stable `PR Gate` job을 실행합니다. Workflow-level path filter를 두지 않아 required check가 skip 상태로 남지 않게 합니다.

PR Gate는 root `tests/` 전체를 항상 `uv --locked` semantics로 실행합니다. 현재 deterministic suite가 충분히 작으므로 test-selection routing보다 full suite를 fail-safe 기본값으로 사용합니다.

추가 비용이 있는 검증만 change impact에 따라 실행합니다.

- tooling configuration → `mise run check`
- canonical Rulesync source → Markdown normalization + `rulesync:doctor`
- Skill route inputs → distribution route regeneration 후 committed output과 diff 확인
- changed Markdown → rumdl normalization 후 diff 확인
- `mols-rpi` / Promptfoo eval surface → Promptfoo fixture-mode smoke

PR Gate는 `contents: read`만 사용합니다. Generated route나 Markdown drift가 있으면 CI가 수정해 push하지 않고 실패시켜 source branch에서 바로잡게 합니다. 따라서 merge 이후 `main`에 직접 write-back하는 CI는 두지 않습니다.

## Rulesync 검증

Reusable library의 기본 순서는 다음과 같습니다.

```text
rulesync doctor --strict
→ 관련 deterministic test / behavioral eval
→ 필요한 경우에만 target projection/runtime 검증
```

Rulesync CLI version은 `mise.toml`에서 exact pin합니다. Repository `npm run rulesync:*` command는 `scripts/run_rulesync.py`를 통해 `src/rulesync/` workspace를 대상으로 실행합니다. Runner는 target path나 projection semantics를 재구현하지 않고 mise-managed Rulesync CLI에 위임합니다.

Root repository workspace가 실제로 존재하면 library와 별도로 검증합니다.

## Promptfoo runtime eval PoC

Promptfoo는 `evals/`의 behavioral contract를 소유하지 않습니다. `mols-rpi` PoC는 기존 `evals/skills/mols-rpi/cases.json`의 일부 case를 실행 시점에 읽어 Promptfoo test로 투영합니다.

먼저 provider, generator와 deterministic assertion 연결만 확인합니다.

```bash
mise exec -- npm run eval:promptfoo:mols-rpi:smoke
```

이 smoke는 fixture-mode plumbing check이며 **runtime behavior evidence가 아닙니다**. 관련 eval surface가 바뀌면 PR Gate가 이 smoke를 blocking verification으로 실행합니다.

실제 local model eval은 Ollama를 사용합니다. 기본 runtime model과 semantic grader는 `qwen2.5`입니다.

```bash
ollama pull qwen2.5
mise exec -- npm run eval:promptfoo:mols-rpi
```

필요한 경우 다음 환경 변수만 override합니다.

- `PROMPTFOO_RUNTIME_MODEL` — 실행 대상 Ollama model
- `PROMPTFOO_GRADER_PROVIDER` — semantic grader provider
- `OLLAMA_BASE_URL` — Ollama endpoint

`scripts/evals/run_promptfoo.py`가 Promptfoo version을 고정하고 필요한 Node.js version을 확인합니다. Telemetry, update check, remote generation과 sharing은 기본 비활성화하며, Promptfoo local state는 `.tmp/` 아래에 둡니다. 두 config 모두 cache, result history와 sharing을 기본적으로 남기지 않습니다.

## 기본 명령

```bash
mise exec -- npm run rulesync:doctor
mise run check
mise run test
```

구체적인 target 검증이 필요할 때만 다음을 추가합니다.

```bash
mise exec -- npm run rulesync:preview -- --targets <target>
mise exec -- npm run rulesync:validate -- --targets <target>
```
