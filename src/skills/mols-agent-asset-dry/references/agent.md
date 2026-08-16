# Agent DRY

Use this reference for custom agent or subagent profiles whose runtime role is a specialist persona, isolated context, or scoped tool set.

## Preserve

Preserve role or mission, discovery metadata, delegation or invocation boundary, context isolation, tools and permissions, model or host constraints, handoff behavior, expected outputs, dependencies, and independent ownership or lifecycle.

Similar expertise does not make two agents duplicates when their authority, tools, context boundary, delegation boundary, or output responsibility differs.

## Repeated Agent Content

- Treat two agent profiles as consolidation candidates only when role, delegation boundary, context model, authority, tools or permissions, outputs, dependencies, and lifecycle are compatible.
- Remove repeated instructions inside one profile when one statement already governs the same behavior.
- Keep specialized agents when they narrow responsibility, permissions, context, or expected outputs even if much of the surrounding guidance is shared.
- Use host-native composition or shared context only when the dependency is explicit and does not blur agent authority.

Do not retire a discoverable agent entrypoint unless its delegated role is itself redundant and retirement is authorized.

## Shared Policy

Do not move common policy from several agents into a rule merely to reduce text unless that cross-type migration is explicitly requested and the rule would have the same intended activation and authority.

Do not give an agent broader tools, permissions, or context as a side effect of consolidation.

## Handoffs

If two agents cooperate through delegation or handoff, repeated interface expectations may be intentional protocol. Remove them only when one authoritative contract is reliably available to both sides.

## Verify

After changes, confirm each intended task still reaches the correct agent, discovery metadata and delegation boundaries remain valid, context isolation and tools or permissions are unchanged, and handoff or output contracts still hold.
