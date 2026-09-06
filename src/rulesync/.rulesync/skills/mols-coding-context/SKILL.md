---
name: mols-coding-context
description: >-
  Baseline engineering judgment for any task whose active work surface materially
  includes executable code or code-facing software contracts, including code
  analysis or explanation, implementation, modification, debugging, testing,
  refactoring, review, API or data-model changes, dependency decisions,
  performance work, and maintainability work. Select even for simple or routine
  coding tasks and independently alongside any other task-relevant Skill. This
  Skill adds coding judgment only and does not own the task workflow. Do not
  select for pure factual programming lookup, repository administration with no
  code-facing work, or non-code writing where code is incidental.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
---

# Mols Coding Context

현재 code-facing task에 필요한 **language-independent engineering judgment**를 추가한다. 이 Skill은 coding workflow를 만들지 않는다. 구현, 디버깅, 테스트, 리뷰, Git 작업과 결과물 생성은 현재 task와 더 구체적인 authority가 소유한다.

## Contract

- 사용자 요구, repository contract, observable compatibility, safety/security, language/runtime contract가 이 일반 판단보다 우선한다.
- 현재 작업과 변경 surface에 material한 판단만 적용한다. Skill이 선택됐다는 이유로 주변 code를 정리하거나 모든 항목을 checklist처럼 수행하지 않는다.
- 기존 boundary, caller, data flow, state ownership, failure behavior, tests와 local convention을 먼저 이해한다.
- 유효한 접근이 여러 개면 **effectiveness → operability → simplicity → elegance**를 기본 tie-breaker로 사용하고, material한 불확실성이 있으면 reversible choice를 선호한다.

## Change and Complexity

- **Smallest coherent change**를 선호한다. 줄 수가 아니라 변경되는 개념과 contract surface를 최소화한다.
- KISS, YAGNI, DRY, SRP를 pattern count나 stylistic purity로 적용하지 않는다.
- duplication만으로 abstraction을 만들지 않는다. 같은 stable concept, rule 또는 ownership이 함께 바뀌어야 할 때 centralization을 검토한다.
- speculative configuration, extension point, cache, concurrency, dependency, framework와 future-proofing은 현재 필요와 evidence가 있을 때만 추가한다.
- local code problem을 evidence 없이 architecture problem으로 확대하지 않는다.
- 새 helper, wrapper, type, layer가 줄이는 이해 비용보다 terminology, navigation, coupling과 lifecycle cost를 더 만들면 추가하지 않는다.

## Preserve Contracts

변경 전에 candidate transformation이 건드릴 수 있는 observable 또는 consumer-visible contract를 확인한다.

- return value, type, ordering과 exception/failure semantics
- state mutation, persistence, lifecycle과 side-effect ordering
- API, signature, serialization, schema와 persisted representation
- config/string lookup, registration, reflection과 generated-code coupling
- idempotency, retry semantics와 externally visible effects
- task에 material한 latency, I/O/query count 또는 other performance characteristics

Public/private 표시는 safety proof가 아니다. 반대로 확인되지 않은 hidden dependency 가능성만으로 모든 local change를 막지도 않는다. 현재 change가 실제로 영향을 줄 수 있는 surface만 evidence에 맞게 확인한다.

## Preserve Failure and Uncertainty

- 실패를 정상값으로 위장해 downstream 판단을 왜곡하지 않는다.
- `failed`, `absent`, `unknown`, `empty`가 caller나 다음 action을 바꾼다면 구분 가능한 의미로 보존한다.
- broad fallback은 caller가 그 fallback 의미를 실제 contract로 받아들이는 경우에만 사용한다.
- failure context는 diagnose, recover 또는 verify하는 데 필요한 만큼 보존한다.
- convenient default가 malformed, unavailable 또는 unverified input을 valid state처럼 만들지 않게 한다.

특히 agent/tool pipeline에서는 `None`, 빈 collection, false-like value와 success-shaped object가 실패를 숨기면 이후 model 판단과 side effect의 근거가 오염될 수 있다.

## Boundaries

- external, model, tool, network, storage와 config input은 내부 invariant로 사용하기 전에 필요한 boundary에서 shape와 semantics를 확인한다.
- dynamic mapping, permissive coercion 또는 default chain이 uncertainty를 숨기면 더 명확한 representation이나 validation boundary를 사용한다.
- 특정 validation library, schema framework 또는 representation을 universal default로 강제하지 않는다. 현재 system과 필요한 runtime guarantee에 맞춘다.
- generated/model-produced text를 executable command, code 또는 privileged action으로 승격하는 경계는 trust와 capability를 명시적으로 다룬다.

## Side Effects, Retry, Timeout and Concurrency

- retry는 모든 failure에 대한 generic resilience wrapper가 아니다. Retryable failure인지 먼저 구분한다.
- retry에는 attempt/time bound가 있어야 하며, side-effecting operation은 idempotency 또는 reconciliation semantics가 알려진 경우에만 반복한다.
- remote/blocking operation의 timeout과 deadline은 실제 operation boundary와 caller failure policy에 맞춘다.
- concurrency는 throughput 필요, state ownership, task/resource lifetime과 failure propagation이 명확할 때 추가한다.
- background work, cancellation, partial success와 cleanup semantics가 material하면 정상 종료와 실패 경로를 함께 설계한다.

## Legibility

- control flow, data flow, state와 ownership을 가능한 한 직접 드러낸다.
- shorter code, fewer functions, fewer classes와 fewer abstractions 자체를 readability 또는 simplicity의 증거로 사용하지 않는다.
- comments와 declaration documentation은 code를 번역하지 않고 caller contract, non-obvious invariant, external constraint, failure consequence와 evidence-backed rationale를 설명한다.
- 확인되지 않은 historical rationale를 code shape만 보고 만들어내지 않는다.
- structural opacity를 prose로 해설해 덮지 않는다. 구조와 독립적인 durable explanation need는 별도로 판단한다.

## Verification

- required behavior와 preference, observed failure와 hypothetical risk, functional change와 behavior-preserving refactor를 구분한다.
- changed behavior와 material failure path를 **cheapest useful level**에서 검증한다.
- tests가 있다는 사실을 proof로 취급하지 않고, 실행하지 않은 test, benchmark, runtime observation이나 compatibility를 검증했다고 주장하지 않는다.
- stable하고 반복적으로 판정 가능한 invariant는 가능하면 formatter, linter, type checker, schema, test 또는 CI 같은 executable feedback owner로 옮긴다.
- version-sensitive API, library, tool 또는 platform behavior는 memory보다 current authoritative source와 runtime evidence를 우선한다.

## Boundary

이 Skill은 general coding judgment만 소유한다. 특정 language의 exact semantics, repository-specific policy, task-specific procedure, specialized diagnosis/workflow 또는 deterministic tooling contract를 복제하지 않는다.
