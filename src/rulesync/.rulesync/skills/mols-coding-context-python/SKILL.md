---
name: mols-coding-context-python
description: >-
  Python-specific engineering judgment for tasks materially dependent on Python
  semantics or runtime behavior: exceptions, typing, imports, asyncio, interpreter
  concurrency, and subprocess execution. Select only with mols-coding-context; exclude
  incidental Python, non-code administration, factual lookup, and prose-only work.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
---

- Scope exception handlers to the intended failure source; the same exception type can arise from unrelated calls.
- Resolve static typing issues without unnecessary runtime changes. Do not hide unresolved type uncertainty with casts, `Any`, or suppressions. Preserve runtime-consumed annotations.
- Diagnose import failures using package layout, entrypoint, and invocation before changing `sys.path`, `PYTHONPATH`, or cwd.
- Account for blocking work, task lifetime, failure propagation, and asyncio event-loop ownership. Preserve cancellation unless intentional handling is consistent with the owning scope; do not bypass the owner with `asyncio.run()` or a new loop.
- Assess thread safety and parallelism against the target interpreter/build and documented guarantees, not assumptions about the GIL or built-in atomicity.
- Judge subprocess argument interpretation by the platform and executable; `shell=False` does not rule out shell interpretation for Windows batch files.
