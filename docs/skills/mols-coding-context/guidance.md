---
description: mols-coding-context의 설계 의도, 지침 채택·제거 기준과 routing 평가를 검토할 때 사용합니다.
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

[저장소 평가 정책](../../development/evaluation.md)에 따라 이 Skill의 자동 Eval은 description 기반 routing에 한정한다. [공통 fixture](../../../evals/skills/mols-coding-context/cases.json)는 Core와 Python add-on의 선택 집합을 함께 검증한다. 일상 코딩의 선택, 비코딩의 비선택, Python 고유 판단이 필요한 작업의 동반 선택, 부수적 Python 언급의 비선택을 확인한다.

```bash
mise run eval -c evals/promptfoo/mols-coding-context.yaml
```

기존 evaluator의 primary_skill 필드에는 Core를 기본 컨텍스트로 지정한다. Python add-on은 이를 보강하며, 이 값은 실제 로딩 순서나 실행 소유권을 뜻하지 않는다. Python 후보 description은 변경 시 fixture에서 갱신한다.

Routing Eval은 실제 런타임의 로딩 횟수·재사용, 판단 품질, 결과물 개선 또는 비용 절감을 검증하지 않는다. 본문 변경은 정적 리뷰와 실제 사용에서 관찰한 오류·결과를 근거로 판단하며, 응답 기반 Behavior Eval이나 별도 평가 프레임워크를 추가하지 않는다.

## References

- [기존 설계 및 마이그레이션](https://github.com/mols3131d/mols-agent-assets/pull/222)
- [pstack (Lauren Tan)](https://github.com/cursor/plugins/tree/9e278fe4d4ecd8bfe98b1b79bf4be662efb338cc/pstack) — domain modeling, premise checking, shared state, contract-oriented testing, failure boundaries, reader load, measurement. [MIT license](https://github.com/cursor/plugins/blob/9e278fe4d4ecd8bfe98b1b79bf4be662efb338cc/pstack/LICENSE).
  - 피드백의 증거와 도달 가능성 판단: [interrogate](https://github.com/cursor/plugins/tree/9e278fe4d4ecd8bfe98b1b79bf4be662efb338cc/pstack/skills/interrogate), [blast-radius](https://github.com/cursor/plugins/tree/9e278fe4d4ecd8bfe98b1b79bf4be662efb338cc/pstack/skills/blast-radius), [triage-issue-reports](https://github.com/cursor/plugins/tree/9e278fe4d4ecd8bfe98b1b79bf4be662efb338cc/pstack/automations/benny/skills/triage-issue-reports).
  - 추측성 보호 장치 억제: [principle-subtract-before-you-add](https://github.com/cursor/plugins/tree/9e278fe4d4ecd8bfe98b1b79bf4be662efb338cc/pstack/skills/principle-subtract-before-you-add).
- [OpenAI: Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) — 모델 발전에 따른 절차형 지침과 컨텍스트 과잉 재검토.
