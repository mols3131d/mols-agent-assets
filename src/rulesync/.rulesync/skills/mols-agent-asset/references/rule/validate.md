# Rule Validate

Rule Validation은 선언된 구조와 intended application contract가 제대로 표현되어 있는지 확인한다. 실제 host application과 behavior 성능은 Eval이 소유한다. 공통 원칙은 `../common/validate.md`를 따른다.

## Deterministic validation

- source ownership, selector, scope, inheritance, precedence, attachment, local delta의 machine-checkable contract를 확인한다.
- project 또는 source framework의 deterministic Rule check가 있으면 재사용한다.
- projection이 검증 대상이면 canonical source와 generated target representation의 drift를 확인한다.
- 적용 범위를 바꾸는 변경에서 대상 집합을 결정론적으로 계산할 수 있으면 before/after coverage를 비교한다.

## Semantic validation

- declared scope와 intended application이 일치하는지 본다.
- requirement, authority, exception, placement가 의도한 책임 경계를 표현하는지 확인한다.
- 여러 layer가 겹치면 실제로 선언된 merge/override/precedence만 기준으로 삼고 universal precedence를 가정하지 않는다.
- semantic relevance가 필요한 요구를 structural selector만으로 흉내 내거나, 항상 필요한 invariant를 optional routing 뒤에 숨기지 않았는지 확인한다.

Structurally valid Rule이 곧 올바르게 적용되는 Rule이라는 뜻은 아니다. Host가 실제 target에 적용하는지와 dynamic routing은 Routing Eval, 적용 이후 behavior는 Behavior Eval로 확인한다.
