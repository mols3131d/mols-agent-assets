# Skill Validate

Agent Skill 검증에만 필요한 근거와 claim을 다룬다. 공통 검증 원칙은 `../common/validate.md`를 따른다.

## Structural evidence

- metadata, entrypoint, resource path, package boundary와 declared option/config surface를 직접 확인한다.
- project 또는 source framework가 제공하는 deterministic Skill check가 있으면 재사용한다.
- generated route나 target representation이 source에서 파생된다면 canonical source에서 다시 생성한 결과와의 drift를 확인한다.
- reference가 progressive disclosure를 위해 분리되어 있다면 entrypoint에서 필요한 조건과 route가 실제로 발견 가능한지 확인한다.
- public argument나 mode가 있으면 allowed value, omission/default/auto resolution과 선택된 conditional context가 서로 일치하는지 확인한다.

## Behavioral evidence

Trigger precision, semantic routing, behavioral stability, target compatibility를 주장하려면 실제 runtime selection 또는 behavior evidence가 필요하다.

- positive case는 intended request에서 선택 또는 적용되는지 본다.
- negative와 near-miss case는 인접 responsibility와 구분되는지 본다.
- keyword 존재 여부나 description 문구만으로 trigger quality를 판단하지 않는다.
- metadata가 후보를 만들고 entrypoint가 applicability를 다시 좁히는 구조라면 각 단계가 맡은 claim을 구분한다.
- target별 variant를 지원하면 실제로 claim하는 variant만 해당 target evidence로 확인한다.

Valid package라고 해서 잘 라우팅되거나 효과적인 Skill이라는 뜻은 아니다. Generated route가 source와 일치해도 runtime selection behavior까지 증명하지 않는다. Runtime evidence가 없으면 structural verification과 inferred behavior를 분리한다.
