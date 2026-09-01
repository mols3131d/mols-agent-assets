# Common Improve

Skill, Rule, Subagent 개선에 공통으로 적용되는 판단을 다룬다. 유형별 개선 기준은 각 유형의 `improve.md`가 소유한다.

## Target

개선은 반복 수정 자체가 아니라 material defect, ambiguity, unnecessary cost, weak ownership, unsupported assumption을 줄이는 작업이다.

- 가장 큰 실제 영향이나 유지보수 비용을 만드는 원인을 먼저 찾는다.
- symptom보다 root cause를 수정한다.
- 현재 owner가 책임을 유지할 수 있으면 새 자산이나 추상화를 만들지 않는다.
- 기능 추가보다 삭제, 단순화, 명확한 경계, 더 직접적인 native mechanism이 문제를 해결하는지 먼저 본다.

## Change discipline

- 무엇이 달라져야 하고 무엇이 반드시 유지되어야 하는지 먼저 정한다.
- 가장 작은 coherent owner를 수정한다.
- 기존의 유효한 책임과 intentional local delta를 보존한다.
- 변경 후 영향을 받은 semantic boundary와 관련 check만 다시 확인한다.
- 남은 문제가 scope 밖이거나 evidence가 없거나 추가 복잡성의 가치가 낮으면 멈춘다.

개선되었다고 말하려면 실제 결함 제거, 더 명확한 책임·적용 경계, 불필요한 context·duplication·indirection 감소, 또는 더 강한 근거 중 하나 이상이 분명해야 한다.
