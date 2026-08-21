# DRY Boundaries

문서 중복은 하나의 repository-wide namespace로 판정하지 않습니다. 목적이 다른 documentation domain 사이의 overlap은 허용하고, 같은 domain 안에서는 하나의 의미를 하나의 owner만 소유하게 합니다.

## Domains

### Project Documentation

`docs/references/`와 asset capsule을 제외한 repository documentation은 하나의 project documentation domain으로 봅니다.

같은 durable rule, convention 또는 rationale을 이 domain 안의 둘 이상의 문서가 함께 소유하면 DRY 위반입니다. Entrypoint의 짧은 routing label과 link는 policy body의 중복으로 보지 않습니다.

### References

`docs/references/**`는 기본적으로 하나의 reference domain입니다.

- references 내부의 둘 이상의 문서가 같은 의미를 중복 소유하면 DRY 위반입니다.
- references와 references 밖의 project documentation이 같은 내용을 각각 필요에 맞게 설명하는 것은 허용합니다.
- reference 내용은 project-local operational authority를 자동으로 획득하지 않습니다.

#### Pattern Capsules

`docs/references/patterns/*.md`의 각 pattern 문서는 하나의 독립 documentation domain입니다.

- 다른 pattern capsule과의 overlap은 허용합니다.
- 같은 capsule 내부의 불필요한 중복은 DRY 위반입니다.
- Pattern capsule의 작성, self-containment, flexibility와 ownership contract는 [Patterns](../references/patterns/README.md)가 소유합니다.

### Asset Capsules

각 `docs/<asset-type>/<owner>/**`는 하나의 독립적인 documentation domain입니다. `<owner>`는 하나의 asset 또는 family일 수 있으며 `development`, `document`, `references`는 asset type이 아니라 reserved documentation namespace입니다.

- 같은 capsule 내부의 중복은 DRY 위반입니다.
- asset-specific capsule과 project documentation, references 또는 다른 capsule 사이의 overlap은 portability와 self-containment를 위해 허용합니다.
- family가 공유하는 durable knowledge는 family capsule이 소유하고 member-specific capsule에 반복하지 않습니다.
- member-specific intent, recovery 또는 invariant는 해당 asset capsule이 소유합니다. Family capsule이 모든 member 문서를 흡수하는 상위 문서가 되지 않습니다.

Asset/family capsule의 portability와 ownership contract는 [Asset Capsules](asset-capsules.md)가 소유합니다.

## Review

중복을 발견하면 먼저 두 문서가 같은 domain인지 판정합니다.

- 같은 domain이면 authoritative owner 하나로 합칩니다.
- 다른 domain이면 독립 사용성에 실제 도움이 되는 overlap인지 확인합니다.
- Family 공유 knowledge라면 member별 복제보다 family capsule을 우선합니다.
- Pattern capsule은 overlap보다 responsibility ownership을 먼저 검토합니다.
- 단순 편의를 위한 무의미한 복제는 domain이 달라도 만들지 않습니다.
