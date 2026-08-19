# 평가 (`evals/`)

`evals/`는 저장소가 소유하는 평가 계약을 저장한다.

- Skill별 trigger, behavior, adversarial 평가 fixture는 `evals/skills/<skill-name>/`을 사용한다.
- 여러 Agent Asset이나 target에 걸친 회귀 계약은 `evals/regression/`을 사용한다.
- 실행 가능한 결정론적 정확성 테스트는 `tests/`가 소유한다.
- 배포 가능한 `src/rulesync/.rulesync/skills/<skill-name>/` package 안에는 저장소 eval을 두지 않는다.
- 결정론적 assertion으로 판정 가능한 계약은 model grader보다 우선한다.
- runtime behavior를 검증하지 않은 case를 runtime evidence처럼 표현하지 않는다.

## 현재 회귀 평가 묶음

- `regression/rulesync-source-isolation.json` — `src/rulesync/` native workspace와 `src/rulesync/.rulesync/` 정본 자산 소스, 저장소 runtime-discovery surface의 격리를 고정하는 결정론적 계약.
- `regression/chatbot-harness-compatibility.json` — `CHATBOT.md` compatibility layer, GitHub context loader, Rule boundary 사이의 authority·discovery·partial-harness invariant를 고정하는 결정론적 계약.
