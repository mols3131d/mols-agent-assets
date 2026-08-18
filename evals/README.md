# Evals

`evals/`는 여러 Agent Asset이나 target에 걸친 **evaluation contract**를 저장한다.

- 실행 가능한 correctness test는 `tests/`가 소유한다.
- 특정 package lifecycle에 종속된 eval은 해당 package 내부 `evals/`에 남길 수 있다.
- deterministic assertion으로 판정 가능한 계약은 model grader보다 우선한다.
- runtime behavior를 검증하지 않은 case를 runtime evidence처럼 표현하지 않는다.

## Current suites

- `regression/agentsmesh-exodus.json` — AgentsMesh EXODUS 이후 canonical authority, active targets, generated projection, explicit exceptions, retired legacy surfaces를 고정하는 deterministic migration contract.
