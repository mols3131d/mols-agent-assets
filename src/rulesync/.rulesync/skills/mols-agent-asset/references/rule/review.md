# Rule Review

Rule 리뷰는 application, authority, placement가 실제 범위를 보존하는지 확인한다. 공통 기준은 `../common/review.md`를 따른다.

## Review axes

- **Fit** — applicability가 structural scope나 explicit Rule mechanism으로 자연스럽게 표현되는가?
- **Application** — intended target에 도달하고 unrelated target에는 새지 않는가?
- **Requirement** — policy 의미와 genuine exception, narrower variant가 보존되는가?
- **Authority** — 가능한 범위에서 semantic requirement의 editable owner가 하나인가?
- **Placement** — 올바른 scope에 필요한 만큼의 context로 배치됐는가?
- **Layering** — nested scope나 override가 실제 applicability/local delta를 표현하는가?
- **Selector / precedence** — selector, inheritance, attachment, precedence가 intended behavior를 보존하면서 필요 이상으로 복잡하지 않은가?
- **Duplication / projection** — 남은 copy가 scope/projection 때문에 필요한가? Generated copy를 derived로 취급하는가?
- **Granularity** — Rule surface마다 독립 scope나 ownership 가치가 있는가?
- **Portability** — target-specific assumption을 다른 runtime에 일반화하지 않았는가?
- **Regression** — nearby non-target coverage, exception behavior, effective precedence를 바꾸지 않았는가?

Materially ambiguous한 candidate는 추측으로 합치거나 이동하지 않는다. Physical repetition만으로 duplicate-authority finding을 만들지 않는다.
