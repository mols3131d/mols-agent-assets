# Inspection Rules

이 문서는 consistency 판단과 검증의 세부 규약입니다.

## Auto-first controls

```yaml
repository: auto
target: auto
relations: auto
rule_sources: auto
scope: auto
baseline: auto
exclude: auto
loops: auto
output: auto
```

고정 directory, 언어, framework, test convention을 전제하지 않습니다. target anchor에서 직접 reference, registration, consumer, dependency, rule source, validation counterpart 순으로 bounded relation frontier를 구성합니다.

## Expected source

Expected는 resolved `rule_sources`, user-specified contract, and baseline에서 결정합니다. 고정된 universal source-type 순서를 적용하지 않습니다.

각 candidate source에 대해 확인합니다.

- **Normativity:** 요구를 정의하는가, 예시나 설명인가
- **Applicability:** component, version, environment, feature state에 적용되는가
- **Activity:** active인가, historical·superseded·proposal-only인가
- **Specificity:** target relation에 얼마나 직접적이고 구체적인가
- **Revision alignment:** 검사 snapshot 또는 comparison에 유효한가
- **Enforcement evidence:** build, lint, schema, validation, ownership, registration에 실제로 연결되는가
- **Repository recognition:** 다른 active artifact가 source를 authority로 참조하는가

사용자가 `rule_sources` 순서를 명시하면 그 순서를 우선합니다. `auto` 후보 간 authority가 불명확하면 같은 unresolved tier로 남깁니다.

## Gap types

| Type | Required evidence |
| --- | --- |
| `contradiction` | 동일 relation과 scope에 동시에 적용되는 source가 양립 불가능한 상태를 주장함 |
| `omission` | expected source가 counterpart를 요구하고 bounded alternate search로 부재를 확인함 |
| `drift` | 함께 변경되어야 할 artifact 중 한쪽만 진전된 change 또는 revision evidence가 있음 |
| `stale-reference` | reference target이 이동·삭제·개명·대체되었고 유효한 compatibility path가 없음 |
| `revision-mismatch` | target relation과 다른 revision 또는 baseline이 적용됨 |
| `handoff-gap` | upstream-to-downstream 전달 과정에서 필수 정보가 유실·변형·미전달됨 |
| `validation-gap` | validation artifact가 구현된 동작과 다른 version·scope·contract를 검증함 |

중복 가능성이 있을 때 root cause 기준 분류 순서:

1. `revision-mismatch`
1. `stale-reference`
1. `validation-gap`
1. `handoff-gap`
1. `omission`
1. `drift`
1. `contradiction`

이 순서는 rule-source authority 순서가 아니라 gap classification tie-breaker입니다.

## Rule and convention findings

- explicit mandatory rule 위반은 direct evidence와 counterevidence가 있으면 `verified` 가능
- recommendation 위반은 mandatory로 표현하지 않음
- executable configuration은 실제 target에 적용되는 wiring이 확인되어야 함
- repeated convention은 mandatory authority가 확인되지 않으면 `unresolved`만 허용
- 외부 업계 관행, 모델 취향, 일반 best practice는 repository rule로 사용하지 않음

## Adversarial verification

각 candidate finding은 다음 반증 가능성을 확인합니다.

- alias, rename, replacement
- registration, manifest, or index
- compatibility layer and redirect
- feature flag and versioned contract
- migration and intentional deferral
- generated authority and parameterized validation
- alternate identifier and direct dependency
- target snapshot versus PR base/head revision
- rule-source scope, supersession, and exception clauses

Zero-result search만으로 omission을 확정하지 않습니다. Expected location, alternate name, registration, manifest, index와 직접 relation 범위를 확인해야 합니다.

## Status

- `verified`: direct evidence가 gap type 기준을 만족하고 counterevidence 검토를 통과
- `unresolved`: 관련성은 있지만 authority, absence, revision, applicability, or mandatory status를 확증하지 못함
- disproved 또는 out-of-scope: 보고서에서 제외

추론은 evidence의 의미를 설명할 수 있지만 단독으로 `verified`를 만들 수 없습니다.

## Result and coverage

Result:

- `findings`
- `incomplete`
- `no-verified-findings`

Coverage:

- `bounded-complete`
- `partial`
- `blocked`

`no-verified-findings`는 기록된 scope와 evidence 안에서 verified gap을 찾지 못했다는 뜻이며 전체 repository 일관성 보장이 아닙니다.
