---
description: RPI의 Implementation을 goal-directed Work로 해석하고, Work가 하나 이상의 다양한 domain action으로 구성될 수 있다는 핵심 설계를 보존하는 maintainer 문서입니다.
---

# RPI Work

RPI의 `I`는 **Implementation**이지만, 이 Skill에서 그 의미는 코드 구현에 한정되지 않는 **goal-directed Work**입니다. Runtime behavior의 canonical source는 `SKILL.md`입니다.

## Work

Work는 accepted Plan에 따라 현재 Goal을 실제로 전진시키는 실행 단계입니다.

가능한 Work에는 코드 구현뿐 아니라 다음과 같은 행위가 포함될 수 있습니다.

- 문서 작성·편집
- 조사와 분석
- 계획 수립
- 리뷰와 평가
- 의사결정
- 설정 변경이나 tool action
- 그 밖에 Goal이 요구하는 결과 생성

즉 **Implementation은 실행의 역할을 뜻하며 결과의 종류를 제한하지 않습니다.**

Work는 하나일 필요가 없습니다. 하나의 Plan은 Goal을 위해 **하나 이상의 Work unit**을 순차적·병렬적·의존적으로 묶을 수 있으며, RPI Work는 현재 Plan이 요구하는 필요한 집합을 수행합니다. Review는 각 Work뿐 아니라 Work 사이의 dependency와 조합 결과가 Plan과 Goal을 충족하는지도 확인합니다.

## Prerequisite

Consequential Work는 다음이 유효할 때 수행합니다.

- 현재 Goal과 Active Scope
- 필요한 material premise를 뒷받침하는 Research
- 수행할 Work를 실제로 포괄하는 accepted Plan
- 해당 행동에 필요한 별도의 authority와 safety gate

Plan은 methodological coverage를 제공할 뿐 operational permission을 만들지 않습니다.

Work 중 material new assumption, approach 또는 Scope gap이 생기면 그대로 진행하지 않고 Review로 넘깁니다. Review가 dependency를 다시 판단해 Research, Plan 또는 bounded Work 중 필요한 가장 이른 지점으로 dispatch합니다.

## Two Semantic Levels

RPI stage와 Work의 domain action은 서로 다른 semantic level입니다.

- **RPI Research** — Work와 downstream 판단에 필요한 prerequisite evidence를 만든다.
- **RPI Plan** — Work를 수행할 방법과 coverage를 만든다.
- **RPI Work** — 사용자가 실제로 요구한 하나 이상의 domain action을 수행한다.
- **RPI Review** — Work 결과와 prerequisite lineage가 충분한지 검증하고 다음 transition을 결정한다.

따라서 Work 자체가 `research`, `plan`, `review`여도 해당 RPI stage와 자동으로 같은 것이 되지 않습니다. 반대로 사용자가 **RPI Research 단계 자체**나 **RPI Plan 단계 자체**를 terminal로 명시한 경우에는 그 stage를 domain Work로 다시 수행하지 않습니다.

예를 들어 요청된 Work가 **review**라면:

1. RPI Research가 리뷰에 필요한 대상·근거·기준을 확보합니다.
2. RPI Plan이 리뷰 범위와 검증 방법을 정합니다.
3. RPI Work가 실제 리뷰를 수행합니다.
4. RPI Review가 **그 리뷰가 충분하고 근거 있으며 Goal을 충족했는지 다시 검증**합니다.

Work가 research나 plan인 경우도 같습니다. Outer RPI는 그 domain Work가 제대로 준비되고 수행되고 검증되도록 orchestration contract를 유지합니다.

## Adaptation and Reuse

이 구분이 같은 활동을 반드시 두 번 하라는 뜻은 아닙니다.

- 기존 evidence나 artifact가 두 역할의 요구를 모두 충족하면 재사용합니다.
- 이름이 같다는 이유만으로 prerequisite stage와 domain Work를 합치지 않습니다.
- 반대로 역할이 실질적으로 겹친다는 이유로 의식적인 중복을 만들지도 않습니다.
- 여러 Work 중 일부만 stale하거나 실패했다면 전체를 다시 수행하지 않고 영향을 받은 Work와 earliest stale prerequisite만 다시 엽니다.

목표는 stage ceremony가 아니라 **역할과 dependency를 보존하면서 중복을 최소화하는 것**입니다.

## Preserve

Work를 고도화할 때 다음을 보존합니다.

- **implementation-as-work** — `I`는 code implementation이 아니라 Goal을 실행하는 Work입니다.
- **domain polymorphism** — research, plan, review를 포함한 다양한 domain action이 Work가 될 수 있습니다.
- **one-or-many Work** — Work는 단일 행위에 한정되지 않으며 Plan이 요구하는 여러 Work unit과 dependency를 포함할 수 있습니다.
- **semantic-level separation** — RPI orchestration stage와 같은 이름의 domain Work를 혼동하지 않습니다.
- **stage-terminal distinction** — RPI stage 자체가 terminal인 요청과 같은 이름의 domain Work를 구분합니다.
- **Plan-before-Work** — consequential Work에는 실제 coverage를 가진 Plan이 선행합니다.
- **Review-of-the-work** — Work가 review여도 outer RPI Review는 그 review 결과의 충분성과 신뢰성을 검증합니다.
- **reuse without collapse** — 유효한 artifact와 Work 결과는 재사용하되 역할 차이를 없애거나 ceremony를 만들지 않습니다.

이를 code-only Implementation, single-action assumption, stage-name collision, stage-terminal confusion, 무조건적인 중복 실행 또는 Work가 스스로 acceptance를 선언하는 구조로 바꾸지 않습니다.
