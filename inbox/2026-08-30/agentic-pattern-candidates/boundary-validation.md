# Boundary Validation

Status: **exploratory candidate**

## Idea

외부에서 들어오는 불확실한 data shape나 protocol을 내부 code가 신뢰 가능한 형태로 사용하기 전에 **명시적인 boundary에서 확인·변환하는 방식**을 고려할 수 있습니다.

핵심은 특정 validation library를 사용하는 것이 아니라, guessed shape나 loosely-typed data가 내부 깊숙한 곳까지 퍼져 여러 위치에서 방어 코드를 반복하게 되는 문제를 줄이는 것입니다.

## Typical Boundaries

- external API response
- user input
- message / event payload
- configuration
- database row 또는 migration boundary
- filesystem / network input
- generated or third-party SDK와 internal domain model 사이

## Typical Signals

- 여러 call site에서 같은 `if field exists` 방어가 반복됩니다.
- 외부 API shape를 문서나 기억만으로 추측해 사용합니다.
- invalid state가 business logic 내부 깊숙한 곳에서 뒤늦게 발견됩니다.
- optional/unknown field handling 때문에 domain code가 계속 복잡해집니다.
- external dependency change가 unrelated internal modules까지 넓게 전파됩니다.

## Possible Responses

- boundary에서 parse/validate한 뒤 내부에서는 더 안정적인 representation을 사용합니다.
- provider가 reliable typed SDK나 generated client를 제공한다면 별도 wrapper보다 그것을 우선할 수 있습니다.
- validation과 domain normalization을 구분해야 한다면 가장 작은 필요한 변환만 둡니다.
- invalid input에 대한 failure mode와 observability가 중요한 경우 명시적인 error surface를 둡니다.
- schema가 매우 안정적이고 language/type system이 이미 충분히 보장한다면 추가 runtime validation이 실제로 필요한지 비교합니다.

## Limits

- 모든 internal function boundary에서 validation을 반복하면 noise와 runtime cost가 커집니다.
- schema wrapper가 provider SDK를 그대로 복제하면 drift source가 하나 더 생깁니다.
- validation이 지나치게 엄격하면 forward compatibility를 해칠 수 있습니다.
- dynamic data나 partially-known payload에서는 완전한 normalization이 현실적이지 않을 수 있습니다.
- security validation, business rule validation, parsing을 하나의 개념으로 섞으면 책임이 불분명해질 수 있습니다.

따라서 이 후보는 **validate everywhere**가 아니라 **trust boundary를 분명히 하고 uncertainty를 가능한 한 그 경계에서 처리하는 것**에 가깝습니다.

## Relationship to Other Candidates

Repository에서 boundary validation이 안정적인 architecture invariant라면 `Executable Architecture Invariants`의 대표 사례가 될 수 있습니다. 이 때문에 독립 pattern보다 해당 문서의 example/consideration으로 흡수하는 편이 더 KISS할 가능성도 큽니다.

`Local-Reasoning Structure` 관점에서는 external uncertainty를 boundary에서 좁히면 downstream code가 더 작은 context로 추론하기 쉬워질 수 있습니다.

## Promotion Questions

- 독립 pattern으로 둘 만큼 responsibility가 분명한가, 아니면 architecture invariant의 한 사례인가?
- parsing, validation, normalization, domain invariant의 경계를 어떻게 설명해야 과도하게 넓어지지 않는가?
- typed language와 dynamic language 모두에서 유효하게 설명할 수 있는가?
- security input validation과 혼동되지 않도록 boundary를 충분히 좁힐 수 있는가?

## Research Notes

- OpenAI의 agent-first repository 사례는 agents가 guessed data shape에 기대지 않도록 boundary에서 data shape를 parse하거나 typed SDK에 의존하는 것을 golden principle의 한 사례로 설명합니다.
