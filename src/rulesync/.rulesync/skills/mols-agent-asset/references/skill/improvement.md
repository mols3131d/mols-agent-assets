# Skill Improvement

Agent Skill 개선에만 필요한 판단을 다룬다. 공통 improvement discipline은 `../common/improvement.md`를 따른다.

## Improvement targets

우선순위가 높은 개선 후보는 다음과 같다.

- responsibility가 너무 넓거나 인접 Skill과 겹침
- activation metadata가 실제 intent를 구분하지 못함
- body가 activation에 필요하지 않은 세부사항으로 과도하게 비대함
- conditional reference가 발견되지 않거나 항상 로드됨
- scripts, references, assets의 역할이 뒤섞임
- target-specific assumption이 portable guidance로 일반화됨
- 기존 유효한 behavior보다 형식 통일이나 lowest-common-denominator adaptation이 우선됨

## Change approach

- existing owner가 적절하면 새 Skill을 만들지 않고 그 owner를 개선한다.
- activation 문제면 body보다 먼저 pre-activation metadata와 near-miss boundary를 본다.
- context cost 문제면 삭제와 progressive disclosure를 우선한다.
- 반복 deterministic work는 prose를 늘리기보다 reusable script나 native mechanism으로 옮길 가치가 있는지 본다.
- target adaptation은 portable intent를 보존하면서 incompatible assumption만 target-native 방식으로 바꾼다.
- unrelated frontmatter, folder, package normalization을 함께 수행하지 않는다.

개선 후에는 변경한 activation, package, resource boundary와 target assumption만 집중적으로 다시 본다.
