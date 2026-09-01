# Rule Improve

Rule과 scoped instruction 개선에만 필요한 판단을 다룬다. 공통 개선 원칙은 `../common/improve.md`를 따른다.

## Diagnose

우선 다음 문제를 찾는다.

- 같은 semantic requirement를 여러 editable owner가 중복 소유함
- 구조적으로 적용 대상을 정할 수 없는 지침을 path/selector Rule로 억지로 표현함
- 항상 적용되어야 하는 requirement가 optional routing 뒤에 숨음
- scope가 너무 넓거나 좁아 intended application이 흐려짐
- selector, inheritance, precedence가 필요 이상으로 복잡함
- exception과 일반 requirement가 섞여 있음
- nested Rule surface가 독립 applicability 없이 늘어남
- generated/projected copy를 사람이 직접 유지하고 있음
- reusable requirement 전체를 project/scope별로 복제하고 있음
- target-specific Rule model이 portable rule처럼 일반화됨

## Improve

개선은 application을 보존한 상태에서 authority, scope와 placement를 단순화하는 방향을 우선한다.

- semantic relevance가 application의 핵심이면 Rule selector를 복잡하게 만들기보다 더 적절한 semantic routing owner로 옮길 가치가 있는지 본다.
- peer duplicate가 명확할 때만 직접 deduplicate한다.
- genuine exception이나 scope-specific variant를 중복으로 오인하지 않는다.
- broadening/narrowing으로 duplication을 없애지 않는다.
- canonical source가 있으면 derived copy가 아니라 source를 수정한다.
- 동일 base requirement를 여러 scope가 복제하면 reusable owner와 필요한 local delta로 줄일 수 있는지 본다.
- 거의 항상 함께 적용되고 같은 이유로 바뀌는 Rule layer는 통합할 수 있는지 본다.
- application이 실제로 다른 scope는 파일 수를 줄이기 위해 합치지 않는다.
- project-native Rule model로 해결할 수 있으면 별도 shared schema, router 또는 indirection을 추가하지 않는다.
- stale selector, obsolete projection, 더 이상 독립 owner 가치가 없는 Rule surface는 제거한다.

Filesystem 재배치는 application, framework convention 또는 operability를 보존하면서 navigation을 실제로 개선할 때만 수행한다.
