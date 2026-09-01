# Skill Improve

Agent Skill 개선에만 필요한 판단을 다룬다. 공통 개선 원칙은 `../common/improve.md`를 따른다.

우선 다음 문제를 찾는다.

- responsibility가 너무 넓거나 인접 Skill과 겹침
- activation metadata가 실제 intent를 구분하지 못함
- entrypoint가 불필요한 세부사항으로 비대함
- conditional reference가 발견되지 않거나 항상 로드됨
- script, reference, asset의 역할이 뒤섞임
- target-specific assumption이 portable guidance로 일반화됨

개선할 때는 existing owner를 우선하고, activation 문제는 pre-activation metadata부터, context cost 문제는 삭제와 progressive disclosure부터 본다. 반복 deterministic work는 prose를 늘리기보다 reusable script나 native mechanism으로 옮길 가치가 있는지 검토한다. Target adaptation은 portable intent를 보존하면서 incompatible assumption만 target-native 방식으로 바꾼다.

Unrelated frontmatter, folder, package normalization은 함께 수행하지 않는다.
