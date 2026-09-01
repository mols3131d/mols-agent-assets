# Common Validate

Skill, Rule, Subagent 검증에 공통으로 적용되는 evidence와 claim 경계를 다룬다. 유형별 검증 기준은 각 유형의 `validate.md`가 소유한다.

## Choose the claim first

검증은 자산 전체의 품질을 한 번에 판정하는 작업이 아니다. 먼저 확인할 claim과 관찰 가능한 property를 정하고, 그 claim에 필요한 가장 싼 근거부터 사용한다.

1. **Inspection** — ownership, wording, route, scope, structure와 명백한 semantic consistency
1. **Deterministic checks** — project, source framework 또는 native tooling이 이미 소유하는 machine-checkable contract
1. **Projection / integration evidence** — source와 generated output의 동기화, target representation 또는 integration shape가 검증 대상일 때
1. **Runtime evidence** — 실제 selection, application, delegation, behavior, permission 또는 compatibility가 정적 근거로 결정되지 않을 때

Machine-checkable하다는 이유만으로 새 check를 만들지 않는다. Type system, schema, framework validator, generator 또는 native constraint가 같은 property를 직접 보장한다면 그 mechanism을 우선한다.

## Executable checks

별도 executable check는 반복되거나 놓쳤을 때 비용이 크고, output에서 객관적으로 관찰할 수 있으며, 값싸고 안정적으로 판정할 수 있는 property에 집중한다.

- 하나의 판정 logic을 local script, test, CI에 각각 복제하지 않는다.
- generated output이나 route drift는 가능하면 canonical source에서 다시 생성한 결과와 비교한다.
- check가 실패한 것과 check 자체를 실행할 수 없었던 것을 구분한다.
- executable result를 자동으로 blocking verdict로 확대하지 않는다. Feedback 강도는 판정 신뢰도와 위반 비용에 비례해야 한다.
- design, naming, cohesion, abstraction quality처럼 맥락 판단이 필요한 품질은 deterministic result로 대체하지 않는다.

## Claims

- 실행하지 않은 중요한 check는 not run 또는 unknown으로 남긴다.
- inspection, simulation, generated shape를 실제 runtime verification으로 표현하지 않는다.
- structural validity를 semantic quality나 behavioral correctness로 확대하지 않는다.
- source와 projection의 일치는 generator의 semantic correctness 전체를 증명하지 않는다.
- target runtime이 결정하는 behavior는 실제 runtime evidence 없이는 verified라고 주장하지 않는다.
- handoff나 durable working state에 기록된 과거 validation은 현재 source, revision 또는 runtime state와 맞는지 확인하기 전까지 현재 evidence로 승격하지 않는다.

Formal audit, adversarial challenge, repeated trials, runtime trace, regression program, independent reviewer reconciliation이 주된 목적이면 `mols-agent-asset-validator`를 primary로 사용한다.
