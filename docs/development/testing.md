---
description: repository의 deterministic verification, tool validation, PR Gate와 merge-blocking test evidence를 확인할 때 사용하는 local policy입니다.
---

# Testing

## Tool ownership

Repository에서 사용하는 도구 버전과 여러 도구를 아우르는 task entrypoint는 `mise.toml`에 고정합니다.

- mise는 `uv`, Node.js, rumdl, Lefthook, Biome, Rulesync와 repository-level task를 소유합니다.
- uv는 `.python-version`의 Python version, `pyproject.toml`의 Python dependency, environment와 `uv.lock`을 소유합니다.
- Ruff는 Python development dependency로 유지하며 uv를 통해 실행합니다.

Python은 의도적으로 `mise.toml`에 선언하지 않습니다. 필요할 때 `uv run`이 project Python을 준비하고 사용합니다.

## Setup

```bash
mise install
mise run setup
```

`mise run setup`은 모든 Python dependency group, lock된 repository-local Rulesync asset, 생성된 Agent Skill과 Git hook을 설치합니다.

## Formatting

```bash
mise run format
```

Format task는 각 도구를 소유하는 runtime을 통해 Ruff, rumdl과 Biome을 실행합니다.

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
- behavioral eval surface → deterministic fixture/plumbing check만 필요한 경우 blocking verification으로 실행

Stochastic model/runtime eval의 evidence 수준과 merge admission 기준은 [Evaluation](evaluation.md)이 소유합니다.

PR Gate는 `contents: read`만 사용합니다. Generated route나 Markdown drift가 있으면 CI가 수정해 push하지 않고 실패시켜 source branch에서 바로잡게 합니다. 따라서 merge 이후 `main`에 직접 write-back하는 CI는 두지 않습니다.

## Rulesync 검증

Rulesync CLI version은 `mise.toml`에서 exact pin합니다. Repository `npm run rulesync:*` command는 `scripts/run_rulesync.py`를 통해 `src/rulesync/` workspace를 대상으로 실행합니다. Runner는 target path나 projection semantics를 재구현하지 않고 mise-managed Rulesync CLI에 위임합니다.

Root repository workspace는 reusable library와 분리된 declarative consumer입니다. `rulesync.jsonc`의 선택과 `rulesync.lock`의 integrity를 deterministic regression으로 검증하고, `mise run setup`이 `rulesync install --frozen` 후 `agentsskills` target을 `.agents/skills/`로 생성합니다.

## Evaluation integration

Behavioral contract, fixture design, Promptfoo의 역할, runtime/model evidence 해석은 [Evaluation](evaluation.md)이 소유합니다.

PR Gate가 실행하는 fixture-mode smoke는 provider/generator/assertion plumbing을 확인하는 deterministic check일 뿐 runtime behavior evidence가 아닙니다.

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
