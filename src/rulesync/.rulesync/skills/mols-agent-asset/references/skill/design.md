# Skill Design

Skill 설계에서는 선택 가치, activation, context loading, package 경계를 본다. 공통 설계 원칙은 `../common/design.md`를 따른다.

## Fit

Skill은 task intent를 보고 선택할 가치가 있는 하나의 capability 또는 instruction context를 소유한다.

- path, subtree, glob만으로 적용 대상을 정할 수 있으면 structural scope가 더 자연스러운지 먼저 본다.
- Skill이라는 형식을 workflow와 동일시하지 않는다. 서로 다른 의미적 책임도 하나의 선택 가능한 capability로 응집될 수 있다.
- 책임이 여러 개여도 항상 함께 선택되고 같은 이유로 바뀌면 형식적으로 쪼개지 않는다. 독립 activation, loading, reuse, ownership 가치가 생길 때만 분리한다.

## Activation

- 무엇을 하는지와 언제 선택해야 하는지를 metadata에 드러낸다.
- selection 전에 필요한 정보는 activation 후에만 읽는 body에 숨기지 않는다.
- 인접 Skill과 혼동되면 realistic near-miss를 구분하는 데 필요한 경계만 추가한다.
- brittle keyword list보다 실제 사용자 intent와 task language를 우선한다.
- 항상 적용되어야 하는 project authority나 safety boundary를 Skill 선택 성공에 의존시키지 않는다.

Metadata는 후보를 좁히고, entrypoint는 실제 applicability와 필요한 다음 context를 더 구체적으로 좁힌다. Routing 단계가 깊어질수록 context도 더 관련성 높게 좁혀져야 한다.

## Package and context

필요한 동작을 보존하는 가장 작은 deployable package를 선호한다.

- 모든 activation에 필요한 instruction만 entrypoint에 둔다.
- conditional detail은 loading 이점이 있을 때만 reference로 분리하고, 언제 읽는지 entrypoint에서 발견 가능하게 한다.
- 거의 항상 함께 읽는 짧은 detail은 따로 분리하지 않는다.
- context를 좁히지 못하는 깊은 reference chain이나 router를 만들지 않는다.
- 반복되는 deterministic work는 prose보다 script나 native mechanism을 고려한다.
- output asset은 실제 task/runtime이 소비할 때만 둔다.
- maintainer-only artifact를 deployable Skill에 섞지 않는다.
- package naming과 placement는 source framework의 자연스러운 layout을 우선한다.

## Variants

같은 capability의 project, target, invocation 차이는 전체 Skill 복제보다 reusable core와 작은 delta로 표현할 수 있는지 본다.

- caller가 실제로 제어할 behavior만 argument나 option으로 노출한다.
- omitted, `default`, `auto`, explicit value를 지원하면 resolution 의미를 구분한다.
- 가능하면 option을 먼저 resolve한 뒤 필요한 conditional context를 읽는다.
- option마다 별도 capability, permission, owner가 생기면 하나의 parameterized Skill로 묶지 않는다.
- configuration layer가 실제로 겹칠 때만 merge/precedence를 정의한다.

## Source and target

Canonical source와 target projection을 구분한다. Source framework가 여러 target으로 투영하면 canonical source를 수정하고, target-specific discovery, metadata, permission, packaging, runtime behavior는 target contract를 따른다. Project-local 차이는 portable core 전체를 fork하지 않고 필요한 delta만 유지한다.
