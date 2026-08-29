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

코드의 작동, observable behavior, caller-visible contract와 material performance를 보존하면서 **코드 자체를 더 쉽게 이해할 수 있게 리팩터링한다.**

목표는 코드를 더 짧게 만드는 것이 아니다. 독자가 필요한 mental model을 만들기 위해 수행하는 불필요한 번역, 탐색, 추론, 상태 추적과 control-flow simulation을 줄인다.

## Arguments

```yaml
target: auto
scope: auto
validation: auto
```

| Argument | `auto` 동작 |
| --- | --- |
| `--target <value\|auto>` | 요청, 선택 영역 또는 현재 변경에서 이해 비용이 큰 코드를 식별한다. |
| `--scope <value,...\|auto>` | target과 실제 caller·entrypoint, 관련 test, 공유 contract까지만 포함한다. |
| `--validation <command\|auto\|none>` | behavior와 필요한 performance 특성을 보존했는지 확인할 가장 작은 기존 validation을 선택한다. |

명시된 argument를 우선한다. 범위나 현재 contract가 불명확하면 추측으로 확대하지 않는다.

## Workflow

1. 적용되는 repository/source instructions와 target, caller·entrypoint, 관련 test를 읽는다. hot path나 latency·allocation·I/O 민감성이 알려져 있으면 함께 확인한다.
1. 변경 전에 보존할 envelope를 확인한다: observable behavior, caller-visible contract, state와 side effect, error semantics, 그리고 task에 중요한 material performance characteristic.
1. 가장 큰 comprehension bottleneck 하나를 진단한다. 코드가 짧거나 syntax가 단순해도 hidden convention이나 representation을 머릿속에서 복원해야 하면 병목일 수 있다.
1. [Diagnosis](references/diagnosis.md)에 따라 원인을 분류하고, [Interventions](references/interventions.md)에서 가장 작은 coherent change를 선택한다. 최소 변경은 line count가 아니라 **병목을 실질적으로 제거하면서 새 conceptual surface를 가장 적게 추가하는 변경**이다.
1. 실행 코드의 이름, representation, control/state flow, responsibility 또는 indirection을 필요한 만큼만 수정한다. unrelated cleanup이나 미래용 abstraction을 섞지 않는다.
1. 설명을 추가해야만 이해되는 문제라면 prose로 구조 문제를 덮지 않는다. code-local rationale나 caller explanation이 별도로 필요하면 `clarify-code`의 책임으로 분리한다.
1. [Validation](references/validation.md)에 따라 가능한 경우 같은 좁은 validation을 변경 전후에 적용한다. performance-sensitive path라면 기존 benchmark나 동등한 측정 근거가 있을 때 함께 비교한다.
1. caller와 maintainer 관점에서 다시 읽고, 이해 비용이 실제로 줄었는지와 새 indirection·ceremony가 생기지 않았는지 확인한 뒤 변경·보존 근거·validation·남은 risk만 짧게 보고한다.

주된 병목이 해소되면 중단한다. 이해 비용을 실질적으로 줄이지 못하면 수정하지 않는다.

## Progressive Disclosure

현재 판단에 필요한 reference만 읽는다.

- 병목의 원인이나 abstraction 가치가 불명확하면 [Diagnosis](references/diagnosis.md)를 읽는다.
- 어떤 code transformation이 가장 작은 해법인지 불명확하면 [Interventions](references/interventions.md)를 읽는다.
- 구조를 바꾸기 전후 behavior·contract·performance 보존 근거를 확인하려면 [Validation](references/validation.md)를 읽는다.

## Boundaries

- 기능, observable behavior, caller-visible contract, error semantics 또는 material performance characteristic을 readability 명목으로 변경하지 않는다.
- performance를 개선하거나 최적화하는 것이 목적이면 이 skill의 범위를 벗어난다.
- line count, 함수 수, class 수, abstraction 수를 단순함의 proxy로 사용하지 않는다.
- tuple, dict, boolean, helper, abstraction, one-liner 자체를 문제로 보지 않는다. 실제 reconstruction cost와 semantic value를 판단한다.
- stable domain concept, invariant, validation, reuse 또는 volatile detail encapsulation을 제공하는 abstraction은 단순히 hop이 있다는 이유로 제거하지 않는다.
- comment나 docstring만 고치면 되는 요청은 `clarify-code`를 사용한다.
- public API redesign, dependency architecture 변경, component boundary 재설계처럼 system-level architecture decision이 주목적인 작업은 수행하지 않는다.
- correctness defect가 의심되면 clarification과 섞지 않고 별도 correctness 작업으로 분리한다.
- test를 약화하거나 기존 failure를 숨겨 behavior 보존을 증명하지 않는다.
- 실행하지 않은 test, benchmark 또는 validation을 수행했다고 보고하지 않는다.
