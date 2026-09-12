---
name: mols-coding-context-python
description: >-
  Python coding-agent add-on for implementation, debugging, refactoring, review, or
  testing that materially involves Python code or executable behavior. Select only
  together with mols-coding-context. Prevents recurring Python agent anti-patterns
  around exception handling, runtime typing and validation, imports and entrypoints,
  async and concurrency, shell or dynamic execution, and Python performance
  mechanisms. Do not select for incidental Python files or mentions, repository or
  tooling administration, factual lookup, or prose-only work.
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
- Import/package failure를 `sys.path`, `PYTHONPATH` 또는 working-directory mutation으로 먼저 우회하지 않는다. Package layout, entrypoint와 실행 방식(`python -m` 포함)을 확인하고 ambient cwd에 우연히 의존하는 import를 만들지 않는다.
- Async code에서는 blocking work, event-loop owner, task lifetime, cancellation과 failure propagation을 실제 lifecycle에 맞춘다. Event loop를 소유하지 않는 library code나 실행 중인 async context에서 새 loop나 `asyncio.run()`으로 경계를 숨기지 않고, cancellation을 ordinary error로 삼키지 않는다.
- Concurrent code의 correctness를 GIL이나 built-in operation의 구현상 atomicity에 맡기지 않는다. Shared mutable state의 owner와 필요한 synchronization contract를 target interpreter/build에 맞게 명시한다.
- Shell semantics가 필요하지 않으면 structured argv나 direct API를 우선한다. `shell=True`, `eval`, `exec` 같은 token 자체를 unconditional defect로 취급하지 않는다.
- Python 성능 통념만으로 `async`, threads, processes, native/vectorized path, memoization 또는 data-structure 교체를 선택하지 않는다. Target interpreter/build에서 실제 gain을 확인한다.
