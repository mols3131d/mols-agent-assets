# Subagent Validate

Agent 또는 Subagent 검증에만 필요한 근거와 claim을 다룬다. 공통 검증 원칙은 `../common/validate.md`를 따른다.

## Structural evidence

- responsibility, delegation condition, context contract, capability, result contract, termination semantics를 직접 확인한다.
- handoff가 revision이나 observable state에 의존하면 state basis가 현재 source와 맞는지 확인한다.
- durable handoff가 있다면 canonical knowledge를 복제하지 않고 continuation에 필요한 state만 소유하는지 확인한다.
- project 또는 source framework가 제공하는 deterministic agent metadata/projection check를 재사용한다.
- target representation이 대상이면 canonical source와 generated agent definition의 drift를 확인한다.

## Runtime evidence

Tool availability, permission behavior, nested delegation, isolation, parallelism, independence, handoff behavior를 주장하려면 실제 runtime evidence를 사용한다.

- delegation claim은 실제 caller가 intended condition에서 해당 agent를 사용할 수 있는지 확인한다.
- independence claim은 다른 reviewer의 결론이 brief에 섞이지 않았는지뿐 아니라 runtime isolation이 실제 제공되는지도 구분한다.
- capability claim은 tool 이름이나 metadata 존재만으로 side effect와 permission semantics를 확정하지 않는다.
- handoff claim은 caller가 결과의 answer, evidence state, unknown과 next action을 실제로 복구할 수 있는지 본다.
- session이나 worker 경계를 넘는 resumption을 주장하면 stale state를 현재 source와 다시 대조한 evidence가 필요하다.

Well-formed agent definition은 runtime이 올바르게 invoke하거나 independence를 보존한다는 증거가 아니다. Generated definition의 일치도 orchestration behavior를 증명하지 않는다. Repeated 또는 adversarial trial이 주된 목적이면 `mols-agent-asset-validator`를 primary로 사용한다.
