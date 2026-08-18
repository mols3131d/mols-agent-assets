# Visual Selection

## Principle

기본 세 표가 답하지 못하는 질문에만 visual을 추가한다.

| Reader question | Preferred form | Condition |
| --- | --- | --- |
| 현재 구현·검증 상태는? | Development Progress table | 항상 |
| 무엇이 덜 구현됐나? | Implementation Gaps table | gap이 있을 때 |
| 무엇이 덜 검증됐나? | Verification Gaps table | gap이 있을 때 |
| 실제 진행을 막는가? | Risks / Blockers table | material risk가 있을 때 |
| 시간이 지나며 나아졌나? | Mermaid line chart | 비교 가능한 여러 snapshot이 있을 때 |
| 어디서 막히는가? | Mermaid flow/state diagram | 관계가 표보다 중요할 때 |

## Default Exclusions

- 원형·도넛 차트
- 현재 진행률을 반복하는 막대 차트
- 상태별 개수만 보여주는 차트
- test function 개수 차트
- 실제 일정 근거가 없는 Gantt

## Rules

1. 차트를 삭제해도 판단이 같으면 삭제한다.
2. snapshot이 하나뿐이면 progress trend를 만들지 않는다.
3. denominator가 달라진 snapshot을 단순 percentage trend로 연결하지 않는다.
4. 복잡한 Mermaid는 사용 가능한 Mermaid 전문 도구나 스킬이 있으면 위임한다. 없어도 핵심 dashboard 완성을 막지 않는다.
5. 같은 사실을 표와 diagram에서 반복하지 않는다.
