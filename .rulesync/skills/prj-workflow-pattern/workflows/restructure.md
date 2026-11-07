# Restructure Patterns

**When:** 패턴을 통합·분리·대체하거나 소유 책임을 재설계할 때.

1. 대상 capsule의 primary problem, core, 대안·근거 및 **각 문서만 가진 지식**을 비교한다. 단순한 주제 연관이 아니라 책임 중복·선택 혼란·유지보수 비용을 근거로 판단한다.
2. 통합할 owner, 분리할 고유 문제, 기존 원본 유지 및 상호 연결 중 가장 단순한 구조를 선택한다. 새 category·bundle·alias는 실제 탐색·소유 가치가 있을 때만 만든다.
3. 결정한 정본에 보존할 맥락을 이관하고, 알려진 capsule·README·문서 링크와 사례를 조정한다. 이관 중 다른 owner의 규칙을 무단으로 다시 쓰지 않는다.
4. [Review](review.md)로 재구성한 책임과 self-containment를, [Validate](validate.md)로 링크·원본·인덱스를 확인한다. 실제 제거가 필요하면 [Delete](delete.md)를 별도 적용한다.

**Result:** 책임 재배치의 이유, 새 정본·이관된 지식, 참조와 소비 위험.
