# Subagent Lifecycle

Use this reference for agent or subagent definitions, delegation boundaries, context handoff, capabilities, result contracts, review, validation, and bounded improvement.

## Principle

Create a separate agent only when delegation produces a concrete specialization, isolation, capability, or coordination benefit. A different persona or label alone is not enough.

The source framework owns canonical representation and the target runtime owns target-specific agent fields, tool syntax, permission semantics, delegation mechanics, and lifecycle behavior. Do not mirror those schemas here.

## Design

### Existence and responsibility

Before creating or splitting an agent, establish why a separate execution unit is useful.

Useful reasons can include:

- specialist judgment that benefits from a bounded responsibility;
- context isolation that reduces contamination or irrelevant history;
- capability or permission restriction that should differ from the caller;
- independent perspective when the runtime can actually preserve that independence;
- parallel or delegated work that materially improves completion or review quality.

Do not create a subagent merely to rename a phase, simulate organizational hierarchy, or move ordinary instructions out of the caller.

Define one coherent responsibility and the boundary with the caller. Decide which judgments belong to the subagent and which remain with the caller after handoff.

### Delegation and selection

Make the invocation condition distinguishable from nearby work:

- state what problem the agent handles and when delegation is useful;
- state a negative boundary when a realistic caller could delegate incorrectly;
- avoid broad descriptions that would make the agent a generic fallback;
- do not promise independent execution if the target runtime cannot provide it.

When exact selection or nested-delegation behavior matters, use the target runtime's current contract.

### Context contract

Pass the smallest context that lets the subagent make its assigned decision correctly.

A useful handoff can include:

- target artifact or object and relevant revision or observable state;
- the assigned question or expected outcome;
- in-scope and out-of-scope boundaries;
- applicable authority, constraints, and known evidence;
- required output contract.

Do not pass the entire conversation or every upstream artifact by default. Do not hide authority that materially changes the assigned decision.

If independence matters, avoid leaking another reviewer's conclusion or speculative diagnosis into the subagent's brief unless reconciliation is the explicit task.

### Capabilities and permissions

Grant only capabilities needed for the responsibility.

- Prefer read-only or narrower capabilities when mutation is unnecessary.
- Keep destructive, privileged, publishing, merge, approval, or other finalizing actions with the caller unless delegation of that authority is explicitly required and permitted.
- Do not infer safety from a tool name; follow the target runtime's actual permission and side-effect semantics.
- If the required capability is unavailable, expose the gap instead of pretending the task was independently or fully executed.

### Result and termination

Define an output that lets the caller continue without reconstructing the subagent's reasoning process.

The result should make clear, as applicable:

- the answer, decision, or candidate findings;
- evidence or unresolved unknowns needed by the caller;
- material coverage gaps or blocked checks;
- whether further action belongs to the caller or another specialist.

Give the agent a bounded completion condition. Avoid open-ended self-recursion, delegation loops, or handoffs that do not establish a new owner.

## Review

Review the axes that can affect orchestration quality:

- **Need** — does a separate agent provide a real specialization, isolation, capability, or coordination benefit?
- **Responsibility** — is its task bounded and distinct from the caller and sibling agents?
- **Delegation** — can the caller distinguish when to invoke it and when not to?
- **Context** — is the handoff sufficient but not polluted with irrelevant history or another specialist's conclusion?
- **Capabilities** — are tools and permissions minimal for the task, with finalizing authority kept at the correct layer?
- **Independence** — when independence is claimed, can the runtime and brief actually preserve it?
- **Result contract** — can the caller act on the result without hidden assumptions or missing evidence state?
- **Termination** — does the agent stop at a clear boundary without recursive or circular delegation?
- **Failure behavior** — does unavailable capability, incomplete context, or blocked delegation remain visible rather than being silently simulated?
- **Portability** — are target-specific fields and runtime semantics isolated from the portable responsibility contract?

## Validate

Use evidence that matches the claim:

- inspect responsibility, delegation condition, context contract, capabilities, result contract, and termination semantics directly;
- run repository or source-framework validation for machine-checkable agent metadata and target projection contracts;
- inspect generated target definitions only when representation is part of the claim;
- require actual runtime evidence before claiming tool availability, permission behavior, nested delegation, isolation, parallelism, independence, or handoff behavior that static definitions cannot establish;
- use repeated or adversarial trials only when stronger behavioral confidence is required, in which case `mols-agent-asset-validator` should be primary.

A well-formed agent definition does not prove that the runtime will invoke it correctly or preserve independence. Report those claims according to the evidence actually observed.
