# Skill Improve

Skill 개선은 activation, context loading, package 경계를 더 직접적으로 만드는 데 집중한다. 공통 개선 원칙은 `../common/improve.md`를 따른다.

## Signals

- responsibility가 너무 넓거나 인접 Skill과 겹친다.
- structural scope로 충분한 지침을 Skill routing에 맡긴다.
- activation metadata가 intended request와 near-miss를 구분하지 못한다.
- metadata, entrypoint, reference가 같은 판단을 반복한다.
- entrypoint가 conditional detail로 비대하거나 reference가 선택 가치 없이 항상 로드된다.
- reference chain은 깊지만 context를 실제로 좁히지 못한다.
- script, reference, output asset의 역할이 뒤섞인다.
- target/project별 Skill fork가 같은 core를 반복한다.
- public option이 caller 선택이 아니라 내부 구현 결정을 노출한다.
- target-specific assumption이 portable guidance처럼 남아 있다.

## Improve

- existing owner를 우선하고 activation 문제는 pre-activation metadata부터 고친다.
- metadata에는 coarse discovery만 남기고 entrypoint가 applicability와 다음 context를 좁히게 한다.
- context cost는 삭제와 direct loading부터 줄인다. 독립 loading/reuse가 있을 때만 reference를 분리한다.
- 거의 항상 함께 읽는 작은 reference는 합쳐 routing과 synchronization 비용을 줄인다.
- near-identical Skill은 reusable core와 local delta 또는 작은 argument surface로 단순화할 수 있는지 본다.
- argument를 남긴다면 omission, `default`, `auto` semantics를 숨기지 않는다.
- 반복 deterministic work는 prose보다 reusable script나 native mechanism으로 옮길 가치가 있는지 본다.
- target adaptation은 portable intent를 보존하고 incompatible assumption만 target-native 방식으로 바꾼다.
- stale reference, unreachable resource, obsolete routing signal은 독립 가치가 없으면 제거한다.

Unrelated frontmatter나 package를 함께 정규화하지 않는다. Filesystem legibility를 이유로 framework-native structure를 재설계하지 않는다.
