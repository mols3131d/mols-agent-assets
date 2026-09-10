---
name: mols-coding-context-python
description: >-
  Python-specific add-on for code-facing tasks materially dependent on Python code
  semantics, runtime behavior, or Python-facing tests. Select only together with
  mols-coding-context. Adds Python-specific judgment for exceptions, async and
  cancellation, runtime validation boundaries, subprocess or dynamic execution,
  and Python performance decisions. Do not select for incidental Python files,
  tooling or mentions, or prose-only edits where Python semantics are irrelevant.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
---

# Mols Coding Context Python

- Version-sensitive Python, standard-library, dependency, or framework behavior는 기억보다 current project/runtime evidence를 우선한다.
- 처리할 exception과 failure contract를 먼저 식별하고 `try` scope를 실제 failure source 주변으로 좁힌다. Broad catch로 programming, parsing, invariant failure를 정상 fallback으로 바꾸지 않는다.
- 불확실하다는 이유만으로 type check, coercion, default, validation, fallback을 추가하지 않는다. Type annotation은 runtime validation이 아니며 필요한 검증은 실제 boundary contract에서 파생한다.
- Async/concurrent code에서는 blocking work, task owner와 lifetime, cancellation, failure propagation을 실제 lifecycle에 맞춘다. `async`나 concurrency를 일반적인 개선책으로 도입하지 않는다.
- Shell semantics가 필요하지 않으면 structured argv나 direct API를 우선한다. External text를 그대로 실행 경계로 넘기지 않으며 `shell=True`, `eval`, `exec` 같은 token만으로 결함을 판정하지 않는다.
- Python 성능 통념만으로 `async`, threads, processes, native/vectorized path, memoization 또는 data-structure 교체를 선택하지 않는다. Target runtime과 representative workload에서 dominant cost를 확인하고 trade-off와 함께 판단한다.
