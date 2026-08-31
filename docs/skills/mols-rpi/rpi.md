---
description: RPI의 prerequisite contract, Review-driven adaptation, intensity와 recursive resolution이 하나의 Run에서 어떻게 연결되는지 보존하는 maintainer 문서입니다.
---

# RPI

이 문서는 이 Skill의 고유한 RPI 설계만 기록합니다. Runtime behavior의 canonical source는 `SKILL.md`입니다.

## Prerequisite Contract

RPI의 기본 관계는 **Research → Plan → Implementation → Review**입니다. 이는 모든 단계를 매번 순서대로 실행하는 고정 pipeline이 아니라, downstream state가 의존하는 prerequisite contract입니다.

- Plan은 현재 Goal과 Active Scope 안의 material assumptions와 decisions를 뒷받침하는 유효한 Research에 근거합니다.
- Consequential Work는 해당 Work를 실제로 포괄하는 유효한 Plan 뒤에 옵니다.
- `Implementation`은 code-only 구현이 아니라 Plan에 따라 Goal을 전진시키는 하나 이상의 **Work**입니다. Work 자체는 research, planning, review, writing, analysis 같은 domain action일 수 있으며 같은 이름의 RPI stage와는 semantic level이 다릅니다.
- RPI Research나 RPI Plan **stage 자체**가 terminal인 요청과, research·plan·review가 **domain Work**인 요청을 구분합니다.
- 사용자가 특정 RPI stage를 terminal로 지정하지 않고 `루프 진행`, `조사 루프`, `improvement loop`처럼 반복 방법을 요청하면 전체 Goal을 향한 Run으로 해석합니다. 첫 Review는 자동 종료 지점이 아니며, 한 Loop만으로 Goal이 accept된 경우에만 종료할 수 있습니다.
- Consequential terminal result는 현재 result와 prerequisite state를 검증한 Review 뒤에만 accept합니다.
- 유효한 prerequisite는 재사용합니다. Material change가 생긴 dependency만 stale해지고, 다음 Loop는 **earliest stale prerequisite**부터 다시 시작합니다.
- 뒤늦게 만든 Research나 Plan은 이미 수행한 Work의 사전조건을 소급해 충족시키지 않습니다.

따라서 하나의 Loop는 네 단계를 기계적으로 한 번씩 도는 횟수가 아니라, **현재 상태에서 다시 필요한 가장 이른 prerequisite부터 Review까지 닫히는 substantive attempt**입니다.

## Review-driven Adaptation

RPI의 동적 적응은 Review가 현재 state를 평가한 뒤 다음 transition을 선택하는 데서 발생합니다.

- Evidence가 부족하면 Research를 다시 엽니다.
- Evidence는 충분하지만 Plan coverage가 stale하면 Plan부터 갱신합니다.
- Plan이 여전히 유효하고 bounded Work gap만 남으면 필요한 Work만 수행합니다.
- 여러 Work 중 일부만 stale하거나 실패했다면 영향을 받은 Work와 그 earliest stale prerequisite만 다시 엽니다.
- Scope 변화가 필요하면 Review는 변경을 직접 실행하지 않고 owning control로 넘깁니다. Expansion은 Research와 Plan의 선행 검증을 다시 요구합니다.
- 더 작은 blocker를 분리하는 편이 materially 유리하면 Review에서 strict-subset child Scope로 내려갈 수 있습니다.
- Convergence, saturation 또는 blocker가 확인되면 해당 owning concern으로 dispatch하고 Loop budget을 채우기 위한 반복을 만들지 않습니다.
- Material finding이나 acceptance gap을 다음에 볼 과제로 남기면서 현재 Run을 완료로 표시하지 않습니다. Review가 Research, Plan 또는 Work로 dispatch했고 Run을 계속할 수 있으면 같은 Run의 다음 Loop를 실제로 시작합니다.

이 구조 때문에 RPI는 처음부터 다시 도는 반복문이 아니라 **dependency validity에 따라 시작점과 범위를 바꾸는 adaptive control loop**입니다. Review는 transition을 선택·dispatch하지만 Scope 변경, authority 또는 Run termination의 세부 규칙을 대신 소유하지 않습니다.

