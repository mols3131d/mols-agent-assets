# Executable Verification Surface

Status: **strong candidate**

## Idea

Change를 수행한 사람이나 agent가 결과가 맞는지 **직접 관찰하고 판정할 수 있는 verification surface**를 갖추는 것을 고려합니다.

핵심은 test count를 늘리는 것이 아니라, 중요한 behavior와 failure를 실제로 구분할 수 있는 feedback loop를 제공하는 것입니다.

## Why It May Be a Pattern

Coding agent의 autonomy는 구현 능력뿐 아니라 결과를 스스로 평가할 수 있는지에 크게 좌우됩니다. Human developer에게도 빠르고 신뢰할 수 있는 feedback surface는 같은 이점을 줍니다.

Verification surface는 다음처럼 다양할 수 있습니다.

- unit / integration / end-to-end test
- contract test
- reference implementation과의 비교
- property / invariant check
- schema validation
- API smoke test
- running application interaction
- screenshot / video / visual comparison
- logs, metrics, traces
- benchmark나 explicit performance budget

중요한 것은 tool 종류가 아니라 **의도한 behavior가 성립했는지를 충분히 구분하는 observable signal**이 있는지입니다.

## Good Verification Surfaces

다음 성질이 있으면 유용성이 높아질 수 있습니다.

- 작업자가 반복 실행할 수 있습니다.
- pass/fail 또는 품질 차이를 비교적 명확히 해석할 수 있습니다.
- 실제 중요한 behavior와 가깝습니다.
- regression을 발견하는 데 도움이 됩니다.
- failure가 발생했을 때 다음 행동을 정할 수 있을 만큼 정보가 있습니다.
- 가능한 경우 implementation과 독립적인 oracle 또는 acceptance criterion을 사용합니다.

## Possible Responses

Agent나 사람이 “완료 여부를 판단하기 어렵다”고 반복해서 겪는다면 다음을 비교합니다.

- 가장 중요한 behavior 하나를 재현 가능한 test나 scenario로 표현합니다.
- 기존 production signal이 충분하다면 별도 test를 만들기보다 그 signal을 읽기 쉽게 노출합니다.
- reference implementation이나 known-good fixture가 있다면 oracle로 활용할 수 있는지 봅니다.
- UI라면 DOM assertion만으로 부족한지 실제 interaction이나 visual evidence가 필요한지 봅니다.
- failure diagnosis가 어렵다면 test 자체를 늘리기 전에 error output, logs, trace를 개선할 수 있습니다.

## Oracle Quality

Verification surface가 있다는 사실만으로 correctness가 보장되지는 않습니다. Agent는 특히 **측정되는 것**에 강하게 최적화할 수 있으므로 oracle이 좁으면 green result가 실제 요구사항을 놓칠 수 있습니다.

따라서 중요한 영역에서는 다음을 고려할 수 있습니다.

- acceptance criterion이 실제 user-visible behavior와 연결되는지 봅니다.
- 서로 다른 종류의 signal이 같은 결론을 지지하는지 확인합니다.
- test fixture가 implementation detail을 그대로 복제해 false confidence를 만들지 않는지 봅니다.
- 중요한 blind spot이 알려져 있다면 limitation으로 남깁니다.

## Limits

- 모든 behavior를 자동화된 oracle로 만들 수는 없습니다.
- subjective quality나 exploratory product judgment는 human evaluation이 더 적합할 수 있습니다.
- high-fidelity e2e surface는 느리고 flaky할 수 있습니다.
- 너무 많은 verification step은 feedback loop 자체를 느리게 만들 수 있습니다.
- test가 implementation과 지나치게 결합되면 refactoring cost가 커질 수 있습니다.

따라서 가능한 verification을 무조건 추가하기보다 **중요한 uncertainty를 가장 싼 신뢰 가능한 signal로 줄이는 것**을 우선합니다.

## Relationship to Existing Patterns

`Source-Mirrored Test Structure`가 test의 filesystem navigation을 다룬다면, 이 후보는 test를 포함한 verification mechanism이 실제로 **판정 가능한 feedback loop를 제공하는가**를 다룹니다.

## Promotion Questions

- 일반적인 `testability` 원칙을 넘어 agentic development에서 독립 pattern으로 유용한가?
- test, observability, visual validation을 너무 넓게 묶고 있지는 않은가?
- `oracle quality`를 pattern의 중요한 limitation으로 충분히 설명할 수 있는가?
- CI workflow가 아니라 software design pattern으로 남길 core가 분명한가?

## Research Notes

- Anthropic의 long-running scientific computing 사례는 autonomous progress에 reference implementation, quantifiable objective 또는 test suite 같은 test oracle이 중요하다고 설명합니다.
- Anthropic의 long-running application harness는 evaluator가 running application을 직접 exercise하고 testable behavior를 기준으로 feedback을 제공하는 구조를 사용합니다.
- OpenAI의 agent-first repository 경험도 test, application interaction, logs, metrics, traces를 agent가 직접 읽을 수 있는 feedback surface로 확장하는 방향을 보여줍니다.
