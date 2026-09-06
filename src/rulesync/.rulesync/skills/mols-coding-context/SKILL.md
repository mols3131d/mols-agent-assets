---
name: mols-coding-context
description: >-
  Core engineering judgment for code-facing tasks, including implementation,
  modification, debugging, testing, refactoring, review, code-facing API or
  data-model changes, dependency decisions, performance and maintainability work,
  and code analysis that requires engineering judgment. Select for simple and
  routine coding tasks too. This is the main coding-context Skill; language-specific
  add-ons may supplement it when material. Adds judgment only, not the task workflow.
  Do not select for pure factual programming lookup, repository administration with
  no code-facing work, or non-code writing where code is incidental.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
---

# Mols Coding Context

Code-facing task의 **language-independent core engineering judgment**를 제공한다. Language add-on은 이 core를 대체하지 않고 필요한 언어별 판단만 추가한다.

## Contract

- 사용자 요구, repository contract, observable compatibility, safety/security와 target runtime contract가 일반 선호보다 우선한다.
- 현재 task와 change surface에 material한 판단만 적용한다. Skill이 선택됐다는 이유로 주변 code를 정리하거나 모든 항목을 checklist처럼 수행하지 않는다.
- 기존 boundary, caller, data flow, state ownership, failure behavior, tests와 local convention을 필요한 만큼 먼저 이해한다.
- 유효한 접근이 여러 개면 **effectiveness → operability → simplicity → elegance**를 기본 tie-breaker로 사용하고, material한 불확실성이 있으면 reversible choice를 선호한다.

## Change and Complexity

- **Smallest coherent change**를 선호한다. 줄 수보다 변경되는 개념과 contract surface를 최소화한다.
- KISS, YAGNI, DRY, SRP를 pattern count나 stylistic purity로 적용하지 않는다.
- Abstraction은 stable concept, invariant 또는 ownership을 실제로 모을 때만 추가한다.
- Speculative configuration, extension point, cache, concurrency, dependency, framework와 future-proofing은 현재 필요와 evidence가 있을 때만 추가한다.
- 새 dependency는 제거하는 implementation, maintenance, operational, security 또는 correctness burden이 도입 비용보다 클 때 사용한다.
- Functional change와 큰 mechanical refactor를 함께 하면 review, rollback, diagnosis 또는 verification이 materially 어려워지는 경우 분리한다.
- Local problem을 evidence 없이 architecture problem으로 확대하지 않는다.

## Preserve Contracts and Failure Meaning

- Candidate change가 건드릴 수 있는 return value, ordering, exception, state, side effect, serialization, registration, config lookup와 material performance 같은 observable contract를 확인한다.
- Readability나 cleanup 명목으로 behavior를 조용히 바꾸지 않는다.
- `failed`, `absent`, `unknown`, `empty`가 caller decision을 바꾸면 의미를 보존한다.
- Failure를 `None`, empty collection, false-like value 또는 success-shaped fallback으로 숨기지 않는다. Caller contract가 실제로 그 의미를 받아들일 때만 fallback을 사용한다.
- Diagnose, recover 또는 verify하는 데 필요한 failure context를 보존한다.

## Boundaries and Operational Machinery

- External, model, tool, network, storage와 config input은 필요한 boundary에서 shape와 semantics를 확인한다.
- Dynamic shape나 permissive default가 uncertainty를 숨기면 더 명확한 representation 또는 validation boundary를 검토한다.
- Retry, timeout, idempotency, concurrency, caching과 observability는 실제 failure, latency, load 또는 ownership requirement가 있을 때만 도입한다.
- Side effect가 있으면 retry 또는 reconciliation semantics를 먼저 확인한다.
- Generated or external text를 executable command, code 또는 privileged action으로 승격하는 경계는 trust와 capability를 명시적으로 다룬다.

## Legibility and Verification

- Control flow, data flow, state와 ownership을 가능한 한 직접 드러낸다.
- Comments와 declaration documentation은 code narration보다 non-obvious contract, constraint, consequence와 evidence-backed rationale에 사용한다.
- 확인되지 않은 rationale를 code shape만 보고 만들지 않는다.
- Changed behavior와 material failure path를 **cheapest useful level**에서 검증한다.
- 실행하지 않은 test, benchmark, runtime observation이나 compatibility를 검증했다고 주장하지 않는다.
- Stable deterministic invariant는 가능하면 formatter, linter, type checker, schema, test 또는 CI가 소유하게 한다.
- Version-sensitive behavior는 memory보다 current authoritative source와 runtime evidence를 우선한다.

## Boundary

이 Skill은 language-independent coding judgment의 core다. 특정 language의 exact semantics, repository-specific policy, task-specific workflow, specialized diagnosis 또는 deterministic tooling contract를 복제하지 않는다.
