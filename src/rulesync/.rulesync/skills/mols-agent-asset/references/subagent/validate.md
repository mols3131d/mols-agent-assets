# Subagent Validate

Subagent 검증은 definition이 잘 구성됐는지와 runtime orchestration이 실제로 동작하는지를 구분한다. 공통 원칙은 `../common/validate.md`를 따른다.

## Structural evidence

- responsibility, delegation condition, context contract, capability, result contract, termination semantics를 확인한다.
- handoff가 revision이나 observable state에 의존하면 state basis가 현재 source와 맞는지 본다.
- durable handoff는 canonical knowledge를 복제하지 않고 continuation에 필요한 state만 소유하는지 확인한다.
- project 또는 source framework의 deterministic agent metadata/projection check가 있으면 재사용한다.
- target representation이 대상이면 canonical source와 generated agent definition의 drift를 확인한다.

## Runtime evidence

Tool availability, permission behavior, nested delegation, isolation, parallelism, independence, handoff behavior를 주장하려면 actual runtime evidence가 필요하다.

- intended condition에서 caller가 실제로 해당 agent를 사용할 수 있는지 본다.
- independence는 brief contamination과 runtime isolation을 구분해 확인한다.
- tool 이름이나 metadata 존재만으로 side effect와 permission semantics를 확정하지 않는다.
- caller가 결과에서 answer, evidence state, unknown, next action을 실제로 복구할 수 있는지 본다.
- session/worker boundary를 넘는 resumption은 stale state를 현재 source와 다시 대조한 근거가 필요하다.

Well-formed definition이나 generated representation의 일치만으로 invocation, independence, orchestration behavior를 증명하지 않는다. Repeated/adversarial trial이 주된 목적이면 `mols-agent-asset-validator`를 사용한다.
