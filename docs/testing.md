# 테스팅 및 품질 검증 가이드

자동화 테스트, AgentsMesh 검증, 정적 분석 및 코드 품질 검증 가이드입니다.

## 테스트 구조

| 경로 | 역할 |
| --- | --- |
| `tests/scripts/` | 저장소 자동화 스크립트의 deterministic correctness test |
| `tests/skills/<skill>/` | Skill-specific deterministic correctness test와 그 fixture |
| `tests/evals/` | repository-owned evaluation fixture의 deterministic syntax/shape check |
| `evals/skills/<skill>/` | Skill-specific trigger, behavior, adversarial 등 model/evaluation fixture |
| `evals/regression/` | 여러 자산·target에 걸친 deterministic regression contract |

Deployable Skill package인 `.agentsmesh/skills/<skill>/`에는 repository verification 자산을 두지 않습니다. `tests/`, `evals/`, `scenarios/`, 생성된 `results/`는 runtime resource가 아닙니다.

Scenario는 독립적인 최상위 유형으로 만들지 않습니다.

- deterministic test가 소비하면 `tests/skills/<skill>/scenarios/`
- behavioral/model eval이 소비하면 `evals/skills/<skill>/`

## 검증 계층

AgentsMesh-managed Rule/Skill/Agent 변경은 가능한 범위에서 다음 순서로 검증합니다.

```text
agentsmesh lint
  → agentsmesh check
  → agentsmesh generate --check
  → affected repository tests
  → applicable behavioral/runtime eval
```

- `lint`는 canonical/target compatibility를 정적으로 검사합니다.
- `check`는 lock과 generated state의 빠른 drift gate입니다.
- `generate --check`는 실제 generation path를 다시 계산하는 stronger regeneration gate입니다.
- `evals/skills/**/*.json` 변경은 최소한 `tests/evals/`의 deterministic parse gate를 통과합니다. 이 검증은 model-based eval 실행을 의미하지 않습니다.
- 위 검증은 실제 LLM behavior를 증명하지 않습니다. trigger precision, task success, runtime parity가 필요한 주장은 별도 runtime evidence가 있어야 합니다.

## 실행 정책

- `uv run pytest`와 Lefthook `pre-push`는 루트 `tests/`를 기본 repository gate로 실행합니다.
- Skill-specific deterministic test도 `tests/skills/<skill>/`에서 같은 pytest gate를 사용합니다.
- 비싼 model-based eval은 모든 PR의 기본 gate로 만들지 않습니다. deterministic check로 판단할 수 없는 behavior만 manual, scheduled, release gate 등 필요한 시점에 실행합니다.
- 테스트나 eval이 생성한 report/result는 durable evidence로 명시적으로 승격하지 않는 한 commit하지 않습니다.

## 기본 명령

```bash
npm ci
npm run agentsmesh:lint
npm run agentsmesh:check
npm run agentsmesh:generate:check
uv run pytest
uv run ruff check .
```
