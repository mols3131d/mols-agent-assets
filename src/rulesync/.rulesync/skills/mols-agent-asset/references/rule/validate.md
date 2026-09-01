# Rule Validate

Rule 검증은 선언된 scope와 실제 runtime application을 구분한다. 공통 원칙은 `../common/validate.md`를 따른다.

## Structural evidence

- source ownership, selector, scope, inheritance, precedence, attachment, local delta를 확인한다.
- project 또는 source framework의 deterministic Rule check가 있으면 재사용한다.
- projection이 검증 대상이면 canonical source와 generated target representation의 drift를 확인한다.
- 적용 범위를 바꾸는 변경은 before/after target coverage를 비교한다.
- 여러 layer가 겹치면 실제로 선언된 merge/override/precedence만 검증하고 universal precedence를 가정하지 않는다.

## Runtime evidence

- structural scope가 실제 host에서 intended target에 적용되는지는 projection 또는 runtime evidence로 강화한다.
- runtime relevance, dynamic precedence, conditional attachment, target compatibility를 주장하려면 actual runtime evidence가 필요하다.
- semantic relevance를 host/model이 동적으로 판단한다면 selector text만으로 application quality를 증명하지 않는다.

Structurally valid Rule이 곧 올바르게 배치된 Rule이라는 뜻은 아니다. Generated projection이 source와 일치해도 runtime application이나 precedence behavior를 증명하지 않는다.
