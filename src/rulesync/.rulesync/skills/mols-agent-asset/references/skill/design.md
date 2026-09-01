# Skill Design

Agent Skill 설계에만 필요한 판단을 다룬다. 공통 ownership, authority, precision, write boundary는 `../common/design.md`를 따른다.

## Responsibility and activation

Skill은 하나의 선택 가능한 coherent capability를 소유한다.

- 무엇을 가능하게 하는지와 무엇을 소유하지 않는지 구분한다.
- selection metadata를 사람용 요약이 아니라 activation surface로 취급한다.
- activation 전에 필요한 정보는 activation 후에만 로드되는 body에 숨기지 않는다.
- 무엇을 하는지와 언제 선택해야 하는지를 함께 드러낸다.
- 인접 Skill과 혼동되면 realistic near-miss를 구분하는 데 필요한 경계만 추가한다.
- brittle keyword list보다 실제 사용자 intent와 task language를 우선한다.

## Package and progressive disclosure

필요한 동작을 보존하는 가장 작은 deployable package를 선호한다.

- source 또는 target contract가 소유하는 필수 field, directory, discovery semantics를 여기서 복제하지 않는다.
- 모든 activation에 필요한 instruction만 entrypoint에 둔다.
- 조건부 세부사항은 직접 발견 가능한 reference로 분리하고 언제 읽는지 entrypoint에서 명시한다.
- retrieval cost를 크게 만드는 깊은 reference chain을 피한다.
- 반복 deterministic mechanics가 있으면 prose 반복보다 script를 고려한다.
- output asset은 실제 task/runtime이 소비할 때만 둔다.
- repository-only maintainer 또는 verification artifact를 deployable Skill에 섞지 않는다.
- host가 supporting `SKILL.md`를 별도 Skill로 발견할 수 있으면 non-entrypoint filename을 사용한다.

## Source and target

canonical source와 target projection을 구분한다.

- source framework가 여러 target으로 투영하면 canonical source를 수정한다.
- target-specific discovery, metadata, permission, packaging과 runtime behavior는 target contract를 따른다.
- target-specific representation을 portable contract처럼 일반화하지 않는다.
