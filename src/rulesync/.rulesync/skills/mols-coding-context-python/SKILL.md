---
name: mols-coding-context-python
description: >-
  Python coding-agent add-on for implementation, debugging, refactoring, review, or
  testing that materially involves Python code or executable behavior. Select only
  together with mols-coding-context. Prevents recurring Python agent anti-patterns
  around exception handling, runtime typing and validation, async and cancellation,
  shell or dynamic execution, and Python performance mechanisms. Do not select for
  incidental Python files or mentions, repository or tooling administration,
  factual lookup, or prose-only work.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
---

- 처리할 exception과 failure contract를 식별하고 `try` scope를 실제 failure source 주변으로 좁힌다.
- Type annotation은 runtime validation이 아니다. Annotation만을 이유로 runtime check, coercion, default를 추가하지 않고 material한 boundary semantics만 확인한다.
- Import/package 문제를 `sys.path` 수정, `PYTHONPATH` 주입 또는 working-directory 변경으로 먼저 우회하지 않는다. Package layout, entrypoint와 실행 방식을 확인하고 ambient cwd에 우연히 의존하는 import를 만들지 않는다.
- Async/concurrent code에서는 blocking work, task owner와 lifetime, cancellation, failure propagation과 event-loop ownership을 실제 lifecycle에 맞춘다. Cancellation을 ordinary error로 삼키지 않으며, 상위 caller/runtime이 event-loop lifecycle을 소유하면 `asyncio.run()`이나 새 loop 생성으로 그 경계를 우회하지 않는다.
- Shared mutable state의 correctness를 GIL이나 문서화되지 않은 built-in operation의 atomicity에 의존시키지 않는다. 동시성의 correctness와 병렬 실행 가능성은 target interpreter/build의 documented guarantees와 실제 concurrency model에 맞춰 판단한다.
- Shell semantics가 필요하지 않으면 structured argv나 direct API를 우선한다. `shell=True`, `eval`, `exec` 같은 token 자체를 unconditional defect로 취급하지 않는다.
