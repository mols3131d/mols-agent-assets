# Evals

`evals/`는 repository-owned evaluation contract를 저장한다.

- Skill-specific trigger, behavior, adversarial 등 evaluation fixture는 `evals/skills/<skill-name>/`을 사용한다.
- 여러 Agent Asset이나 target에 걸친 regression contract는 `evals/regression/`을 사용한다.
- 실행 가능한 deterministic correctness test는 `tests/`가 소유한다.
- deployable `.agentsmesh/skills/<skill-name>/` package 안에는 repository eval을 두지 않는다.
- deterministic assertion으로 판정 가능한 계약은 model grader보다 우선한다.
- runtime behavior를 검증하지 않은 case를 runtime evidence처럼 표현하지 않는다.

## Current suites

- `regression/agentsmesh-exodus.json` — AgentsMesh EXODUS 이후 canonical authority, active targets, generated projection, explicit exceptions, retired legacy surfaces를 고정하는 deterministic migration contract.
