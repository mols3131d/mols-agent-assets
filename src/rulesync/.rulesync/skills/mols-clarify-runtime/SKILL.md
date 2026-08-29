---
name: mols-clarify-runtime
description: >-
  Use this skill to understand or reduce runtime understanding debt when actual
  execution paths, decisions, state transitions, external actions, or failure
  causes in existing code or tests are hard to reconstruct. Start by observing
  the smallest existing executable scenario and native runtime evidence. Use
  bounded transient observation only when needed, and maintain runtime evidence
  only when the same question should remain answerable on future executions or
  the user explicitly requests that surface. Preserve observable behavior and
  existing caller or consumer contracts. Do not use for defect debugging,
  correctness review, test design, monitoring or telemetry-platform design,
  performance profiling, or feature implementation.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
---

# Mols Clarify Runtime

기능이나 domain behavior를 추가하지 않고 runtime 이해 부채를 줄인다. **실행 후 답하기 어려운 가장 중요한 복원 질문 하나를 고르고, 먼저 기존 실행과 evidence를 관찰한다. 현재 조사만으로 충분하면 변경하지 않고, future execution에서도 같은 질문을 반복해서 복원해야 할 때만 가장 작은 runtime evidence를 유지한다.**

코드를 읽는 것 자체가 어렵다면 `clarify-code`, defect 판단은 review/debugging 책임이다. 이 Skill은 기존 소스 코드와 테스트 코드가 실제로 어떻게 실행되는지 관찰하고, 실행 경로·결정·상태 변화·외부 작업·실패 원인을 복원하는 데 집중한다.

## Arguments

```yaml
target: auto
scope: auto
evidence: auto
validation: auto
```

| Argument | `auto` 동작 |
| --- | --- |
| `--target <value\|auto>` | 요청이나 실행 경계에서 runtime 이해 대상을 식별한다. |
| `--scope <value,...\|auto>` | target과 직접 관련된 entrypoint, caller, runtime surface와 test까지만 포함한다. |
| `--evidence <value\|auto>` | 기존 observation surface를 먼저 사용하고, 필요하면 future execution에 유지할 가장 작은 runtime evidence 변경을 선택한다. |
| `--validation <command\|auto\|none>` | behavior 보존과 evidence 유효성을 확인할 가장 작은 기존 validation을 선택한다. |

명시된 argument를 우선한다. 실행 의미나 책임 경계가 불명확하면 추측으로 instrumentation을 확대하지 않는다.

## Workflow

1. 적용되는 project instructions와 target, entrypoint/caller, 관련 test, 기존 result·exception·artifact·metadata·history·log·trace 등 현재 runtime evidence를 읽어 실행 경계를 복원한다.
1. 먼저 문제를 분류한다. 주된 병목이 runtime understanding이 아니면 instrumentation하지 않고 해당 책임으로 넘긴다. 경계가 애매하면 [Diagnosis](references/diagnosis.md)를 따른다.
1. **복원 질문 하나**를 정한다: 어떤 경로를 탔거나 타지 않았는가, 왜 결정됐는가, 어떤 input/context가 영향을 줬는가, 무엇이 바뀌거나 만들어졌는가, 무엇이 실패했는가, 어떤 실행·attempt와 연결되는가.
1. **Observe before instrument.** 가능한 경우 기존 test, command, request 같은 가장 작은 executable scenario를 사용하고 result·exception, state delta, output artifact/report, framework-native execution history, existing trace/coverage와 relevant input/config를 관찰한다. 세부 선택은 [Observation](references/observation.md)을 따른다.
1. 기존 observation만으로 질문에 답할 수 있고 future execution에 유지할 evidence 변경이 명시적으로 필요하지 않으면 수정하지 않는다. 부족하면 이번 조사에만 필요한 transient observation인지 future execution에도 evidence를 유지해야 하는지 구분하고, 관찰 공백의 형태를 진단한다.
1. Future execution에 evidence를 유지해야 하면 가장 작은 변경 방식과 owner를 고른다. 기존 evidence를 재사용·보강·이동·병합·제거하는 것을 새 evidence 추가보다 먼저 고려하고, semantic owner뿐 아니라 실제 생성·가용성·필요한 durability·completeness와 correlation도 확인한다. [Evidence](references/evidence.md)와 필요한 경우 [Correlation](references/correlation.md)을 따른다.
1. 선택한 책임 경계만 수정한다. 같은 사실을 여러 surface에 반복하거나 포괄적인 observability 체계를 만들지 않는다.
1. 가능한 경우 같은 좁은 executable scenario로 observable behavior와 기존 contract가 보존되고, 변경 후 남은 evidence만으로 복원 질문에 답할 수 있는지 다시 확인한다. 불필요한 field·event를 제거하고 질문이 해소되면 중단한다.

넓은 audit에서 여러 공백을 발견해도 실제 변경은 복원 질문 하나씩 같은 절차로 처리한다. 실행할 수 없으면 관찰하지 않은 사실을 추측하지 말고 가능한 static evidence와 limitation을 명시한다.

## Progressive Disclosure

현재 판단에 필요한 reference만 읽는다.

| Need | Reference |
| --- | --- |
| 복원 질문, 문제 형태, 우선순위 또는 책임 경계 진단 | [Diagnosis](references/diagnosis.md) |
| 기존 code/test를 좁게 실행하고 현재 behavior를 관찰 | [Observation](references/observation.md) |
| result, exception, artifact/metadata, history, log 등 future runtime evidence의 owner와 viability 선택 | [Evidence](references/evidence.md) |
| retry, async, batch, cross-process 실행의 operation·attempt·causal relation | [Correlation](references/correlation.md) |
| 좋은 log event, context, level, 중복과 noise 판단 | [Logging](references/logging.md) |
| behavior와 contract 보존, evidence 검증 | [Validation](references/validation.md) |

언어·framework·runtime별 구현 방식은 해당 project convention과 현재 authoritative documentation을 따른다. 이 Skill은 특정 test runner, debugger, coverage tool, logging library, telemetry stack 또는 framework artifact schema를 범용 contract로 고정하지 않는다.

## Boundaries

- runtime clarification 명목으로 domain behavior, public contract, acceptance criteria 또는 architecture를 변경하지 않는다.
- **실행을 관찰하는 것과 correctness를 판단하는 것을 구분한다.** 기존 test를 scenario로 실행할 수 있지만 새 test 설계, defect 판정과 수정은 testing 또는 review/debugging 책임이다.
- logging이나 future runtime evidence 추가를 기본 해법으로 가정하지 않는다. 기존 실행 관찰이나 정리·이동·병합·제거가 더 작은 해법이면 그것을 사용한다.
- 한 test/run에서 관찰한 behavior를 다른 input, environment 또는 concurrency 조건으로 일반화하지 않는다.
- 모든 함수 entry/exit, branch, 상태를 기록하지 않는다.
- 같은 사건을 여러 계층이나 surface에 반복 기록하지 않는다.
- secret, credential, 불필요한 raw payload 또는 대용량 데이터를 남기지 않는다.
- clarification만을 위해 새로운 debugger, coverage, logging, tracing, metrics framework나 dependency를 도입하지 않는다.
- 지속적인 상태 감시, alert, SLO와 aggregate health는 monitoring/observability 책임이며 per-execution reconstruction과 혼합하지 않는다.
- 실행하지 않은 validation이나 runtime observation을 수행했다고 보고하지 않는다.
