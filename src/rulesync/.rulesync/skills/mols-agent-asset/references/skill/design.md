# Skill Design

Agent Skill 설계에만 필요한 판단을 다룬다. 공통 ownership, scope, granularity, authority, precision은 `../common/design.md`를 따른다.

## Fit

Skill은 task intent나 의미적 관련성을 보고 선택할 가치가 있는 coherent capability 또는 instruction context를 소유한다.

- path, subtree, glob처럼 구조만으로 적용 여부가 결정되면 Rule이나 runtime-native structural scope가 더 자연스러운지 먼저 본다.
- Skill이라는 representation을 workflow와 동일시하지 않는다. Knowledge, procedure, constraint-supporting context처럼 semantic responsibility가 달라도 하나의 선택 가능한 capability로 응집되면 Skill일 수 있다.
- 여러 책임이 섞여 있어도 항상 함께 선택되고 같은 이유로 바뀐다면 형식적으로 쪼개지 않는다. 독립 loading, reuse, activation 또는 ownership 가치가 생길 때만 분리한다.

## Responsibility and activation

- 무엇을 가능하게 하는지와 무엇을 소유하지 않는지 구분한다.
- selection metadata를 사람용 요약이 아니라 coarse discovery surface로 취급한다.
- activation 전에 필요한 정보는 activation 후에만 로드되는 body에 숨기지 않는다.
- 무엇을 하는지와 언제 선택해야 하는지를 함께 드러낸다.
- 인접 Skill과 혼동되면 realistic near-miss를 구분하는 데 필요한 경계만 추가한다.
- brittle keyword list보다 실제 사용자 intent와 task language를 우선한다.
- 항상 적용되어야 하는 project authority나 safety boundary를 Skill 선택 성공에 의존시키지 않는다.

Metadata가 후보를 좁힌 뒤 entrypoint에서는 현재 task에 실제로 적용할 가치가 있는지와 어떤 추가 context가 필요한지를 더 구체적으로 결정할 수 있다. Routing 단계는 깊어질수록 더 관련성 높은 context로 좁혀져야 하며, 단계를 늘리는 것 자체가 목적이 아니다.

## Package and progressive disclosure

필요한 동작을 보존하는 가장 작은 deployable package를 선호한다.

- source 또는 target contract가 소유하는 필수 field, directory, discovery semantics를 여기서 복제하지 않는다.
- 모든 activation에 필요한 instruction만 entrypoint에 둔다.
- 조건부 세부사항은 실제 loading 이점이 있을 때만 별도 reference로 분리하고, 필요한 시점을 entrypoint에서 발견 가능하게 한다.
- 거의 항상 함께 읽는 짧은 detail을 progressive disclosure라는 이유만으로 분리하지 않는다.
- retrieval cost를 크게 만드는 깊은 reference chain이나 context를 좁히지 못하는 router를 피한다.
- 반복 deterministic mechanics가 있으면 prose 반복보다 script나 native mechanism을 고려한다.
- output asset은 실제 task/runtime이 소비할 때만 둔다.
- repository-only maintainer 또는 verification artifact를 deployable Skill에 섞지 않는다.
- host가 supporting `SKILL.md`를 별도 Skill로 발견할 수 있으면 non-entrypoint filename을 사용한다.
- filesystem naming과 placement는 탐색을 도울 수 있게 하되 source framework의 natural layout을 왜곡하지 않는다.

## Variants and configuration

같은 capability의 project, target 또는 invocation별 차이는 전체 Skill 복제보다 reusable core와 작은 delta로 표현할 수 있는지 본다.

- caller가 실제로 제어할 가치가 있는 behavior만 argument나 option으로 노출한다.
- omitted, `default`, `auto`, explicit value를 지원하면 각각의 resolution 의미를 구분한다.
- 가능하면 option을 resolve한 뒤 해당 variant에 필요한 conditional context를 로드한다.
- option마다 독립 capability, permission, owner가 생기면 하나의 parameterized Skill로 억지로 묶지 않는다.
- configuration layer가 여러 개 겹치지 않으면 복잡한 merge/precedence model을 만들지 않는다.

## Source and target

canonical source와 target projection을 구분한다.

- source framework가 여러 target으로 투영하면 canonical source를 수정한다.
- target-specific discovery, metadata, permission, packaging과 runtime behavior는 target contract를 따른다.
- target-specific representation을 portable contract처럼 일반화하지 않는다.
- project-local customization은 portable core 전체를 fork하지 않고 필요한 delta만 유지한다.
