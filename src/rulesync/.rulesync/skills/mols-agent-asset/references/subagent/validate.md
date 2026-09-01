# Subagent Validate

Agent 또는 Subagent 검증에만 필요한 근거와 claim을 다룬다. 공통 검증 원칙은 `../common/validate.md`를 따른다.

- responsibility, delegation condition, context contract, capability, result contract, termination semantics를 직접 확인한다.
- project 또는 source framework가 제공하는 deterministic agent metadata/projection check를 재사용한다.
- target representation이 대상이면 generated agent definition을 확인한다.
- tool availability, permission behavior, nested delegation, isolation, parallelism, independence, handoff behavior를 주장하려면 실제 runtime evidence를 사용한다.

Well-formed agent definition은 runtime이 올바르게 invoke하거나 independence를 보존한다는 증거가 아니다. Repeated 또는 adversarial trial이 주된 목적이면 `mols-agent-asset-validator`를 primary로 사용한다.
