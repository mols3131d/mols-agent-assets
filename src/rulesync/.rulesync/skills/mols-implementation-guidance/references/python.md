# Python Guidance

- Scope `try` to the intended failure source; unrelated calls can raise the same exception.
- Type annotations alone do not validate at runtime. Fix static typing without needless runtime changes or masking uncertainty with casts, `Any`, or suppressions; preserve runtime-consumed annotations.
- Diagnose import failures via package layout, entrypoint, and invocation before `sys.path`, `PYTHONPATH`, or cwd workarounds.
- Account for asyncio blocking work, task lifetime, and failure propagation. Propagate cancellation unless intentionally handled under the owning scope's contract; don't bypass loop ownership with `asyncio.run()` or a new loop.
- Judge thread safety and parallelism by documented interpreter/build guarantees, not assumptions about the GIL or built-in atomicity.
