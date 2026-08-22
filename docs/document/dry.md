# DRY Boundaries

문서 중복은 repository 전체를 하나의 namespace로 보고 판정하지 않습니다. **같은 scope에서 같은 의미를 둘 이상의 owner가 함께 소유하지 않는 것**을 기본 원칙으로 합니다.

## Principle

- 하나의 durable rule, convention, rationale 또는 contract는 같은 scope 안에서 authoritative owner 하나만 둡니다.
- Entrypoint의 짧은 routing label과 link는 원문 책임의 중복으로 보지 않습니다.
- 서로 다른 scope의 문서는 portability, self-containment 또는 독립 사용성에 실제 도움이 될 때 필요한 만큼 overlap할 수 있습니다.
- 단순 편의를 위한 무의미한 복제는 scope가 달라도 만들지 않습니다.

## Local Boundaries

특정 directory나 documentation surface에만 적용되는 ownership·duplication boundary는 그 local owner가 정의합니다.

`docs/document/`는 `references/`, `inbox/`, `route/` 같은 개별 directory 내부의 세부 책임 분할을 대신 소유하지 않습니다. 해당 directory의 `README.md`나 local document가 자기 범위의 owner와 중복 경계를 설명합니다.

Asset/family documentation capsule의 repository-wide portability contract는 [Asset Capsules](asset-capsules.md)가 소유합니다.

## Review

중복을 발견하면 다음 순서로 판단합니다.

1. 두 문서가 실제로 같은 의미를 소유하는지 확인합니다.
1. 같은 scope라면 authoritative owner 하나로 합치고 다른 곳에서는 link나 짧은 routing만 남깁니다.
1. 다른 scope라면 독립 사용성이나 self-containment를 위해 overlap이 필요한지 확인합니다.
1. 특정 directory에만 해당하는 판단은 그 directory의 local owner로 돌려보냅니다.
1. 여러 local owner에서 같은 규칙이 반복되면 repository-wide 원칙으로 승격할 가치가 있는지 검토합니다.
