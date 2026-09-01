# Skill Validate

Agent Skill 검증에만 필요한 근거와 claim을 다룬다. 공통 검증 원칙은 `../common/validate.md`를 따른다.

- metadata, entrypoint, resource link, package boundary를 직접 확인한다.
- project 또는 source framework가 제공하는 deterministic Skill check가 있으면 재사용한다.
- target representation이 검증 대상이면 generated projection을 확인한다.
- trigger precision, behavioral stability, target compatibility를 주장하려면 실제 runtime selection 또는 behavior evidence를 사용한다.

필요한 경우 positive, negative, near-miss case로 activation boundary를 확인하되, keyword 존재 여부만으로 trigger quality를 판단하지 않는다.

Valid package라고 해서 잘 라우팅되거나 효과적인 Skill이라는 뜻은 아니다. Runtime evidence가 없으면 structural verification과 inferred behavior를 분리한다.
