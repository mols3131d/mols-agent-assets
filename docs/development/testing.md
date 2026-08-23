---
description: 저장소의 결정론적 검증, 도구 검증, PR Gate와 merge를 차단하는 테스트 근거를 확인할 때 사용하는 정책입니다.
---

# Testing

## Tool ownership

저장소에서 사용하는 도구 버전과 여러 도구를 아우르는 작업 진입점은 `mise.toml`에 고정합니다.

- mise는 `uv`, Node.js, rumdl, Lefthook, Biome, Rulesync, skills CLI와 저장소 수준 작업을 소유합니다.
- uv는 `.python-version`의 Python 버전, `pyproject.toml`의 Python 의존성, 환경과 `uv.lock`을 소유합니다.
- Ruff는 Python 개발 의존성으로 유지하며 uv를 통해 실행합니다.

Python은 의도적으로 `mise.toml`에 선언하지 않습니다. 필요할 때 `uv run`이 프로젝트 Python을 준비하고 사용합니다.

## Setup

```bash
mise install
mise run setup
```

`mise run setup`은 모든 Python 의존성 그룹, 저장소 내부의 잠금된 Rulesync 자산, 생성된 Agent Skill, `skills-lock.json`의 외부 Skill dependency와 Git hook을 설치합니다. 외부 Skill의 vendor별 설치·갱신은 `mise run skills-sync`와 같은 구현을 사용합니다.

## Formatting

```bash
mise run format
```

`format` task는 각 도구를 소유하는 runtime을 통해 Ruff, rumdl과 Biome을 실행합니다.

## Validation

```bash
mise run check
mise run test
```

## PR Gate

`main` 대상 모든 PR은 하나의 고정된 `PR Gate` job을 실행합니다. Workflow 수준 path filter를 두지 않아 required check가 skip 상태로 남지 않게 합니다.

PR Gate는 root `tests/` 전체를 항상 `uv --locked` semantics로 실행합니다. 현재 결정론적 test suite가 충분히 작으므로 test 선택 routing보다 전체 suite를 안전한 기본값으로 사용합니다.

추가 비용이 있는 검증만 변경 영향에 따라 실행합니다.

- tooling configuration → `mise run check`
- canonical Rulesync source → Markdown normalization + `rulesync:doctor`
- Skill route inputs → distribution route regeneration 후 committed output과 diff 확인
- changed Markdown → rumdl normalization 후 diff 확인
- behavioral eval surface → deterministic fixture/plumbing check만 필요한 경우 blocking verification으로 실행

확률적 model/runtime eval의 근거 수준과 merge admission 기준은 [Evaluation](evaluation.md)이 소유합니다.

PR Gate는 `contents: read`만 사용합니다. 생성된 route나 Markdown drift가 있으면 CI가 수정해 push하지 않고 실패시켜 source branch에서 바로잡게 합니다. 따라서 merge 이후 `main`에 직접 write-back하는 CI는 두지 않습니다.

## Rulesync 검증

Rulesync CLI 버전은 `mise.toml`에 정확히 고정합니다. Repository `npm run rulesync:*` command는 `scripts/run_rulesync.py`를 통해 `src/rulesync/` workspace를 대상으로 실행합니다. Runner는 target path나 projection semantics를 재구현하지 않고 mise-managed Rulesync CLI에 위임합니다.

Root repository workspace는 reusable library와 분리된 declarative consumer입니다. `rulesync.jsonc`의 선택과 `rulesync.lock`의 무결성을 deterministic regression으로 검증하고, `mise run setup`이 `rulesync install --frozen` 후 `agentsskills` target을 `.agents/skills/`로 생성합니다.

## Evaluation integration

동작 계약, fixture 설계, Promptfoo의 역할, runtime/model 근거 해석은 [Evaluation](evaluation.md)이 소유합니다.

PR Gate가 실행하는 fixture-mode smoke는 provider/generator/assertion 연결을 확인하는 deterministic check일 뿐 runtime 동작의 근거가 아닙니다.

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
