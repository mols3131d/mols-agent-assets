# Rule Review

Rule과 scoped instruction review에만 필요한 축을 다룬다. 공통 review 기준은 `../common/review.md`를 따른다.

- **Fit** — applicability가 structural scope 또는 explicit Rule mechanism으로 자연스럽게 표현되는가? semantic relevance를 복잡한 selector로 흉내 내고 있지 않은가?
- **Application** — intended target에 도달하고 unrelated target에는 새지 않는가? 항상 적용되어야 하는 requirement가 optional route에 의존하지 않는가?
- **Requirement** — policy 의미와 genuine exception, narrower variant가 보존되는가?
- **Authority** — runtime이 허용하는 범위에서 semantic requirement의 editable owner가 하나인가?
- **Placement** — 올바른 scope에 필요한 만큼만 context를 사용해 배치됐는가?
- **Layering** — nested scope나 override가 실제 applicability/local delta를 표현하는가, 아니면 같은 requirement를 여러 layer가 중복 소유하는가?
- **Selector / precedence** — selector, inheritance, attachment, precedence 관계가 intended behavior를 보존하면서 필요 이상으로 복잡하지 않은가?
- **Duplication** — 남은 copy가 projection이나 scope 때문에 필요한가, 아니면 competing semantic owner인가?
- **Projection** — generated copy를 derived로 취급하고 source와의 drift를 사람이 수동으로 관리하지 않는가?
- **Granularity** — Rule surface마다 독립 scope나 ownership 가치가 있는가? 거의 항상 함께 적용되는 layer가 과도하게 분리되지 않았는가?
- **Portability** — target-specific assumption을 다른 runtime에 일반화하지 않았는가?
- **Structure** — file/directory placement가 탐색을 돕되 application이나 framework convention을 왜곡하지 않는가?
- **Regression** — nearby non-target coverage, exception behavior, effective precedence를 바꾸지 않았는가?

Materially ambiguous한 candidate는 추측으로 합치거나 이동하지 않는다. Physical repetition만으로 duplicate-authority finding을 만들지 않는다.
