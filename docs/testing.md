# 테스팅 및 품질 검증 가이드

자동화 테스트, AgentsMesh 검증, 정적 분석 및 코드 품질 검증 가이드입니다.

## 테스트 구조

| 경로 | 역할 |
| --- | --- |
| `tests/scripts/` | 저장소 자동화 스크립트의 기본 correctness 테스트 |
| `tests/skills/<skill>/` | portable Skill 스크립트의 기본 correctness 테스트 |
| `.agentsmesh/skills/<skill>/.tests/` | 선택적 tuning/evaluation harness |
| `evals/` | 여러 자산에 걸친 evaluation contract |
| `src/skills-chatbot-runtime/<skill>/evals/` | package lifecycle에 종속된 package-local eval |

기본 correctness 테스트는 저장소 루트 `tests/`에 둡니다. Skill 내부 `.tests/`는 반복 튜닝, 평가, 실험처럼 Skill과 함께 둘 명확한 이유가 있을 때만 사용합니다.

## 검증 계층

AgentsMesh-managed Rule/Skill 변경은 가능한 범위에서 다음 순서로 검증합니다.

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
- 위 검증은 실제 LLM behavior를 증명하지 않습니다. trigger precision, task success, runtime parity가 필요한 주장은 별도 runtime evidence가 있어야 합니다.

## 실행 정책

- `uv run pytest`와 Lefthook `pre-push`는 루트 `tests/`를 기본 repository gate로 실행합니다.
- Skill 내부 `.tests/`는 기본 gate에 자동 포함하지 않습니다.
- `.tests/` 검증이 일반 correctness에 필수가 되면 `tests/skills/<skill>/`로 승격합니다.
- 비싼 model-based eval은 모든 PR의 기본 gate로 만들지 않습니다. deterministic check로 판단할 수 없는 behavior만 manual, scheduled, release gate 등 필요한 시점에 실행합니다.

## 기본 명령

```bash
npm ci
npm run agentsmesh:lint
npm run agentsmesh:check
npm run agentsmesh:generate:check
uv run pytest
uv run ruff check .
```
