---
description: mols-coding-context의 설계 의도, 지침 채택·제거 기준과 행동 회귀 평가를 검토할 때 사용합니다.
---

# Coding Context

[mols-coding-context](../../../src/rulesync/.rulesync/skills/mols-coding-context/SKILL.md)는 코딩 에이전트의 자체 역량을 대체하지 않고, 비용이 큰 엔지니어링 판단 오류를 줄이는 언어 독립적 기본 컨텍스트다. 일상적인 코딩 작업에도 적용하므로 개별 지침의 실익뿐 아니라 상시 주입·추론 비용도 중요하다.

실행 판단과 선택 조건은 SKILL.md가 소유한다. 이 문서는 해당 자산의 변경을 판단할 때만 참조한다.

## Activation

SKILL.md의 description은 코딩 작업 진입 시 최초 선택·로드하고, 유효한 컨텍스트를 재사용하도록 설계했다. 작업 단위는 대화의 턴이나 구현·테스트·리뷰 단계와 다르다. 작업 도중 처음 적용 범위에 들어오거나 컨텍스트가 유실되면 필요한 시점에 로드한다. 호출 횟수를 런타임에서 강제한다는 의미는 아니다.

선택 범위를 변경할 때는 일상적인 코딩 작업의 누락과 코드 추론이 필요 없는 작업의 오선택을 함께 고려한다. 언어별 세부 선택 조건은 대응 add-on의 description이 소유한다.

## Maintenance

공통 [자산 관리 기준](../../development/agent-assets/agent-asset-management.md#유지보수-문서)과 [Skill 작성 규약](../../development/agent-assets/skills/skill-authoring-conventions.md)을 적용한다. 다음은 Core 고유의 유지 판단이다.

- **채택:** 반복되는 실패 또는 비용이 큰 판단 위험에 대해 기존 모델·하네스·전문 자산이 충분히 대응하지 못하는 언어 독립적 판단만 추가한다. 외부 원칙의 인지도나 포괄성 자체는 근거가 아니다.
- **제거·압축:** 모델·도구의 발전으로 실익이 사라진 지침, 일반 지식, 중복을 제거한다. 판단 조건과 예외를 보존하며 표준 전문용어로 압축한다. 단어 수 감소와 추론 비용 감소를 동일시하지 않는다.
- **소유권:** 결정적 도구가 판정·해소할 수 있는 규칙은 도구에 맡긴다. 도구가 없더라도 그 규칙이나 실행 절차를 복제하지 않는다. 저장소 정책·권한·검증 보고·구현·리뷰·테스트 절차·최적화 도구는 각각의 정본에 둔다. [Python add-on](../mols-coding-context-python/guidance.md)은 언어 고유의 판단만 보강한다.

Core는 판단을 보강하되 워크플로우를 제공하지 않는다. 리뷰·분석·제안의 근거 검증은 실제 변경 판단에 필요한 만큼 수행하는 것이 목적이며, 모든 finding에 실행 증거를 요구하거나 다중 모델·재현 절차·체크리스트·산출물·추가 자료 로딩을 강제하는 방향으로 확장하지 않는다.

## Evaluation

[저장소 평가 정책](../../development/evaluation.md)에 따른 비교 관점이다. 구체적인 평가 계약과 fixture는 [evals/](../../../evals/README.md)가 소유한다.

| 평가 관점 | 확인할 행동과 회귀 |
| --- | --- |
| 선택·로딩 | 일상 코딩의 최초 선택 및 재사용, 비코딩의 비선택, 언어별 add-on의 조건부 동반 선택 |
| 설계·변경 | 계약·실패 의미 보존, 적절한 상태 모델링과 ownership, 안전한 부작용 처리 ↔ 과잉 추상화·재설계 |
| 주장·해결책 | 근거 있는 결함의 수용과 독립적인 해결책 판단 ↔ 근거 없는 가설의 요구사항화, 추측성 방어 추가, 필요한 보호 장치 누락 |
| 검증·최적화 | 반복 실패 시 전제 검증, 계약 중심 테스트, 타당한 측정 ↔ 과잉 검증·근거 없는 finding과 성능 주장 |
| 비용 | 입력·추론 토큰, 소요 시간, 도구 호출·재로딩·추가 작업을 측정 가능한 범위에서 비교 |

같은 모델·런타임·하네스와 작업 조건에서 Core 미적용, 기존 Core, 변경 Core를 필요에 따라 비교한다. 조건이 다르면 그 차이를 결과 해석에 반영한다. 선택·로딩은 실제 대상 런타임에서 확인하고, 판단 품질은 관찰 가능한 결과와 근거로 평가한다. 파일 길이와 정적 검사만으로 행동 동등성이나 비용 절감을 단정하지 않는다.

## References

- [기존 설계 및 마이그레이션](https://github.com/mols3131d/mols-agent-assets/pull/222)
- [pstack (Lauren Tan)](https://github.com/cursor/plugins/tree/9e278fe4d4ecd8bfe98b1b79bf4be662efb338cc/pstack) — domain modeling, premise checking, shared state, contract-oriented testing, failure boundaries, reader load, measurement. [MIT license](https://github.com/cursor/plugins/blob/9e278fe4d4ecd8bfe98b1b79bf4be662efb338cc/pstack/LICENSE).
  - 피드백의 증거와 도달 가능성 판단: [interrogate](https://github.com/cursor/plugins/tree/9e278fe4d4ecd8bfe98b1b79bf4be662efb338cc/pstack/skills/interrogate), [blast-radius](https://github.com/cursor/plugins/tree/9e278fe4d4ecd8bfe98b1b79bf4be662efb338cc/pstack/skills/blast-radius), [triage-issue-reports](https://github.com/cursor/plugins/tree/9e278fe4d4ecd8bfe98b1b79bf4be662efb338cc/pstack/automations/benny/skills/triage-issue-reports).
  - 추측성 보호 장치 억제: [principle-subtract-before-you-add](https://github.com/cursor/plugins/tree/9e278fe4d4ecd8bfe98b1b79bf4be662efb338cc/pstack/skills/principle-subtract-before-you-add).
- [OpenAI: Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) — 모델 발전에 따른 절차형 지침과 컨텍스트 과잉 재검토.
