# Agentic Software Engineering Pattern Candidates

최신 coding agent와 agent-first repository에서 반복적으로 보이는 software engineering 문제를 `catalog/patterns/`에 승격하기 전에 검토하기 위한 working bundle입니다.

이 문서들은 **정본 pattern이 아닙니다.** 각 후보가 독립 pattern으로 충분한지, 기존 pattern과 책임이 겹치지 않는지, 특정 vendor·harness 사례를 과도하게 일반화하지 않는지를 검토한 뒤 승격·통합·폐기합니다.

## Candidates

| Candidate | Primary area | 현재 판단 | 핵심 질문 |
| --- | --- | --- | --- |
| [Local-Reasoning Structure](local-reasoning-structure.md) | software-engineering | strong | 한 부분을 바꾸기 위해 얼마나 넓은 context를 알아야 하는가? |
| [Executable Architecture Invariants](executable-architecture-invariants.md) | software-engineering | strong / draft | 어떤 architecture invariant를 어디까지 검증하고, 검증 비용을 어떻게 제한할 것인가? |
| [Executable Verification Surface](executable-verification-surface.md) | software-engineering | strong | agent나 사람이 결과의 correctness를 스스로 판정할 수 있는가? |
| [Self-Contained Change](self-contained-change.md) | workflow / software-engineering | strong | 하나의 change가 독립적으로 이해·검증·통합 가능한가? |
| [Durable Progress Handoff](durable-progress-handoff.md) | workflow | promising | 긴 작업을 다음 session이나 agent가 반복 탐색 없이 이어갈 수 있는가? |
| [Continuous Entropy Cleanup](continuous-entropy-cleanup.md) | workflow / software-engineering | exploratory | 반복되는 작은 drift를 큰 cleanup 전에 낮은 비용으로 다룰 수 있는가? |
| [Boundary Validation](boundary-validation.md) | software-engineering | exploratory | 불확실한 외부 shape를 어디에서 신뢰 가능한 내부 형태로 바꿀 것인가? |

## Review Lens

승격 여부는 다음을 중심으로 봅니다.

- 기존 `catalog/patterns/`의 책임을 단순히 다른 이름으로 반복하지 않는가?
- 특정 제품이나 모델의 현재 limitation을 영구적인 software design rule로 만들고 있지 않은가?
- 숫자 threshold보다 problem signal과 trade-off를 설명하는가?
- 소개·제안·권장 수준으로 읽히며 project contract처럼 강제하지 않는가?
- 실질적인 한계나 주의사항이 있다면 가능한 대응과 함께 설명하는가?
- 반대로 형식을 맞추기 위해 억지 limitation이나 section을 만들고 있지 않은가?

## Research Anchors

이번 후보군은 다음 공개 자료에서 반복되는 아이디어를 출발점으로 삼았습니다. 각 후보를 승격할 때는 더 좁고 직접적인 근거를 다시 검토합니다.

- OpenAI, *Harness engineering: leveraging Codex in an agent-first world* — repository legibility, mechanical invariants, verification loops, entropy cleanup.
- Anthropic, *Harness design for long-running application development* — testable behavior, evaluator feedback, harness complexity를 필요 이상 고정하지 않는 원칙.
- Anthropic, *Long-running Claude for scientific computing* — durable progress notes와 test oracle.
- Anthropic, *Effective harnesses for long-running agents* — session handoff, feature-level progress, self-verification.
- Google Engineering Practices, *Small CLs* — line count보다 self-contained change를 중심으로 한 change sizing.

## Promotion Order

현재는 다음 순서로 깊게 검토하는 것이 가장 자연스럽습니다.

1. `local-reasoning-structure.md`
2. `executable-architecture-invariants.md`
3. `executable-verification-surface.md`
4. `self-contained-change.md`
5. 나머지 exploratory candidates

후보가 약하면 독립 pattern으로 승격하지 않고 다른 pattern의 consideration/example로 흡수하는 것을 우선합니다.
