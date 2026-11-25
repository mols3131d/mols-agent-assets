---
name: mols-coding-context-python
description: >-
  Python-specific judgment when Python semantics or runtime behavior materially affect the task. Select only with mols-coding-context; reuse while in context. Exclude incidental Python, non-code administration, factual lookup, and prose-only work.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
---

- Scope `try` to the intended failure source; unrelated calls can raise the same exception.
- Don't change runtime behavior solely to satisfy static typing or hide unresolved type uncertainty with casts, `Any`, or suppressions. Preserve runtime-consumed annotations.
- Diagnose import failures from package layout, entrypoint, and invocation before using `sys.path`, `PYTHONPATH`, or cwd workarounds.
- Respect asyncio event-loop ownership and task lifetime, including blocking work and failure propagation. Propagate cancellation unless the owning scope intentionally handles it; don't bypass the owner with `asyncio.run()` or a new loop.
- Judge thread safety and parallelism by documented target interpreter/build guarantees, not assumptions about the GIL or built-in atomicity.
