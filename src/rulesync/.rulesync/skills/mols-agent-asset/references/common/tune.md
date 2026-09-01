# Common Tune

튜닝은 기존 자산을 특정 목적, 상황, 저장소, 프로젝트, 런타임에 맞게 적응시키는 작업이다. 필요하면 새 자산이나 variant를 만들고, 기존 owner가 그 맥락을 직접 소유해야 하면 기존 자산을 수정한다.

## Target

먼저 무엇에 맞추는지 명확히 한다.

- 달성하려는 목적이나 작업 방식은 무엇인가?
- 어떤 상황이나 사용 맥락에서 동작해야 하는가?
- 저장소나 프로젝트가 요구하는 convention, ownership, scope는 무엇인가?
- 특정 framework나 runtime의 semantics가 결과에 영향을 주는가?
- 원본 자산에서 반드시 보존해야 할 intent와 invariant는 무엇인가?

튜닝은 막연한 품질 개선이 아니다. 목표 맥락과 원본 사이의 실제 차이를 찾고 그 차이만 반영한다.

## Choose the owner

원본이 범용으로 계속 유효하고 튜닝 결과가 더 좁은 맥락에만 필요하면 별도 자산이나 variant를 만든다. 새 변형은 독립적인 applicability, loading, reuse, ownership 가치가 있어야 한다.

반대로 해당 맥락이 기존 owner의 정상적인 책임이 되었거나 원본을 별도로 유지할 이유가 없다면 기존 자산을 수정한다. 단순히 원본을 보존하고 싶다는 이유만으로 fork를 만들지 않는다.

## Tune the delta

- 원본의 핵심 intent와 유효한 behavior를 먼저 보존한다.
- 목적, 상황, 저장소, target에 필요한 차이만 delta로 추가한다.
- reusable core를 그대로 복제하지 않는다. 분리가 실제 duplication을 줄일 때만 core와 delta를 나눈다.
- target-specific field, path, permission, packaging, runtime behavior는 필요할 때 authoritative source를 확인한다.
- 저장소 convention을 일반 규칙처럼 원본에 역전파하지 않는다.
- 튜닝을 빌미로 관련 없는 구조 개선이나 정규화를 함께 수행하지 않는다.

## Finish

새 자산이나 variant를 만들면 해당 유형의 `design.md` 기준으로 책임, applicability, package를 확인한다. 기존 자산을 수정하면 해당 유형의 `improve.md` 기준으로 변경 범위와 보존 조건을 확인한다.

마지막에는 튜닝 목표가 실제 변경에 반영되었는지, 원본 intent가 불필요하게 훼손되지 않았는지, 새 duplication이나 competing owner가 생기지 않았는지만 확인한다. runtime 적합성은 관찰한 근거보다 강하게 주장하지 않는다.
