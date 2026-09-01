# Common Validate

Skill, Rule, Subagent 검증에 공통으로 적용되는 evidence와 claim 경계를 다룬다. 유형별 검증 기준은 각 유형의 `validate.md`가 소유한다.

## Evidence

주장에 필요한 가장 싼 근거부터 사용하고 필요할 때만 강화한다.

1. **Inspection** — ownership, wording, links, scope, structure와 명백한 semantic consistency
1. **Deterministic checks** — project 또는 source framework가 이미 소유하는 machine-checkable contract
1. **Projection / integration evidence** — target representation이나 integration behavior가 검증 대상일 때
1. **Runtime evidence** — 실제 selection, application, delegation, behavior, compatibility가 정적 근거로 결정되지 않을 때

기존 validator나 framework check가 소유하는 계약을 별도 구현으로 복제하지 않는다.

## Claims

- 실행하지 않은 중요한 check는 not run 또는 unknown으로 남긴다.
- inspection, simulation, generated shape를 실제 runtime verification으로 표현하지 않는다.
- structural validity를 semantic quality나 behavioral correctness로 확대하지 않는다.
- target runtime이 결정하는 behavior는 실제 runtime evidence 없이는 verified라고 주장하지 않는다.

Formal audit, adversarial challenge, repeated trials, runtime trace, regression program, independent reviewer reconciliation이 주된 목적이면 `mols-agent-asset-validator`를 primary로 사용한다.
