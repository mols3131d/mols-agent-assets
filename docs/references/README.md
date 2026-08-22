---
description: 외부 specification이나 tooling의 current authority를 확인해야 할 때 authoritative source routing을 찾는 데 사용합니다.
---

# References

`docs/references/`는 **외부 specification과 tooling의 authoritative source를 찾기 위한 routing knowledge**를 보관합니다.

이 디렉터리는 Agent Asset 자체의 설계 원칙이나 pattern을 소유하지 않습니다. 그런 reusable design knowledge는 [`docs/agent-assets/`](../agent-assets/)가 소유합니다.

Reference는 upstream behavior를 local prose로 대체하지 않고, 작업 시점에 확인해야 할 official source와 이 repository에서 필요한 integration boundary를 연결합니다.

같은 external authority나 integration concern을 여러 reference가 중복 소유하지 않습니다. 중복 경계는 [Documentation DRY policy](../document/dry.md)를 따릅니다.
