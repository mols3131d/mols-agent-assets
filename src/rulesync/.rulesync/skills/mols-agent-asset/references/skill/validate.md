# Skill Validate

Skill 검증은 package가 올바른지와 실제로 잘 선택·동작하는지를 구분한다. 공통 원칙은 `../common/validate.md`를 따른다.

## Structural evidence

- metadata, entrypoint, resource path, package boundary, declared option/config surface를 확인한다.
- project 또는 source framework의 deterministic Skill check가 있으면 재사용한다.
- generated route나 target representation이 파생 결과라면 canonical source와의 drift를 확인한다.
- conditional reference는 entrypoint에서 언제 필요한지 실제로 발견 가능한지 본다.
- public argument나 mode가 있으면 allowed value와 omission, `default`, `auto` resolution이 일치하는지 확인한다.

## Behavioral evidence

Trigger precision, semantic routing, behavioral stability, target compatibility를 주장하려면 actual runtime evidence가 필요하다.

- positive case는 intended request에서 선택·적용되는지 본다.
- negative와 near-miss case는 인접 responsibility와 구분되는지 본다.
- keyword나 description 문구만으로 trigger quality를 판단하지 않는다.
- metadata와 entrypoint가 단계적으로 routing한다면 각 단계가 맡은 claim을 구분한다.
- target별 variant는 실제로 주장하는 target만 해당 evidence로 확인한다.

Valid package가 곧 잘 라우팅되거나 효과적인 Skill이라는 뜻은 아니다. Generated route가 source와 일치해도 runtime selection을 증명하지 않는다. Runtime evidence가 없으면 structural verification과 inferred behavior를 구분한다.