## Adaptive Intensity

사용자는 `light`, `standard`, `deep` 중 하나로 effort bias를 지정할 수 있습니다. 기본값은 `standard`입니다.

Intensity는 Research 깊이, challenge, validation, alternative exploration과 recursive narrowing의 적극성에 영향을 주지만 고정 절차나 Loop quota가 아닙니다. `deep`도 convergence 뒤의 추가 작업을 강제하지 않고, `light`도 genuine prerequisite나 material validation을 생략하지 않습니다.

## Perspective Control

조사나 Review가 하나의 관점에 고정되면 중요한 전제와 failure mode를 놓칠 수 있습니다. 사용자 요청이나 material risk가 요구할 때는 **decision-relevant question이 다른 최소 관점 집합**을 선택합니다.

- 관점은 persona, source 수, agent 수 또는 vote가 아니라 서로 다른 질문·가정·failure lens입니다.
- 각 관점은 무엇을 확인하는지, 어떤 evidence·authority surface가 맞는지, 결과가 downstream decision이나 acceptance를 어떻게 바꿀 수 있는지 드러냅니다.
- stakeholder, time horizon, system boundary, competing hypothesis, user outcome, regression, safety, operability 같은 축은 후보일 뿐 고정 checklist가 아닙니다.
- 실제 격리된 context나 evidence path가 없다면 independent review라고 부르지 않습니다. 단일 agent의 role-separated sequential pass도 유효하며, multi-agent 실행은 capability가 있고 실익이 있을 때만 사용합니다.
- 관점 결과는 consensus나 다수결로 정하지 않고 evidence quality와 claim relevance로 reconcile합니다.
- 새 관점의 material information gain이 없으면 관점 수를 채우기 위한 pass를 만들지 않습니다.

## Recursive Resolution

Recursion은 adaptive transition의 한 형태이지 별도 실행 체계가 아닙니다.

- Child Scope는 parent Active Scope의 strict subset이어야 합니다.
- Child는 parent의 Goal, authority, safety, acceptance boundary와 Loop budget을 상속하며 넓히거나 reset하지 않습니다.
- Child RPI도 같은 prerequisite contract와 Review gate를 따릅니다.
- Child가 반환한 evidence나 decision은 parent에 자동 적용하지 않습니다. Parent Research, Scope와 Plan에 미치는 영향을 다시 검증한 뒤 필요한 earliest stale prerequisite만 엽니다.
- 더 작은 문제로 분리할 실익이 없으면 recursion을 만들지 않습니다.

## Preserve

이 Skill을 변경할 때 다음 성질을 함께 보존합니다.

- **genuine prerequisites** — Evidence before Plan, Plan before Work, Review before acceptance
- **polymorphic Work** — Implementation은 하나 이상의 domain Work를 실행하며 code-only 또는 single-action으로 제한하지 않습니다.
- **stage/domain separation** — RPI stage terminal과 같은 이름의 domain Work를 혼동하지 않습니다.
- **dependency-aware reuse** — valid state는 재사용하고 stale dependency만 다시 엽니다.
- **Review-driven adaptation** — 다음 Loop의 시작점, Scope 처리와 recursion 여부는 Review 결과에 따라 달라집니다.
- **Goal-directed loop intent** — 특정 RPI stage terminal이 없으면 loop-method 요청은 첫 pass가 아니라 Goal acceptance까지 이어지는 Run입니다.
- **evidence-led perspectives** — 필요한 Research와 Review는 materially distinct lens를 사용하되 persona·vote·고정 관점 수로 대체하지 않습니다.
- **adaptive intensity** — 3단계 intensity는 effort를 bias하지만 quality waiver, fixed procedure나 Loop quota가 아닙니다.
- **strict-subset recursion** — child는 parent control boundary를 넓히지 않습니다.
- **shared accounting and reintegration** — parent와 child가 하나의 Run budget을 공유하고 child 결과를 parent state에 재검증해 합칩니다.

이를 고정된 stage repetition, 전체 재작성, code-only Implementation, single-action Work, stage-terminal confusion, intensity별 고정 절차, 고정 recursion depth 또는 무조건적인 recursive descent로 바꾸지 않습니다.
