# Subagent Validate

Subagent Validation은 definition과 intended delegation contract가 제대로 표현되어 있는지 확인한다. 실제 invocation과 orchestration 성능은 Eval이 소유한다. 공통 원칙은 `../common/validate.md`를 따른다.

## Deterministic validation

- metadata, declared capability, resource path와 target representation의 machine-checkable contract를 확인한다.
- project 또는 source framework의 deterministic agent metadata/projection check가 있으면 재사용한다.
- target representation이 파생 결과라면 canonical source와의 drift를 확인한다.

## Semantic validation

- responsibility, delegation condition, context contract, capability, result contract, termination semantics가 intended design을 표현하는지 확인한다.
- handoff가 revision이나 observable state에 의존하면 state basis와 freshness contract가 명확한지 본다.
- durable handoff가 canonical knowledge를 복제하지 않고 continuation에 필요한 state만 소유하도록 설계됐는지 확인한다.
- capability와 permission이 맡긴 책임보다 넓지 않고, destructive/publish/approval 경계가 적절한 owner에 남아 있는지 본다.
- independence가 다른 reviewer나 specialist의 결론을 미리 주입하지 않도록 contract가 분리됐는지 확인한다.

Well-formed definition이 곧 실제로 잘 호출되고 독립적으로 동작한다는 뜻은 아니다. 실제 delegation과 agent selection은 Routing Eval, tool permission, handoff, isolation, result usability는 Behavior Eval로 확인한다.
