---
description: mols-mermaid-chart의 후속 재설계에서 검토할 책임과 보존할 계약을 확인할 때 사용합니다.
---

# Remake Recommendation

수치·단위·순서·규모 보존과 대상 renderer 검증의 특수성은 유지한다. Mermaid diagram과 공통으로 사용하는 type 선택, 의미 보존, 편집·검증 지침은 단일 진입점과 조건부 chart reference로 통합할 실익을 검토한다. 독립 선택 및 로딩의 가치가 더 크면 분리를 유지한다.

권고 상태이며 현재 실행 계약은 변경하지 않는다.
