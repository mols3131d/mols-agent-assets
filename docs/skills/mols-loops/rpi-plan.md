---
description: Adaptive recursive RPI에서 Plan의 prerequisite, coverage, delta replanning과 downstream Work transition을 보존하는 maintainer 문서입니다.
---

# RPI Plan

RPI의 Plan은 한 번 만들고 끝나는 문서가 아니라 **현재 Research와 Active Scope를 다음 Work로 연결하는 revisable control artifact**입니다. Runtime behavior의 canonical source는 `SKILL.md`입니다.

## Prerequisite

Consequential Plan은 다음 prerequisite가 유효할 때만 성립합니다.

- 현재 Goal과 Active Scope
- Plan의 material assumptions와 decisions를 뒷받침하는 Research
- Scope expansion이 포함된다면 그 필요와 boundary를 검증한 선행 Research

사용자가 Plan을 제공했더라도 자동으로 accepted prerequisite로 보지 않습니다. Material assumption을 기존 Research로 검증하거나 필요한 최소 Research를 먼저 수행합니다.

## Coverage

Plan은 현재 Scope 안에서 **어떤 state change를 어떤 Work로 만들며 무엇으로 accept할지**를 충분히 설명해야 합니다. Work는 하나 이상의 unit일 수 있고, dependency가 실제로 중요할 때 ordering이나 concurrency를 함께 드러냅니다. 그러나 세부 절차를 과잉 고정하는 것이 목적은 아닙니다.

- Work가 실제로 의존하는 decision과 dependency를 포함합니다.
- 필요한 경우 Work unit의 ordering이나 safe concurrency를 포함합니다.
- Acceptance와 validation 방법, material condition이 충족되지 않을 때 Review가 되돌릴 dependency를 포함합니다.
- 바뀌면 replanning이 필요한 material assumption을 드러냅니다.
- Operational permission이나 authority를 Plan 자체가 부여한다고 취급하지 않습니다.

이미 유효한 Plan coverage가 있으면 재사용합니다.

## Adaptive Replanning

Plan은 Review와 upstream state 변화에 따라 필요한 부분만 갱신합니다.

- Research가 바뀌어 기존 decision을 더 이상 지지하지 않으면 affected Plan부터 stale합니다.
- Scope가 좁아지면 남은 Goal과 acceptance를 보존하면서 불필요한 Work를 제거하고 coverage를 다시 확인합니다.
- Scope expansion이 필요하면 Review의 proposal만으로 Plan을 넓히지 않습니다. Research가 need와 boundary를 먼저 검증한 뒤 smallest justified delta만 Plan에 반영합니다.
- 여러 Work 중 일부만 stale하면 dependency가 영향을 받지 않은 valid Work까지 다시 계획하지 않습니다.
- Review가 bounded Work gap만 찾고 Plan coverage가 여전히 유효하다면 Plan을 다시 만들지 않고 Work로 바로 돌아갈 수 있습니다.

즉, replanning의 단위는 전체 문서가 아니라 **invalidated dependency가 영향을 준 최소 Plan delta**입니다.

## Exit and Reopening

Plan은 현재 Goal과 Scope에 필요한 Work를 안전하게 시작할 만큼 coverage가 유효할 때 downstream Work로 넘어갑니다. RPI Plan stage 자체가 requested terminal이면 Main RPI Review가 Plan과 그 Research lineage를 검증해 candidate exit를 만들고 Finalize Gate가 accept 여부를 결정합니다. Domain Work가 planning인 경우와는 구분합니다.

Implementation 중 material new assumption, approach 또는 Scope gap이 나타나면 Work를 계속 밀어붙이지 않습니다. Review가 gap을 reconcile한 뒤 Research 또는 Plan 중 earliest stale prerequisite를 다시 엽니다.

## Recursive Interaction

Child Scope는 parent의 strict subset 안에서 그 blocker를 해결하는 데 필요한 좁은 Plan만 가집니다. Child 결과가 돌아오면 parent는 다음을 다시 확인합니다.

- parent Research premise가 여전히 유효한가
- parent Scope에 영향이 있는가
- parent Plan decision이나 coverage가 stale해졌는가

Child Plan이나 결과는 parent Plan을 자동으로 덮어쓰지 않습니다.

## Preserve

Plan을 고도화할 때 다음을 보존합니다.

- **Research-before-Plan** — consequential Plan에는 유효한 evidence lineage가 필요합니다.
- **coverage-before-Work** — consequential Work는 해당 Work를 실제로 포괄하는 Plan 뒤에 옵니다.
- **one-or-many Work coverage** — 필요한 Work unit과 material dependency를 표현하되 single-action으로 제한하지 않습니다.
- **delta replanning** — upstream 변화가 영향을 준 최소 부분만 다시 계획합니다.
- **Scope-aware planning** — narrowing과 validated expansion에 맞춰 coverage를 재검증합니다.
- **child-to-parent reintegration** — child 결과가 parent dependency를 stale하게 만드는지 다시 판단합니다.

이를 one-shot 계획, 전체 재작성, single-action planning, speculative expansion 또는 ceremony를 위한 replanning으로 바꾸지 않습니다.
