---
name: mols-coding-context-python
description: >-
  Python-specific judgment for coding tasks materially dependent on Python semantics or runtime behavior. Extends mols-coding-context; use only alongside it. Load once at task entry unless already in context; reuse while available. Excludes incidental Python, non-code administration, factual lookup, and prose-only work.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
---

- Scope `try` to the intended failure source; unrelated calls can raise the same exception.
- Type annotations alone do not validate at runtime. Fix static typing without needless runtime changes or masking uncertainty with casts, `Any`, or suppressions; preserve runtime-consumed annotations.
- Diagnose import failures via package layout, entrypoint, and invocation before `sys.path`, `PYTHONPATH`, or cwd workarounds.
- Account for asyncio blocking work, task lifetime, and failure propagation. Propagate cancellation unless intentionally handled under the owning scope's contract; don't bypass loop ownership with `asyncio.run()` or a new loop.
- Judge thread safety and parallelism by documented interpreter/build guarantees, not assumptions about the GIL or built-in atomicity.
