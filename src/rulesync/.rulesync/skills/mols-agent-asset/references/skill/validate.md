# Skill Validate

Skill Validation은 package·규격 준수와 intended Skill design의 표현을 확인한다. 실제 selection과 behavior 성능은 Eval이 소유한다. 공통 원칙은 `../common/validate.md`를 따른다.

## Deterministic validation

- metadata, entrypoint, resource path, package boundary, declared option/config surface를 확인한다.
- project 또는 source framework의 deterministic Skill check가 있으면 재사용한다.
- generated route나 target representation이 파생 결과라면 canonical source와의 drift를 확인한다.
- schema나 allowed value가 명시된 public argument/config는 그 contract를 기계적으로 확인한다.

## Semantic validation

- description과 activation boundary가 intended responsibility와 negative boundary를 표현하는지 본다.
- metadata가 selection 전에 필요한 정보를 제공하고 entrypoint/reference routing이 필요한 context를 단계적으로 좁히는지 본다.
- conditional reference가 언제 필요한지 entrypoint에서 발견 가능한지 확인한다.
- project/target adaptation이 portable intent와 local delta 경계를 보존하는지 확인한다.
- supporting material이 우연히 별도 Skill entrypoint로 해석되지 않는지 본다.

Valid package와 잘 표현된 activation contract가 곧 실제로 잘 선택되는 Skill이라는 뜻은 아니다. Positive·negative·near-miss에서 실제 selection을 확인하려면 Routing Eval을 사용하고, 선택 이후 효과는 Behavior Eval을 사용한다.
