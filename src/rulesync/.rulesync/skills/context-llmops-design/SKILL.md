---
name: context-llmops-design
description: >-
  Load task-relevant LLMOps design context and official references when deciding whether and how to delegate work to an LLM or agent. Covers deterministic-first allocation, evidence and execution authority, bounded tools, failure handling, observability, and verification. Do not use for generic LLM explanations, prompt editing, model benchmarking alone, or implementing a settled design.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
---

# LLMOps Design Context

Load only context that can change the current design decision. The project owns requirements, permissions, execution contracts, and acceptance criteria. This Skill neither creates a security policy nor mandates a framework or vendor.

## Decision Context

Establish from existing project and runtime evidence:

- **Outcome:** task, correctness, latency, cost, reproducibility, and failure risk.
- **Existing owner:** deterministic code, schema, rule, query, or service already responsible for the facts or action.
- **Model value:** the specific ambiguity or judgment that a simpler, maintainable deterministic method does not adequately address.
- **Trust boundary:** authoritative evidence, tool scope, side effects, trusted executor, and independently verifiable results.

If deterministic methods suffice, keep the work deterministic and stop. Missing evidence is an unknown, not a reason to invent permissions or policy.

## Design Boundaries

- **Deterministic facts and controls:** Parsing, calculations, validation, schema checks, authorization, state guards, and data mutation belong to their reliable existing owners, not to model judgment.
- **Bounded LLM judgment:** Use models for evidence-based interpretation, investigation, prioritization, or dynamic tool choice only when their contribution is justified. Model output is a proposal, not authoritative evidence, approval, or proof of execution success.
- **Trusted execution:** Keep scheduling, locks, state guards, retries, and recovery with existing executors. Bind actions to caller authority and validated targets. Do not impose blanket human approval on already authorized paths without a project requirement.
- **Tool and failure limits:** Prefer scoped, typed tools with runtime checks and bounded steps, time, context, and cost. No unrestricted shell, SQL write, filesystem, or network permissions. Handle denial, model/tool failure, missing evidence, timeout, stale state, and partial effects with safe rejection or explicit handoff. Retry effects only when idempotency or reconciliation is established.
- **Trace and verify:** Correlate evidence references, tool decisions, run/step IDs, prompt and model revisions, outcomes, errors, latency, and available usage/cost. Minimize sensitive trace data. Use deterministic contract tests and offline fake-model scenarios for safety boundaries; add live-model or human utility evidence only when the outcome requires it. Telemetry and LLM evaluation do not replace domain truth.

For example, a source schema validator determines ingestion readiness; an agent may choose an additional investigation, while the trusted loader alone performs an authorized write.

## Conditional References

Read only the official material relevant to the current decision. Verify version-sensitive details before implementing an integration.

| Design concern | Reference |
| --- | --- |
| Explicit workflow states, branching, recovery | [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview) |
| Multi-step planning, context management, delegation | [Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview) |
| Interoperable telemetry and GenAI traces | [OpenTelemetry semantic conventions](https://opentelemetry.io/docs/specs/semconv/) |
| Tracing when Langfuse is already in scope | [Langfuse tracing](https://langfuse.com/docs/observability/get-started) |
| LangGraph and Langfuse when both are selected | [Langfuse integration](https://langfuse.com/integrations/frameworks/langgraph) |

These links are references, not a dependency or product adoption checklist. Reuse existing adapters and observability before adding parallel machinery.

## Handoff

Supply only the deterministic owner, justification for LLM involvement, evidence and authority boundaries, relevant failure/verification gaps, and links actually needed by the downstream design task. Implementation, tests, installation, and project-specific policy remain with their respective owners.
