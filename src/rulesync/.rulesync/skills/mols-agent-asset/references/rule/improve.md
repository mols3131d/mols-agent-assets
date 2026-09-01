# Rule Improve

Rule 개선은 application을 보존하면서 authority, scope, placement를 단순화한다. 공통 개선 원칙은 `../common/improve.md`를 따른다.

## Signals

- 같은 requirement를 여러 editable owner가 소유한다.
- 의미 판단이 필요한 지침을 path/selector Rule로 억지로 표현한다.
- 항상 적용되어야 하는 requirement가 optional routing 뒤에 숨는다.
- scope가 너무 넓거나 좁아 intended application이 흐려진다.
- selector, inheritance, precedence가 필요 이상으로 복잡하다.
- exception과 일반 requirement가 섞여 있다.
- nested Rule surface가 독립 applicability 없이 늘어난다.
- generated/projected copy를 사람이 직접 유지한다.
- reusable requirement 전체를 project/scope별로 복제한다.
- target-specific Rule model을 portable rule처럼 일반화한다.

## Improve

- semantic relevance가 핵심이면 selector를 복잡하게 만들기보다 더 적절한 semantic routing owner를 검토한다.
- peer duplicate가 명확할 때만 직접 deduplicate한다.
- genuine exception이나 scope-specific variant를 중복으로 오인하지 않는다.
- broadening/narrowing으로 duplication을 없애지 않는다.
- canonical source가 있으면 derived copy가 아니라 source를 수정한다.
- 동일 base requirement의 반복은 reusable owner와 필요한 local delta로 줄인다.
- 거의 항상 함께 적용되고 같은 이유로 바뀌는 Rule layer는 통합할 수 있는지 본다.
- 실제 application이 다른 scope는 파일 수를 줄이기 위해 합치지 않는다.
- project-native Rule model로 충분하면 shared schema, router, indirection을 추가하지 않는다.
- stale selector, obsolete projection, 독립 owner 가치가 사라진 surface는 제거한다.

Filesystem 재배치는 application, framework convention, operability를 보존하면서 navigation을 실제로 개선할 때만 수행한다.
