---
name: code-comprehension-refactor
description: Use this skill to refactor existing code so it is easier to understand while preserving observable behavior, caller-visible contracts, and material performance characteristics. Trigger for code with opaque representations, hidden conventions, difficult control or state reasoning, unnecessary indirection, abstraction mismatch, mixed responsibilities, or code that is short but mentally expensive to decode. Do not use when only docstrings or comments need improvement; use clarify-code. Do not use for feature work, correctness fixes, performance optimization, public API redesign, or architecture redesign.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
---

# Code Comprehension Refactor

코드의 observable behavior, 실제 usage·contract surface와 task에 material한 performance characteristic을 보존하면서 **executable code 자체의 comprehension cost를 줄인다.**

목표는 코드를 더 짧게 만드는 것이 아니다. 독자가 현재 task에 필요한 mental model을 만들기 위해 수행하는 불필요한 lexical/domain decoding, representation 해독, 탐색, navigation, control-flow simulation과 state·ordering 추적을 줄인다.

## Arguments

```yaml
target: auto
scope: auto
validation: auto
```

| Argument | `auto` 동작 |
| --- | --- |
| `--target <value\|auto>` | 요청, 선택 영역 또는 현재 변경에서 이해 비용이 큰 executable code를 식별한다. |
| `--scope <value,...\|auto>` | mutation은 target과 필요한 coupled code surface로 제한한다. Preservation 판단을 위한 caller·entrypoint·test·contract·registration/config 같은 context read는 적용되는 user/repository scope와 authority 안에서 가장 좁게 수행하며, 읽은 surface에 write authority가 생기지는 않는다. |
| `--validation <command\|auto\|none>` | 변경한 transformation과 실제 preservation envelope를 확인할 가장 작은 유효한 validation을 선택한다. |

명시된 argument를 우선한다. 범위나 현재 contract가 불명확하면 추측으로 확대하지 않는다.

## Core Decision Contract

### One Coherent Bottleneck

한 taxonomy label이나 code smell을 고치는 것이 아니라 **하나의 coherent comprehension bottleneck 또는 root-cause cluster**를 해결한다.

다음 reader work가 실제로 material한지 본다.

- generic/abbreviated 표현을 domain meaning으로 번역함
- positional, boolean, sentinel 또는 generic shape의 규칙을 복원함
- hidden dependency·registration·convention을 찾아 연결함
- semantic gain 없는 helper/wrapper를 이동하며 관계를 다시 조립함
- compound/negative flow를 머릿속에서 simulation함
- mutation, phase, ordering과 mode를 동시에 추적함
- generic abstraction을 실제 domain model로 반복 번역함

하나의 root cause를 제거하기 위해 naming+representation 또는 control+state처럼 tightly coupled edits가 함께 필요할 수 있다. 이를 unrelated cleanup까지 넓히는 근거로 사용하지 않는다.

### Preservation before Transformation

Executable refactor를 고르기 전에 **무엇이 관찰되거나 의존되는지** 먼저 확인한다.

Preservation surface는 public caller에 한정되지 않는다. Target에 따라 다음이 contract가 될 수 있다.

- return value/type/ordering과 exception semantics
- state mutation, persistence, lifecycle, idempotency와 side-effect ordering
- symbol name, import/path, signature, shape 또는 identity
- framework callback, hook, plugin/DI registration과 generated-code coupling
- config/string/dynamic lookup, reflection, serialization 또는 schema/persisted representation
- log/event/failure visibility처럼 실제 consumer가 의존하는 observability
- latency, complexity, allocation, I/O/query count처럼 task에 material한 performance characteristic

모든 항목을 기계적으로 조사하지 않는다. **후보 transformation이 실제로 건드릴 수 있고 현재 consumer가 의존할 수 있는 surface만** 확인한다. Public/private visibility나 tool의 static reference 결과만으로 safety를 단정하지 않는다.

Tests, static analysis와 refactoring-tool preview는 preservation evidence가 될 수 있지만 자동으로 complete specification이나 proof가 되지는 않는다. 위험한 transformation의 preservation 근거가 약하면 더 작은 안전한 change를 선택하거나 중단한다.

Behavior preservation을 위해 함께 갱신해야 하는 consumer·registration·shape가 mutation scope 밖에 있으면 target만 부분 변경하지 않는다. 적용되는 scope policy와 authority가 허용하면 필요한 최소 scope expansion을 거치고, 그렇지 않으면 기존 contract를 유지하거나 handoff/no-op으로 남긴다.

### Net Comprehension Gain

Intervention은 한 cognitive dimension만 최적화하지 않는다. 줄어드는 reader work와 새로 생기는 reader work를 함께 본다.

새 type/helper/file, local-only synonym, duplicated knowledge, extra navigation, ceremony 또는 broader coupling이 추가된다면 그 비용보다 기존 decoding·search·simulation cost가 더 material하게 줄어드는지 확인한다. 숫자 score는 만들지 않는다.

## Workflow

