# 테스팅 및 품질 검증 가이드

자동화 테스트, Rulesync 검증, 정적 분석 및 코드 품질 검증 가이드입니다.

## 테스트 구조

| 경로 | 역할 |
| --- | --- |
| `tests/scripts/` | repository automation script의 deterministic correctness test |
| `tests/skills/<skill>/` | Skill-specific deterministic correctness test와 fixture |
| `tests/evals/` | repository-owned evaluation fixture의 syntax/shape check |
| `evals/skills/<skill>/` | Skill-specific trigger, behavior, adversarial 등 model/evaluation fixture |
| `evals/regression/` | 여러 source·target에 걸친 deterministic regression contract |

Deployable Skill package인 `src/rulesync/.rulesync/skills/<skill>/`에는 repository verification 자산을 두지 않습니다. `tests/`, `evals/`, `scenarios/`, generated `results/`는 runtime resource가 아닙니다.

## 검증 계층

Rulesync-managed source 변경은 가능한 범위에서 다음 순서로 검증합니다.

```text
native workspace: src/rulesync
  → rulesync doctor --strict / generate --dry-run directly
  → copy workspace verbatim to a temporary directory for generation
  → rulesync generate + generate --check
  → affected repository tests
  → applicable behavioral/runtime eval
```

Repository `npm run rulesync:*` command는 `scripts/run_rulesync.py`를 사용합니다. `doctor`와 `preview`는 native workspace에서 직접 실행하고, `validate`만 temporary copy를 사용합니다. Generated target projection과 Rulesync lock state는 canonical repository file로 남기지 않습니다.

Rulesync schema와 target mapping 자체는 upstream contract가 소유합니다. Repository test는 다음처럼 이 저장소가 추가로 보장해야 하는 invariant에 집중합니다.

- distribution source와 repository runtime surface의 isolation
- deployable Skill package와 verification surface의 분리
- generated projection의 package/body fidelity
- repository-owned route generation
- behavioral/runtime claim에 필요한 별도 evidence

Deterministic check로 판정할 수 있는 계약은 model grader보다 우선합니다. Trigger precision, task success 또는 runtime parity가 필요한 주장은 실제 runtime/eval evidence 없이 성공으로 간주하지 않습니다.

## 기본 명령

```bash
npm run rulesync:doctor
npm run rulesync:preview
npm run rulesync:validate
uv run pytest
uv run ruff check .
```
