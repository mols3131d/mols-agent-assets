---
description: mols-coding-context의 설계 의도, 지침 채택·제거 기준과 행동 회귀 평가를 검토할 때 사용합니다.
---

# Coding Context

[mols-coding-context](../../../src/rulesync/.rulesync/skills/mols-coding-context/SKILL.md)는 코딩 에이전트의 자체 역량을 대체하지 않고, 비용이 큰 엔지니어링 판단 오류를 줄이는 언어 독립적 기본 컨텍스트다. 일상적인 코딩 작업에도 적용하므로 반복 주입 비용을 고려한다. 실행 판단과 선택 조건은 SKILL.md가 소유하며, 이 문서는 유지보수 시에만 참조한다.

## Activation

코드 또는 실행 동작에 대한 추론이 필요한 작업에 진입할 때 최초 로드하고, 이미 컨텍스트에 있으면 재사용한다. 작업 도중 처음 필요해지거나 컨텍스트가 유실되면 필요한 시점에 로드한다. 턴·구현·테스트·리뷰마다 재로딩하지 않는다. 사실 조회, 코드와 무관한 저장소 관리, 일반 문서 작성은 제외한다.

최초 로딩은 description이 표현하는 선택 의도이지 런타임이 보장하는 호출 횟수 제한이 아니다. 언어별 의미가 중요한 경우에만 대응 add-on을 함께 사용한다.

## Maintenance

- **채택:** 반복되는 에이전트 실패 또는 중요한 판단 위험을 근거로, 기존 모델·하네스·전문 자산에 부족한 언어 독립적 판단만 추가한다. 원칙의 인지도나 외부 자산의 구성은 채택 근거가 아니다.
- **제거:** 일반 코딩 지식, 이미 충분히 수행되는 행동, 중복 표현, 모델의 일시적인 약점에 한정된 지침은 재검토한다. 결정적 도구가 충분히 판정·해소할 수 있는 규칙은 도구에 맡기며, 도구의 부재만으로 규칙이나 실행 절차를 복제하지 않는다.
- **압축:** 판단 조건과 예외를 보존하고, 표준 전문용어로 중복·열거를 줄인다. 단어 수나 토큰 수를 줄이기 위해 추론 부담을 늘리지 않는다.
- **책임:** 저장소 정책, 권한, 검증 보고, 구현·리뷰·테스트 절차와 최적화 도구는 각각의 정본이 소유한다. Core에 체크리스트, 도구 호출, 산출물, 추가 자료 로딩을 강제하지 않는다. 언어별 판단은 [Python add-on](../mols-coding-context-python/guidance.md)과 같은 별도 자산에서 해당 언어의 delta만 유지한다.

pstack은 판단 기준의 참고 출처로만 사용했다. 추가 흡수는 하지 않으며, 향후 지침 변경은 위 기준과 실제 실패 근거에 따라 판단한다.

## Evaluation

[저장소 평가 정책](../../development/evaluation.md)에 따라 아래 행동을 비교한다. 구체적인 평가 계약과 fixture는 evals/가 소유한다.

| 대상 | 확인할 행동 |
| --- | --- |
| 선택·로딩 | 일반 코딩의 최초 선택, 같은 컨텍스트에서 재사용, 비코딩 작업의 비선택, 언어별 add-on의 조건부 선택 |
| 판단 품질 | 호환성·실패 의미 보존, 적절한 상태 모델링·ownership, 안전한 부작용 처리, 근거 있는 최적화·리뷰·검증 |
| 회귀·비용 | 과잉 추상화·재설계·검증, 반복 실패 시 전제 검증 누락, 불필요한 도구 호출과 재로딩 |

동일한 모델·런타임·하네스와 비교 가능한 조건에서 Core 적용 여부 또는 변경 전후를 비교한다. 판단 품질과 함께 입력·추론 토큰, 소요 시간, 추가 작업을 측정 가능한 범위에서 확인한다. 파일 길이와 정적 검사만으로 행동 동등성이나 비용 절감을 단정하지 않는다.

## References

- [기존 설계 및 마이그레이션](https://github.com/mols3131d/mols-agent-assets/pull/222)
- [pstack (Lauren Tan)](https://github.com/cursor/plugins/tree/9e278fe4d4ecd8bfe98b1b79bf4be662efb338cc/pstack) — domain modeling, premise checking, shared state, contract-oriented testing, failure boundaries, reader load, measurement. [MIT license](https://github.com/cursor/plugins/blob/9e278fe4d4ecd8bfe98b1b79bf4be662efb338cc/pstack/LICENSE).
- [OpenAI: Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) — 모델 발전에 따른 절차형 지침과 컨텍스트 과잉 재검토.
