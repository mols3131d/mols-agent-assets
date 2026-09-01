# Common Improve

개선은 더 많이 고치는 일이 아니라 실제 결함과 불필요한 비용을 줄이는 일이다. 특정 목적이나 환경에 맞추는 적응이 주된 목표면 `tune.md`를 사용한다. 유형별 기준은 각 `improve.md`가 소유한다.

## Diagnose

먼저 영향이 큰 root cause를 찾는다.

- 책임이 겹치거나 owner가 불명확한가?
- 적용 범위나 routing이 실제 필요보다 복잡한가?
- 불필요한 context, reference, layer, surface가 남아 있는가?
- reusable core를 project/target별로 반복하고 있는가?
- stale metadata, obsolete reference, derived copy를 사람이 유지하고 있는가?
- native mechanism이나 기존 check로 충분한 문제를 새 abstraction으로 풀고 있는가?

## Simplify

- 현재 owner가 책임을 유지할 수 있으면 새 자산을 만들지 않는다.
- 삭제, 통합, 직접적인 native mechanism을 기능 추가보다 먼저 본다.
- 독립 applicability, loading, reuse, ownership이 없는 surface는 합칠 수 있는지 본다.
- 반대로 불필요한 context가 반복해서 함께 로드되면 필요한 부분만 분리한다.
- context를 줄이지 못하는 router/reference chain은 제거한다.
- 같은 core의 복제는 reusable core와 필요한 delta로 줄인다.

## Change

무엇을 바꾸고 무엇을 보존할지 먼저 정한 뒤 가장 작은 owner를 수정한다. 변경 후 영향을 받은 의미 경계와 check만 다시 확인한다.

남은 문제가 scope 밖이거나 근거가 없거나 추가 복잡성의 가치가 낮으면 멈춘다. 개선되었다는 주장은 결함 제거, 경계 명확화, context·duplication·indirection 감소, 더 직접적인 handoff, 더 강한 근거처럼 실제 변화에 연결되어야 한다.
