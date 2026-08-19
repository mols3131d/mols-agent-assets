# 테스팅 및 품질 검증 가이드

자동화 테스트, Rulesync 검증, 정적 분석 및 코드 품질 검증 가이드입니다.

## 테스트 구조

| 경로 | 역할 |
| --- | --- |
| `tests/scripts/` | repository automation script의 deterministic correctness test |
| `tests/skills/<skill>/` | Skill-specific deterministic correctness test와 fixture |
| `tests/evals/` | repository-owned evaluation fixture의 syntax/shape check |
| `evals/skills/<skill>/` | Skill-specific trigger, behavior, adversarial 등 model/evaluation fixture |
| `evals/regression/` | 여러 source에 걸친 deterministic regression contract |

Deployable Skill package인 `src/rulesync/.rulesync/skills/<skill>/`에는 repository verification 자산을 두지 않습니다. `tests/`, `evals/`, `scenarios/`, generated `results/`는 runtime resource가 아닙니다.

## Rulesync workspace

Rulesync 검증에서는 두 workspace를 섞지 않습니다.

- root `.rulesync/` + `rulesync.jsonc`: 이 repository 자체를 위한 optional workspace
- `src/rulesync/.rulesync/` + `src/rulesync/rulesync.jsonc`: reusable asset library workspace

Root workspace가 존재해도 library 검증에 암묵적으로 포함하지 않으며, library asset을 repository runtime configuration으로 간주하지 않습니다.

## 검증 계층

```text
selected canonical workspace
  → rulesync doctor --strict
  → 필요할 때 target을 선택해 generate --dry-run
  → write-producing generate/check는 temporary workspace에서만 수행
  → affected repository tests
  → applicable behavioral/runtime eval
```

Repository `npm run rulesync:*` command는 현재 library workspace인 `src/rulesync/`를 대상으로 `scripts/run_rulesync.py`를 사용합니다. Runner는 Rulesync의 target path나 projection semantics를 재구현하지 않고 CLI에 위임합니다. Generated target projection과 Rulesync lock state는 repository에 남기지 않습니다.

Repository-level Rulesync workspace가 생기면 root에서 별도로 native diagnostics를 실행합니다. Library command에 root workspace를 숨겨서 합치지 않습니다.

이 저장소는 supported vendor/target matrix를 검증하지 않습니다. Repository CI는 target을 선택하지 않고 library canonical Rulesync configuration과 repository-owned invariant만 검증합니다. 특정 target projection이 작업에 중요할 때만 해당 target과 workspace를 명시해 temporary workspace에서 별도로 검증합니다.

Repository test는 Rulesync 자체가 아니라 이 저장소가 추가로 소유하는 invariant에 집중합니다.

- repository Rulesync workspace와 reusable library workspace의 isolation
- canonical source와 generated projection surface의 분리
- deployable Skill package와 verification surface의 분리
- repository-owned route generation
- behavioral/runtime claim에 필요한 별도 evidence

Deterministic check로 판정할 수 있는 계약은 model grader보다 우선합니다. Trigger precision, task success 또는 runtime parity가 필요한 주장은 실제 runtime/eval evidence 없이 성공으로 간주하지 않습니다.

## 기본 명령

Library workspace:

```bash
npm run rulesync:doctor
npm run rulesync:preview -- --targets <target>
npm run rulesync:validate -- --targets <target>
uv run pytest
uv run ruff check .
```

Repository workspace가 존재하면 root에서 Rulesync native CLI를 별도로 사용합니다.
