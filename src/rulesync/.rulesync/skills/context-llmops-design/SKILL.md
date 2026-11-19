---
name: context-llmops-design
description: >-
  Load decision-relevant context for LLMOps and agent-system design or design
  review: deterministic-first task allocation, justified LLM delegation, trust
  and execution boundaries, evidence, observability, and verification. Use when
  deciding what an LLM or agent should do in a software, data, or operational
  workflow. Do not use for generic LLM explanations, model benchmarking alone,
  prompt editing, or implementing a previously settled design.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
  - agentsskills
---

# LLMOps Design Context

Load the smallest context that changes an LLMOps design decision. This Skill
provides design judgment and authoritative reference links; the active project
owns its requirements, implementation, permissions, and acceptance criteria.
It does not prescribe an agent framework, model provider, or observability vendor.

## Resolve the Decision

Before recommending an LLM or agent, establish only what is material:

- **Task and outcome:** the decision or action, consumer, required correctness,
  latency, cost, reproducibility, and failure tolerance.
- **Existing owner:** deterministic code, schema, rule, query, workflow, tool,
  operator, or service that already performs or authorizes the work.
- **Trust and effects:** authoritative input, available evidence, external data,
  tool permissions, side effects, and the party allowed to execute them.
- **Uncertainty:** the actual ambiguity or judgment that deterministic methods
  cannot meet adequately, including evidence for that limitation.
- **Verification:** independent checks and observable outcomes that can detect
  incorrect reasoning or action.

Reuse current repository and runtime context; do not assume the project has
a particular model, orchestration stack, credential, or observability service.

## Design Defaults

1. **Deterministic first.** If explicit rules, parsing, types, constraints,
   calculations, queries, or existing workflow logic can meet the requirement,
   keep them deterministic. Do not replace them with an LLM for novelty.
2. **Delegate only meaningful uncertainty.** Consider an LLM for bounded
   interpretation, evidence-driven investigation, prioritization, or selecting
   further inquiry when that adds value beyond a maintainable deterministic
   approach. State why a model is needed and what it is *not* deciding.
3. **Separate evidence, recommendation, and authority.** Model text and tool
   observations are not authoritative facts, permission grants, approvals,
   or successful executions. Validate structured facts with their owning
   systems; keep authorization and state mutation with trusted executors.
4. **Constrain the action surface.** Give an agent scoped, typed tools and
   bounded input, time, steps, context, and cost. Validate tool arguments and
   targets at the execution boundary. Do not grant arbitrary shell, SQL write,
   filesystem, or network access merely because a framework supports it.
5. **Respect existing execution contracts.** Keep pipeline scheduling, data
   mutation, locking, retry, and recovery with their established owners.
   Advisory planning can hand off to a trusted caller. Do not add mandatory
   human approval to an already authorized deterministic path without a
   requirement; require explicit authorization where risk or policy demands it.
6. **Treat failure as a design input.** Define malformed evidence, tool denial,
   unavailable model, timeout, budget exhaustion, stale state, and partial
   execution as applicable. Prefer fail-closed decisions or explicit handoff
   where the required proof is missing. Retry side effects only with verified
   idempotency or reconciliation semantics.
7. **Observe decisions, not just model calls.** Correlate request/run IDs,
   evidence references, selected tools, transitions, prompt/model/config
   revisions, validated outcomes, failures, latency, and available usage/cost.
   Minimize sensitive data in traces; telemetry is not the data-plane truth.
8. **Verify at the right boundary.** Use deterministic unit/contract tests for
   parsers, permissions, schemas, routing invariants, and execution guards.
   Use fake-model scenarios to check tool choices and failures offline.
   Add representative live-model evidence or human utility assessment only
   when needed for the stated outcome; do not substitute an LLM judge for
   deterministic correctness.
9. **Prefer minimal, portable machinery.** Reuse an existing model adapter,
   execution API, tests, and telemetry before adding agents, graph layers,
   state stores, or vendors. Do not confuse a framework feature with a
   justified requirement.

## Examples of Task Allocation

- **Source schema validity:** a deterministic parser and required-column
  contract decide pass/fail; an agent may investigate the failure and propose
  a next check, but cannot override the validator.
- **Ingestion or recovery:** established transactional services own writes and
  stale-state checks; an agent can prepare an evidence-bound plan or request
  a permitted action through the trusted caller.
- **Investigation routing:** use a simple decision table for stable, enumerable
  branches; consider model-driven tool selection only if real evidence and
  uncertainty make a static route materially inadequate.

## Context Links

Read a source **only when its concern affects the active design**. Confirm
version-sensitive integration details against current official documentation.

| Concern | Authoritative reference |
| --- | --- |
| Explicit state, branches, interrupts, replay | [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) |
| Multi-step planning, delegated investigation, context tools | [Deep Agents overview](https://docs.langchain.com/oss/python/deepagents/overview) |
| Instrumentation semantics and interoperable traces | [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/) |
| Tracing when Langfuse is already selected or under evaluation | [Langfuse tracing](https://langfuse.com/docs/observability/get-started) |
| LangGraph-to-Langfuse integration when that pair is chosen | [Langfuse LangGraph integration](https://langfuse.com/integrations/frameworks/langgraph) |

Treat the links as sources for their respective product or standard contracts,
not as instructions to introduce all of those dependencies.

## Handoff

Pass downstream only the decision-relevant context: deterministic owner,
justified model role, evidence and authority boundaries, needed controls,
verification gaps, and relevant official links. If deterministic methods meet
the requirement, say so and stop; an LLMOps design need not contain an LLM.

## Boundary

This Skill selects and loads **LLMOps design context**. It does not implement
agent workflows, choose or install dependencies, configure telemetry, evaluate
model quality, define project-wide authorization, or replace a project's
canonical architectural decisions. Context guidance is not a security control:
enforce permission and mutation boundaries in the actual runtime.
