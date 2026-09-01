# Rule Validate

Rule과 scoped instruction 검증에만 필요한 근거와 claim을 다룬다. 공통 검증 원칙은 `../common/validate.md`를 따른다.

## Structural evidence

- source ownership, selector, scope, inheritance, precedence, attachment와 declared local delta를 직접 확인한다.
- project 또는 source framework가 제공하는 deterministic Rule check를 재사용한다.
- projection correctness가 대상이면 canonical source에서 generated target representation을 다시 만들거나 동일한 generator contract로 drift를 확인한다.
- 적용 범위를 바꾸는 변경이면 before/after target coverage를 비교한다. 가능하면 path, selector, scope처럼 관찰 가능한 대상 집합으로 확인한다.
- 여러 layer가 겹치면 실제로 claim하는 merge/override/precedence 관계만 검증하고 존재하지 않는 universal precedence를 가정하지 않는다.

## Behavioral evidence

- structurally scoped Rule은 intended structural target에 적용되는지를 실제 host projection 또는 runtime evidence로 강화할 수 있다.
- runtime relevance, dynamic precedence, conditional attachment, target compatibility를 주장하려면 실제 runtime evidence를 사용한다.
- semantic relevance를 host/model이 동적으로 판단하는 surface라면 selector text inspection만으로 application quality를 증명하지 않는다.

Structurally valid Rule이라고 해서 semantic placement가 올바르다는 뜻은 아니다. Generated projection이 source와 일치해도 host의 runtime application이나 precedence behavior까지 증명하지 않는다. Static inspection은 declarative structure와 예상 coverage를 검증할 수 있지만 dynamic relevance는 별도 evidence가 필요하다.
