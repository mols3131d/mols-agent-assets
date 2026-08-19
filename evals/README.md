# Evals

`evals/`는 repository-owned evaluation contract를 저장한다.

- Skill-specific trigger, behavior, adversarial 등 evaluation fixture는 `evals/skills/<skill-name>/`을 사용한다.
- 여러 Agent Asset이나 target에 걸친 regression contract는 `evals/regression/`을 사용한다.
- 실행 가능한 deterministic correctness test는 `tests/`가 소유한다.
- deployable `src/agentsmesh/.agentsmesh/skills/<skill-name>/` package 안에는 repository eval을 두지 않는다.
- deterministic assertion으로 판정 가능한 계약은 model grader보다 우선한다.
- runtime behavior를 검증하지 않은 case를 runtime evidence처럼 표현하지 않는다.

## Current suites

- `regression/agentsmesh-source-isolation.json` — `src/agentsmesh/` native workspace와 `src/agentsmesh/.agentsmesh/` canonical asset source, repository runtime-discovery surface 격리를 고정하는 deterministic contract.
- `regression/chatbot-harness-compatibility.json` — `CHATBOT.md` compatibility layer, GitHub context loader, Rule boundary 사이의 authority·discovery·partial-harness invariant를 고정하는 deterministic contract.
