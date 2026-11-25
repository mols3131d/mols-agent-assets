---
name: mols-coding-context
description: >-
  Engineering judgment for tasks materially involving code or executable contracts,
  including routine coding, design, debugging, testing, refactoring, review, and
  code reasoning. Adds judgment, not workflow. Excludes factual lookup, repository
  administration without code-facing work, and prose-only work.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
---

# Mols Coding Context

언어 독립적인 engineering judgment를 보강하는 context다. 사용자 요구, 정확성, 안전·보안, 실제 repository·caller·runtime contract와 권한이 아래 기본 판단보다 우선한다. 현재 문제에 material한 항목만 적용한다. 별도 workflow, checklist, 도구 호출, 산출물 또는 language add-on 로딩을 강제하지 않는다.

- **Trade-offs.** 유효한 대안은 effectiveness → operability → simplicity → elegance 순으로 판단한다. 동등하면 기존 mechanism과 convention을 따른다. 기존 설계나 사용자 제안도 실질적으로 더 나은 대안이 있으면 근거와 trade-off를 들어 재검토한다. 불확실성이 크면 reversible choice를 선호한다.
- **Smallest coherent change.** 줄 수보다 개념·owner·contract surface를 최소화한다. 삭제·직접화·기존 mechanism 재사용을 우선한다. Maintainability는 control/data flow의 추적 비용과 이해해야 하는 mutable state의 범위로 판단한다. 새 abstraction, config, dependency, automation은 실제 필요와 도입·유지 비용을 상회하는 효과로 정당화한다. 국소 문제를 근거 없이 architecture 문제로 확대하지 않는다. KISS, YAGNI, DRY, SRP를 외형이나 pattern count로 적용하지 않는다. 큰 mechanical refactor가 검토·검증·복구를 어렵게 하면 기능 변경과 분리한다.
- **Data and state modeling.** 실제 domain semantics, invariant와 access pattern에 맞는 data structure를 선택한다. 반복되는 상태 분기·동기화보다 invalid state를 표현하기 어려운 구조를 선호하되, 국소적이고 단순한 문제에 modeling layer를 추가하지 않는다.
- **Observable contracts.** 변경이 영향을 주는 caller, return, ordering, failure, state, side effect, serialization, registration, configuration과 material performance를 고려한다. Readability나 robustness를 명목으로 동작을 조용히 바꾸거나 요청 밖의 문제까지 정리하지 않는다. 의도적인 contract 변경은 명시한다.
- **Failure and trust boundaries.** `failed`, `absent`, `unknown`, `empty`가 caller decision을 바꾸면 구분한다. 계약 없는 success-like fallback으로 실패를 숨기지 않고 진단·복구에 필요한 맥락을 보존한다. 정상적으로 발생 가능한 failure와 invariant violation을 구분하고 후자의 원인을 downstream guard나 fallback으로 은폐하지 않는다. External·model·tool input의 material한 shape와 의미를 신뢰 경계에서 확인하되 보장된 invariant를 근거 없이 중복 검증하지 않는다. Text를 executable code·command·privileged action으로 승격할 때 trust와 capability를 구분한다.
- **Operational complexity.** Retry, timeout, idempotency, concurrency, cache, validation, observability는 실제 failure model이나 constraint를 해결할 때만 추가한다. Side effect의 retry는 idempotency 또는 reconciliation 가능성을 전제로 판단한다. 동시성 제어에 앞서 불필요한 shared mutable state를 제거하거나 ownership을 분리할 수 있는지 판단한다. 실제 invariant나 reuse 없이 control/data flow와 state ownership을 generic layer로 숨기지 않는다.
- **Performance.** 실제 제약·bottleneck과 representative workload 및 비교 가능한 baseline에 근거한다. 복잡한 최적화보다 불필요한 work, indirection, allocation, I/O와 data movement 제거를 우선한다. 측정값이 의도한 work를 반영하는지, 작업 생략·cache 효과·측정 잡음이 결론을 왜곡하는지 판단한다. 같은 조건에서 비교하지 않은 성능 향상을 측정했다고 주장하지 않는다.
- **Review signal.** 근거 있는 material defect와 regression을 우선하고, 변경이 유발한 문제와 기존 문제, 불확실한 위험, stylistic preference, optional improvement를 구분한다. 검토의 엄격함을 보이기 위해 finding을 만들거나 충분한 개선에 완벽을 요구하지 않는다.
- **Evidence and acceptance.** 동일한 전제에 의존한 수정이 반복 실패하면 다음 수정안보다 전제의 타당성을 재검토한다. 변경된 계약과 material failure path에 비례해 검증하며, test는 계약 위반을 탐지하고 behavior-preserving change에 불필요하게 결합되지 않아야 한다. 하위 수준의 성공을 end-to-end acceptance로 확대하거나 미실행 검증을 성공으로 표현하지 않는다. Version-sensitive behavior는 현재 authoritative source와 runtime evidence를 우선한다. 결정적 invariant는 기존 도구가 소유할 수 있으면 중복 instruction 대신 그 도구에 맡긴다. 실질적 요구와 regression risk가 해결되면 불필요한 polish를 만들지 않는다.

언어별 semantics, 저장소 정책, 구현·리뷰·테스트 절차, 최적화 도구는 각 책임의 owner에게 맡긴다. 언어별 add-on은 해당 semantics가 material할 때 core와 함께 선택되어 필요한 delta만 더한다.
