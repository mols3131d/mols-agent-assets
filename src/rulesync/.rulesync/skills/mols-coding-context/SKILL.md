---
name: mols-coding-context
description: >-
  Core engineering judgment for code-facing implementation, debugging, testing,
  refactoring, review, API or data-model changes, dependency decisions, performance,
  and maintainability work, including routine changes. Select when solving the task
  materially depends on reasoning about code or executable behavior. Language-specific
  add-ons may supplement it. Adds judgment, not workflow. Do not select for factual
  programming lookup, repository administration without code-facing work, or prose-only
  work.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
---

# Mols Coding Context

Code-facing task의 **language-independent core engineering judgment**를 제공한다. Language add-on은 이 core를 대체하지 않고 필요한 언어별 delta만 추가한다.

## Contract

- 사용자 요구, repository contract, observable compatibility, safety/security와 target runtime contract가 일반 선호보다 우선한다.
- 현재 task와 change surface에 material한 판단만 적용한다. Skill이 선택됐다는 이유로 주변 code를 정리하거나 모든 항목을 checklist처럼 수행하지 않는다.
- 기존 boundary, caller, data flow, state ownership, failure behavior와 relevant evidence를 변경에 필요한 만큼 이해한다.
- 유효한 접근이 여러 개면 **effectiveness → operability → simplicity → elegance**를 기본 tie-breaker로 사용하고, material한 불확실성이 있으면 reversible choice를 선호한다.

## Shape the Change

- **Smallest coherent change**를 선호한다. 줄 수보다 변경되는 개념, owner와 contract surface를 최소화한다.
- 삭제·직접화·기존 mechanism 재사용으로 해결되는 문제를 새 abstraction, helper layer, configuration 또는 framework로 먼저 풀지 않는다.
- KISS, YAGNI, DRY, SRP를 pattern count나 stylistic purity로 적용하지 않는다. Abstraction은 stable concept, invariant 또는 ownership을 실제로 모을 때만 추가한다.
- Speculative extension point, cache, concurrency, dependency와 future-proofing은 현재 consumer, failure model 또는 evidence가 있을 때만 추가한다.
- 새 dependency는 제거하는 implementation, maintenance, operational, security 또는 correctness burden이 도입 비용보다 클 때 사용한다.
- Functional change와 큰 mechanical refactor를 함께 하면 review, rollback, diagnosis 또는 verification이 materially 어려워지는 경우 분리한다. Local problem을 evidence 없이 architecture problem으로 확대하지 않는다.

## Preserve Contracts and Failure Meaning

- Candidate change가 건드릴 수 있는 return, ordering, exception, state, side effect, serialization, registration, config lookup와 material performance 같은 observable contract를 확인한다.
- Readability, cleanup 또는 robustness 명목으로 behavior를 조용히 바꾸지 않는다.
- `failed`, `absent`, `unknown`, `empty`가 caller decision을 바꾸면 의미를 보존한다.
- Failure를 `None`, empty collection, false-like value 또는 success-shaped fallback으로 숨기지 않는다. Caller contract가 실제로 그 의미를 받아들일 때만 fallback을 사용한다.
- Diagnose, recover 또는 verify하는 데 필요한 failure context를 보존한다.

## Boundaries and Operational Machinery

- External, model, tool, network, storage와 config input은 downstream decision에 material한 shape와 semantics를 필요한 boundary에서 확인한다.
- Retry, timeout, idempotency, concurrency, caching과 observability는 실제 failure, latency, load 또는 ownership requirement가 있을 때만 도입한다. Side effect가 있으면 retry 전에 idempotency 또는 reconciliation semantics를 확인한다.
- “robustness”를 이유로 guard, fallback, retry, cache, configuration과 abstraction을 한꺼번에 추가하지 않는다. 각 mechanism은 해결하는 concrete failure 또는 constraint가 있어야 한다.
- Generated, user, model, tool 또는 external text를 executable command, code 또는 privileged action으로 승격하는 경계는 trust와 capability를 명시적으로 다룬다.
- Control flow, data flow와 state ownership을 가능한 한 직접 드러내고, shared invariant나 실제 reuse가 없는 generic layer로 숨기지 않는다.

## Evidence-Driven Optimization

Performance, resource use 또는 material maintenance cost의 최적화가 실제 scope이거나 evidence가 bottleneck을 가리킬 때만 적용한다.

1. **Target** — 개선하려는 metric, constraint 또는 cost와 대표 workload를 정한다. 측정 가능한 문제라면 practical한 baseline을 먼저 확보한다.
2. **Locate** — 추측이나 folklore보다 profile, benchmark, trace, complexity/data-flow evidence로 dominant cost를 찾는다.
3. **Reduce first** — cache, concurrency, dependency 또는 architecture를 추가하기 전에 불필요한 work, indirection, allocation, data movement와 repeated I/O를 제거할 수 있는지 본다.
4. **Change narrowly** — 가장 작은 owner에서 최적화하고 observable behavior와 failure semantics를 보존한다. 의도적인 trade-off가 contract를 바꾸면 숨기지 않는다.
5. **Compare and stop** — 같은 representative condition에서 before/after를 비교한다. 목표가 충족됐거나 추가 복잡성보다 gain이 작거나 evidence가 더 이상 material bottleneck을 지지하지 않으면 멈춘다.

Benchmark, profile 또는 representative runtime evidence를 실행하지 않았다면 성능 개선을 측정했다고 주장하지 않는다.

## Verification and Stop

- Changed behavior와 material failure path를 **cheapest useful level**에서 검증하되, acceptance가 end-to-end behavior라면 lower-level test만으로 완료를 선언하지 않는다.
- 실행하지 않은 test, benchmark, runtime observation이나 compatibility를 검증했다고 주장하지 않는다.
- Stable deterministic invariant가 실제로 필요하면 가능한 한 이미 사용하는 formatter, linter, type checker, schema, test 또는 CI 같은 direct mechanism이 소유하게 한다. 새 tooling은 그 자체가 필요할 때만 추가한다.
- Version-sensitive behavior는 memory보다 current authoritative source와 target runtime evidence를 우선한다.
- Acceptance와 material regression path가 충분히 확인되고 evidence-backed blocker가 없으면 멈춘다. Hypothetical polish나 unrelated cleanup을 새 scope로 만들지 않는다.

## Boundary

이 Skill은 language-independent coding judgment의 core다. 특정 language의 exact semantics, repository-specific policy, task-specific workflow, specialized diagnosis, optimization tooling 또는 deterministic tooling contract를 복제하지 않는다.
