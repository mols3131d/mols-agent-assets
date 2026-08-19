# 테스팅 및 품질 검증 가이드

자동화 테스트, AgentsMesh 검증, 정적 분석 및 코드 품질 검증 가이드입니다.

## 테스트 구조

| 경로 | 역할 |
| --- | --- |
| `tests/scripts/` | 저장소 자동화 스크립트의 deterministic correctness test |
| `tests/skills/<skill>/` | Skill-specific deterministic correctness test와 fixture |
| `tests/evals/` | repository-owned evaluation fixture의 deterministic syntax/shape check |
| `evals/skills/<skill>/` | Skill-specific trigger, behavior, adversarial 등 model/evaluation fixture |
| `evals/regression/` | 여러 자산·target에 걸친 deterministic regression contract |

Deployable Skill package인 `src/agentsmesh/skills/<skill>/`에는 repository verification 자산을 두지 않습니다. `tests/`, `evals/`, `scenarios/`, 생성된 `results/`는 runtime resource가 아닙니다.

## 검증 계층

AgentsMesh-compatible Rule/Skill/Agent 변경은 가능한 범위에서 다음 순서로 검증합니다.

```text
stage src/agentsmesh into a temporary .agentsmesh workspace
  → agentsmesh lint
  → temporary generation / drift checks
  → affected repository tests
  → applicable behavioral/runtime eval
```

Repository `npm run agentsmesh:*` 명령은 `scripts/run_agentsmesh.py`를 통해 temporary workspace에서 실행됩니다. 생성된 `.agentsmesh/`, `.github/skills/`, `.github/agents/`, `.agents/rules/`, `.agents/skills/`를 이 저장소에 검증 산출물로 남기지 않습니다.

- deterministic check로 판정할 수 있는 계약을 model grader보다 우선합니다.
- `evals/skills/**/*.json` 변경은 최소한 `tests/evals/`의 deterministic parse gate를 통과합니다.
- 위 검증은 실제 LLM behavior를 증명하지 않습니다. trigger precision, task success, runtime parity가 필요한 주장은 별도 runtime evidence가 있어야 합니다.

## 기본 명령

```bash
npm ci
npm run agentsmesh:lint
npm run agentsmesh:check
npm run agentsmesh:generate:check
uv run pytest
uv run ruff check .
```
