# Common Improve

Skill, Rule, Subagent 개선에 공통으로 적용되는 판단을 다룬다. 유형별 개선 기준은 각 유형의 `improve.md`가 소유한다.

## Target

개선은 반복 수정 자체가 아니라 material defect, ambiguity, unnecessary cost, weak ownership, unsupported assumption을 줄이는 작업이다.

- 가장 큰 실제 영향이나 유지보수 비용을 만드는 원인을 먼저 찾는다.
- symptom보다 root cause를 수정한다.
- 현재 owner가 책임을 유지할 수 있으면 새 자산이나 추상화를 만들지 않는다.
- 기능 추가보다 삭제, 단순화, 명확한 경계, 더 직접적인 native mechanism이 문제를 해결하는지 먼저 본다.

## Simplify surfaces

자산이 커졌다는 이유만으로 분리하지 않고, 현재 surface의 선택·loading·reuse·ownership 비용을 함께 본다.

- 독립적인 applicability, loading, reuse 또는 ownership이 없는 작은 surface는 통합할 수 있는지 본다.
- 반대로 반복적으로 불필요한 context가 함께 로드되거나 독립 reuse가 필요한 책임은 분리를 고려한다.
- router, index, reference chain이 context를 실제로 좁히지 못하면 중간 layer를 제거한다.
- stale metadata, obsolete reference, 중복 owner처럼 독립적으로 남을 이유가 없는 surface는 정리한다.
- filesystem을 더 설명적으로 보이게 하기 위한 wrapper, duplication, abstraction은 추가하지 않는다.

## Preserve the core

같은 core를 project나 target별로 복제한 상태라면 전체 fork보다 reusable core와 필요한 delta로 되돌릴 수 있는지 본다.

- local customization은 필요한 차이만 남긴다.
- target-specific detail은 portable core에서 분리하되 작은 차이 때문에 별도 capability를 만들지 않는다.
- 여러 variant가 사실상 같은 capability라면 caller가 의미 있게 제어할 수 있는 작은 option이나 argument로 표현하는 편이 더 단순한지 검토한다.
- option이 지나치게 많아 mini-framework가 되거나 permission, authority, lifecycle이 달라지면 다시 책임 분리를 고려한다.

## Change discipline

- 무엇이 달라져야 하고 무엇이 반드시 유지되어야 하는지 먼저 정한다.
- 가장 작은 coherent owner를 수정한다.
- 기존의 유효한 책임과 intentional local delta를 보존한다.
- machine-observable 문제를 native mechanism이나 기존 deterministic check가 이미 예방한다면 새 checker를 만들지 않는다.
- 변경 후 영향을 받은 semantic boundary와 관련 check만 다시 확인한다.
- 남은 문제가 scope 밖이거나 evidence가 없거나 추가 복잡성의 가치가 낮으면 멈춘다.

개선되었다고 말하려면 실제 결함 제거, 더 명확한 책임·적용 경계, 불필요한 context·duplication·indirection 감소, 더 직접적인 continuation/handoff, 또는 더 강한 근거 중 하나 이상이 분명해야 한다.
