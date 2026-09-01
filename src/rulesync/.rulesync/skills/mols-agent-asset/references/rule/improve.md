# Rule Improve

Rule과 scoped instruction 개선에만 필요한 판단을 다룬다. 공통 개선 원칙은 `../common/improve.md`를 따른다.

우선 다음 문제를 찾는다.

- 같은 semantic requirement를 여러 editable owner가 중복 소유함
- scope가 너무 넓거나 좁아 intended application이 흐려짐
- selector, inheritance, precedence가 필요 이상으로 복잡함
- exception과 일반 requirement가 섞여 있음
- generated/projected copy를 사람이 직접 유지하고 있음
- target-specific Rule model이 portable rule처럼 일반화됨

개선은 application을 보존한 상태에서 authority와 placement를 단순화하는 방향을 우선한다.

- peer duplicate가 명확할 때만 직접 deduplicate한다.
- genuine exception이나 scope-specific variant를 중복으로 오인하지 않는다.
- broadening/narrowing으로 duplication을 없애지 않는다.
- canonical source가 있으면 derived copy가 아니라 source를 수정한다.
- project-native Rule model로 해결할 수 있으면 별도 shared schema나 indirection을 추가하지 않는다.
