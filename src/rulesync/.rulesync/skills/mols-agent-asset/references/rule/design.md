# Rule Design

Rule과 scoped instruction 설계에만 필요한 판단을 다룬다. 공통 설계 원칙은 `../common/design.md`를 따른다.

## Application → Requirement → Authority → Placement

반복되거나 겹치는 지침은 다음 순서로 판단한다.

1. **Application** — 각 후보가 현재 어디에 적용되고 어디에 적용되어야 하는가?
1. **Requirement** — 같은 요구사항인가, exception이나 scope-specific variant인가?
1. **Authority** — 어떤 editable source가 요구사항을 소유하는가? 다른 copy는 inherited, generated, projected, peer duplicate 중 무엇인가?
1. **Placement** — intended application과 precedence를 가장 적은 context로 보존하는 supported scope, selector, attachment는 무엇인가?

이 네 가지가 충분히 해결되기 전에는 이동하거나 deduplicate하지 않는다.

## Ownership and scope

Physical repetition은 자동으로 duplicate authority가 아니다. Scope, selector, attachment, precedence, inheritance, projection 차이 때문에 같은 요구사항의 물리적 표현이 여러 개 필요할 수 있다.

- runtime이 application을 보존할 수 있으면 semantic requirement의 editable owner는 하나를 선호한다.
- genuine exception과 narrower override를 보존한다.
- duplication 제거를 위해 Rule을 불필요하게 넓히거나 좁히지 않는다.
- generated/projected copy는 독립 authority로 취급하지 않는다.
- vendor-specific selector와 precedence model을 다른 runtime에 일반화하지 않는다.
