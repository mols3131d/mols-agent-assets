# Rule Validate

Rule과 scoped instruction 검증에만 필요한 근거와 claim을 다룬다. 공통 검증 원칙은 `../common/validate.md`를 따른다.

- source ownership, selector, scope, inheritance, precedence, attachment를 직접 확인한다.
- project 또는 source framework가 제공하는 deterministic Rule check를 재사용한다.
- projection correctness가 대상이면 generated target representation을 확인한다.
- 적용 범위를 바꾸는 변경이면 before/after target coverage를 비교한다.
- runtime relevance, dynamic precedence, target compatibility를 주장하려면 실제 runtime evidence를 사용한다.

Structurally valid Rule이라고 해서 semantic placement가 올바르다는 뜻은 아니다. Static inspection은 declarative structure를 검증할 수 있지만 host가 동적으로 결정하는 relevance까지 증명하지는 않는다.
