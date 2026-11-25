---
description: 범용 코딩 판단 컨텍스트의 설계 의도와 지침 채택·회귀 검토 기준을 설명한다.
---

# Coding context

`mols-coding-context`는 코드 또는 실행 계약을 다루는 에이전트의 판단을 보강하는 언어 독립적인 Context Skill이다. 코딩 워크플로우나 플레이북을 제공하지 않는다.

## Guidance admission

- 기존 모델·하네스·저장소 지침과 전문 자산이 충분히 담당하는 행동은 복제하지 않는다.
- 실제 코드 계약, 실패 의미, 변경 범위, 운영 복잡도와 같이 잘못된 판단의 비용이 큰 기준을 우선한다.
- 일반적인 프로그래밍 지식, 단계별 작업법, 무조건적인 확인·보고·도구 호출 요구를 추가하지 않는다.
- 모델 세대에 따라 지침의 필요성을 다시 평가한다. 특정 모델의 일시적 약점을 범용 Core의 영구 계약으로 고정하지 않는다.

언어별 지침은 해당 언어의 실제 의미나 런타임에 의존할 때만 [Python add-on](../mols-coding-context-python/guidance.md)과 같은 독립적인 add-on으로 유지한다.

## Regression evidence

[기존 설계 및 마이그레이션](https://github.com/mols3131d/mols-agent-assets/pull/222)의 취지를 유지한다. 변경 전후에 일반 코딩 작업의 선택, 단순 사실 조회·문서 작업의 비선택, Python 의미에 따른 add-on 동반 선택, 불필요한 작업 증가, 호환성·실패 의미 보존과 근거 없는 최적화·리뷰 finding을 비교한다. 실제 실행 없이 동등한 런타임 행동이나 품질 향상을 주장하지 않는다.

## References

- [OpenAI: Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) — 모델 발전에 따른 절차적 지시와 컨텍스트 과잉 재검토.
