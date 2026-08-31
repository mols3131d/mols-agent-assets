---
description: repository-wide 문서의 목적·scope·authority·신뢰성·탐색성과 유지보수성을 판단할 때 적용하는 공통 원칙입니다.
---

# Documentation Principles

문서는 독자가 현재 필요한 판단·행동·이해를 정확하게 돕는 durable knowledge입니다. 형식이나 도구보다 독자에게 필요한 의미와 신뢰할 수 있는 내용을 우선합니다.

## Principles

- **Reader need first.** 작성자가 설명하고 싶은 순서보다 독자가 해결하려는 질문, 판단과 행동에서 시작합니다. 독자의 필요를 바꾸지 않는 내용은 관성적으로 추가하지 않습니다.
- **Clear responsibility and scope.** 문서마다 주된 책임을 분명히 하고 그 책임을 소유할 가장 좁은 유효 scope에 둡니다. 파일이나 directory가 존재한다는 이유만으로 문서를 만들지 않으며, 선택한 scope 안에서는 독자가 잘못 판단하지 않을 만큼 필요한 맥락과 제약을 충분히 다룹니다.
- **Progressive disclosure.** 결론, 중요한 조건과 다음 판단에 필요한 정보를 먼저 제공합니다. 세부 설명과 깊은 reference는 필요할 때 더 탐색할 수 있게 하며, 독자에게 당장 필요하지 않은 깊이를 먼저 강요하지 않습니다.
- **One authority, minimal repetition.** 같은 scope의 같은 durable 의미는 하나의 authoritative owner가 소유합니다. 다른 문서는 상위 원칙을 재정의하지 않고 필요한 routing, link와 짧은 context만 제공하며, 다른 scope의 overlap은 portability나 self-containment를 실제로 개선할 때만 허용합니다.
- **Current and trustworthy.** 문서는 현재의 truth와 맞고 정확·일관·명확해야 합니다. 사실, 결정과 불확실성을 구분하고 필요한 근거를 확인할 수 있게 하며, 오래된 상태나 추측을 현재 guidance처럼 유지하지 않습니다.
- **Discoverable and navigable.** 필요한 독자가 문서를 발견하고 다른 후보와 구분해 선택할 수 있어야 하며, 읽은 뒤 필요한 다음 정보로 이동할 수 있어야 합니다. 중요한 규칙이나 지식을 우연한 발견에 의존하게 숨기지 않습니다.
- **Maintainable by design.** 문서의 가치는 작성 비용뿐 아니라 앞으로의 유지 비용까지 포함해 판단합니다. Filesystem, search나 generated projection에서 쉽게 복구할 수 있는 정보는 authored knowledge로 반복하지 않고, 반복되는 local rule은 더 적절한 공통 owner가 필요한지 검토합니다.
