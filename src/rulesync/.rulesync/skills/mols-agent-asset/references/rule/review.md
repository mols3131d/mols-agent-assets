# Rule Review

Rule과 scoped instruction review에만 필요한 축을 다룬다. 공통 review 기준은 `../common/review.md`를 따른다.

- **Application** — intended target에 도달하고 unrelated target에는 새지 않는가?
- **Requirement** — policy 의미와 genuine exception, narrower variant가 보존되는가?
- **Authority** — runtime이 허용하는 범위에서 semantic requirement의 editable owner가 하나인가?
- **Placement** — 올바른 scope에 필요한 만큼만 context를 사용해 배치됐는가?
- **Selector / precedence** — selector, inheritance, attachment, precedence 관계가 intended behavior를 보존하는가?
- **Duplication** — 남은 copy가 projection이나 scope 때문에 필요한가, 아니면 competing semantic owner인가?
- **Projection** — generated copy를 derived로 취급하고 있는가?
- **Portability** — target-specific assumption을 다른 runtime에 일반화하지 않았는가?
- **Regression** — nearby non-target coverage, exception behavior, effective precedence를 바꾸지 않았는가?

Materially ambiguous한 candidate는 추측으로 합치거나 이동하지 않는다.
