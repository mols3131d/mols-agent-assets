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

- 처리할 exception과 failure contract를 식별하고 `try` scope를 실제 failure source 주변으로 좁힌다. Broad catch로 unrelated failure를 정상 fallback으로 바꾸지 않는다.
- Type annotation은 runtime validation이 아니다. Annotation만을 이유로 runtime check, coercion, default를 추가하지 않고 material한 boundary semantics만 확인한다.
- Async/concurrent code에서는 blocking work, task owner와 lifetime, cancellation, failure propagation을 실제 lifecycle에 맞춘다. Cancellation을 ordinary error로 삼키지 않으며 `async`나 concurrency를 일반적인 개선책으로 도입하지 않는다.
- Shell semantics가 필요하지 않으면 structured argv나 direct API를 우선한다. `shell=True`, `eval`, `exec` 같은 token 자체를 unconditional defect로 취급하지 않는다.
- Python 성능 통념만으로 `async`, threads, processes, native/vectorized path, memoization 또는 data-structure 교체를 선택하지 않는다. Target interpreter/build에서 실제 gain을 확인한다.
