---
description: repository-wide 문서 생성·배치·ownership과 authority 판단에 적용하는 공통 원칙입니다.
---

# Documentation Principles

문서는 실제 책임과 durable knowledge를 명확하게 소유하고, 독자의 판단·행동·복구를 개선할 때만 둡니다.

## Principles

- **필요한 문서만 둡니다.** 파일이나 directory가 존재한다는 이유만으로 README나 별도 문서를 만들지 않습니다.
- **가장 좁은 scope가 소유합니다.** Repository-wide principle과 convention은 `docs/documentation/`, 특정 directory나 surface의 contract·navigation·maintenance·recovery knowledge는 가장 가까운 local owner, 개별 asset이나 family의 maintainer knowledge는 해당 maintainer documentation이 소유합니다.
- **한 의미에는 한 authoritative owner를 둡니다.** 같은 scope의 durable rule, convention, rationale 또는 contract를 여러 문서가 함께 소유하지 않습니다. 다른 surface는 필요한 만큼만 route하거나 link합니다.
- **상위 원칙을 local에서 복제하거나 재정의하지 않습니다.** Local document는 자기 scope를 구체화할 수 있지만 repository-wide 원칙과 충돌하는 별도 authority를 만들지 않습니다.
- **복구 가능한 inventory를 authored knowledge로 만들지 않습니다.** Filesystem, search 또는 generated projection에서 얻을 수 있는 정보는 사람이 유지하는 문서에 불필요하게 복제하지 않습니다.
- **반복되는 local rule은 공통 원칙으로 승격할지 검토합니다.** 여러 local owner가 같은 의미를 반복해서 소유하기 시작하면 repository-wide principle인지 다시 판단합니다.
