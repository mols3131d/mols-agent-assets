# 평가 (`evals/`)

`evals/`는 repository-owned behavioral/model evaluation fixture와 **기계적으로 검증할 가치가 있는 cross-asset regression contract**를 저장합니다.

- Skill별 trigger, behavior, adversarial fixture → `evals/skills/<skill-name>/`
- 여러 source에 걸친 deterministic invariant → 필요한 경우에만 `evals/regression/`
- 실행 가능한 deterministic correctness test → `tests/`
- Deployable Skill package 안에는 repository eval을 두지 않습니다.

Eval을 언제 추가하고 어떤 evidence로 해석할지는 [`docs/development/evaluation.md`](../docs/development/evaluation.md)가 소유합니다. 이 README는 `evals/`의 fixture placement와 local boundary만 소유합니다.

Deterministic assertion이 가능한 계약은 model grader보다 우선하지만, **문장 동기화나 semantic prose consistency를 문자열 regression으로 고정하지 않습니다.** 그런 의미는 authoritative source와 해당 behavioral review/eval이 소유합니다.

현재 `evals/regression/rulesync-source-isolation.json`은 repository/library Rulesync workspace와 generated surface의 최소 격리 contract만 소유합니다.
