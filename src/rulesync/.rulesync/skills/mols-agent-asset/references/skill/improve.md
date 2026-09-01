# Skill Improve

Agent Skill 개선에만 필요한 판단을 다룬다. 공통 개선 원칙은 `../common/improve.md`를 따른다.

## Diagnose

우선 다음 문제를 찾는다.

- responsibility가 너무 넓거나 인접 Skill과 겹침
- structural scope로 충분한 지침을 semantic Skill routing에 맡김
- activation metadata가 실제 intent를 구분하지 못함
- metadata, entrypoint, reference가 같은 routing 판단을 반복함
- entrypoint가 불필요한 세부사항으로 비대함
- conditional reference가 발견되지 않거나 선택 가치 없이 항상 로드됨
- reference chain이 깊지만 context를 실제로 좁히지 못함
- script, reference, asset의 역할이 뒤섞임
- target 또는 project별 Skill fork가 reusable core를 반복함
- public option이 실제 caller 선택 가치 없이 내부 구현 결정을 노출함
- target-specific assumption이 portable guidance로 일반화됨

## Improve

- existing owner를 우선하고, activation 문제는 pre-activation metadata부터 고친다.
- metadata는 coarse discovery에 필요한 정보만 남기고, entrypoint는 applicability와 다음 context를 더 구체적으로 좁히게 한다.
- context cost 문제는 삭제와 direct loading부터 보고, 독립 loading이나 reuse가 실제로 있을 때만 reference를 분리한다.
- 거의 항상 함께 읽히는 작은 reference는 합쳐 discovery와 synchronization 비용을 줄일 수 있는지 본다.
- 여러 near-identical Skill이 target이나 mode 차이만 가진다면 reusable core + local delta 또는 작은 argument surface로 단순화할 수 있는지 본다.
- argument나 mode를 도입한다면 omission/default/auto semantics를 숨기지 않고, option resolution이 conditional context loading보다 먼저 가능하게 한다.
- 반복 deterministic work는 prose를 늘리기보다 reusable script나 native mechanism으로 옮길 가치가 있는지 검토한다.
- target adaptation은 portable intent를 보존하면서 incompatible assumption만 target-native 방식으로 바꾼다.
- stale reference, unreachable resource, obsolete routing signal은 독립적인 가치가 없으면 제거한다.

Unrelated frontmatter, folder, package normalization은 함께 수행하지 않는다. Filesystem legibility를 이유로 framework-natural package structure를 재설계하지 않는다.
