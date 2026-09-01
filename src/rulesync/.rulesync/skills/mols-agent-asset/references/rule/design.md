# Rule Design

Rule 설계에서는 적용 범위와 authority를 먼저 본다. 공통 설계 원칙은 `../common/design.md`를 따른다.

## Fit

Rule은 repository, directory, path, glob, attachment scope처럼 구조적으로 applicability를 표현할 수 있거나 runtime이 명시적인 Rule application mechanism을 제공할 때 자연스럽다.

- task intent나 의미적 관련성을 봐야 적용 여부를 알 수 있으면 semantic routing surface가 더 적합한지 본다.
- 항상 적용되어야 하는 repository invariant나 safety boundary를 optional semantic routing에 맡기지 않는다.
- Rule이라는 형식을 곧바로 control 역할과 동일시하지 않는다. 실제 responsibility와 application mechanism이 Rule에 맞는지 판단한다.

## Application → Requirement → Authority → Placement

반복되거나 겹치는 지침은 다음 순서로 판단한다.

1. **Application** — 현재 어디에 적용되고 어디에 적용되어야 하는가?
1. **Requirement** — 같은 요구사항인가, exception이나 scope-specific variant인가?
1. **Authority** — 어떤 editable source가 요구사항을 소유하는가? 다른 copy는 inherited, generated, projected, peer duplicate 중 무엇인가?
1. **Placement** — intended application과 precedence를 가장 적은 context로 보존하는 scope, selector, attachment는 무엇인가?

이 네 가지가 충분히 해결되기 전에는 이동하거나 deduplicate하지 않는다.

## Ownership and scope

Physical repetition은 자동으로 duplicate authority가 아니다. Scope, selector, attachment, precedence, inheritance, projection 차이 때문에 같은 requirement가 여러 물리적 표현을 가질 수 있다.

- runtime이 application을 보존할 수 있으면 editable owner는 하나를 선호한다.
- requirement는 편리한 가장 넓은 scope가 아니라 올바른 가장 넓은 scope에 둔다.
- genuine exception과 narrower override를 보존한다.
- duplication 제거를 위해 Rule을 불필요하게 넓히거나 좁히지 않는다.
- generated/projected copy는 독립 authority로 취급하지 않는다.
- vendor-specific selector와 precedence를 다른 runtime에 일반화하지 않는다.

## Layering and delta

Reusable requirement 전체를 여러 scope에 복제하지 말고 native inheritance, projection, scoped delta를 우선한다. 실제 local override가 있을 때만 precedence나 merge semantics를 추가하고, nested Rule surface도 applicability나 ownership이 실제로 다를 때만 만든다.

Naming과 placement는 탐색을 돕되 application이나 source authority를 왜곡하지 않는다.
