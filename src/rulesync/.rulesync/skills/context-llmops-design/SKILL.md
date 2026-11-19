---
name: context-llmops-design
description: >-
  Load LLMOps design context when deciding which tasks need an LLM or agent versus deterministic code, and how model decisions relate to trusted execution. Use for agent or data-pipeline architecture design and review. Do not use for routine implementation, prompt editing, or model benchmarking alone.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
---

# LLMOps Design Context

Use the existing project architecture and contracts to decide whether an LLM adds value. Do not introduce an agent framework merely to automate a deterministic workflow.

## Design Decisions

- **Deterministic first:** Use existing code, queries, schemas, and validators for reproducible decisions. Delegate only interpretation, investigation, or tool selection where model judgment has a concrete advantage.
- **Authority stays outside the model:** Model outputs are proposals, not verified facts or permission to change state. Existing services own validation and execution; do not add new approval steps to already authorized paths without a requirement.
- **Make uncertainty observable:** Ground agent decisions in tool evidence, keep tools scoped to the task, and define what happens when evidence is absent or contradictory. Test deterministic contracts separately from model-dependent behavior; trace the latter only where useful.

## References

Load only sources needed for the active design question, and verify current APIs before implementation.

| Need | Reference |
| --- | --- |
| Explicit state transitions and branching | [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview) |
| Planning and specialist agent delegation | [Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview) |
| LLM execution traces | [Langfuse](https://langfuse.com/docs/observability/get-started) |
| Vendor-neutral telemetry conventions | [OpenTelemetry](https://opentelemetry.io/docs/specs/semconv/) |
