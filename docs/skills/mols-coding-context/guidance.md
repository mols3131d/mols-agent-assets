---
description: 범용 코딩 판단 컨텍스트의 설계 의도와 지침 채택·회귀 검토 기준을 설명한다.
---

# Coding context

`mols-coding-context`는 코드 또는 실행 계약을 다루는 에이전트의 판단을 보강하는 언어 독립적인 Context Skill이다. 코딩 워크플로우나 플레이북을 제공하지 않는다.

코딩 작업 진입 시 아직 컨텍스트에 없다면 한 번 선택·로드하고, 유지되는 동안 재사용한다. 대화의 매 턴이나 구현·테스트·리뷰 단계마다 다시 로드하지 않는다. 이는 선택 의도이며 런타임이 강제하는 호출 횟수 제한은 아니다.

## Guidance admission

- 기존 모델·하네스·저장소 지침과 전문 자산이 충분히 담당하는 행동은 복제하지 않는다.
- 실제 코드 계약, 실패 의미, 변경 범위, 운영 복잡도와 같이 잘못된 판단의 비용이 큰 기준을 우선한다.
- 일반적인 프로그래밍 지식, 단계별 작업법, 강제 체크리스트·도구 호출·산출물·add-on 로딩 요구를 추가하지 않는다. 일반적인 정직성 및 검증 결과 보고 규칙은 기본 모델·하네스의 책임으로 두고 중복 주입하지 않는다.
- 모델 세대에 따라 지침의 필요성을 다시 평가한다. 특정 모델의 일시적 약점을 범용 Core의 영구 계약으로 고정하지 않는다.

언어별 의미, 저장소 정책, 구현·리뷰·테스트 절차 및 최적화 도구는 각각의 정본이 소유한다. 언어별 지침은 해당 언어의 실제 의미나 런타임에 의존할 때만 [Python add-on](../mols-coding-context-python/guidance.md)과 같은 독립적인 add-on에서 필요한 delta만 유지한다.

pstack에서 얻은 설계 관점은 독립적인 판단 기준으로 재구성한다. 개별 principle의 강제 절차·횟수·도구 요구나 plugin 구조는 가져오지 않는다.

## Regression evidence

[기존 설계 및 마이그레이션](https://github.com/mols3131d/mols-agent-assets/pull/222)의 취지를 유지한다. 변경 전후에 일반 코딩 작업 진입 시 최초 선택과 컨텍스트 유지 중 불필요한 재로딩 여부, 단순 사실 조회·문서 작업의 비선택, Python 의미에 따른 add-on 동반 선택, 불필요한 작업 증가, 호환성·실패 의미 보존과 근거 없는 최적화·리뷰 finding을 비교한다. 상태 표현과 ownership, 반복 실패 시 가설 재검토, 계약 중심 테스트, 측정의 타당성도 비교하되 불필요한 modeling·재설계·검증이 증가하는지 함께 본다. 실제 실행 없이 동등한 런타임 행동이나 품질 향상을 주장하지 않는다.

## References

- [pstack (Lauren Tan)](https://github.com/cursor/plugins/tree/9e278fe4d4ecd8bfe98b1b79bf4be662efb338cc/pstack) — domain modeling, premise checking, shared state, contract-oriented testing, failure boundaries, reader load, measurement. [MIT license](https://github.com/cursor/plugins/blob/9e278fe4d4ecd8bfe98b1b79bf4be662efb338cc/pstack/LICENSE).

- [OpenAI: Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) — 모델 발전에 따른 절차적 지시와 컨텍스트 과잉 재검토.
