# Executable Architecture Invariants

Status: **strong candidate**

## Idea

Repository에서 정말 중요한 architecture constraint가 있다면, 가능한 경우 문서에만 의존하지 않고 **가장 싼 신뢰 가능한 mechanism으로 위반을 확인할 수 있게 하는 것**을 고려합니다.

핵심은 implementation style을 세세하게 강제하는 것이 아니라, 깨지면 구조적 비용이 큰 invariant를 식별하고 그 invariant만 executable하게 만드는 것입니다.

## Why It May Be a Pattern

Human과 coding agent 모두 기존 code의 local pattern을 따라가며 변경하는 경향이 있습니다. Repository에 잘못된 dependency나 예외가 누적되면 이후 작업이 그것을 다시 복제할 수 있습니다.

따라서 다음과 같은 constraint는 설명만 하는 것보다 mechanical feedback이 더 적합할 수 있습니다.

- 특정 layer에서 역방향 dependency를 금지합니다.
- domain boundary를 넘어 internal implementation에 직접 접근하지 않습니다.
- generated 영역을 source처럼 직접 수정하지 않습니다.
- schema나 boundary data는 정해진 validation surface를 통과합니다.
- 특정 reliability/security invariant가 항상 성립해야 합니다.

## Possible Enforcement Surfaces

Invariant의 성격과 ecosystem에 따라 다음 중 가장 단순한 수단을 선택할 수 있습니다.

- language/module system
- compiler 또는 type checker
- package visibility
- static analysis / linter
- dependency graph check
- architecture test / structural test
- schema validation
- CI check

더 낮은 계층에서 자연스럽게 보장되는 invariant를 굳이 custom CI script로 다시 만들 필요는 없습니다.

## Choosing What to Enforce

다음 성질이 강할수록 executable invariant 후보가 될 수 있습니다.

- 위반 여부를 비교적 객관적으로 판정할 수 있습니다.
- 위반이 반복될 가능성이 있습니다.
- 위반 후 발견 비용이나 복구 비용이 큽니다.
- project의 architecture나 reliability에서 오래 유지될 핵심 경계입니다.
- 사람이 review할 때 매번 같은 판단을 반복하고 있습니다.

반대로 taste, readability, context-dependent design judgment처럼 기계적으로 판정하기 어려운 항목은 억지 rule로 만들지 않는 편이 나을 수 있습니다.

## Responses to Drift

문서에 반복해서 같은 architecture warning이 추가되고 있다면, 먼저 그 warning이 정말 invariant인지 확인합니다. 그렇다면 다음을 비교할 수 있습니다.

1. 기존 language/framework mechanism으로 표현할 수 있는지 봅니다.
2. dependency 또는 structural test처럼 좁은 check로 충분한지 봅니다.
3. custom enforcement의 유지보수 비용이 실제 drift 비용보다 작은지 비교합니다.
4. enforcement가 implementation choice까지 불필요하게 제한하지 않는지 확인합니다.

## Limits

- 모든 design preference를 executable rule로 만들면 architecture가 경직되고 accidental complexity가 늘 수 있습니다.
- custom lint가 너무 많으면 rule ownership과 failure interpretation이 어려워질 수 있습니다.
- model이나 team이 쉽게 고칠 수 있다는 이유만으로 low-value rule을 계속 추가하면 CI noise가 커집니다.
- architecture가 아직 탐색 단계라면 invariant를 너무 일찍 고정하는 것이 오히려 학습을 방해할 수 있습니다.

따라서 이 후보의 핵심은 **enforce everything**이 아니라 **stable and costly-to-break invariant를 가장 단순한 신뢰 가능한 mechanism으로 보호하는 것**에 가깝습니다.

## Relationship to Existing Patterns

`Filesystem-Legible Structure`에서 filesystem cue가 architecture contract의 증거가 아니라고 설명하는 지점과 연결될 수 있습니다. 이 후보는 실제 contract가 필요할 때 어떤 형태로 enforce할지를 더 직접적으로 다룹니다.

## Promotion Questions

- architecture test, lint, type system을 하나의 pattern으로 묶을 만큼 공통 core가 분명한가?
- `testing`이나 `CI policy` 문서와 ownership 충돌 없이 reusable pattern으로 설명할 수 있는가?
- invariant와 preference를 구분하는 좋은 heuristic을 더 정교하게 만들 수 있는가?
- 과도한 enforcement의 한계와 완화책이 충분히 설명되는가?

## Research Notes

- OpenAI의 agent-first repository 사례는 architecture dependency direction과 일부 structural/taste invariant를 custom lint와 structural test로 기계적으로 검증하면서, implementation 자체는 micromanage하지 않는 방향을 설명합니다.