1. 적용되는 repository/source instructions와 target code를 읽고, 현재 task에서 누가 어떤 mental model을 만들어야 하는지 확인한다.
1. **Preservation before Transformation.** 후보 change가 영향을 줄 수 있는 observable behavior와 usage·contract surface를 식별한다. Caller, entrypoint, test, current contract와 relevant registration/config/tooling context를 필요한 만큼 확인하고, known hot path나 performance budget이 있으면 함께 보존 대상으로 둔다.
1. 가장 material한 **coherent bottleneck/root-cause cluster**를 찾는다. 원인이 불명확하거나 여러 cost source의 trade-off가 판단을 바꿀 수 있으면 [Diagnosis](references/diagnosis.md)을 읽는다.
1. Concern을 분리한다. Executable comprehension problem은 이 Skill이 다루되, independent prose need는 `clarify-code`, correctness defect는 correctness work, genuine optimization은 performance work, system boundary redesign은 architecture-level work로 분리한다. 한 sibling concern 때문에 valid comprehension work 전체를 버리지도, 다른 concern을 readability 명목으로 흡수하지도 않는다.
1. 후보 transformation이 줄이는 reader work와 새로 만드는 conceptual surface를 비교해 **smallest safe coherent change**를 선택한다. Rename, move, extract, inline, representation/control-state change처럼 preservation precondition이 material할 수 있거나 transformation 선택이 단순하지 않으면 [Interventions](references/interventions.md)을 읽고 현재 language·repository·tooling contract에서 relevant risk를 확인한다.
1. 필요한 executable code만 수정한다. 한 root cause를 제거하는 tightly coupled edit는 함께 할 수 있지만 unrelated cleanup, speculative abstraction 또는 future-proofing을 섞지 않는다. Preservation에 필요한 coupled consumer update가 write scope 밖이면 부분 mutation을 수행하지 않는다.
1. 변경 전 확인한 preservation envelope를 기준으로 after state를 검증한다. Test coverage의 충분성, dynamic/hidden usage, characterization baseline, performance 또는 verification gap이 material하면 [Validation](references/validation.md)을 읽는다. Tests나 tooling 결과만으로 확인되지 않은 equivalence를 과대 주장하지 않는다.
1. Caller와 maintainer 관점에서 다시 읽고, bottleneck이 실제로 줄었는지와 새 terminology·indirection·ceremony·coupling이 더 큰 이해 비용을 만들지 않았는지 확인한다. 변경, 보존 근거, 실제 수행한 validation, sibling concern과 남은 uncertainty만 짧게 보고한다.

한 coherent bottleneck이 충분히 해소되면 중단한다. 안전한 refactor가 가능하더라도 net comprehension gain이 없으면 수정하지 않는다. Material preservation evidence가 부족한 고위험 transformation은 더 작은 intervention으로 줄이거나 중단한다.

## Progressive Disclosure

Common-path 판단은 이 `SKILL.md`가 소유한다. 다음 세부 판단이 실제로 필요할 때만 reference를 읽는다.

- bottleneck의 root cause, abstraction 가치, usage surface 또는 cognitive trade-off가 불명확하면 [Diagnosis](references/diagnosis.md)
- transformation 선택, tightly coupled edit, rename/move/extract/inline/representation/control-state의 preservation risk가 단순하지 않으면 [Interventions](references/interventions.md)
- tests/contract가 불완전·충돌하거나 dynamic usage, characterization, material performance, before/after equivalence 판단이 단순하지 않으면 [Validation](references/validation.md)

Reference를 읽었다는 이유로 mutation scope나 operational authority가 넓어지지는 않는다.

## Boundaries

- 기능, observable behavior, relevant usage·contract surface, error semantics 또는 material performance characteristic을 readability 명목으로 변경하지 않는다.
- public API뿐 아니라 framework discovery, registration, reflection, config/string lookup, serialization처럼 현재 consumer가 의존하는 non-public surface도 확인 없이 변경하지 않는다.
- behavior-preserving refactor가 scope 밖 consumer의 coordinated mutation을 요구하면 target만 부분 변경하지 않는다. Authorized scope expansion, contract 유지 또는 handoff/no-op 중 적용 가능한 경로를 선택한다.
- performance를 개선하거나 최적화하는 것이 목적이면 이 Skill의 범위를 벗어난다.
- line count, 함수 수, class 수, abstraction 수, hop count를 단순함의 proxy로 사용하지 않는다.
- tuple, dict, boolean, helper, abstraction, one-liner 자체를 문제로 보지 않는다. 실제 misunderstanding risk와 reconstruction cost를 판단한다.
- stable domain concept, invariant, validation, compatibility boundary, reuse 또는 volatile detail encapsulation을 제공하는 abstraction은 단순히 explicit하거나 local하게 만들기 위해 제거하지 않는다.
- comment나 declaration documentation만 고치면 되는 concern은 `clarify-code`가 소유한다. Structural refactor와 independent prose concern이 함께 있으면 concern별로 분리한다.
- public API redesign, dependency architecture 변경, component boundary 재설계처럼 system-level architecture decision이 주목적인 작업은 수행하지 않는다.
- correctness defect가 의심되면 refactor가 그 defect를 우연히 고치거나 새 contract로 고정하지 않게 분리해 보고한다.
- test를 약화하거나 existing failure를 숨겨 behavior preservation을 증명하지 않는다. Test가 통과했다는 사실만으로 untested contract까지 보존됐다고 주장하지 않는다.
- 실행하지 않은 test, benchmark, usage analysis 또는 validation을 수행했다고 보고하지 않는다.
