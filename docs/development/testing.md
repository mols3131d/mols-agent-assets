# Testing

## Tool ownership

Repository tool versions and cross-tool task entry points are pinned in `mise.toml`.

- mise owns `uv`, Node.js, rumdl, Lefthook, Biome, Rulesync, and repository-level tasks.
- uv owns the Python version from `.python-version`, Python dependencies from `pyproject.toml`, the environment, and `uv.lock`.
- Ruff remains a Python development dependency and runs through uv.

Python is intentionally not declared in `mise.toml`; `uv run` provisions and uses the project Python when required.

## Setup

```bash
mise install
mise run setup
```

`mise run setup` installs all Python dependency groups, locked repository-local Rulesync assets, and Git hooks.

## Formatting

```bash
mise run format
```

The format task runs Ruff, rumdl, and Biome through their owning runtimes.

## Validation

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

Rulesync CLI version은 `mise.toml`에서 exact pin합니다. Repository `npm run rulesync:*` command는 `scripts/run_rulesync.py`를 통해 `src/rulesync/` workspace를 대상으로 실행합니다. Runner는 target path나 projection semantics를 재구현하지 않고 mise-managed Rulesync CLI에 위임합니다.

Root repository workspace는 reusable library와 분리된 declarative consumer입니다. `rulesync.jsonc`의 선택과 `rulesync.lock`의 integrity를 deterministic regression으로 검증하고, `mise run setup`이 `rulesync install --frozen`으로 설치합니다.

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

Local-model semantic eval은 **비차단 evidence**로 취급합니다. 동일한 Skill과 case도 model capacity와 생성·grading 변동성에 따라 결과가 달라질 수 있으므로 단일 run의 PASS/FAIL을 merge admission으로 사용하지 않습니다. 반복 가능한 failure pattern은 Skill, fixture, provider, grader 중 원인을 분리한 뒤 regression contract로 승격합니다.

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
