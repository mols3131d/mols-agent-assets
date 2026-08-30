---
description: RPI의 prerequisite contract, Review-driven adaptation과 recursive resolution이 하나의 Run에서 어떻게 연결되는지 보존하는 maintainer 문서입니다.
---

# RPI

이 문서는 이 Skill의 고유한 RPI 설계만 기록합니다. Runtime behavior의 canonical source는 `SKILL.md`입니다.

## Prerequisite Contract

RPI의 기본 관계는 **Research → Plan → Implementation → Review**입니다. 이는 모든 단계를 매번 순서대로 실행하는 고정 pipeline이 아니라, downstream state가 의존하는 prerequisite contract입니다.

- Plan은 현재 Goal과 Active Scope를 설명할 수 있는 유효한 Research에 근거합니다.
- Consequential Work는 해당 Work를 실제로 포괄하는 유효한 Plan 뒤에 옵니다.
- Consequential terminal result는 현재 result와 prerequisite state를 검증한 Review 뒤에만 accept합니다.
- 유효한 prerequisite는 재사용합니다. Material change가 생긴 dependency만 stale해지고, 다음 Loop는 **earliest stale prerequisite**부터 다시 시작합니다.
- 뒤늦게 만든 Research나 Plan은 이미 수행한 Work의 사전조건을 소급해 충족시키지 않습니다.

따라서 하나의 Loop는 네 단계를 기계적으로 한 번씩 도는 횟수가 아니라, **현재 상태에서 다시 필요한 가장 이른 prerequisite부터 Review까지 닫히는 substantive attempt**입니다.

## Review-driven Adaptation

RPI의 동적 적응은 Review가 현재 state를 평가한 뒤 다음 transition을 선택하는 데서 발생합니다.

- Evidence가 부족하면 Research를 다시 엽니다.
- Evidence는 충분하지만 Plan coverage가 stale하면 Plan부터 갱신합니다.
- Plan이 여전히 유효하고 bounded Work gap만 남으면 필요한 Work만 수행합니다.
- Scope 변화가 필요하면 Review는 변경을 직접 실행하지 않고 owning control로 넘깁니다. Expansion은 Research와 Plan의 선행 검증을 다시 요구합니다.
- 더 작은 blocker를 분리하는 편이 materially 유리하면 Review에서 strict-subset child Scope로 내려갈 수 있습니다.
- Convergence, saturation 또는 blocker가 확인되면 Loop budget을 채우기 위한 반복을 만들지 않습니다.

이 구조 때문에 RPI는 처음부터 다시 도는 반복문이 아니라 **dependency validity에 따라 시작점과 범위를 바꾸는 adaptive control loop**입니다.

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
- **dependency-aware reuse** — valid state는 재사용하고 stale dependency만 다시 엽니다.
- **Review-driven adaptation** — 다음 Loop의 시작점, Scope 처리와 recursion 여부는 Review 결과에 따라 달라집니다.
- **strict-subset recursion** — child는 parent control boundary를 넓히지 않습니다.
- **shared accounting and reintegration** — parent와 child가 하나의 Run budget을 공유하고 child 결과를 parent state에 재검증해 합칩니다.

이를 고정된 stage repetition, 전체 재작성, 고정 recursion depth 또는 무조건적인 recursive descent로 바꾸지 않습니다.
