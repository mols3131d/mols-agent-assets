# Common Validate

검증은 먼저 확인할 주장을 정하고, 그 주장에 필요한 가장 싼 근거부터 사용한다. 유형별 기준은 각 `validate.md`가 소유한다.

## Evidence

| 근거 | 적합한 주장 |
| --- | --- |
| Inspection | ownership, wording, route, scope, structure, 명백한 의미 일관성 |
| Deterministic check | project/framework가 소유하는 machine-checkable contract |
| Projection / integration | source와 generated output의 동기화, target representation |
| Runtime evidence | 실제 selection, application, delegation, permission, behavior, compatibility |

이미 type system, schema, framework validator, generator, native constraint가 같은 성질을 보장하면 새 check를 만들지 않는다.

별도 executable check는 반복되거나 실패 비용이 크고, output에서 객관적이며 값싸고 안정적으로 판정할 수 있는 성질에만 둔다. 판정 logic을 script/test/CI에 복제하지 않고, generated drift는 가능한 한 canonical source에서 재생성한 결과와 비교한다.

## Claims

- check 실패와 실행 불가를 구분한다.
- 실행하지 않은 중요한 check는 `not run` 또는 `unknown`으로 남긴다.
- structural validity를 semantic quality나 runtime correctness로 확대하지 않는다.
- source와 projection 일치가 generator 전체의 semantic correctness를 증명하지 않는다.
- 과거 handoff의 validation은 현재 source, revision, state와 맞는지 확인하기 전까지 현재 근거가 아니다.
- target runtime이 결정하는 behavior는 runtime evidence 없이는 verified로 주장하지 않는다.

Formal audit, adversarial challenge, repeated trials, runtime trace, regression program, independent reviewer reconciliation은 `mols-agent-asset-validator`의 책임이다.
