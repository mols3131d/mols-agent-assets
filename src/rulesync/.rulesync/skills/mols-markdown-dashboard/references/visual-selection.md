# Visual Selection

## Principle

기본 세 표가 답하지 못하는 질문이 있을 때만 추가 visual을 고려한다.

Dashboard Skill은 **visual이 필요한지와 어떤 reader question을 보완해야 하는지**까지만 판단한다. 실제 chart/diagram type, syntax와 visual design은 사용 가능한 전문 visual Skill이나 tool이 소유한다.

| Reader question | Dashboard decision | Condition |
| --- | --- | --- |
| 현재 구현·검증 상태는? | Development Progress table | 항상 |
| 무엇이 덜 구현됐나? | Implementation Gaps table | gap이 있을 때 |
| 무엇이 덜 검증됐나? | Verification Gaps table | gap이 있을 때 |
| 실제 진행을 막는가? | Risks / Blockers table | material risk가 있을 때 |
| 시간이 지나며 나아졌나? | trend visual을 고려 | 비교 가능한 여러 snapshot이 있을 때 |
| 어디서 막히는가? | dependency/state visual을 고려 | 관계가 표보다 중요할 때 |

## Default Exclusions

- 원형·도넛 차트
- 현재 진행률을 반복하는 막대 차트
- 상태별 개수만 보여주는 차트
- test function 개수 차트
- 실제 일정 근거가 없는 Gantt

## Rules

1. visual을 삭제해도 판단이 같으면 삭제한다.
1. snapshot이 하나뿐이면 progress trend를 만들지 않는다.
1. denominator가 달라진 snapshot을 단순 percentage trend로 연결하지 않는다.
1. 추가 visual이 필요하면 현재 환경에서 사용할 수 있는 chart/diagram 전문 Skill이나 tool에 reader question과 evidence를 넘긴다.
1. 전문 visual capability가 없어도 핵심 dashboard 완성을 막지 않는다.
1. 같은 사실을 표와 visual에서 반복하지 않는다.
